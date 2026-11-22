"""F3 · Ek tablo toplulaştırma: bureau (kredi bürosu geçmişi).

İlişki 1-N: bir başvuru (SK_ID_CURR) birçok büro kaydına (SK_ID_BUREAU) sahip.
Toplulaştırma SK_ID_CURR düzeyinde yapılır; başvuruya birleştirince satır sayısı DEĞİŞMEZ.

Sızıntı disiplini: toplulaştırma yalnız bureau sütunlarından; TARGET hiçbir yerde kullanılmaz.
"Kayıt yok" ≠ "0 gecikme": büro kaydı olmayan başvuruda sayımlar 0, tut/oran NaN, BURO_KAYDI_VAR=0.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Birleştirmeden sonra "kayıt yok" olan başvurularda 0 ile doldurulacak sayım sütunları.
SAYIM_SUTUNLARI = [
    "BURO_KAYIT_SAYISI", "BURO_AKTIF_SAYISI",
    "BURO_GECIKMELI_SAYISI", "BURO_UZATMA_SAYISI",
]


def buro_ozellikleri(bureau: pd.DataFrame) -> pd.DataFrame:
    """bureau tablosunu SK_ID_CURR düzeyinde özetler. Kayıt bulunan başvuruları döndürür.

    Gecikme izi (6. kriter ham hali): CREDIT_DAY_OVERDUE>0 VEYA AMT_CREDIT_MAX_OVERDUE>0.
    NaN tutar ">0" sayılmaz (eksik = bilgi yok, gecikme kanıtı değil).
    """
    b = bureau
    gecikme_izi = (b["CREDIT_DAY_OVERDUE"] > 0) | (b["AMT_CREDIT_MAX_OVERDUE"] > 0)
    yardimci = pd.DataFrame({
        "SK_ID_CURR": b["SK_ID_CURR"],
        "_aktif": (b["CREDIT_ACTIVE"] == "Active").astype("int64"),
        "_gecikme": gecikme_izi.astype("int64"),
    })
    g = b.groupby("SK_ID_CURR")
    gy = yardimci.groupby("SK_ID_CURR")
    ozet = pd.DataFrame({
        "BURO_KAYIT_SAYISI": g.size(),
        "BURO_AKTIF_SAYISI": gy["_aktif"].sum(),
        "BURO_GECIKMELI_SAYISI": gy["_gecikme"].sum(),
        "BURO_MAKS_GECIKME_GUN": g["CREDIT_DAY_OVERDUE"].max(),
        "BURO_MAKS_GECIKME_TUTAR": g["AMT_CREDIT_MAX_OVERDUE"].max(),
        "BURO_TOPLAM_BORC": g["AMT_CREDIT_SUM_DEBT"].sum(min_count=1),
        "BURO_TOPLAM_KREDI": g["AMT_CREDIT_SUM"].sum(min_count=1),
        "BURO_SON_KREDI_GUN": g["DAYS_CREDIT"].max(),
        "BURO_UZATMA_SAYISI": g["CNT_CREDIT_PROLONG"].sum(),
    })
    payda = ozet["BURO_TOPLAM_KREDI"].replace(0, np.nan)
    ozet["BURO_BORC_ORANI"] = ozet["BURO_TOPLAM_BORC"] / payda
    return ozet.reset_index()


def basvuruya_birlestir(basvuru_kimlikleri: pd.Series, buro_ozet: pd.DataFrame) -> pd.DataFrame:
    """Büro özetini başvuru kimliklerine SOL birleştirir; 'kayıt yok' kuralını uygular.

    Satır sayısı = len(basvuru_kimlikleri). Sayımlar 0, diğerleri NaN, BURO_KAYDI_VAR 0/1.
    """
    taban = pd.DataFrame({"SK_ID_CURR": pd.Series(basvuru_kimlikleri).to_numpy()})
    birlesik = taban.merge(buro_ozet, on="SK_ID_CURR", how="left")
    birlesik["BURO_KAYDI_VAR"] = birlesik["BURO_KAYIT_SAYISI"].notna().astype("int8")
    for c in SAYIM_SUTUNLARI:
        birlesik[c] = birlesik[c].fillna(0)
    assert len(birlesik) == len(taban), "birleştirme satır sayısını değiştirdi"
    return birlesik
