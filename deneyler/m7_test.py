"""M7 · Test kümesinde TEK SEFERLİK değerlendirme (kapı K-C).

Model seçimi M5'te CV ile yapıldı (XGBoost). Burada üç model (aynı M5 parametreleri, tüm eğitimle fit)
test kümesinde ölçülür: AUC, Gini, KS, PR-AUC, Brier, ECE + eşleştirilmiş bootstrap %95 GA (B=1000),
XGBoost'a göre farklar. Test tahminleri E1 için saklanır.

Kilit: gerçek sonuç dosyası varsa betik çalışmayı REDDEDER (test kümesine ikinci bakış yok).
Çalıştırma:
    .\\.venv\\Scripts\\python.exe deneyler\\m7_test.py deneme   (eğitimden ayrılmış sahte test, kod kontrolü)
    .\\.venv\\Scripts\\python.exe deneyler\\m7_test.py gercek   (BİR KEZ)
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deneyler.final_model import final_boru_hatti
from src.boru_hatti import on_isleme_boru_hatti
from src.degerlendirme import bootstrap
from src.veri_yukle import egitim_matrisi, test_matrisi

KOK = Path(__file__).resolve().parents[1]
TOHUM = 42


def m5_param(model):
    m5 = sorted((KOK / "deneyler").glob("m5_arama_*_tam.json"))[-1]
    return json.loads(m5.read_text(encoding="utf-8"))["sonuclar"][model]["en_iyi_parametreler"]


def diger_modeller():
    return {
        "logreg": Pipeline([("on", on_isleme_boru_hatti(olcekle=True)),
                            ("model", LogisticRegression(max_iter=2000, random_state=TOHUM, **m5_param("logreg")))]),
        "random_forest": Pipeline([("on", on_isleme_boru_hatti(olcekle=False)),
                                   ("model", RandomForestClassifier(n_jobs=-1, random_state=TOHUM,
                                                                    **m5_param("random_forest")))]),
    }


def calistir(mod: str):
    kilit = KOK / "deneyler" / "m7_test_sonuc.json"
    if mod == "gercek" and kilit.exists():
        raise SystemExit("Test kümesi zaten açıldı (deneyler/m7_test_sonuc.json). İkinci bakış yok.")

    if mod == "deneme":
        X, y = egitim_matrisi(ornek=30000)
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=TOHUM)
        xgb, _, _ = final_boru_hatti()
        xgb.fit(Xtr, ytr)
        B = 50
    else:
        Xtr, ytr = egitim_matrisi()
        Xte, yte = test_matrisi()
        xgb = joblib.load(KOK / "data/processed/model/final_model.joblib")["boru"]
        B = 1000

    tahmin = {"xgboost": xgb.predict_proba(Xte)[:, 1]}
    for ad, boru in diger_modeller().items():
        boru.fit(Xtr, ytr)
        tahmin[ad] = boru.predict_proba(Xte)[:, 1]
        print(f"{ad} hazır", flush=True)

    sonuc = bootstrap(yte.to_numpy(), tahmin, B=B, tohum=TOHUM, referans="xgboost")
    for m in tahmin:
        r = sonuc[m]
        print(f"{m:14s} AUC {r['roc_auc']['deger']:.4f} [{r['roc_auc']['ga_alt']:.4f}, {r['roc_auc']['ga_ust']:.4f}] | "
              f"KS {r['ks']['deger']:.3f} | PR-AUC {r['pr_auc']['deger']:.4f} | Brier {r['brier']['deger']:.4f} | "
              f"ECE {r['ece']['deger']:.4f}", flush=True)
    for f, r in sonuc["farklar"].items():
        a = r["roc_auc"]
        print(f"fark {f}: AUC {a['deger']:+.4f} [{a['ga_alt']:+.4f}, {a['ga_ust']:+.4f}]", flush=True)

    if mod == "gercek":
        klasor = KOK / "data/processed/test_tahmin"
        klasor.mkdir(parents=True, exist_ok=True)
        pd.DataFrame({"SK_ID_CURR": Xte["SK_ID_CURR"].to_numpy(), "TARGET": yte.to_numpy(),
                      **{f"PD_{m}": p for m, p in tahmin.items()}}).to_csv(klasor / "test_tahminleri.csv", index=False)
        kayit = {"tarih": date.today().isoformat(), "tohum": TOHUM, "B": B, "n_test": int(len(yte)),
                 "pozitif_orani": float(yte.mean()), "secilen_model": "xgboost (M5, CV)",
                 "sonuclar": sonuc}
        kilit.write_text(json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("deneme", "gercek"):
        raise SystemExit("kullanım: m7_test.py deneme|gercek")
    calistir(sys.argv[1])
