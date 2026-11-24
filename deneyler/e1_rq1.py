"""E1 · RQ1 politika bedeli: PD-tek eşikleme vs AHP-TOPSIS (ön-kayıt docs/08_on_kayit_v1.md §3–§4).

Modlar:
  deneme  — eğitim OOF'u ikiye bölünür (A: kriter/TOPSIS/eşik öğrenme, B: değerlendirme), EŞİT ağırlık.
            Test kümesine dokunulmaz; sonuçlar RAPORLANMAZ (kod doğrulama), çıktı deneyler/deneme/.
  gercek  — ağırlıklar docs/kaynaklar/ahp_yargilar.csv (AHP, CR<0,10 şartı); her şey tüm eğitimden öğrenilir,
            TEST kümesinde bir kez değerlendirilir. Cinsiyetsiz final modelin test AUC'si de burada raporlanır (D16).
            Kilit: deneyler/e1_rq1_sonuc.json varsa çalışmaz.
Çalıştırma: .\\.venv\\Scripts\\python.exe deneyler\\e1_rq1.py deneme|gercek
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
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.ahp import yargilardan_agirlik
from src.kalibrasyon import ece
from src.kriterler import KRITERLER, YONLER, KriterHazirlayici
from src.oran_ozellikleri import oran_ozellikleri_ekle
from src.politika import (ORANLAR, bant_esikleri, bant_tablosu, bantla, egri, karsilastir, swap_set,
                          wpd_agirliklari)
from src.topsis import SabitTopsis
from src.veri_hazirlama import temizle_basvuru
from src.veri_yukle import egitim_matrisi, test_matrisi

KOK = Path(__file__).resolve().parents[1]
TOHUM = 42


def _turet(X):
    return oran_ozellikleri_ekle(temizle_basvuru(X)).reset_index(drop=True)


def _grafikler(e_pd, e_m, tarama, w0_pd, ana, klasor, etiket):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    a = np.array(e_pd["oran"]) * 100
    axes[0].plot(a, np.array(e_pd["kotu_orani"]) * 100, "o-", label="PD-tek")
    axes[0].plot(a, np.array(e_m["kotu_orani"]) * 100, "s-", label="AHP-TOPSIS")
    axes[0].set_xlabel("Onay oranı (%)"); axes[0].set_ylabel("Onaylananlarda kötü oranı (%)")
    axes[0].set_title("Eşit onay oranında kötü oranı"); axes[0].legend(); axes[0].axvspan(20, 80, alpha=0.08)
    axes[1].plot(a, np.array(e_pd["ihlal"]) * 100, "o-", label="PD-tek")
    axes[1].plot(a, np.array(e_m["ihlal"]) * 100, "s-", label="AHP-TOPSIS")
    axes[1].set_xlabel("Onay oranı (%)"); axes[1].set_ylabel("Onaylananlarda politika ihlali (%)")
    axes[1].set_title("Politika ihlali (KREDI_GELIR veya TAKSIT_GELIR > eğitim p90)"); axes[1].legend()
    fig.suptitle(etiket); fig.tight_layout(); fig.savefig(klasor / "08_rq1_egriler.png", dpi=120); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 5))
    x = [t["delta_ihlal"] * 100 for t in tarama]; y = [t["delta"] * 100 for t in tarama]
    ax.plot(x, y, "o-", color="#4C72B0")
    for t, xi, yi in zip(tarama, x, y):
        ax.annotate(f"{t['w_pd']:.1f}", (xi, yi), textcoords="offset points", xytext=(4, 4), fontsize=8)
    ax.plot(ana["delta_ihlal"]["deger"] * 100, ana["delta"]["deger"] * 100, "*", color="#C44E52", ms=16,
            label=f"AHP ağırlıkları (w_PD = {w0_pd:.2f})", zorder=5)
    ax.legend(loc="upper right")
    ax.axhline(0, color="k", lw=0.6); ax.axvline(0, color="k", lw=0.6)
    ax.set_xlabel("Δ politika ihlali (puan; negatif = daha az ihlal)")
    ax.set_ylabel("Δ kötü oranı (puan; pozitif = bedel)")
    ax.set_title(f"w_PD taraması (etiketler = PD ağırlığı; AHP w_PD = {w0_pd:.2f})\n{etiket}")
    fig.tight_layout(); fig.savefig(klasor / "09_rq1_wpd_tarama.png", dpi=120); plt.close(fig)


def calistir(mod):
    kilit = KOK / "deneyler" / "e1_rq1_sonuc.json"
    if mod == "gercek" and kilit.exists():
        raise SystemExit("E1 zaten test kümesinde koşuldu (deneyler/e1_rq1_sonuc.json).")

    Xtr, ytr = egitim_matrisi()
    dtr = _turet(Xtr)
    oof = pd.read_csv(KOK / "data/processed/oof/final_oof.csv")[["SK_ID_CURR", "PD"]]
    dtr = dtr.merge(oof, on="SK_ID_CURR", how="left")
    assert dtr["PD"].notna().all() and len(dtr) == len(Xtr)

    if mod == "deneme":
        w0 = np.ones(6) / 6
        ahp = {"not": "DENEME: eşit ağırlık (raporlanmaz)"}
        fit, deg = train_test_split(dtr, test_size=0.5, stratify=dtr["TARGET"], random_state=TOHUM)
        pd_deg = deg["PD"].to_numpy()
        y = deg["TARGET"].to_numpy()
        B = 200
        klasor = KOK / "deneyler" / "deneme"
        etiket = "DENEME (eğitim içi bölme, eşit ağırlık) — RAPORLANMAZ"
        model_test = None
    else:
        ahp = yargilardan_agirlik(KOK / "docs/kaynaklar/ahp_yargilar.csv")
        if not ahp["hepsi_tutarli"]:
            raise SystemExit(f"CR ≥ 0,10 olan yargıç var: { {k: round(v['CR'], 3) for k, v in ahp['bireysel'].items()} }")
        w0 = np.asarray(ahp["agirliklar"])
        fit = dtr
        Xte, yte = test_matrisi()
        deg = _turet(Xte)
        paket = joblib.load(KOK / "data/processed/model/final_model.joblib")
        pd_deg = paket["boru"].predict_proba(Xte)[:, 1]
        if paket["kalibrator"] is not None:
            pd_deg = paket["kalibrator"].predict(pd_deg)
        y = yte.to_numpy()
        model_test = {"roc_auc": float(roc_auc_score(y, pd_deg)), "ece": ece(y, pd_deg),
                      "ort_pd": float(pd_deg.mean()), "gozlenen": float(y.mean())}
        B = 1000
        klasor = KOK / "rapor" / "sekiller"
        etiket = "Test kümesi (n=61.502), AHP ağırlıkları"

    kh = KriterHazirlayici().fit(fit, fit["PD"])
    M_fit = kh.transform(fit, fit["PD"])
    M_deg = kh.transform(deg, pd_deg)
    topsis = SabitTopsis(w0, YONLER).fit(M_fit)
    c_fit, c_deg = topsis.transform(M_fit), topsis.transform(M_deg)
    s_pd, s_m = 1 - pd_deg, c_deg
    esik_kg = float(np.quantile(fit["KREDI_GELIR"], 0.9)); esik_tg = float(np.quantile(fit["TAKSIT_GELIR"], 0.9))
    kg, tg = deg["KREDI_GELIR"].to_numpy(), deg["TAKSIT_GELIR"].to_numpy()

    ana = karsilastir(y, s_pd, s_m, kg, tg, esik_kg, esik_tg, B=B, tohum=TOHUM)
    e_pd = egri(y, s_pd, kg, tg, esik_kg, esik_tg); e_m = egri(y, s_m, kg, tg, esik_kg, esik_tg)
    sw = swap_set(y, s_pd, s_m, 0.7)
    profil = {grp: dict(zip(KRITERLER, M_deg[sw[f"maske_{grp}"]].mean(axis=0).round(4).tolist()))
              for grp in ("yalniz_pd", "yalniz_mcdm")}
    tarama = []
    for w_pd in np.round(np.arange(0, 1.01, 0.1), 2):
        w = wpd_agirliklari(w0, w_pd)
        c = SabitTopsis(w, YONLER).fit(M_fit).transform(M_deg)
        r = karsilastir(y, s_pd, c, kg, tg, esik_kg, esik_tg, B=1)
        tarama.append({"w_pd": float(w_pd), "delta": r["delta"]["deger"], "delta_ihlal": r["delta_ihlal"]["deger"]})
    esik_m = bant_esikleri(c_fit); esik_p = bant_esikleri(1 - fit["PD"].to_numpy())
    bant = {"esikler_mcdm_Cstar": esik_m, "esikler_pdtek_1-PD": esik_p,
            "mcdm": bant_tablosu(y, bantla(s_m, esik_m)), "pd_tek": bant_tablosu(y, bantla(s_pd, esik_p))}

    klasor.mkdir(parents=True, exist_ok=True)
    _grafikler(e_pd, e_m, tarama, float(w0[0]), ana, klasor, etiket)
    for k, v in ana.items():
        print(f"{k:15s} {v['deger']*100:+.2f} puan  [%95 GA {v['ga_alt']*100:+.2f}, {v['ga_ust']*100:+.2f}]")
    print("Swap-set (a=0,70):", {k: v for k, v in sw.items() if not k.startswith("maske")})
    print("w_PD=1,0 sağlaması (≈0 beklenir): Δ =", round(tarama[-1]["delta"] * 100, 3), "puan")
    print("Bantlar (AHP-TOPSIS):", {b: (v["n"], round(v["kotu_orani"], 4)) for b, v in bant["mcdm"].items()})
    if model_test:
        print("Cinsiyetsiz final model, test:", model_test)

    kayit = {"tarih": date.today().isoformat(), "mod": mod, "w0": dict(zip(KRITERLER, np.round(w0, 4).tolist())),
             "ahp": {k: v for k, v in ahp.items() if k != "agirliklar"} if mod == "gercek" else ahp,
             "n_degerlendirme": int(len(y)), "B": B, "ihlal_esikleri_p90": {"KREDI_GELIR": esik_kg, "TAKSIT_GELIR": esik_tg},
             "birincil_ve_ikincil": ana, "egri_pd_tek": e_pd, "egri_mcdm": e_m,
             "swap_set_a07": {k: v for k, v in sw.items() if not k.startswith("maske")}, "swap_profili": profil,
             "wpd_taramasi": tarama, "bantlar": bant, "final_model_test": model_test}
    hedef = kilit if mod == "gercek" else klasor / f"e1_deneme_{date.today().isoformat()}.json"
    hedef.write_text(json.dumps(kayit, ensure_ascii=False, indent=2, default=float), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("deneme", "gercek"):
        raise SystemExit("kullanım: e1_rq1.py deneme|gercek")
    calistir(sys.argv[1])
