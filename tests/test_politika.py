import numpy as np

from src.politika import (BIRINCIL, egri, ihlal_orani, karsilastir, kotu_orani, onayla, swap_set,
                          wpd_agirliklari)


def test_onay_orani_ve_secim():
    skor = np.array([0.1, 0.9, 0.5, 0.7, 0.3])
    o = onayla(skor, 0.4)                        # ⌈0,4·5⌉ = 2 → en yüksek iki skor
    assert o.sum() == 2 and o[1] and o[3]


def test_kotu_orani_ve_ihlal():
    y = np.array([1, 0, 0, 1])
    o = np.array([True, True, False, False])
    assert kotu_orani(y, o) == 0.5
    assert ihlal_orani(o, [5, 1, 9, 9], [0.1, 0.1, 0.1, 0.1], 4, 0.5) == 0.5


def test_ayni_skor_delta_sifir():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 2000)
    s = rng.uniform(size=y.size)
    kg = rng.uniform(0, 10, y.size); tg = rng.uniform(0, 1, y.size)
    r = karsilastir(y, s, s, kg, tg, 9, 0.9, B=50)
    assert r["delta"]["deger"] == 0 and r["delta"]["ga_alt"] == 0 and r["delta"]["ga_ust"] == 0


def test_bilgili_skor_rastgeleden_iyi_delta_pozitif():
    rng = np.random.default_rng(1)
    n = 5000
    y = (rng.uniform(size=n) < 0.1).astype(int)
    s_pd = -(y + rng.normal(0, 0.7, n))          # bilgili: kötüler düşük skor
    s_rast = rng.uniform(size=n)                  # bilgisiz politika
    kg = rng.uniform(0, 10, n); tg = rng.uniform(0, 1, n)
    r = karsilastir(y, s_pd, s_rast, kg, tg, 9, 0.9, B=100)
    assert r["delta"]["ga_alt"] > 0               # rastgele politikanın kötü oranı daha yüksek


def test_ihlal_azaltan_politika():
    rng = np.random.default_rng(2)
    n = 4000
    y = rng.integers(0, 2, n)
    kg = rng.uniform(0, 10, n); tg = rng.uniform(0, 1, n)
    s_pd = rng.uniform(size=n)
    s_pol = -kg                                    # yüksek kredi/geliri cezalandıran politika
    r = karsilastir(y, s_pd, s_pol, kg, tg, 9, 2.0, B=100)
    assert r["delta_ihlal"]["ga_ust"] < 0          # politika ihlali azalır


def test_egri_ve_swap_ve_wpd():
    rng = np.random.default_rng(3)
    y = rng.integers(0, 2, 1000); a = rng.uniform(size=1000); b = rng.uniform(size=1000)
    e = egri(y, a, a, a, 2, 2)
    assert len(e["oran"]) == 9
    s = swap_set(y, a, b, 0.7)
    assert s["n_yalniz_pd_onaylar"] == s["n_yalniz_mcdm_onaylar"]   # eşit onay oranı → eşit takas
    w = wpd_agirliklari([0.4, 0.2, 0.1, 0.1, 0.1, 0.1], 0.7)
    assert np.isclose(w.sum(), 1) and np.isclose(w[0], 0.7) and np.isclose(w[1] / w[2], 2)
    assert list(BIRINCIL) == [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]


def test_bantlar_egitim_niceliklerinden():
    from src.politika import bant_esikleri, bant_tablosu, bantla
    egitim = np.arange(1000) / 1000                  # 0,000 … 0,999
    e = bant_esikleri(egitim)
    assert np.isclose(e[0], 0.15, atol=1e-3) and np.isclose(e[1], 0.30, atol=1e-3)
    b = bantla(egitim, e)
    t = bant_tablosu(np.zeros(1000, int), b)
    assert abs(t["Reddet"]["pay"] - 0.15) < 0.002 and abs(t["Onayla"]["pay"] - 0.70) < 0.002
    assert bantla([0.05, 0.2, 0.9], e).tolist() == ["Reddet", "Şartlı Onayla", "Onayla"]
