"""TOPSIS testleri: bilinen davranışlar + pymcdm ile çapraz doğrulama."""
import numpy as np
import pytest

from src.topsis import FAYDA, MALIYET, SabitTopsis, batch_topsis

YON = np.array([MALIYET, MALIYET, FAYDA])


def _rastgele(n=200, tohum=0):
    rng = np.random.default_rng(tohum)
    return rng.uniform(1, 10, size=(n, 3))


def test_baskin_alternatif_bir_ve_sifir():
    # 1. satır her kriterde en iyi (maliyetler düşük, fayda yüksek), 2. satır her kriterde en kötü
    X = np.array([[1.0, 1.0, 9.0], [9.0, 9.0, 1.0], [5.0, 5.0, 5.0]])
    C = batch_topsis(X, [1, 1, 1], YON)
    assert np.isclose(C[0], 1.0) and np.isclose(C[1], 0.0)
    assert 0 < C[2] < 1


def test_pymcdm_ile_ayni():
    pytest.importorskip("pymcdm")
    from pymcdm import normalizations
    from pymcdm.methods import TOPSIS
    X = _rastgele()
    w = np.array([0.5, 0.3, 0.2])
    bizim = batch_topsis(X, w, YON)
    onlarin = TOPSIS(normalization_function=normalizations.vector_normalization)(X, w, YON)
    # pymcdm maliyet kriterlerini normalizasyonda tersine çevirebilir; sıralama ve değer uyumu kontrolü
    assert np.corrcoef(bizim, onlarin)[0, 1] > 0.999
    assert (np.argsort(bizim) == np.argsort(onlarin)).mean() > 0.99


def test_sabit_egitimde_batch_ile_ayni():
    X = _rastgele(500)
    w = [0.5, 0.3, 0.2]
    st = SabitTopsis(w, YON).fit(X)
    Xk = np.clip(X, st.alt_, st.ust_)
    assert np.allclose(st.transform(X), batch_topsis(Xk, w, YON))


def test_sabit_referans_rank_reversal_yok():
    # Sabit referansta bir başvurunun puanı, yanında kimin değerlendirildiğinden bağımsızdır
    X = _rastgele(500)
    st = SabitTopsis([0.5, 0.3, 0.2], YON).fit(X)
    yeni = _rastgele(50, tohum=1)
    tek_tek = np.array([st.transform(satir)[0] for satir in yeni])
    toplu = st.transform(yeni)
    assert np.allclose(tek_tek, toplu)


def test_batch_rank_reversal_olabilir():
    # Klasik TOPSIS'te aynı alternatifin puanı küme değişince değişir (D21 gerekçesi)
    X = _rastgele(30)
    w = [0.5, 0.3, 0.2]
    once = batch_topsis(X, w, YON)[:5]
    asiri = np.array([[0.1, 0.1, 100.0]])            # yeni, aşırı iyi bir alternatif eklenir
    sonra = batch_topsis(np.vstack([X, asiri]), w, YON)[:5]
    assert not np.allclose(once, sonra)


def test_tek_basvuru_ve_nan():
    st = SabitTopsis([1, 1, 1], YON).fit(_rastgele())
    assert st.transform([5.0, 5.0, 5.0]).shape == (1,)
    with pytest.raises(ValueError):
        st.transform([np.nan, 5.0, 5.0])


def test_yanlis_parametre():
    with pytest.raises(ValueError):
        batch_topsis(_rastgele(), [1, 1], YON)
    with pytest.raises(ValueError):
        batch_topsis(_rastgele(), [1, 1, 1], [1, 0, 1])
