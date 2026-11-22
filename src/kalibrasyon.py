"""M6 · Olasılık kalibrasyonu: ölçütler ve sızıntısız kalibrasyon.

Neden önemli: TOPSIS PD'nin DEĞERİNİ kullanır (sıralamasını değil). Ayırt edicilik (AUC)
iyi olsa bile olasılıklar kaymışsa karar katmanı yanlış girdi alır.
"""
from __future__ import annotations

import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.model_selection import StratifiedKFold


def ece(y, p, n_kutu: int = 10) -> float:
    """Beklenen kalibrasyon hatası (eşit frekanslı kutular).

    Her kutuda |ortalama tahmin − gözlenen oran|, kutu payıyla ağırlıklı toplam.
    Eşit frekans: %8 pozitifli veride eşit genişlikli kutuların çoğu boş kalırdı.
    """
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    sira = np.argsort(p, kind="mergesort")
    kutular = np.array_split(sira, n_kutu)
    n = len(p)
    return float(sum(len(k) / n * abs(p[k].mean() - y[k].mean()) for k in kutular if len(k)))


def prior_duzeltme(p, agirlik: float):
    """Pozitifler `agirlik` katı ağırlıklandırılarak eğitilen modelin olasılığını geri düzeltir.

    Ağırlık w ile eğitim, pozitifleri w kat çoğaltmaya denktir; düzeltme:
        p_gercek = p / (p + w·(1 − p))
    (Dal Pozzolo ve ark. 2015'teki undersampling düzeltmesinin ağırlık karşılığı.)
    """
    p = np.asarray(p, dtype=float)
    return p / (p + agirlik * (1.0 - p))


def cv_isotonic(skor, y, n_kat: int = 5, tohum: int = 42) -> np.ndarray:
    """OOF skorlarını çapraz doğrulamalı isotonic regresyonla kalibre eder.

    Her satırın kalibrasyon eşlemesi, o satırın etiketi görülmeden öğrenilir.
    """
    skor = np.asarray(skor, dtype=float)
    y = np.asarray(y)
    cikti = np.empty_like(skor)
    cv = StratifiedKFold(n_splits=n_kat, shuffle=True, random_state=tohum)
    for egit, dogr in cv.split(skor.reshape(-1, 1), y):
        iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
        iso.fit(skor[egit], y[egit])
        cikti[dogr] = iso.predict(skor[dogr])
    return cikti
