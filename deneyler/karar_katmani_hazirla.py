"""Panel için karar katmanı paketini üretir (yalnız eğitim verisi; test kullanılmaz).

İçerik: KriterHazirlayici (eğitim OOF'una fit), eğitim kriter matrisi (TOPSIS referansı ve bant eşikleri
ağırlık değişince buradan yeniden hesaplanır), panel için 500 başvuruluk eğitim örnek havuzu (TARGET yok),
AHP ağırlıkları (yargı dosyası varsa).
Çıktı: data/processed/karar_katmani.joblib
Çalıştırma: .\\.venv\\Scripts\\python.exe deneyler\\karar_katmani_hazirla.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.ahp import yargilardan_agirlik
from src.kriterler import KriterHazirlayici
from src.oran_ozellikleri import oran_ozellikleri_ekle
from src.veri_hazirlama import temizle_basvuru
from src.veri_yukle import egitim_matrisi

KOK = Path(__file__).resolve().parents[1]


def calistir():
    X, _ = egitim_matrisi()
    df = oran_ozellikleri_ekle(temizle_basvuru(X)).reset_index(drop=True)
    oof = pd.read_csv(KOK / "data/processed/oof/final_oof.csv")[["SK_ID_CURR", "PD"]]
    df = df.merge(oof, on="SK_ID_CURR", how="left")
    assert df["PD"].notna().all() and len(df) == len(X)
    kh = KriterHazirlayici().fit(df, df["PD"])
    M = kh.transform(df, df["PD"]).astype(np.float32)
    havuz = X.sample(n=500, random_state=42).drop(columns=["TARGET"]).reset_index(drop=True)
    yargi = KOK / "docs/kaynaklar/ahp_yargilar.csv"
    ahp = yargilardan_agirlik(yargi) if yargi.exists() else None
    paket = {"kh": kh, "M_egitim": M, "havuz": havuz,
             "w_ahp": None if ahp is None else np.asarray(ahp["agirliklar"]),
             "ahp": None if ahp is None else {k: v for k, v in ahp.items() if k != "agirliklar"}}
    hedef = KOK / "data/processed/karar_katmani.joblib"
    joblib.dump(paket, hedef)
    print(f"Paket yazıldı: {hedef} | eğitim matrisi {M.shape} | AHP: {'var' if ahp else 'yok (eşit ağırlık)'}")


if __name__ == "__main__":
    calistir()
