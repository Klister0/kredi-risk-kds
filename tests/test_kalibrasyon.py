"""Kalibrasyon ölçütleri testleri (bilinen sonuçlarla)."""
import numpy as np

from src.kalibrasyon import cv_isotonic, ece, prior_duzeltme


def test_ece_mukemmel_kalibrasyon_sifira_yakin():
    rng = np.random.default_rng(0)
    p = rng.uniform(0, 1, 200_000)
    y = (rng.uniform(0, 1, p.size) < p).astype(int)   # y ~ Bernoulli(p): tanım gereği kalibre
    assert ece(y, p) < 0.01


def test_ece_kaymis_olasilik_buyuk():
    rng = np.random.default_rng(1)
    p_gercek = rng.uniform(0, 0.2, 100_000)
    y = (rng.uniform(0, 1, p_gercek.size) < p_gercek).astype(int)
    p_sisik = np.clip(p_gercek * 3, 0, 1)              # olasılıklar 3 kat şişirilmiş
    assert ece(y, p_sisik) > 0.1


def test_prior_duzeltme_bilinen_deger():
    # w=1 → değişmez; w=3, p=0.5 → 0.5/(0.5+1.5)=0.25
    assert np.allclose(prior_duzeltme([0.2, 0.7], 1.0), [0.2, 0.7])
    assert np.isclose(prior_duzeltme([0.5], 3.0)[0], 0.25)


def test_prior_duzeltme_agirlikli_ornegi_geri_alir():
    # Gerçek oran q iken w ağırlıkla görülen oran: wq/(wq+1-q); düzeltme q'yu geri vermeli
    q, w = 0.08, 11.4
    gorulen = w * q / (w * q + 1 - q)
    assert np.isclose(prior_duzeltme([gorulen], w)[0], q)


def test_cv_isotonic_aralik_ve_uzunluk():
    rng = np.random.default_rng(2)
    s = rng.uniform(0, 1, 5000)
    y = (rng.uniform(0, 1, s.size) < s ** 2).astype(int)
    k = cv_isotonic(s, y)
    assert k.shape == s.shape
    assert (k >= 0).all() and (k <= 1).all()
    assert ece(y, k) < ece(y, s)                        # kalibrasyon hatayı azaltmalı
