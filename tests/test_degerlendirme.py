import numpy as np
from sklearn.metrics import roc_auc_score

from src.degerlendirme import bootstrap, ks_istatistigi


def test_ks_mukemmel_ve_rastgele():
    y = np.array([0] * 500 + [1] * 500)
    assert np.isclose(ks_istatistigi(y, np.r_[np.zeros(500), np.ones(500)]), 1.0)
    rng = np.random.default_rng(0)
    yr = rng.integers(0, 2, 20000)
    assert ks_istatistigi(yr, rng.uniform(size=yr.size)) < 0.03


def test_bootstrap_ga_nokta_tahminini_kapsar_ve_tekrarlanabilir():
    rng = np.random.default_rng(1)
    y = rng.integers(0, 2, 3000)
    iyi = y + rng.normal(0, 1.0, y.size)
    kotu = y + rng.normal(0, 3.0, y.size)
    olc = {"roc_auc": lambda a, b: roc_auc_score(a, b)}
    s1 = bootstrap(y, {"iyi": iyi, "kotu": kotu}, olcutler=olc, B=200, referans="iyi")
    s2 = bootstrap(y, {"iyi": iyi, "kotu": kotu}, olcutler=olc, B=200, referans="iyi")
    r = s1["iyi"]["roc_auc"]
    assert r["ga_alt"] <= r["deger"] <= r["ga_ust"]
    assert s1 == s2                                       # aynı tohum → aynı GA
    fark = s1["farklar"]["iyi-kotu"]["roc_auc"]
    assert fark["ga_alt"] > 0                             # belirgin fark: GA 0'ı içermez
