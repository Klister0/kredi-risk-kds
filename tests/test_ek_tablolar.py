"""F3 bureau toplulaştırma testleri."""
import numpy as np
import pandas as pd

from src.ek_tablolar import basvuruya_birlestir, buro_ozellikleri


def _bureau():
    # 3 başvuru: 100 (2 kayıt, biri gecikmeli), 101 (1 kayıt temiz), 102 (1 kayıt, tutardan gecikme)
    return pd.DataFrame({
        "SK_ID_CURR":          [100, 100, 101, 102],
        "SK_ID_BUREAU":        [1, 2, 3, 4],
        "CREDIT_ACTIVE":       ["Active", "Closed", "Closed", "Active"],
        "CREDIT_DAY_OVERDUE":  [5, 0, 0, 0],
        "AMT_CREDIT_MAX_OVERDUE": [np.nan, np.nan, np.nan, 1200.0],
        "AMT_CREDIT_SUM":      [1000.0, 2000.0, 500.0, 800.0],
        "AMT_CREDIT_SUM_DEBT": [400.0, 0.0, 0.0, 800.0],
        "DAYS_CREDIT":         [-100, -500, -200, -50],
        "CNT_CREDIT_PROLONG":  [1, 0, 0, 0],
    })


def test_ozet_sayimlar():
    o = buro_ozellikleri(_bureau()).set_index("SK_ID_CURR")
    assert o.loc[100, "BURO_KAYIT_SAYISI"] == 2
    assert o.loc[100, "BURO_AKTIF_SAYISI"] == 1
    assert o.loc[100, "BURO_GECIKMELI_SAYISI"] == 1     # gün>0
    assert o.loc[102, "BURO_GECIKMELI_SAYISI"] == 1     # tutar>0
    assert o.loc[101, "BURO_GECIKMELI_SAYISI"] == 0


def test_borc_orani():
    o = buro_ozellikleri(_bureau()).set_index("SK_ID_CURR")
    # 100: borç 400/ kredi 3000
    assert abs(o.loc[100, "BURO_BORC_ORANI"] - 400/3000) < 1e-9


def test_kayit_yok_kurali():
    o = buro_ozellikleri(_bureau())
    # 103 başvurusunun büro kaydı yok
    out = basvuruya_birlestir(pd.Series([100, 101, 102, 103]), o)
    assert len(out) == 4
    satir = out.set_index("SK_ID_CURR").loc[103]
    assert satir["BURO_KAYDI_VAR"] == 0
    assert satir["BURO_KAYIT_SAYISI"] == 0          # sayım → 0
    assert satir["BURO_GECIKMELI_SAYISI"] == 0
    assert np.isnan(satir["BURO_BORC_ORANI"])       # oran → NaN (0 gecikme DEĞİL)
    assert np.isnan(satir["BURO_MAKS_GECIKME_TUTAR"])


def test_birlestirme_satir_korur():
    o = buro_ozellikleri(_bureau())
    ids = pd.Series([100, 101, 102, 103, 104, 105])
    out = basvuruya_birlestir(ids, o)
    assert len(out) == len(ids)
    assert out["BURO_KAYDI_VAR"].tolist() == [1, 1, 1, 0, 0, 0]
