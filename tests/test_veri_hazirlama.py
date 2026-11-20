"""F1 temizleme testleri."""
import numpy as np
import pandas as pd

from src.veri_hazirlama import (
    cinsiyet_xna_nan,
    gunleri_yila_cevir,
    istihdam_anomalisini_isaretle,
    temizle_basvuru,
)


def _ornek():
    return pd.DataFrame({
        "DAYS_EMPLOYED": [-1000, 365243, -5000, 365243],
        "CODE_GENDER": ["M", "F", "XNA", "F"],
        "DAYS_BIRTH": [-3653, -7305, -10958, -14610],
    })


def test_anomali_bayrak_ve_nan():
    out = istihdam_anomalisini_isaretle(_ornek())
    assert out["ISTIHDAM_ANOMALI"].tolist() == [0, 1, 0, 1]
    assert out["DAYS_EMPLOYED"].isna().tolist() == [False, True, False, True]
    # normal değerler dokunulmadan kaldı
    assert out.loc[0, "DAYS_EMPLOYED"] == -1000


def test_anomali_idempotent():
    # iki kez uygulamak bayrağı bozmamalı
    bir = istihdam_anomalisini_isaretle(_ornek())
    iki = istihdam_anomalisini_isaretle(bir)
    assert iki["ISTIHDAM_ANOMALI"].tolist() == [0, 1, 0, 1]


def test_cinsiyet_xna():
    out = cinsiyet_xna_nan(_ornek())
    assert out["CODE_GENDER"].isna().sum() == 1
    assert out["CODE_GENDER"].tolist()[0] == "M"


def test_gun_yil():
    out = gunleri_yila_cevir(_ornek())
    # -3653 gün ≈ 10 yıl, pozitif
    assert abs(out.loc[0, "YAS_YIL"] - 10.0) < 0.05
    assert (out["YAS_YIL"] > 0).all()


def test_temizle_satir_korur():
    df = _ornek()
    out = temizle_basvuru(df)
    assert len(out) == len(df)
    # orijinal df değişmedi (kopya mantığı)
    assert "ISTIHDAM_ANOMALI" not in df.columns
