r"""V2 · Keşifsel veri analizi (EDA) — application_train.

Sızıntı disiplini (D33): EDA YALNIZCA eğitim kümesinde yapılır. Bölme (V3) daha önce
yapıldığı için burada test kimliklerine bakılmaz. Çıktılar: konsol özeti + rapor/sekiller/ grafikleri.

Çalıştırma (proje kökünden):
    .\.venv\Scripts\python.exe notebooks\01_kesif.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

KOK = Path(__file__).resolve().parents[1]
SEKIL = KOK / "rapor" / "sekiller"
C0, C1 = "#4C72B0", "#C44E52"


def egitim_verisi() -> pd.DataFrame:
    """application_train'i yükler, yalnız eğitim kimliklerini döndürür (D33)."""
    ids = set(pd.read_csv(KOK / "data/processed/bolme/egitim_kimlikleri.csv")["SK_ID_CURR"])
    df = pd.read_csv(KOK / "data/raw/application_train.csv")
    return df[df["SK_ID_CURR"].isin(ids)].copy()


def ozet(e: pd.DataFrame) -> None:
    t = e["TARGET"]
    print(f"Eğitim satır: {len(e):,} | sütun: {e.shape[1]}")
    print(f"TARGET oranı: %{t.mean()*100:.2f} (pozitif {int(t.sum()):,})")
    anom = e["DAYS_EMPLOYED"] == 365243
    print(f"DAYS_EMPLOYED=365243: %{anom.mean()*100:.1f} "
          f"(temerrüt anomali %{e.loc[anom,'TARGET'].mean()*100:.2f} vs "
          f"normal %{e.loc[~anom,'TARGET'].mean()*100:.2f})")
    miss = (e.isna().mean() * 100).sort_values(ascending=False)
    print(f">%50 eksik sütun: {int((miss>50).sum())} | hiç eksiksiz: {int((miss==0).sum())}")
    for c in ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]:
        print(f"  {c}: eksik %{e[c].isna().mean()*100:.1f}, "
              f"TARGET korelasyon {e[[c,'TARGET']].corr().iloc[0,1]:.3f}")
    print(f"Bellek (deep): {e.memory_usage(deep=True).sum()/1e6:.0f} MB")


def sekiller(e: pd.DataFrame) -> None:
    SEKIL.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"figure.dpi": 120, "font.size": 11})

    v = e["TARGET"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(["0 · Ödüyor", "1 · Güçlük"], v.values, color=[C0, C1])
    for i, val in enumerate(v.values):
        ax.text(i, val, f"{val:,}\n%{val/len(e)*100:.1f}", ha="center", va="bottom")
    ax.set_title(f"TARGET dağılımı (eğitim, n={len(e):,})")
    ax.set_ylabel("Başvuru"); ax.set_ylim(0, v.max() * 1.15)
    fig.tight_layout(); fig.savefig(SEKIL / "01_target_dengesizligi.png"); plt.close(fig)

    miss = (e.isna().mean() * 100).sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(miss.index[::-1], miss.values[::-1], color=C0)
    ax.set_title("En çok eksik 15 sütun (eğitim %)"); ax.set_xlabel("Eksik (%)")
    fig.tight_layout(); fig.savefig(SEKIL / "02_eksik_sutunlar.png"); plt.close(fig)

    anom = e["DAYS_EMPLOYED"] == 365243
    rates = [e.loc[~anom, "TARGET"].mean() * 100, e.loc[anom, "TARGET"].mean() * 100]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar([f"Normal\n(n={(~anom).sum():,})", f"Anomali\n(n={anom.sum():,})"],
           rates, color=[C0, C1])
    for i, r in enumerate(rates):
        ax.text(i, r, f"%{r:.2f}", ha="center", va="bottom")
    ax.set_title("DAYS_EMPLOYED=365243 ve temerrüt"); ax.set_ylabel("Temerrüt (%)")
    ax.set_ylim(0, max(rates) * 1.2)
    fig.tight_layout(); fig.savefig(SEKIL / "03_istihdam_anomalisi.png"); plt.close(fig)


if __name__ == "__main__":
    e = egitim_verisi()
    ozet(e)
    sekiller(e)
    print(f"Grafikler: {SEKIL}")
