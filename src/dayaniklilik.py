"""E2 · RQ2 ağırlık dayanıklılığı (ön-kayıt docs/08 §5, KEŞİFSEL).

1) Dirichlet belirsizliği: w ~ Dirichlet(α·w0). α büyüdükçe çekimler w0'a yakınlaşır (dar belirsizlik).
   Her çekimde bant eşikleri EĞİTİM C* niceliklerinden yeniden hesaplanır, değerlendirme kümesine uygulanır.
   Karar kararlılık indeksi S_i = max_k P(karar_i = k)  (1 = her çekimde aynı karar).
2) Ağırlıklandırma yöntemleri: entropi ve CRITIC (veri temelli, politika bilmez) vs AHP.
"""
from __future__ import annotations

import numpy as np

from src.politika import BANTLAR, bant_esikleri, bantla
from src.topsis import FAYDA, SabitTopsis


def dirichlet_kararlilik(M_egitim, M_deg, w0, yon, alfa: float, N: int = 1000, tohum: int = 42,
                         red: float = 0.15, sartli: float = 0.15) -> dict:
    """Her değerlendirme başvurusu için karar sıklıkları ve S indeksi."""
    rng = np.random.default_rng(tohum)
    w0 = np.asarray(w0, dtype=float) / np.sum(w0)
    sayac = np.zeros((len(M_deg), len(BANTLAR)), dtype=np.int32)
    cekimler = rng.dirichlet(alfa * w0, size=N)
    ref = SabitTopsis(w0, yon).fit(M_egitim)                       # kırpma/norm ağırlıktan bağımsız
    for w in cekimler:
        t = SabitTopsis(w, yon)
        t.w_, t.yon_, t.alt_, t.ust_, t.norm_ = w / w.sum(), ref.yon_, ref.alt_, ref.ust_, ref.norm_
        v_alt, v_ust = t.alt_ / t.norm_ * t.w_, t.ust_ / t.norm_ * t.w_
        t.ideal_ = np.where(t.yon_ == FAYDA, v_ust, v_alt)
        t.anti_ = np.where(t.yon_ == FAYDA, v_alt, v_ust)
        esik = bant_esikleri(t.transform(M_egitim), red, sartli)
        karar = bantla(t.transform(M_deg), esik)
        for k, b in enumerate(BANTLAR):
            sayac[:, k] += karar == b
    olasilik = sayac / N
    return {"olasilik": olasilik, "S": olasilik.max(axis=1), "cekimler": cekimler}


def _minmax_yonlu(M, yon):
    M = np.asarray(M, dtype=float)
    alt, ust = M.min(axis=0), M.max(axis=0)
    aralik = np.where(ust > alt, ust - alt, 1.0)
    Z = (M - alt) / aralik
    return np.where(np.asarray(yon) == FAYDA, Z, 1 - Z)


def entropi_agirlik(M, yon) -> np.ndarray:
    """Entropi yöntemi: kriterin değerleri ne kadar dağınıksa (düşük entropi) ağırlığı o kadar yüksek."""
    Z = _minmax_yonlu(M, yon) + 1e-12
    P = Z / Z.sum(axis=0)
    e = -(P * np.log(P)).sum(axis=0) / np.log(len(Z))
    d = 1 - e
    return d / d.sum()


def critic_agirlik(M, yon) -> np.ndarray:
    """CRITIC: ağırlık ∝ std × Σ(1 − korelasyon) — hem değişkenliği hem diğer kriterlerle çatışmayı ödüllendirir."""
    Z = _minmax_yonlu(M, yon)
    s = Z.std(axis=0, ddof=1)
    with np.errstate(invalid="ignore", divide="ignore"):      # sabit kriterde korelasyon tanımsız → 0
        R = np.nan_to_num(np.corrcoef(Z, rowvar=False))
    C = s * (1 - R).sum(axis=0)
    return C / C.sum()
