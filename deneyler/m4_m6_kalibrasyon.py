"""M4 (dar) + M6 · Dengesizlik stratejisi × kalibrasyon, XGBoost, OOF üzerinde (RQ3 ilk kanıt).

Varyantlar: dengeleme yok / scale_pos_weight (=negatif/pozitif)  ×  ham / isotonic(CV) / prior düzeltme.
Tüm tahminler 5 katlı OOF (her satır onu görmemiş modelden). Kalibrasyon ikinci bir CV ile (src/kalibrasyon.py).
Test kümesine BAKILMAZ. OOF tahminleri data/processed/oof/ altına yazılır (K-D eşikleri bunlardan öğrenilecek).

Çalıştırma: .\\.venv\\Scripts\\python.exe deneyler\\m4_m6_kalibrasyon.py [ornek_satir]
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.boru_hatti import on_isleme_boru_hatti
from src.kalibrasyon import cv_isotonic, ece, prior_duzeltme
from src.veri_yukle import egitim_matrisi

KOK = Path(__file__).resolve().parents[1]
TOHUM = 42


def xgb(agirlik=1.0):
    return XGBClassifier(n_estimators=400, learning_rate=0.05, max_depth=6, subsample=0.8,
                         colsample_bytree=0.8, tree_method="hist", eval_metric="auc",
                         scale_pos_weight=agirlik, n_jobs=-1, random_state=TOHUM)


def olcutler(y, p):
    return {"roc_auc": float(roc_auc_score(y, p)), "brier": float(brier_score_loss(y, p)),
            "ece": ece(y, p), "log_loss": float(log_loss(y, np.clip(p, 1e-6, 1 - 1e-6))),
            "ort_tahmin": float(np.mean(p)), "gozlenen_oran": float(np.mean(y))}


ETIKETLER = {
    "yok_ham": "Dengeleme yok (ham)",
    "agirlik_ham": "Sınıf ağırlığı (ham)",
    "agirlik_prior": "Sınıf ağırlığı + prior düzeltme",
    "agirlik_isotonic": "Sınıf ağırlığı + isotonic",
}


def guvenilirlik_grafigi(y, tahminler, yol):
    """20 eşit frekanslı kutuda ortalama tahmin vs gözlenen oran."""
    fig, ax = plt.subplots(figsize=(6, 5))
    for ad, etiket in ETIKETLER.items():
        p = np.asarray(tahminler[ad])
        kut = np.array_split(np.argsort(p), 20)
        ax.plot([p[k].mean() for k in kut], [y[k].mean() for k in kut], marker="o", ms=3, label=etiket)
    m = max(ax.get_xlim()[1], ax.get_ylim()[1])
    ax.plot([0, m], [0, m], "k--", lw=1, label="Mükemmel kalibrasyon")
    ax.set_xlabel("Ortalama tahmin edilen PD (kutu)"); ax.set_ylabel("Gözlenen temerrüt oranı")
    ax.set_title("Güvenilirlik eğrisi (XGBoost, OOF, eğitim kümesi)"); ax.legend(fontsize=8)
    fig.tight_layout(); Path(yol).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(yol, dpi=120); plt.close(fig)


def calistir(ornek=None):
    X, y = egitim_matrisi(ornek=ornek)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=TOHUM)
    w = float((y == 0).sum() / (y == 1).sum())

    oof = {}
    for ad, agirlik in [("yok", 1.0), ("agirlik", w)]:
        boru = Pipeline([("on", on_isleme_boru_hatti(olcekle=False)), ("model", xgb(agirlik))])
        oof[ad] = cross_val_predict(boru, X, y, cv=cv, method="predict_proba", n_jobs=1)[:, 1]
        print(f"OOF hazır: {ad}", flush=True)

    tahminler = {
        "yok_ham": oof["yok"],
        "yok_isotonic": cv_isotonic(oof["yok"], y),
        "agirlik_ham": oof["agirlik"],
        "agirlik_prior": prior_duzeltme(oof["agirlik"], w),
        "agirlik_isotonic": cv_isotonic(oof["agirlik"], y),
    }
    sonuclar = {ad: olcutler(y, p) for ad, p in tahminler.items()}
    for ad, r in sonuclar.items():
        print(f"{ad:17s} AUC {r['roc_auc']:.4f} | Brier {r['brier']:.4f} | ECE {r['ece']:.4f} | "
              f"ort.tahmin {r['ort_tahmin']:.3f} (gözlenen {r['gozlenen_oran']:.3f})")

    # OOF'u sakla (git dışı: data/processed/*)
    oof_klasor = KOK / "data" / "processed" / "oof"
    oof_klasor.mkdir(parents=True, exist_ok=True)
    etiket = "ornek" if ornek else "tam"
    pd.DataFrame({"SK_ID_CURR": X["SK_ID_CURR"].to_numpy(), "TARGET": y.to_numpy(), **tahminler}
                 ).to_csv(oof_klasor / f"xgb_oof_{etiket}.csv", index=False)

    guvenilirlik_grafigi(y.to_numpy(), tahminler, KOK / "rapor" / "sekiller" / "04_guvenilirlik_egrisi.png")

    kayit = {"tarih": date.today().isoformat(), "tohum": TOHUM, "ornek": ornek, "n": int(len(X)),
             "scale_pos_weight": w, "ozellik_seti": "temel+buro", "sonuclar": sonuclar}
    (KOK / "deneyler" / f"m4_m6_kalibrasyon_{date.today().isoformat()}_{etiket}.json").write_text(
        json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    calistir(int(sys.argv[1]) if len(sys.argv) > 1 else None)
