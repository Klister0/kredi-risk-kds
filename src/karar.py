"""Tek başvuru değerlendirme (panel ve testler için saf mantık).

Akış: ham başvuru satırı → final model PD → kriterler (D34) → sabit referanslı TOPSIS C* (D21)
→ bant (eğitim C* niceliklerinden, D22) + PD-tek karşılaştırma bandı → SHAP açıklaması.
Ağırlık ya da bant oranı değişince yalnız `katman_kur` yeniden çağrılır (eğitim matrisi bellekte).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.aciklama import degiskene_topla, shap_hesapla
from src.kriterler import KRITERLER, YONLER
from src.oran_ozellikleri import oran_ozellikleri_ekle
from src.politika import bant_esikleri, bantla
from src.topsis import FAYDA, SabitTopsis
from src.veri_hazirlama import temizle_basvuru

KRITER_ADLARI = {
    "K1_PD": "Temerrüt olasılığı (PD)", "K2_KREDI_GELIR": "Kredi / gelir", "K3_TAKSIT_GELIR": "Taksit / gelir",
    "K4_GELIR": "Gelir", "K5_ISTIHDAM_YIL": "İstihdam süresi (yıl)", "K6_GECIKME": "Geçmiş gecikmeli kredi sayısı",
}


def katman_kur(M_egitim, w, red: float = 0.15, sartli: float = 0.15) -> dict:
    """Ağırlık ve bant oranlarına göre TOPSIS + bant eşikleri (hepsi eğitim matrisinden)."""
    topsis = SabitTopsis(w, YONLER).fit(M_egitim)
    c_egitim = topsis.transform(M_egitim)
    return {"topsis": topsis, "esik": bant_esikleri(c_egitim, red, sartli),
            "esik_pd": bant_esikleri(1 - np.asarray(M_egitim)[:, 0], red, sartli),
            "c_egitim": c_egitim}


def kriter_konumlari(M, topsis: SabitTopsis) -> np.ndarray:
    """Her kriterde 0 = anti-ideal (eğitim p99/p1), 1 = ideal. Ağırlıktan bağımsız okunabilir skor."""
    Mk = np.clip(np.atleast_2d(M), topsis.alt_, topsis.ust_)
    aralik = np.where(topsis.ust_ > topsis.alt_, topsis.ust_ - topsis.alt_, 1.0)
    fayda = (Mk - topsis.alt_) / aralik
    return np.where(topsis.yon_ == FAYDA, fayda, 1 - fayda)


def degerlendir(X_satir: pd.DataFrame, boru, kh, katman: dict, kalibrator=None) -> dict:
    pd_ = boru.predict_proba(X_satir)[:, 1]
    if kalibrator is not None:
        pd_ = kalibrator.predict(pd_)
    df = oran_ozellikleri_ekle(temizle_basvuru(X_satir)).reset_index(drop=True)
    M = kh.transform(df, pd_)
    t = katman["topsis"]
    c = t.transform(M)
    konum = kriter_konumlari(M, t)[0]
    tablo = pd.DataFrame({"Kriter": [KRITER_ADLARI[k] for k in KRITERLER],
                          "Değer": M[0], "Yön": ["fayda" if y == FAYDA else "maliyet" for y in YONLER],
                          "Ağırlık": t.w_, "İdeale yakınlık (0–1)": konum})
    return {"PD": float(pd_[0]), "C*": float(c[0]),
            "karar": str(bantla(c, katman["esik"])[0]),
            "karar_pd_tek": str(bantla(1 - pd_, katman["esik_pd"])[0]),
            "c_yuzdelik": float((katman["c_egitim"] < c[0]).mean()),
            "kriterler": tablo}


def shap_katkilari(X_satir: pd.DataFrame, boru, aciklayici=None, k: int = 8) -> pd.Series:
    """Değişken düzeyinde en büyük k SHAP katkısı (log-odds) + 'Diğer'."""
    S, _, _, _, kaynak = shap_hesapla(boru, X_satir, aciklayici)
    katki = degiskene_topla(S, kaynak).iloc[0]
    ust = katki.reindex(katki.abs().sort_values(ascending=False).index[:k])
    return pd.concat([ust, pd.Series({"Diğer değişkenler": katki.sum() - ust.sum()})])
