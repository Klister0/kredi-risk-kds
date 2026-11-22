"""F4 boru hattı testleri. Asıl kanıt: imputer/scaler istatistikleri YALNIZ eğitimden gelir."""
import numpy as np
import pandas as pd

from src.boru_hatti import on_isleme_boru_hatti


def _cerceve(gelir_degerleri, ekstra=0.0):
    n = len(gelir_degerleri)
    return pd.DataFrame({
        "SK_ID_CURR": range(100, 100 + n),
        "AMT_INCOME_TOTAL": gelir_degerleri,
        "AMT_CREDIT": [100000.0] * n,
        "AMT_ANNUITY": [10000.0] * n,
        "DAYS_BIRTH": [-10000.0] * n,
        "DAYS_EMPLOYED": [-2000.0] * n,
        "CODE_GENDER": ["M"] * n,
    })


def test_sizinti_imputer_egitimden():
    # Eğitimde gelir medyanı belli; testte NaN var → testteki NaN EĞİTİM medyanıyla dolmalı
    egitim = _cerceve([10000.0, 20000.0, 30000.0, 40000.0, 50000.0])  # medyan 30000
    test = _cerceve([999999.0, np.nan, 999999.0])                     # testin kendi medyanı çok farklı
    boru = on_isleme_boru_hatti(olcekle=False)
    boru.fit(egitim)
    imputer = boru.named_steps["sutunlar"].named_transformers_["sayisal"].named_steps["imputer"]
    # AMT_INCOME_TOTAL hangi sütun indeksindeyse onun istatistiği 30000 olmalı
    ct = boru.named_steps["sutunlar"]
    sayisal_sutunlar = ct.transformers_[0][2]  # seçilen sayısal sütun adları
    idx = list(sayisal_sutunlar).index("AMT_INCOME_TOTAL")
    assert abs(imputer.statistics_[idx] - 30000.0) < 1e-6   # eğitim medyanı, test değil


def test_fit_transform_boyut_ve_sonlu():
    egitim = _cerceve([10000.0, 20000.0, 30000.0, 40000.0])
    boru = on_isleme_boru_hatti(olcekle=True)
    X = boru.fit_transform(egitim)
    assert X.shape[0] == 4
    assert np.isfinite(X).all()


def test_gorulmemis_kategori_patlamaz():
    # handle_unknown='ignore': testte yeni kategori gelirse hata vermemeli
    egitim = _cerceve([10000.0, 20000.0, 30000.0])
    egitim["CODE_GENDER"] = ["M", "F", "M"]
    boru = on_isleme_boru_hatti()
    boru.fit(egitim)
    test = _cerceve([25000.0])
    test["CODE_GENDER"] = ["XNA"]  # eğitimde yok (zaten temizlemede NaN olur ama güvence)
    X = boru.transform(test)
    assert X.shape[0] == 1
