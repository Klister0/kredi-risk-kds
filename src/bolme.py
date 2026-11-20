"""Eğitim/test bölmesi.

Kritik parça (CLAUDE.md §3): katmanlı bölme sıfırdan yazıldı; testlerde sklearn ile
sınıf bazında karşılaştırılarak doğrulanıyor. Bölme bir kez yapılır, test kimlikleri
dosyaya kaydedilir ve model seçimine kadar (kapı K-C) test kümesine bakılmaz.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd


def katmanli_bol(
    kimlikler: pd.Series | np.ndarray,
    hedef: pd.Series | np.ndarray,
    test_orani: float = 0.2,
    tohum: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Her sınıfı ayrı ayrı karıştırıp `test_orani` kadarını teste ayırır (katmanlı holdout).

    Katmanlı: pozitif ve negatif sınıf **ayrı ayrı** bölünür, böylece azınlık sınıfının
    (TARGET=1, ~%8) oranı iki tarafta da korunur.

    Döndürür: (egitim_kimlikleri, test_kimlikleri) — ikisi de artan sırada, ayrık,
    birleşimleri tüm kimlikler.
    """
    kimlikler = np.asarray(kimlikler)
    hedef = np.asarray(hedef)
    if kimlikler.shape != hedef.shape:
        raise ValueError("kimlikler ve hedef aynı uzunlukta olmalı")
    if len(np.unique(kimlikler)) != len(kimlikler):
        raise ValueError("kimlikler tekil olmalı (SK_ID_CURR)")
    if not 0.0 < test_orani < 1.0:
        raise ValueError("test_orani (0, 1) aralığında olmalı")

    rng = np.random.default_rng(tohum)

    test_parcalari = []
    for sinif in np.unique(hedef):
        sinif_kimlikleri = kimlikler[hedef == sinif]
        karisik = rng.permutation(sinif_kimlikleri)
        n_test = round(len(karisik) * test_orani)
        test_parcalari.append(karisik[:n_test])

    test_kimlikleri = np.sort(np.concatenate(test_parcalari))
    test_kumesi = set(test_kimlikleri.tolist())
    egitim_kimlikleri = np.sort(
        np.array([k for k in kimlikler if k not in test_kumesi])
    )
    return egitim_kimlikleri, test_kimlikleri


def bolmeyi_kaydet(
    egitim_kimlikleri: np.ndarray,
    test_kimlikleri: np.ndarray,
    hedef_adi: str,
    klasor: str | Path,
    tohum: int,
    test_orani: float,
) -> None:
    """Kimlik listelerini ve üretim meta bilgisini `klasor` altına yazar.

    Kimlikler CSV (okunabilir, tek sütun), meta JSON. Böylece bölme tekrar üretilebilir
    ve commit'le tarihlenebilir (sızıntı disiplini: kimse bu dosyaları elle değiştirmez).
    """
    klasor = Path(klasor)
    klasor.mkdir(parents=True, exist_ok=True)
    pd.Series(egitim_kimlikleri, name="SK_ID_CURR").to_csv(
        klasor / "egitim_kimlikleri.csv", index=False
    )
    pd.Series(test_kimlikleri, name="SK_ID_CURR").to_csv(
        klasor / "test_kimlikleri.csv", index=False
    )
    meta = {
        "tarih": date.today().isoformat(),
        "tohum": tohum,
        "test_orani": test_orani,
        "hedef": hedef_adi,
        "n_egitim": int(len(egitim_kimlikleri)),
        "n_test": int(len(test_kimlikleri)),
    }
    (klasor / "bolme_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    # Gerçek veride bölmeyi üretir (kapı K-B). Yalnızca SK_ID_CURR ve TARGET okunur;
    # test kümesinin ÖZELLİKLERİNE bakılmaz. Çıktı data/processed/bolme/ altına yazılır.
    kok = Path(__file__).resolve().parents[1]
    df = pd.read_csv(
        kok / "data" / "raw" / "application_train.csv",
        usecols=["SK_ID_CURR", "TARGET"],
    )
    egitim, test = katmanli_bol(df["SK_ID_CURR"], df["TARGET"], test_orani=0.2, tohum=42)
    bolmeyi_kaydet(
        egitim, test, "TARGET", kok / "data" / "processed" / "bolme",
        tohum=42, test_orani=0.2,
    )
    print(f"Bölme kaydedildi: egitim={len(egitim)}, test={len(test)}")
