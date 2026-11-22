"""M8 · SHAP açıklamaları (final XGBoost) + LR katsayılarıyla tutarlılık kontrolü.

Eğitim kümesinden 10.000 başvuruluk örneklem (test kilitli). Çıktılar:
  rapor/sekiller/05_shap_global.png, 06_shap_dagilim.png, 07_shap_ornek_basvurular.png
  deneyler/m8_shap_<tarih>.json
Çalıştırma: .\\.venv\\Scripts\\python.exe deneyler\\m8_shap.py
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
import shap
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.aciklama import degiskene_topla, global_onem, shap_hesapla
from deneyler.final_model import SURUM
from src.veri_yukle import egitim_matrisi

KOK = Path(__file__).resolve().parents[1]
SEKIL = KOK / "rapor" / "sekiller"
ETIKET = {
    "EXT_ORT": "EXT_ORT (dış skor ort.)", "EXT_SOURCE_1": "EXT_SOURCE_1", "EXT_SOURCE_2": "EXT_SOURCE_2",
    "EXT_SOURCE_3": "EXT_SOURCE_3", "ODEME_ORANI": "Ödeme oranı (taksit/kredi)", "YAS_YIL": "Yaş (yıl)",
    "ISTIHDAM_YIL": "İstihdam (yıl)", "KREDI_MAL_ORANI": "Kredi/mal fiyatı", "AMT_GOODS_PRICE": "Mal fiyatı",
    "AMT_ANNUITY": "Taksit tutarı", "AMT_CREDIT": "Kredi tutarı", "CODE_GENDER": "Cinsiyet",
    "BURO_AKTIF_SAYISI": "Büro: aktif kredi sayısı", "BURO_SON_KREDI_GUN": "Büro: son kredi (gün)",
    "BURO_BORC_ORANI": "Büro: borç oranı", "NAME_EDUCATION_TYPE": "Eğitim düzeyi",
    "ORGANIZATION_TYPE": "Kurum türü", "OCCUPATION_TYPE": "Meslek", "KREDI_GELIR": "Kredi/gelir",
    "TAKSIT_GELIR": "Taksit/gelir", "AMT_INCOME_TOTAL": "Gelir", "BURO_GECIKMELI_SAYISI": "Büro: gecikmeli kredi",
    "DAYS_BIRTH": "DAYS_BIRTH (yaş, gün)", "DAYS_EMPLOYED": "DAYS_EMPLOYED", "ISTIHDAM_ANOMALI": "İstihdam anomali bayrağı",
}
et = lambda v: ETIKET.get(v, v)


def calistir(n=10_000):
    paket = joblib.load(KOK / "data/processed/model/final_model.joblib")
    boru = paket["boru"]
    X, y = egitim_matrisi(ornek=n)
    S, taban, Z, adlar, kaynak = shap_hesapla(boru, X)
    Sd = degiskene_topla(S, kaynak)
    onem = global_onem(Sd)
    pd_ = boru.predict_proba(X)[:, 1]
    print("En önemli 10 değişken (ort. |SHAP|, log-odds):")
    print(onem.head(10).round(4).to_string(), flush=True)

    SEKIL.mkdir(parents=True, exist_ok=True)
    # 1) Global önem (değişken düzeyi, ilk 20)
    ilk = onem.head(20)[::-1]
    fig, ax = plt.subplots(figsize=(7, 6.5))
    ax.barh([et(v) for v in ilk.index], ilk.values, color="#4C72B0")
    ax.set_xlabel("Ortalama |SHAP| (log-odds)")
    ax.set_title("Final XGBoost: değişken önemi (SHAP, eğitim örneklemi n=10.000)")
    fig.tight_layout(); fig.savefig(SEKIL / "05_shap_global.png", dpi=120); plt.close(fig)

    # 2) Dağılım (beeswarm): en önemli sayısal özellikler, renk = özellik değeri
    sayisal = [i for i, (a, k) in enumerate(zip(adlar, kaynak)) if a == k]
    sira = sorted(sayisal, key=lambda i: -np.abs(S[:, i]).mean())[:12]
    plt.figure()
    shap.summary_plot(S[:, sira], Z[:, sira], feature_names=[et(adlar[i]) for i in sira],
                      show=False, plot_size=(8, 6))
    plt.title("SHAP dağılımı: sağa = temerrüt riskini artırır; renk = değişken değeri")
    plt.tight_layout(); plt.savefig(SEKIL / "06_shap_dagilim.png", dpi=120); plt.close("all")

    # 3) Yerel açıklama: düşük ve yüksek PD'li iki örnek başvuru
    secim = {"Düşük riskli başvuru": int(np.argsort(pd_)[int(0.10 * n)]),
             "Yüksek riskli başvuru": int(np.argsort(pd_)[int(0.98 * n)])}
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    ornekler = {}
    for ax, (baslik, i) in zip(axes, secim.items()):
        katki = Sd.iloc[i]
        ust = katki.reindex(katki.abs().sort_values(ascending=False).index[:8])
        diger = katki.sum() - ust.sum()
        seri = pd.concat([ust, pd.Series({"Diğer değişkenler": diger})])[::-1]
        ax.barh([et(v) for v in seri.index], seri.values,
                color=["#C44E52" if v > 0 else "#4C72B0" for v in seri.values])
        ax.axvline(0, color="k", lw=0.8)
        ax.set_title(f"{baslik}: PD = {pd_[i]:.1%}  (taban ≈ {1/(1+np.exp(-taban)):.1%})")
        ax.set_xlabel("Katkı (log-odds); kırmızı = riski artırır, mavi = azaltır")
        ornekler[baslik] = {"SK_ID_CURR": int(X["SK_ID_CURR"].iloc[i]), "PD": float(pd_[i]),
                            "en_buyuk_katkilar": {k: float(v) for k, v in ust.items()}}
    fig.tight_layout(); fig.savefig(SEKIL / "07_shap_ornek_basvurular.png", dpi=120); plt.close(fig)

    # 4) Tutarlılık: LR (M5 parametreleri, tüm eğitim) katsayıları vs SHAP (ortak sayısal özellikler)
    from deneyler.m7_test import diger_modeller
    Xtam, ytam = egitim_matrisi()
    lr = diger_modeller()["logreg"].fit(Xtam, ytam)
    from src.aciklama import ozellik_eslemesi
    lr_adlar, lr_kaynak = ozellik_eslemesi(lr)
    katsayi = pd.Series(lr.named_steps["model"].coef_[0], index=lr_adlar)
    ortak = [a for a, k in zip(adlar, kaynak) if a == k and a in katsayi.index]
    shap_yon = pd.Series([np.corrcoef(Z[:, adlar.index(a)], S[:, adlar.index(a)])[0, 1]
                          if np.std(Z[:, adlar.index(a)]) > 0 else 0.0 for a in ortak], index=ortak)
    shap_ort = pd.Series([np.abs(S[:, adlar.index(a)]).mean() for a in ortak], index=ortak)
    ilk15 = shap_ort.sort_values(ascending=False).index[:15]
    yon_uyumu = float((np.sign(shap_yon[ilk15]) == np.sign(katsayi[ilk15])).mean())
    rho = float(spearmanr(shap_ort[ilk15], katsayi[ilk15].abs()).statistic)
    print(f"LR–SHAP yön uyumu (SHAP ilk 15 sayısal): {yon_uyumu:.0%} | önem sıra korelasyonu ρ = {rho:.2f}")

    kayit = {"tarih": date.today().isoformat(), "n_ornek": n, "taban_log_odds": taban,
             "global_onem_ilk20": {k: float(v) for k, v in onem.head(20).items()},
             "ornek_basvurular": ornekler,
             "lr_tutarlilik": {"yon_uyumu_ilk15": yon_uyumu, "spearman_onem_ilk15": rho,
                               "ayrinti": {a: {"lr_katsayi": float(katsayi[a]), "shap_yon_korelasyon": float(shap_yon[a]),
                                               "ort_abs_shap": float(shap_ort[a])} for a in ilk15}}}
    (KOK / "deneyler" / f"m8_shap_{date.today().isoformat()}_{SURUM}.json").write_text(
        json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    calistir()
