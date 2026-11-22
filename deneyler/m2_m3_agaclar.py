"""M2 Random Forest + M3 XGBoost, M1 ile AYNI 5 katlı katmanlı CV şeması.

- Boru hattı olcekle=False (ağaçlar tekdüze dönüşüme duyarsız).
- Hiperparametreler sabit ve makul (arama M5'te, eşit bütçeyle). Erken durdurma YOK:
  erken durdurma için ayrı doğrulama katı gerekir; burada sızıntı riskini sıfırlamak için kullanılmadı.
- return_train_score=True: eğitim-CV farkı aşırı uyumu gösterir (savunma S14).
- Test kümesine BAKILMAZ (K-C'ye kadar).

Çalıştırma: .\\.venv\\Scripts\\python.exe deneyler\\m2_m3_agaclar.py [ornek_satir]
"""
from __future__ import annotations

import json
import sys
import time
from datetime import date
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.boru_hatti import on_isleme_boru_hatti
from src.veri_yukle import egitim_matrisi

KOK = Path(__file__).resolve().parents[1]
TOHUM = 42


def modeller():
    return {
        "random_forest": RandomForestClassifier(
            n_estimators=150, max_depth=12, min_samples_leaf=50,
            max_features="sqrt", max_samples=0.3, n_jobs=-1, random_state=TOHUM),
        "xgboost": XGBClassifier(
            n_estimators=400, learning_rate=0.05, max_depth=6,
            subsample=0.8, colsample_bytree=0.8, tree_method="hist",
            eval_metric="auc", n_jobs=-1, random_state=TOHUM),
    }


def calistir(ornek=None):
    X, y = egitim_matrisi(ornek=ornek)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=TOHUM)
    sonuclar = {}
    for ad, model in modeller().items():
        boru = Pipeline([("on", on_isleme_boru_hatti(olcekle=False)), ("model", model)])
        t0 = time.time()
        cvr = cross_validate(boru, X, y, cv=cv, scoring=["roc_auc", "average_precision"],
                             return_train_score=True, n_jobs=1)
        sure = time.time() - t0
        sonuclar[ad] = {
            "roc_auc_ort": float(np.mean(cvr["test_roc_auc"])),
            "roc_auc_std": float(np.std(cvr["test_roc_auc"])),
            "pr_auc_ort": float(np.mean(cvr["test_average_precision"])),
            "egitim_roc_auc_ort": float(np.mean(cvr["train_roc_auc"])),
            "sure_sn": round(sure, 1),
            "parametreler": {k: v for k, v in model.get_params().items()
                             if k in ("n_estimators", "max_depth", "min_samples_leaf",
                                      "max_features", "max_samples", "learning_rate",
                                      "subsample", "colsample_bytree")},
        }
        r = sonuclar[ad]
        print(f"{ad:14s} CV ROC-AUC {r['roc_auc_ort']:.4f} ± {r['roc_auc_std']:.4f} | "
              f"PR-AUC {r['pr_auc_ort']:.4f} | eğitim AUC {r['egitim_roc_auc_ort']:.4f} | {r['sure_sn']} sn",
              flush=True)

    kayit = {"tarih": date.today().isoformat(), "tohum": TOHUM, "ornek": ornek,
             "n": int(len(X)), "cv": "StratifiedKFold(5)", "ozellik_seti": "temel+buro",
             "sonuclar": sonuclar}
    etiket = "ornek" if ornek else "tam"
    (KOK / "deneyler").mkdir(exist_ok=True)
    (KOK / "deneyler" / f"m2_m3_agaclar_{date.today().isoformat()}_{etiket}.json").write_text(
        json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")
    return sonuclar


if __name__ == "__main__":
    calistir(int(sys.argv[1]) if len(sys.argv) > 1 else None)
