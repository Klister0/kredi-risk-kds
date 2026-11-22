"""M8 · SHAP ile açıklama (T9).

SHAP (Lundberg & Lee 2017 ⚠️ künye doğrulanacak): her özelliğin bir tahmine katkısı; toplanabilir:
  taban değer + Σ katkılar = modelin ham çıktısı (XGBoost'ta log-odds).
Toplanabilirlik sayesinde one-hot sütunların katkıları orijinal değişkende TOPLANABİLİR.
Sınırlılık: SHAP nedensellik değildir; korele özelliklerde katkı paylaşımı kararsız olabilir.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import shap


def _parcalar(boru):
    on = boru.named_steps["on"]
    return on, on.named_steps["sutunlar"], boru.named_steps["model"]


def donusmus_matris(boru, X: pd.DataFrame) -> np.ndarray:
    on, _, _ = _parcalar(boru)
    return on.transform(X)


def ozellik_eslemesi(boru) -> tuple[list[str], list[str]]:
    """Dönüşmüş her sütunun (adı, ait olduğu orijinal değişken)."""
    _, ct, _ = _parcalar(boru)
    adlar, kaynak = [], []
    for ad, donusturucu, sutunlar in ct.transformers_:
        if ad == "sayisal":
            for s in sutunlar:
                adlar.append(s); kaynak.append(s)
        elif ad == "kategorik":
            ohe = donusturucu.named_steps["ohe"]
            for s, kategoriler in zip(sutunlar, ohe.categories_):
                for k in kategoriler:
                    adlar.append(f"{s}={k}"); kaynak.append(s)
    return adlar, kaynak


def shap_hesapla(boru, X: pd.DataFrame):
    """(shap matrisi [n × özellik], taban değer, dönüşmüş X, özellik adları, kaynak değişkenler)."""
    Z = donusmus_matris(boru, X)
    _, _, model = _parcalar(boru)
    aciklayici = shap.TreeExplainer(model)
    S = np.asarray(aciklayici.shap_values(Z), dtype=np.float64)   # float32 yuvarlamasını önle
    taban = float(np.ravel(aciklayici.expected_value)[0])
    adlar, kaynak = ozellik_eslemesi(boru)
    if S.shape[1] != len(adlar):
        raise ValueError("SHAP sütun sayısı ile özellik adları uyuşmuyor")
    return S, taban, Z, adlar, kaynak


def degiskene_topla(S: np.ndarray, kaynak: list[str]) -> pd.DataFrame:
    """One-hot katkılarını orijinal değişkende toplar (satır toplamı korunur)."""
    return pd.DataFrame(S, columns=kaynak).T.groupby(level=0, sort=False).sum().T


def global_onem(S_degisken: pd.DataFrame) -> pd.Series:
    """Ortalama |SHAP| (değişken düzeyinde), büyükten küçüğe."""
    return S_degisken.abs().mean().sort_values(ascending=False)
