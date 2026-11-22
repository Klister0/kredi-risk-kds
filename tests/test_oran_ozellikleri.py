"""F2 oran özellikleri testleri."""
import numpy as np
import pandas as pd

from src.oran_ozellikleri import oran_ozellikleri_ekle


def _ornek():
    return pd.DataFrame({
        "AMT_CREDIT": [100000.0, 200000.0, 50000.0],
        "AMT_INCOME_TOTAL": [50000.0, 0.0, 25000.0],   # 2. satır gelir 0 → NaN testi
        "AMT_ANNUITY": [10000.0, 20000.0, np.nan],
        "AMT_GOODS_PRICE": [90000.0, 180000.0, 0.0],
        "CNT_FAM_MEMBERS": [2.0, 4.0, 1.0],
        "EXT_SOURCE_1": [0.5, np.nan, 0.3],
        "EXT_SOURCE_2": [0.7, 0.6, np.nan],
        "EXT_SOURCE_3": [np.nan, np.nan, 0.9],
    })


def test_kredi_gelir():
    out = oran_ozellikleri_ekle(_ornek())
    assert out.loc[0, "KREDI_GELIR"] == 2.0            # 100000/50000
    assert np.isnan(out.loc[1, "KREDI_GELIR"])         # gelir 0 → NaN, inf değil


def test_sifira_bolme_nan_degil_inf():
    out = oran_ozellikleri_ekle(_ornek())
    assert not np.isinf(out["KREDI_GELIR"]).any()
    assert np.isnan(out.loc[2, "KREDI_MAL_ORANI"])     # goods_price 0 → NaN


def test_ext_ozetleri():
    out = oran_ozellikleri_ekle(_ornek())
    # satır 0: 0.5 ve 0.7 var, biri eksik
    assert abs(out.loc[0, "EXT_ORT"] - 0.6) < 1e-9
    assert out.loc[0, "EXT_EKSIK_SAYISI"] == 1
    assert out.loc[1, "EXT_EKSIK_SAYISI"] == 2         # satır 1: iki eksik
    # satır 1: tek değer (EXT_SOURCE_2) → std NaN
    assert np.isnan(out.loc[1, "EXT_STD"])
    # satır 2: iki değer (0.3, 0.9) → std tanımlı
    assert out.loc[2, "EXT_STD"] > 0


def test_satir_korur_ve_orijinal_bozulmaz():
    df = _ornek()
    out = oran_ozellikleri_ekle(df)
    assert len(out) == len(df)
    assert "KREDI_GELIR" not in df.columns             # kopya mantığı
