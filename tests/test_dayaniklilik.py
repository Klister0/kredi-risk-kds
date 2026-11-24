import numpy as np

from src.dayaniklilik import critic_agirlik, dirichlet_kararlilik, entropi_agirlik
from src.topsis import FAYDA, MALIYET

YON = np.array([MALIYET, FAYDA, FAYDA])


def _M(n=3000, tohum=0):
    rng = np.random.default_rng(tohum)
    return np.column_stack([rng.uniform(0, 1, n), rng.lognormal(0, 1, n), rng.uniform(0, 10, n)])


def test_buyuk_alfa_neredeyse_tam_kararli():
    M = _M()
    r = dirichlet_kararlilik(M, M[:500], [0.5, 0.3, 0.2], YON, alfa=1e6, N=30)
    assert np.mean(r["S"] == 1.0) > 0.99


def test_kucuk_alfa_daha_kararsiz():
    M = _M()
    genis = dirichlet_kararlilik(M, M[:800], [0.5, 0.3, 0.2], YON, alfa=5, N=100)["S"].mean()
    dar = dirichlet_kararlilik(M, M[:800], [0.5, 0.3, 0.2], YON, alfa=500, N=100)["S"].mean()
    assert genis < dar
    r = dirichlet_kararlilik(M, M[:10], [0.5, 0.3, 0.2], YON, alfa=5, N=50)
    assert np.allclose(r["olasilik"].sum(axis=1), 1.0)


def test_entropi_ve_critic():
    rng = np.random.default_rng(1)
    # 2. kriter tamamen sabit: hiçbir başvuruyu ayırt etmez → iki veri temelli yöntemde de ağırlığı 0 olmalı
    M = np.column_stack([rng.uniform(0, 1, 2000), np.full(2000, 3.0), rng.lognormal(0, 1, 2000)])
    for f in (entropi_agirlik, critic_agirlik):
        w = f(M, YON)
        assert np.isclose(w.sum(), 1) and (w >= 0).all()
        assert w[1] < 1e-9
