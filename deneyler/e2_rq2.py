"""E2 · RQ2 ağırlık dayanıklılığı (ön-kayıt docs/08 §5; KEŞİFSEL, betimsel).

Modlar (E1 ile aynı mantık):
  deneme — eğitim OOF 50/50 (A: öğrenme, B: değerlendirme), w0 = eşit; test yok, RAPORLANMAZ (deneyler/deneme/).
  gercek — w0 = AHP (docs/kaynaklar/ahp_yargilar.csv); tüm eğitimden öğrenilir, TEST kümesinde bir kez; kilitli.
Çalıştırma: .\\.venv\\Scripts\\python.exe deneyler\\e2_rq2.py deneme|gercek
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from sklearn.metrics import cohen_kappa_score
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deneyler.e1_rq1 import _turet
from src.ahp import yargilardan_agirlik
from src.dayaniklilik import critic_agirlik, dirichlet_kararlilik, entropi_agirlik
from src.kriterler import KRITERLER, YONLER, KriterHazirlayici
from src.politika import bant_esikleri, bantla, kotu_orani
from src.topsis import SabitTopsis
from src.veri_yukle import egitim_matrisi, test_matrisi

KOK = Path(__file__).resolve().parents[1]
ALFALAR = (10, 50, 200)


def calistir(mod):
    kilit = KOK / "deneyler" / "e2_rq2_sonuc.json"
    if mod == "gercek" and kilit.exists():
        raise SystemExit("E2 zaten test kümesinde koşuldu (deneyler/e2_rq2_sonuc.json).")
    Xtr, _ = egitim_matrisi()
    dtr = _turet(Xtr).merge(pd.read_csv(KOK / "data/processed/oof/final_oof.csv")[["SK_ID_CURR", "PD"]],
                            on="SK_ID_CURR", how="left")
    if mod == "deneme":
        w0 = np.ones(6) / 6
        fit, deg = train_test_split(dtr, test_size=0.5, stratify=dtr["TARGET"], random_state=42)
        pd_deg, y = deg["PD"].to_numpy(), deg["TARGET"].to_numpy()
        N, klasor, etiket = 300, KOK / "deneyler" / "deneme", "DENEME (eşit ağırlık) — RAPORLANMAZ"
    else:
        ahp = yargilardan_agirlik(KOK / "docs/kaynaklar/ahp_yargilar.csv")
        if not ahp["hepsi_tutarli"]:
            raise SystemExit("CR ≥ 0,10 olan yargıç var.")
        w0 = np.asarray(ahp["agirliklar"])
        fit = dtr
        Xte, yte = test_matrisi()
        deg = _turet(Xte)
        paket = joblib.load(KOK / "data/processed/model/final_model.joblib")
        pd_deg = paket["boru"].predict_proba(Xte)[:, 1]
        if paket["kalibrator"] is not None:
            pd_deg = paket["kalibrator"].predict(pd_deg)
        y = yte.to_numpy()
        N, klasor, etiket = 1000, KOK / "rapor" / "sekiller", "Test kümesi, AHP ağırlıkları etrafında"
    kh = KriterHazirlayici().fit(fit, fit["PD"])
    M_fit, M_deg = kh.transform(fit, fit["PD"]), kh.transform(deg, pd_deg)

    ref = SabitTopsis(w0, YONLER).fit(M_fit)
    c0 = ref.transform(M_deg)
    karar0 = bantla(c0, bant_esikleri(ref.transform(M_fit)))
    onay0 = karar0 == "Onayla"

    sonuc_alfa, S_hepsi = {}, {}
    for a in ALFALAR:
        r = dirichlet_kararlilik(M_fit, M_deg, w0, YONLER, alfa=a, N=N, tohum=42)
        S = r["S"]; S_hepsi[a] = S
        dusuk = S < 0.8
        sonuc_alfa[str(a)] = {
            "S_medyan": float(np.median(S)), "S<0.8_payi": float(dusuk.mean()), "S=1_payi": float((S == 1).mean()),
            "dusukS_icinde_sartli_payi": float((karar0[dusuk] == "Şartlı Onayla").mean()) if dusuk.any() else None,
            "sartli_icinde_dusukS_payi": float(dusuk[karar0 == "Şartlı Onayla"].mean()),
            "onaylanan_kotu_orani_dusukS": kotu_orani(y, onay0 & dusuk) if (onay0 & dusuk).any() else None,
            "onaylanan_kotu_orani_yuksekS": kotu_orani(y, onay0 & ~dusuk),
            "n_onay_dusukS": int((onay0 & dusuk).sum())}
        print(f"α={a:>3}: S medyan {np.median(S):.3f} | S<0,8 payı {dusuk.mean():.1%} | "
              f"Şartlı bandında düşük-S payı {sonuc_alfa[str(a)]['sartli_icinde_dusukS_payi']:.1%}", flush=True)

    yontemler = {"AHP (w0)": w0, "Eşit": np.ones(6) / 6,
                 "Entropi": entropi_agirlik(M_fit, YONLER), "CRITIC": critic_agirlik(M_fit, YONLER)}
    karsilastirma = {}
    for ad, w in yontemler.items():
        t = SabitTopsis(w, YONLER).fit(M_fit)
        c = t.transform(M_deg)
        k = bantla(c, bant_esikleri(t.transform(M_fit)))
        karsilastirma[ad] = {"agirliklar": dict(zip(KRITERLER, np.round(w, 4).tolist())),
                             "kendall_tau_vs_w0": float(kendalltau(c0, c).statistic),
                             "cohen_kappa_vs_w0": float(cohen_kappa_score(karar0, k)),
                             "onay_kotu_orani": kotu_orani(y, k == "Onayla")}
        print(f"{ad:9s} τ {karsilastirma[ad]['kendall_tau_vs_w0']:.3f} | κ {karsilastirma[ad]['cohen_kappa_vs_w0']:.3f} | "
              f"ağırlıklar {np.round(w, 2)}", flush=True)

    klasor.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    for a in ALFALAR:
        axes[0].hist(S_hepsi[a], bins=np.linspace(0.33, 1, 35), histtype="step", lw=1.8, label=f"α = {a}")
    axes[0].set_xlabel("Karar kararlılık indeksi S"); axes[0].set_ylabel("Başvuru sayısı"); axes[0].set_yscale("log")
    axes[0].set_title("Ağırlık belirsizliğinde karar kararlılığı"); axes[0].legend()
    x = np.arange(6); gen = 0.2
    for i, (ad, w) in enumerate(yontemler.items()):
        axes[1].bar(x + (i - 1.5) * gen, w, gen, label=ad)
    axes[1].set_xticks(x, ["PD", "Kredi/gelir", "Taksit/gelir", "Gelir", "İstihdam", "Gecikme"], rotation=20)
    axes[1].set_ylabel("Ağırlık"); axes[1].set_title("Ağırlıklandırma yöntemleri"); axes[1].legend(fontsize=8)
    fig.suptitle(etiket); fig.tight_layout(); fig.savefig(klasor / "10_rq2_dayaniklilik.png", dpi=120); plt.close(fig)

    kayit = {"tarih": date.today().isoformat(), "mod": mod, "N": N, "w0": dict(zip(KRITERLER, np.round(w0, 4).tolist())),
             "n_degerlendirme": int(len(y)), "alfa": sonuc_alfa, "yontemler": karsilastirma}
    hedef = kilit if mod == "gercek" else klasor / f"e2_deneme_{date.today().isoformat()}.json"
    hedef.write_text(json.dumps(kayit, ensure_ascii=False, indent=2, default=float), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("deneme", "gercek"):
        raise SystemExit("kullanım: e2_rq2.py deneme|gercek")
    calistir(sys.argv[1])
