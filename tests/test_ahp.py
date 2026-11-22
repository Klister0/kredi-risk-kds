"""AHP testleri: bilinen sonuçlar + numpy.linalg ile çapraz doğrulama."""
import numpy as np
import pytest

from src.ahp import agirliklar, grup_birlestir, matris_dogrula, tutarlilik, ust_ucgenden_matris


def _tutarli(w):
    w = np.asarray(w, float)
    return np.outer(w, 1 / w)          # a_ij = w_i / w_j → tam tutarlı matris


def test_tutarli_matris_agirligi_geri_verir():
    w = np.array([0.35, 0.25, 0.15, 0.10, 0.10, 0.05])
    sonuc = tutarlilik(_tutarli(w))
    assert np.allclose(sonuc["agirliklar"], w, atol=1e-9)
    assert abs(sonuc["lambda_max"] - 6) < 1e-9        # tutarlı matriste λmax = n
    assert abs(sonuc["CR"]) < 1e-9


def test_numpy_ozvektoru_ile_ayni():
    # tutarsız ama geçerli bir 4×4 matris: kendi kuvvet yinelememiz vs numpy.linalg.eig
    A = ust_ucgenden_matris([3, 5, 7, 2, 4, 3], 4)
    w, lam = agirliklar(A)
    ozdeg, ozvek = np.linalg.eig(A)
    i = np.argmax(ozdeg.real)
    v = np.abs(ozvek[:, i].real); v /= v.sum()
    assert np.allclose(w, v, atol=1e-8)
    assert abs(lam - ozdeg[i].real) < 1e-8


def test_dongusel_yargi_tutarsiz():
    # A>B (9), B>C (9) ama C>A (9): mantıksal döngü → CR çok büyük
    A = ust_ucgenden_matris([9, 1 / 9, 9], 3)
    assert tutarlilik(A)["CR"] > 0.10
    assert not tutarlilik(A)["kabul"]


def test_karsiliksiz_matris_reddedilir():
    A = np.array([[1, 3], [3, 1]])    # a21 1/3 olmalıydı
    with pytest.raises(ValueError):
        matris_dogrula(A)


def test_ust_ucgen_kurulum():
    A = ust_ucgenden_matris([2, 4, 2], 3)
    assert A[0, 1] == 2 and A[1, 0] == 0.5 and A[0, 2] == 4 and A[2, 1] == 0.5
    with pytest.raises(ValueError):
        ust_ucgenden_matris([2, 4], 3)


def test_grup_birlestirme():
    A1 = ust_ucgenden_matris([2, 4, 2], 3)
    A2 = ust_ucgenden_matris([8, 4, 1 / 2], 3)
    G = grup_birlestir([A1, A2])
    assert abs(G[0, 1] - 4.0) < 1e-12              # sqrt(2·8)
    assert np.allclose(G * G.T, 1.0)               # karşılıklılık korunur
    assert np.allclose(grup_birlestir([A1, A1]), A1)


def test_ri_alti_kriter():
    from src.ahp import RI
    assert RI[6] == 1.24 and RI[3] == 0.58


def test_en_tutarsiz_cift_bulunur():
    # 6 kriterli tutarlı matriste tek bir yargı bozulursa en tutarsız çift o olmalı
    from src.ahp import en_tutarsiz_ciftler
    w = np.array([0.35, 0.25, 0.15, 0.10, 0.10, 0.05])
    A = _tutarli(w)
    A[0, 5], A[5, 0] = 1 / 3.0, 3.0        # tutarlı değer 7 idi; ters yöne çevrildi
    i, j, verilen, tutarli = en_tutarsiz_ciftler(A, k=1)[0]
    assert (i, j) == (0, 5)
    assert np.isclose(verilen, 1 / 3.0)


def test_uc_kriterde_yer_tespiti_mumkun_degil():
    # n=3'te tek döngü vardır: tüm çiftlerin sapması eşittir (yer tespiti imkânsız)
    from src.ahp import en_tutarsiz_ciftler
    A = _tutarli([0.5, 0.3, 0.2])
    A[0, 2], A[2, 0] = 9.0, 1 / 9.0
    sapmalar = [abs(np.log(v / t)) for _, _, v, t in en_tutarsiz_ciftler(A, k=3)]
    assert np.allclose(sapmalar, sapmalar[0])
