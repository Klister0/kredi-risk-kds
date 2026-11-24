"""E1 (RQ1) · Politika karşılaştırması: PD-tek eşikleme vs AHP-TOPSIS (ön-kayıt docs/08 §4).

Onay kuralı: değerlendirilen küme içinde skoru en yüksek a oranı onaylanır (sıralama temelli,
etiket kullanılmaz). Kötü oranı BR(a) = onaylananlarda TARGET=1 oranı.
Birincil metrik: Δ = ortalama_{a∈A} [BR_MCDM(a) − BR_PD(a)],  A = {0,2; …; 0,8}.
"""
from __future__ import annotations

import numpy as np

ORANLAR = np.round(np.arange(0.1, 0.91, 0.1), 2)
BIRINCIL = np.round(np.arange(0.2, 0.81, 0.1), 2)


def onayla(skor, a: float) -> np.ndarray:
    """Skoru en yüksek ⌈a·n⌉ başvuru (eşitlikte sıra korunur)."""
    skor = np.asarray(skor, dtype=float)
    k = int(np.ceil(a * len(skor)))
    onay = np.zeros(len(skor), dtype=bool)
    onay[np.argsort(-skor, kind="mergesort")[:k]] = True
    return onay


def kotu_orani(y, onay) -> float:
    y = np.asarray(y)
    return float(y[onay].mean()) if onay.any() else float("nan")


def ihlal_orani(onay, kredi_gelir, taksit_gelir, esik_kg: float, esik_tg: float) -> float:
    """Onaylananlarda KREDI_GELIR > eşik VEYA TAKSIT_GELIR > eşik olanların payı (eşikler eğitim p90)."""
    ihlal = (np.asarray(kredi_gelir) > esik_kg) | (np.asarray(taksit_gelir) > esik_tg)
    return float(ihlal[onay].mean()) if onay.any() else float("nan")


def egri(y, skor, kg, tg, esik_kg, esik_tg, oranlar=ORANLAR) -> dict:
    out = {"oran": [], "kotu_orani": [], "ihlal": []}
    for a in oranlar:
        o = onayla(skor, a)
        out["oran"].append(float(a)); out["kotu_orani"].append(kotu_orani(y, o))
        out["ihlal"].append(ihlal_orani(o, kg, tg, esik_kg, esik_tg))
    return out


def _ozet(y, s_pd, s_mcdm, ihlal_vektor, oranlar):
    """Bir örneklemde: Δ (kötü oranı), Δ_ihlal (ortalama), a=0,7'de ihlal farkı."""
    br_pd, br_m, ih_pd, ih_m = [], [], [], []
    for a in oranlar:
        op, om = onayla(s_pd, a), onayla(s_mcdm, a)
        br_pd.append(y[op].mean()); br_m.append(y[om].mean())
        ih_pd.append(ihlal_vektor[op].mean()); ih_m.append(ihlal_vektor[om].mean())
    br_pd, br_m, ih_pd, ih_m = map(np.array, (br_pd, br_m, ih_pd, ih_m))
    i07 = int(np.argmin(np.abs(np.asarray(oranlar) - 0.7)))
    return {"delta": float((br_m - br_pd).mean()),
            "delta_ihlal": float((ih_m - ih_pd).mean()),
            "ihlal_fark_a07": float(ih_m[i07] - ih_pd[i07])}


def karsilastir(y, s_pd, s_mcdm, kg, tg, esik_kg, esik_tg, B: int = 1000, tohum: int = 42,
                oranlar=BIRINCIL) -> dict:
    """Nokta tahmini + eşleştirilmiş bootstrap %95 GA (aynı yeniden örneklem iki politikaya)."""
    y = np.asarray(y)
    s_pd = np.asarray(s_pd, dtype=float)
    s_mcdm = np.asarray(s_mcdm, dtype=float)
    ihlal = ((np.asarray(kg) > esik_kg) | (np.asarray(tg) > esik_tg)).astype(float)
    nokta = _ozet(y, s_pd, s_mcdm, ihlal, oranlar)
    rng = np.random.default_rng(tohum)
    n = len(y)
    orn = {k: np.empty(B) for k in nokta}
    for b in range(B):
        i = rng.integers(0, n, n)
        r = _ozet(y[i], s_pd[i], s_mcdm[i], ihlal[i], oranlar)
        for k in nokta:
            orn[k][b] = r[k]
    return {k: {"deger": nokta[k], "ga_alt": float(np.percentile(orn[k], 2.5)),
                "ga_ust": float(np.percentile(orn[k], 97.5))} for k in nokta}


def swap_set(y, s_pd, s_mcdm, a: float = 0.7) -> dict:
    """a oranında iki politikanın farklı karar verdiği başvurular (betimsel, keşifsel)."""
    y = np.asarray(y)
    op, om = onayla(s_pd, a), onayla(s_mcdm, a)
    yalniz_pd = op & ~om
    yalniz_m = om & ~op
    return {"a": a, "n_yalniz_pd_onaylar": int(yalniz_pd.sum()), "n_yalniz_mcdm_onaylar": int(yalniz_m.sum()),
            "kotu_orani_yalniz_pd": kotu_orani(y, yalniz_pd), "kotu_orani_yalniz_mcdm": kotu_orani(y, yalniz_m),
            "maske_yalniz_pd": yalniz_pd, "maske_yalniz_mcdm": yalniz_m}


def wpd_agirliklari(w0, w_pd: float) -> np.ndarray:
    """K1 (PD) ağırlığı w_pd; kalan 1−w_pd diğer kriterlere w0 oranlarıyla dağıtılır."""
    w0 = np.asarray(w0, dtype=float)
    diger = w0[1:] / w0[1:].sum()
    return np.r_[w_pd, (1 - w_pd) * diger]


# --- K4 · Karar bantları (K-D: eşikler YALNIZ eğitimden; ön-kayıt docs/08 §3) ---
BANTLAR = ("Reddet", "Şartlı Onayla", "Onayla")


def bant_esikleri(skor_egitim, red: float = 0.15, sartli: float = 0.15) -> tuple[float, float]:
    """Eğitim skor niceliklerinden (Reddet üst sınırı, Şartlı üst sınırı). Yüksek skor = iyi."""
    s = np.asarray(skor_egitim, dtype=float)
    return float(np.quantile(s, red)), float(np.quantile(s, red + sartli))


def bantla(skor, esikler) -> np.ndarray:
    t_red, t_sartli = esikler
    s = np.asarray(skor, dtype=float)
    return np.where(s < t_red, BANTLAR[0], np.where(s < t_sartli, BANTLAR[1], BANTLAR[2]))


def bant_tablosu(y, bantlar) -> dict:
    """Bant başına başvuru sayısı, payı ve kötü oranı (T10: gruplar ayrışıyor mu?)."""
    y = np.asarray(y)
    return {b: {"n": int((bantlar == b).sum()), "pay": float((bantlar == b).mean()),
                "kotu_orani": kotu_orani(y, bantlar == b)} for b in BANTLAR}
