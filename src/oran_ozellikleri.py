"""F2 · Oran ve türev özellikler.

Satır bazlı, durumsuz. Sıfıra/NaN'a bölme güvenli: payda 0 veya NaN → sonuç NaN (asla inf).
Gelir ve taksit dönemi belirsiz (D32) → bu oranlar MUTLAK yük değil, başvurular arası
GÖRELİ göstergedir. TOPSIS sıralama/yön kullandığından karar katmanı bundan etkilenmez.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

EXT_SUTUNLARI = ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]


def _guvenli_bol(pay: pd.Series, payda: pd.Series) -> pd.Series:
    """pay/payda; payda 0 veya NaN olduğunda NaN döndürür (inf üretmez)."""
    payda = payda.replace(0, np.nan)
    return pay / payda


def oran_ozellikleri_ekle(df: pd.DataFrame) -> pd.DataFrame:
    """Kredi/gelir, taksit/gelir, ödeme oranı, kredi/mal, kişi başı gelir ve EXT özetleri.

    Satır sayısını değiştirmez; yeni sütunlar ekler.
    """
    n = len(df)
    df = df.copy()

    if {"AMT_CREDIT", "AMT_INCOME_TOTAL"} <= set(df.columns):
        df["KREDI_GELIR"] = _guvenli_bol(df["AMT_CREDIT"], df["AMT_INCOME_TOTAL"])
    if {"AMT_ANNUITY", "AMT_INCOME_TOTAL"} <= set(df.columns):
        df["TAKSIT_GELIR"] = _guvenli_bol(df["AMT_ANNUITY"], df["AMT_INCOME_TOTAL"])
    if {"AMT_ANNUITY", "AMT_CREDIT"} <= set(df.columns):
        df["ODEME_ORANI"] = _guvenli_bol(df["AMT_ANNUITY"], df["AMT_CREDIT"])
    if {"AMT_CREDIT", "AMT_GOODS_PRICE"} <= set(df.columns):
        df["KREDI_MAL_ORANI"] = _guvenli_bol(df["AMT_CREDIT"], df["AMT_GOODS_PRICE"])
    if {"AMT_INCOME_TOTAL", "CNT_FAM_MEMBERS"} <= set(df.columns):
        df["KISI_BASI_GELIR"] = _guvenli_bol(df["AMT_INCOME_TOTAL"], df["CNT_FAM_MEMBERS"])

    mevcut_ext = [c for c in EXT_SUTUNLARI if c in df.columns]
    if mevcut_ext:
        df["EXT_ORT"] = df[mevcut_ext].mean(axis=1)          # NaN'ları atlar
        df["EXT_STD"] = df[mevcut_ext].std(axis=1)           # tek değerde NaN
        df["EXT_EKSIK_SAYISI"] = df[mevcut_ext].isna().sum(axis=1).astype("int8")

    assert len(df) == n, "oran özellikleri satır sayısını değiştirmemeli"
    return df
