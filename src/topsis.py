"""K3 · TOPSIS, sıfırdan: klasik (batch) ve eğitimden sabit referanslı.

Adımlar: (1) normalizasyon r_ij = x_ij / sqrt(Σ_i x_ij²)  (vektör normalizasyonu)
(2) ağırlıklı matris v_ij = w_j · r_ij
(3) ideal (A+) ve anti-ideal (A−): fayda kriterinde A+ = en büyük, maliyette en küçük
(4) uzaklıklar S+ = ||v − A+||, S− = ||v − A−||
(5) yakınlık katsayısı C* = S− / (S+ + S−) ∈ [0, 1]; 1 = ideale en yakın (en iyi).

Neden "sabit referans" (D21)? Klasik TOPSIS'te normalizasyon ve A+/A− değerlendirilen kümeden
hesaplanır: tek başvuruda tanımsızdır ve küme değişince aynı başvurunun puanı/sırası değişebilir
(rank reversal; García-Cascales & Lamata 2012). SabitTopsis bu değerleri YALNIZ eğitimden öğrenir
(sızıntısız) ve her başvuruyu bağımsız puanlar.
"""
from __future__ import annotations

import numpy as np

FAYDA, MALIYET = 1, -1


def _hazirla(w, yon, m):
    w = np.asarray(w, dtype=float)
    yon = np.asarray(yon)
    if w.shape != (m,) or yon.shape != (m,):
        raise ValueError("ağırlık ve yön sayısı kriter sayısına eşit olmalı")
    if (w < 0).any() or w.sum() <= 0:
        raise ValueError("ağırlıklar negatif olamaz ve toplamı pozitif olmalı")
    if not np.isin(yon, [FAYDA, MALIYET]).all():
        raise ValueError("yön +1 (fayda) ya da -1 (maliyet) olmalı")
    return w / w.sum(), yon


def _yakinlik(V, ideal, anti):
    s_arti = np.sqrt(((V - ideal) ** 2).sum(axis=1))
    s_eksi = np.sqrt(((V - anti) ** 2).sum(axis=1))
    payda = s_arti + s_eksi
    return np.where(payda > 0, s_eksi / np.where(payda > 0, payda, 1.0), 0.5)


def batch_topsis(X, w, yon) -> np.ndarray:
    """Klasik TOPSIS: normalizasyon ve ideal noktalar verilen kümeden."""
    X = np.asarray(X, dtype=float)
    w, yon = _hazirla(w, yon, X.shape[1])
    norm = np.sqrt((X ** 2).sum(axis=0))
    V = X / np.where(norm > 0, norm, 1.0) * w
    ideal = np.where(yon == FAYDA, V.max(axis=0), V.min(axis=0))
    anti = np.where(yon == FAYDA, V.min(axis=0), V.max(axis=0))
    return _yakinlik(V, ideal, anti)


class SabitTopsis:
    """Eğitimden öğrenilen kırpma sınırları, normalizasyon paydası ve ideal/anti-ideal ile TOPSIS.

    fit(X_egitim): alt/üst yüzdelik (varsayılan p1/p99), kırpılmış eğitimin vektör normu,
    A+/A− = kırpma sınırlarının ağırlıklı-normalize hâli. transform(X): her satırı bağımsız puanlar.
    Eğitim kümesinin kendisinde batch_topsis(kırpılmış eğitim) ile aynı sonucu verir (testli).
    """

    def __init__(self, agirlik, yon, alt_yuzdelik: float = 1.0, ust_yuzdelik: float = 99.0):
        self.agirlik = agirlik
        self.yon = yon
        self.alt_yuzdelik = alt_yuzdelik
        self.ust_yuzdelik = ust_yuzdelik

    def fit(self, X):
        X = np.asarray(X, dtype=float)
        self.w_, self.yon_ = _hazirla(self.agirlik, self.yon, X.shape[1])
        self.alt_ = np.nanpercentile(X, self.alt_yuzdelik, axis=0)
        self.ust_ = np.nanpercentile(X, self.ust_yuzdelik, axis=0)
        Xk = np.clip(X, self.alt_, self.ust_)
        norm = np.sqrt((Xk ** 2).sum(axis=0))
        self.norm_ = np.where(norm > 0, norm, 1.0)
        v_alt = self.alt_ / self.norm_ * self.w_
        v_ust = self.ust_ / self.norm_ * self.w_
        self.ideal_ = np.where(self.yon_ == FAYDA, v_ust, v_alt)
        self.anti_ = np.where(self.yon_ == FAYDA, v_alt, v_ust)
        return self

    def transform(self, X) -> np.ndarray:
        X = np.atleast_2d(np.asarray(X, dtype=float))
        if np.isnan(X).any():
            raise ValueError("TOPSIS girdisinde NaN var: önce kriter eksik kuralları uygulanmalı (D34)")
        V = np.clip(X, self.alt_, self.ust_) / self.norm_ * self.w_
        return _yakinlik(V, self.ideal_, self.anti_)

    def fit_transform(self, X):
        return self.fit(X).transform(X)
