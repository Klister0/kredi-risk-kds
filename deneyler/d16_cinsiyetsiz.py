"""D16 · Cinsiyetsiz model maliyeti (yalnız eğitim, 5 katlı CV; test kilitli).

Final XGBoost (M5 parametreleri) ile aynı katlarda, CODE_GENDER çıkarılmış hâli karşılaştırılır.
Eşleştirilmiş kat farkları raporlanır.
Çalıştırma: .\\.venv\\Scripts\\python.exe deneyler\\d16_cinsiyetsiz.py
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
from sklearn.base import clone
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deneyler.final_model import final_boru_hatti
from src.kalibrasyon import ece
from src.veri_yukle import egitim_matrisi

KOK = Path(__file__).resolve().parents[1]


def calistir():
    X, y = egitim_matrisi()
    boru, _, _ = final_boru_hatti()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    oof = {"tam": np.zeros(len(y)), "cinsiyetsiz": np.zeros(len(y))}
    katlar = []
    for k, (e, d) in enumerate(cv.split(X, y)):
        for ad, Xv in [("tam", X), ("cinsiyetsiz", X.drop(columns=["CODE_GENDER"]))]:
            # "tam" kolu açıkça cinsiyetli: final_boru_hatti artık CODE_GENDER'ı dışlıyor (D16)
            m = clone(boru).set_params(on__ozellik__dislanan=()).fit(Xv.iloc[e], y.iloc[e])
            oof[ad][d] = m.predict_proba(Xv.iloc[d])[:, 1]
        a_t, a_c = roc_auc_score(y.iloc[d], oof["tam"][d]), roc_auc_score(y.iloc[d], oof["cinsiyetsiz"][d])
        katlar.append({"kat": k, "auc_tam": a_t, "auc_cinsiyetsiz": a_c, "fark": a_t - a_c})
        print(f"kat {k}: tam {a_t:.4f} | cinsiyetsiz {a_c:.4f} | fark {a_t - a_c:+.4f}", flush=True)
    f = np.array([k["fark"] for k in katlar])
    sonuc = {"tarih": date.today().isoformat(), "katlar": katlar,
             "ort_fark": float(f.mean()), "fark_std": float(f.std(ddof=1)),
             "oof_auc_tam": float(roc_auc_score(y, oof["tam"])),
             "oof_auc_cinsiyetsiz": float(roc_auc_score(y, oof["cinsiyetsiz"])),
             "oof_ece_cinsiyetsiz": ece(y, oof["cinsiyetsiz"])}
    print(f"Ortalama AUC maliyeti: {f.mean():+.4f} (kat std {f.std(ddof=1):.4f}) | "
          f"ECE cinsiyetsiz {sonuc['oof_ece_cinsiyetsiz']:.4f}", flush=True)
    (KOK / "deneyler" / f"d16_cinsiyetsiz_{date.today().isoformat()}.json").write_text(
        json.dumps(sonuc, ensure_ascii=False, indent=2), encoding="utf-8")
    np.save(KOK / "data/processed/oof/cinsiyetsiz_oof.npy", oof["cinsiyetsiz"])


if __name__ == "__main__":
    calistir()
