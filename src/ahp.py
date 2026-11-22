"""K2 · AHP (Analitik Hiyerarşi Süreci), sıfırdan.

İkili karşılaştırma matrisi A: a_ij = "i kriteri j'ye göre ne kadar önemli" (Saaty 1–9 ölçeği),
a_ji = 1/a_ij, köşegen 1. Ağırlık = A'nın en büyük özdeğerine ait (Perron) özvektör, toplamı 1.
Tutarlılık: CI = (λmax − n)/(n − 1), CR = CI/RI(n); CR < 0,10 kabul edilir.
Grup kararı: yargıçların matrisleri eleman bazında GEOMETRİK ortalamayla birleştirilir
(geometrik ortalama karşılıklılığı korur: 1/a'ların geometrik ortalaması = 1/(a'ların g.o.)).
"""
from __future__ import annotations

import numpy as np

# Saaty rastgele indeks (RI) değerleri; doğrulama: docs/05 (web, 2026-11-22).
RI = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}


def matris_dogrula(A, tol: float = 1e-9) -> np.ndarray:
    """Kare, pozitif, köşegeni 1, karşılıklı (a_ji = 1/a_ij) olmalı."""
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("matris kare olmalı")
    if (A <= 0).any():
        raise ValueError("tüm elemanlar pozitif olmalı")
    if not np.allclose(np.diag(A), 1.0, atol=tol):
        raise ValueError("köşegen 1 olmalı")
    if not np.allclose(A * A.T, 1.0, atol=1e-6):
        raise ValueError("matris karşılıklı değil (a_ji = 1/a_ij)")
    return A


def ust_ucgenden_matris(yargilar: list[float], n: int) -> np.ndarray:
    """Üst üçgen yargılardan (satır sırasıyla: a12, a13, ..., a1n, a23, ...) tam matris kurar."""
    if len(yargilar) != n * (n - 1) // 2:
        raise ValueError(f"{n} kriter için {n*(n-1)//2} yargı gerekir")
    A = np.ones((n, n))
    k = 0
    for i in range(n):
        for j in range(i + 1, n):
            A[i, j] = float(yargilar[k])
            A[j, i] = 1.0 / float(yargilar[k])
            k += 1
    return A


def agirliklar(A, max_iter: int = 1000, tol: float = 1e-12) -> tuple[np.ndarray, float]:
    """Kuvvet yinelemesiyle (power iteration) baskın özvektör ve λmax.

    Pozitif matriste (Perron–Frobenius) baskın özvektör tektir ve pozitiftir;
    w ← A·w, normalize et, yakınsayana dek tekrarla. λmax = ortalama((A·w)_i / w_i).
    """
    A = matris_dogrula(A)
    n = A.shape[0]
    w = np.full(n, 1.0 / n)
    for _ in range(max_iter):
        w_yeni = A @ w
        w_yeni /= w_yeni.sum()
        if np.abs(w_yeni - w).max() < tol:
            w = w_yeni
            break
        w = w_yeni
    lam_max = float(np.mean((A @ w) / w))
    return w, lam_max


def tutarlilik(A) -> dict:
    """CI, RI, CR döndürür. n ≤ 2 için CR = 0 (her 2×2 karşılıklı matris tutarlıdır)."""
    A = matris_dogrula(A)
    n = A.shape[0]
    w, lam = agirliklar(A)
    ci = (lam - n) / (n - 1) if n > 1 else 0.0
    ri = RI[n]
    cr = ci / ri if ri > 0 else 0.0
    return {"agirliklar": w, "lambda_max": lam, "CI": ci, "RI": ri, "CR": cr, "kabul": cr < 0.10}


def grup_birlestir(matrisler) -> np.ndarray:
    """Yargıç matrislerini eleman bazında geometrik ortalamayla birleştirir (AIJ)."""
    M = np.stack([matris_dogrula(A) for A in matrisler])
    return np.exp(np.log(M).mean(axis=0))


def en_tutarsiz_ciftler(A, k: int = 3) -> list[tuple[int, int, float, float]]:
    """Tutarsızlığa en çok katkı veren k çifti döndürür: (i, j, verilen a_ij, tutarlı olsaydı w_i/w_j).

    Sapma ölçüsü |log(a_ij · w_j / w_i)|; tam tutarlı matriste 0. Yargıca "bu çifti yeniden
    düşünür müsünüz?" diye sormak için kullanılır (indeksler 0 tabanlı).
    Not: n=3'te tek bir döngü olduğundan sapma üç çifte EŞİT dağılır; yer tespiti için n≥4 gerekir
    (projede n=6). Bu durumda sıralama bilgi taşımaz, yargıca tüm matris yeniden sorulur.
    """
    A = matris_dogrula(A)
    w, _ = agirliklar(A)
    n = A.shape[0]
    ciftler = [(i, j, float(A[i, j]), float(w[i] / w[j]), abs(np.log(A[i, j] * w[j] / w[i])))
               for i in range(n) for j in range(i + 1, n)]
    ciftler.sort(key=lambda c: c[4], reverse=True)
    return [c[:4] for c in ciftler[:k]]
