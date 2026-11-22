"""Eğitim özellik matrisini (application + bureau) tek çağrıda üretir.

Yalnız EĞİTİM kimlikleri (D33/K-B). Büro toplulaştırma sızıntısız (F3).
Dönüş: (X, y) — X ham+türetilebilir sütunları içerir (boru hattı türetir/temizler),
y = TARGET. SK_ID_CURR X'te kalır; boru hattı onu düşürür.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ek_tablolar import basvuruya_birlestir, buro_ozellikleri

KOK = Path(__file__).resolve().parents[1]


def egitim_matrisi(ornek: int | None = None, tohum: int = 42):
    """ornek verilirse ilk 'ornek' satırla sınırlı hızlı çalışma (kod doğrulama)."""
    ids = pd.read_csv(KOK / "data/processed/bolme/egitim_kimlikleri.csv")["SK_ID_CURR"]
    app = pd.read_csv(KOK / "data/raw/application_train.csv")
    egitim = app[app["SK_ID_CURR"].isin(set(ids))].copy()
    if ornek is not None:
        egitim = egitim.sample(n=ornek, random_state=tohum).reset_index(drop=True)
    buro = buro_ozellikleri(pd.read_csv(KOK / "data/raw/bureau.csv"))
    buro_feat = basvuruya_birlestir(egitim["SK_ID_CURR"], buro).drop(columns=["SK_ID_CURR"])
    X = pd.concat([egitim.reset_index(drop=True), buro_feat.reset_index(drop=True)], axis=1)
    y = X["TARGET"].astype(int)
    return X, y
