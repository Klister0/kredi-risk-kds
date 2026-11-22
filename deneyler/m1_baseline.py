"""M1 · Dummy baseline + Logistic Regression, 5 katlı katmanlı CV.

Boru hattı CV içinde fit edilir (kat başına yalnız eğitim → sızıntı yok). Test kümesine
BAKILMAZ (K-C'ye kadar). Sonuç deneyler/ altına tarihli JSON olarak yazılır.

Çalıştırma:  .\\.venv\\Scripts\\python.exe deneyler\\m1_baseline.py [ornek_satir]
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.boru_hatti import on_isleme_boru_hatti
from src.veri_yukle import egitim_matrisi

KOK = Path(__file__).resolve().parents[1]
TOHUM = 42


def calistir(ornek=None):
    X, y = egitim_matrisi(ornek=ornek)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=TOHUM)
    skor = ["roc_auc", "average_precision"]

    from sklearn.pipeline import Pipeline
    modeller = {
        "dummy": Pipeline([("on", on_isleme_boru_hatti(olcekle=True)),
                           ("model", DummyClassifier(strategy="stratified", random_state=TOHUM))]),
        "logreg": Pipeline([("on", on_isleme_boru_hatti(olcekle=True)),
                            ("model", LogisticRegression(max_iter=1000, random_state=TOHUM))]),
    }

    sonuclar = {}
    for ad, boru in modeller.items():
        cvr = cross_validate(boru, X, y, cv=cv, scoring=skor, n_jobs=-1)
        sonuclar[ad] = {
            "roc_auc_ort": float(np.mean(cvr["test_roc_auc"])),
            "roc_auc_std": float(np.std(cvr["test_roc_auc"])),
            "pr_auc_ort": float(np.mean(cvr["test_average_precision"])),
        }
        print(f"{ad:8s}  ROC-AUC {sonuclar[ad]['roc_auc_ort']:.4f} "
              f"± {sonuclar[ad]['roc_auc_std']:.4f}  PR-AUC {sonuclar[ad]['pr_auc_ort']:.4f}")

    kayit = {"tarih": date.today().isoformat(), "tohum": TOHUM,
             "ornek": ornek, "n": int(len(X)), "cv": "StratifiedKFold(5)",
             "sonuclar": sonuclar}
    cikti = KOK / "deneyler"
    cikti.mkdir(exist_ok=True)
    etiket = "ornek" if ornek else "tam"
    (cikti / f"m1_baseline_{date.today().isoformat()}_{etiket}.json").write_text(
        json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")
    return sonuclar


if __name__ == "__main__":
    ornek = int(sys.argv[1]) if len(sys.argv) > 1 else None
    calistir(ornek)
