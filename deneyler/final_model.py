"""Final PD modeli: M5'te seçilen XGBoost (parametreler M5 JSON'undan okunur).

1) 5 katlı OOF tahmin (eğitim)  → K-D eşikleri ve karar katmanı deneyleri bunu kullanır.
2) D13 ön-belirlenmiş kuralı: OOF ECE < 0,01 ise ham PD; değilse tüm OOF'a fit edilen isotonic.
3) Tüm eğitim verisiyle final fit → model dosyası (git dışı, yeniden üretilebilir).
Test kümesine BAKILMAZ (M7'de, K-C).

Çalıştırma: .\\.venv\\Scripts\\python.exe deneyler\\final_model.py
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.boru_hatti import on_isleme_boru_hatti
from src.kalibrasyon import ece
from src.veri_yukle import egitim_matrisi

KOK = Path(__file__).resolve().parents[1]
TOHUM = 42
ECE_ESIGI = 0.01   # D13 kuralı
DISLANAN = ("CODE_GENDER",)   # D16 (2026-11-22): cinsiyet final modelden çıkarıldı (CV maliyeti AUC 0,0016)
SURUM = "cinsiyetsiz"


def final_boru_hatti():
    m5 = sorted((KOK / "deneyler").glob("m5_arama_*_tam.json"))[-1]
    p = json.loads(m5.read_text(encoding="utf-8"))["sonuclar"]["xgboost"]["en_iyi_parametreler"]
    model = XGBClassifier(tree_method="hist", eval_metric="auc", n_jobs=-1, random_state=TOHUM, **p)
    return Pipeline([("on", on_isleme_boru_hatti(olcekle=False, dislanan=DISLANAN)), ("model", model)]), p, m5.name


def calistir():
    X, y = egitim_matrisi()
    boru, parametreler, kaynak = final_boru_hatti()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=TOHUM)
    oof = cross_val_predict(boru, X, y, cv=cv, method="predict_proba", n_jobs=1)[:, 1]
    oof_ece = ece(y, oof)
    kalibrasyon = "ham" if oof_ece < ECE_ESIGI else "isotonic"
    print(f"OOF AUC {roc_auc_score(y, oof):.4f} | Brier {brier_score_loss(y, oof):.4f} | "
          f"ECE {oof_ece:.4f} → kural: {kalibrasyon}", flush=True)

    kalibrator = None
    if kalibrasyon == "isotonic":
        kalibrator = IsotonicRegression(out_of_bounds="clip", y_min=0, y_max=1).fit(oof, y)

    klasor = KOK / "data" / "processed"
    (klasor / "oof").mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"SK_ID_CURR": X["SK_ID_CURR"].to_numpy(), "TARGET": y.to_numpy(), "PD": oof}
                 ).to_csv(klasor / "oof" / "final_oof.csv", index=False)

    boru.fit(X, y)
    (klasor / "model").mkdir(parents=True, exist_ok=True)
    joblib.dump({"boru": boru, "kalibrator": kalibrator, "parametreler": parametreler},
                klasor / "model" / "final_model.joblib")
    print("Final model tüm eğitimle eğitildi ve kaydedildi.", flush=True)

    kayit = {"tarih": date.today().isoformat(), "tohum": TOHUM, "n": int(len(X)), "surum": SURUM,
             "dislanan": list(DISLANAN),
             "parametre_kaynagi": kaynak, "parametreler": parametreler,
             "oof": {"roc_auc": float(roc_auc_score(y, oof)), "brier": float(brier_score_loss(y, oof)),
                     "ece": oof_ece, "ort_pd": float(oof.mean()), "gozlenen": float(y.mean())},
             "kalibrasyon_karari": kalibrasyon, "kural": f"ECE < {ECE_ESIGI} → ham (D13)"}
    (KOK / "deneyler" / f"final_model_{date.today().isoformat()}_{SURUM}.json").write_text(
        json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    calistir()
