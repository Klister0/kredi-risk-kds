"""M7 · Değerlendirme ölçütleri ve eşleştirilmiş bootstrap güven aralıkları.

Kritik parça (CLAUDE.md §3): bootstrap sıfırdan. Eşleştirilmiş: her yeniden örneklemde AYNI satırlar
tüm modellere uygulanır, böylece model farklarının GA'sı (paired difference) geçerli olur.
"""
from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score

from src.kalibrasyon import ece


def ks_istatistigi(y, p) -> float:
    """Kolmogorov–Smirnov: iyi ve kötülerin skor birikimli dağılımları arasındaki en büyük fark."""
    y = np.asarray(y)
    p = np.asarray(p, dtype=float)
    sira = np.argsort(p, kind="mergesort")
    ys = y[sira]
    kotu = np.cumsum(ys) / max(ys.sum(), 1)
    iyi = np.cumsum(1 - ys) / max((1 - ys).sum(), 1)
    return float(np.max(np.abs(kotu - iyi)))


OLCUTLER = {
    "roc_auc": lambda y, p: roc_auc_score(y, p),
    "gini": lambda y, p: 2 * roc_auc_score(y, p) - 1,
    "ks": ks_istatistigi,
    "pr_auc": lambda y, p: average_precision_score(y, p),
    "brier": lambda y, p: brier_score_loss(y, p),
    "ece": lambda y, p: ece(y, p),
}


def bootstrap(y, tahminler: dict, olcutler=OLCUTLER, B: int = 1000, tohum: int = 42,
              referans: str | None = None) -> dict:
    """Her model ve ölçüt için nokta tahmini + %95 yüzdelik GA; referans verilirse eşleştirilmiş farklar."""
    y = np.asarray(y)
    tahminler = {m: np.asarray(p, dtype=float) for m, p in tahminler.items()}
    rng = np.random.default_rng(tohum)
    n = len(y)
    indeksler = rng.integers(0, n, size=(B, n))
    sonuc = {}
    ornekler = {m: {o: np.empty(B) for o in olcutler} for m in tahminler}
    for b in range(B):
        i = indeksler[b]
        yb = y[i]
        for m, p in tahminler.items():
            for o, f in olcutler.items():
                ornekler[m][o][b] = f(yb, p[i])
    for m, p in tahminler.items():
        sonuc[m] = {o: {"deger": float(f(y, p)),
                        "ga_alt": float(np.percentile(ornekler[m][o], 2.5)),
                        "ga_ust": float(np.percentile(ornekler[m][o], 97.5))}
                    for o, f in olcutler.items()}
    if referans is not None:
        sonuc["farklar"] = {}
        for m in tahminler:
            if m == referans:
                continue
            sonuc["farklar"][f"{referans}-{m}"] = {
                o: {"deger": sonuc[referans][o]["deger"] - sonuc[m][o]["deger"],
                    "ga_alt": float(np.percentile(ornekler[referans][o] - ornekler[m][o], 2.5)),
                    "ga_ust": float(np.percentile(ornekler[referans][o] - ornekler[m][o], 97.5))}
                for o in olcutler}
    return sonuc
