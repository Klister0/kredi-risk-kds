"""M5 · Eşit bütçeli rastgele hiperparametre araması (LR, RF, XGBoost).

Bütçe: her model için N_ADAY aday × 3 katlı katmanlı CV, ölçüt roc_auc (D10).
Sonra her modelin en iyi parametreleri M1–M3 ile AYNI 5 katlı CV'de yeniden ölçülür.
SEÇİM KURALI (arama ÖNCESİ yazıldı): 5 katlı CV ROC-AUC'si en yüksek model seçilir.
Test kümesine BAKILMAZ (K-C, M7'de).

Çalıştırma (proje kökünden, uzun sürer — gece koşusu):
    .\\.venv\\Scripts\\python.exe deneyler\\m5_arama.py
Hızlı kod denemesi:
    .\\.venv\\Scripts\\python.exe deneyler\\m5_arama.py 20000 2
"""
from __future__ import annotations

import json
import sys
import time
from datetime import date, datetime
from pathlib import Path

import numpy as np
from scipy.stats import loguniform, randint, uniform
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.boru_hatti import on_isleme_boru_hatti
from src.veri_yukle import egitim_matrisi

KOK = Path(__file__).resolve().parents[1]
TOHUM = 42


def adaylar():
    """(boru hattı, arama uzayı). Uzaylar makul aralıklar; parametre adı 'model__...'."""
    return {
        "logreg": (
            Pipeline([("on", on_isleme_boru_hatti(olcekle=True)),
                      ("model", LogisticRegression(max_iter=2000, random_state=TOHUM))]),
            {"model__C": loguniform(1e-3, 10)},
        ),
        "random_forest": (
            Pipeline([("on", on_isleme_boru_hatti(olcekle=False)),
                      ("model", RandomForestClassifier(n_jobs=-1, random_state=TOHUM))]),
            {"model__n_estimators": randint(150, 401),
             "model__max_depth": [8, 12, 16, 20, None],
             "model__min_samples_leaf": randint(10, 201),
             "model__max_features": ["sqrt", 0.1, 0.2],
             "model__max_samples": [0.3, 0.5, 0.8]},
        ),
        "xgboost": (
            Pipeline([("on", on_isleme_boru_hatti(olcekle=False)),
                      ("model", XGBClassifier(tree_method="hist", eval_metric="auc",
                                              n_jobs=-1, random_state=TOHUM))]),
            {"model__n_estimators": randint(300, 901),
             "model__learning_rate": loguniform(0.02, 0.15),
             "model__max_depth": randint(3, 9),
             "model__min_child_weight": randint(1, 21),
             "model__subsample": uniform(0.6, 0.4),
             "model__colsample_bytree": uniform(0.4, 0.6),
             "model__reg_lambda": loguniform(0.1, 10),
             "model__reg_alpha": loguniform(1e-3, 5)},
        ),
    }


def _yazdir(*a):
    print(f"[{datetime.now():%H:%M:%S}]", *a, flush=True)


def _sade(d):
    return {k.replace("model__", ""): (v.item() if hasattr(v, "item") else v) for k, v in d.items()}


def calistir(ornek=None, n_aday=12):
    X, y = egitim_matrisi(ornek=ornek)
    cv3 = StratifiedKFold(n_splits=3, shuffle=True, random_state=TOHUM)
    cv5 = StratifiedKFold(n_splits=5, shuffle=True, random_state=TOHUM)
    sonuc = {}
    for ad, (boru, uzay) in adaylar().items():
        _yazdir(f"{ad}: arama başlıyor ({n_aday} aday × 3 kat)")
        t0 = time.time()
        # verbose=3: her deneme (aday × kat) bittiğinde skor ve süreyle bir satır yazar (ilerleme takibi)
        arama = RandomizedSearchCV(boru, uzay, n_iter=n_aday, scoring="roc_auc", cv=cv3,
                                   random_state=TOHUM, n_jobs=1, refit=False, verbose=3)
        arama.fit(X, y)
        en_iyi = arama.best_params_
        _yazdir(f"{ad}: en iyi 3-kat AUC {arama.best_score_:.4f} → 5 katlı yeniden ölçüm")
        boru.set_params(**en_iyi)
        cvr = cross_validate(boru, X, y, cv=cv5, scoring=["roc_auc", "average_precision"],
                             return_train_score=True, n_jobs=1, verbose=2)
        sonuc[ad] = {
            "arama_en_iyi_3kat_auc": float(arama.best_score_),
            "aday_auc_dagilimi": [float(s) for s in arama.cv_results_["mean_test_score"]],
            "en_iyi_parametreler": _sade(en_iyi),
            "cv5_roc_auc_ort": float(np.mean(cvr["test_roc_auc"])),
            "cv5_roc_auc_std": float(np.std(cvr["test_roc_auc"])),
            "cv5_pr_auc_ort": float(np.mean(cvr["test_average_precision"])),
            "cv5_egitim_auc_ort": float(np.mean(cvr["train_roc_auc"])),
            "sure_dk": round((time.time() - t0) / 60, 1),
        }
        r = sonuc[ad]
        _yazdir(f"{ad}: 5-kat AUC {r['cv5_roc_auc_ort']:.4f} ± {r['cv5_roc_auc_std']:.4f} | "
                f"eğitim {r['cv5_egitim_auc_ort']:.4f} | {r['sure_dk']} dk")

    secilen = max(sonuc, key=lambda m: sonuc[m]["cv5_roc_auc_ort"])
    _yazdir(f"SEÇİLEN MODEL (kural: en yüksek 5-kat CV AUC): {secilen}")
    etiket = "ornek" if ornek else "tam"
    kayit = {"tarih": date.today().isoformat(), "tohum": TOHUM, "ornek": ornek, "n": int(len(X)),
             "butce": {"n_aday": n_aday, "arama_cv": 3, "degerlendirme_cv": 5},
             "secim_kurali": "en yüksek 5 katlı CV ROC-AUC", "secilen": secilen, "sonuclar": sonuc}
    (KOK / "deneyler").mkdir(exist_ok=True)
    (KOK / "deneyler" / f"m5_arama_{date.today().isoformat()}_{etiket}.json").write_text(
        json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    ornek = int(sys.argv[1]) if len(sys.argv) > 1 else None
    n_aday = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    calistir(ornek, n_aday)
