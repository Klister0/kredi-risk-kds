"""F1 · Başvuru (application) temizleme.

Satır bazlı, durumsuz dönüşümler (veriden parametre öğrenmez → sızıntı riski yok).
Her fonksiyon df'i kopyalar, değiştirmez; böylece zincirleme ve test kolay.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Başvuruya göre negatif gün (geçmiş) olarak kodlanmış sütunlar.
GUN_SUTUNLARI = {
    "DAYS_BIRTH": "YAS_YIL",
    "DAYS_EMPLOYED": "ISTIHDAM_YIL",
    "DAYS_REGISTRATION": "KAYIT_YIL",
    "DAYS_ID_PUBLISH": "KIMLIK_YIL",
    "DAYS_LAST_PHONE_CHANGE": "TELEFON_YIL",
}
ISTIHDAM_ANOMALI_KODU = 365243


def istihdam_anomalisini_isaretle(df: pd.DataFrame) -> pd.DataFrame:
    """DAYS_EMPLOYED=365243 (≈1000 yıl, emekli/çalışmayan) → NaN + ISTIHDAM_ANOMALI bayrağı.

    İdempotent: bayrak zaten varsa yeniden hesaplamaz (ikinci çağrıda değer NaN olduğundan
    bayrak sıfırlanmasın diye).
    """
    df = df.copy()
    if "ISTIHDAM_ANOMALI" not in df.columns:
        anom = df["DAYS_EMPLOYED"] == ISTIHDAM_ANOMALI_KODU
        df["ISTIHDAM_ANOMALI"] = anom.astype("int8")
        df.loc[anom, "DAYS_EMPLOYED"] = np.nan
    return df


def cinsiyet_xna_nan(df: pd.DataFrame) -> pd.DataFrame:
    """CODE_GENDER='XNA' (eğitimde 4 satır) → NaN."""
    df = df.copy()
    if "CODE_GENDER" in df.columns:
        df.loc[df["CODE_GENDER"] == "XNA", "CODE_GENDER"] = np.nan
    return df


def gunleri_yila_cevir(df: pd.DataFrame) -> pd.DataFrame:
    """GUN_SUTUNLARI'ndaki negatif gün sütunlarını pozitif yıla çevirir (yeni sütun ekler).

    yil = -gun / 365.25. Ham DAYS_* sütunları korunur (özellik seçimi sonra, F5).
    """
    df = df.copy()
    for gun, yil in GUN_SUTUNLARI.items():
        if gun in df.columns:
            df[yil] = -df[gun] / 365.25
    return df


def temizle_basvuru(df: pd.DataFrame) -> pd.DataFrame:
    """F1 tam temizleme: anomali bayrağı → XNA → gün-yıl. Satır sayısı değişmez."""
    n = len(df)
    df = istihdam_anomalisini_isaretle(df)
    df = cinsiyet_xna_nan(df)
    df = gunleri_yila_cevir(df)
    assert len(df) == n, "temizleme satır sayısını değiştirmemeli"
    return df
