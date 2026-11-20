"""katmanli_bol için testler.

Sentetik veriyle değişmezleri (ayrıklık, bütünlük, oran, belirlenircilik) ve
sklearn ile sınıf bazında uyumu doğrular. 'Çalıştı' kanıt değildir; aşağıdaki
assert'ler kanıttır.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.bolme import katmanli_bol


def _sentetik(n=1000, pozitif_orani=0.08, tohum=0):
    rng = np.random.default_rng(tohum)
    kimlikler = np.arange(100000, 100000 + n)          # SK_ID_CURR gibi tekil
    hedef = (rng.random(n) < pozitif_orani).astype(int)
    return pd.Series(kimlikler), pd.Series(hedef)


def test_ayrik_ve_butun():
    # egitim ve test kesişmez, birleşimleri tüm kimlikler
    kimlikler, hedef = _sentetik()
    egitim, test = katmanli_bol(kimlikler, hedef)
    assert set(egitim).isdisjoint(set(test))
    assert set(egitim) | set(test) == set(kimlikler)
    assert len(egitim) + len(test) == len(kimlikler)


def test_test_orani():
    kimlikler, hedef = _sentetik(n=1000)
    _, test = katmanli_bol(kimlikler, hedef, test_orani=0.2)
    assert len(test) == 200  # round(800*0.2)+round(... ) sınıf bazında toplanır


def test_katmanlama_orani_korur():
    # test kümesindeki pozitif oranı, toplam pozitif oranına çok yakın olmalı
    kimlikler, hedef = _sentetik(n=10000, pozitif_orani=0.08)
    egitim, test = katmanli_bol(kimlikler, hedef, test_orani=0.2)
    h = np.asarray(hedef)
    k = np.asarray(kimlikler)
    toplam_oran = h.mean()
    test_oran = h[np.isin(k, test)].mean()
    assert abs(test_oran - toplam_oran) < 0.005


def test_belirlenircilik():
    # aynı tohum -> aynı bölme; farklı tohum -> farklı bölme
    kimlikler, hedef = _sentetik()
    e1, t1 = katmanli_bol(kimlikler, hedef, tohum=42)
    e2, t2 = katmanli_bol(kimlikler, hedef, tohum=42)
    e3, t3 = katmanli_bol(kimlikler, hedef, tohum=7)
    assert np.array_equal(t1, t2)
    assert not np.array_equal(t1, t3)


def test_ciktilar_sirali():
    kimlikler, hedef = _sentetik()
    egitim, test = katmanli_bol(kimlikler, hedef)
    assert np.all(egitim[:-1] <= egitim[1:])
    assert np.all(test[:-1] <= test[1:])


def test_sklearn_ile_sinif_bazinda_uyum():
    # Elemanlar aynı olmaz (farklı algoritma), ama sınıf başına test sayıları aynı olmalı
    kimlikler, hedef = _sentetik(n=10000, pozitif_orani=0.08)
    _, test = katmanli_bol(kimlikler, hedef, test_orani=0.2, tohum=42)
    _, sk_test_idx = train_test_split(
        np.arange(len(hedef)), test_size=0.2, stratify=hedef, random_state=42
    )
    h = np.asarray(hedef)
    k = np.asarray(kimlikler)
    bizim_pozitif = int(h[np.isin(k, test)].sum())
    sk_pozitif = int(h[sk_test_idx].sum())
    assert bizim_pozitif == sk_pozitif
    assert len(test) == len(sk_test_idx)


def test_tekil_olmayan_kimlik_hata():
    import pytest
    kimlikler = pd.Series([1, 2, 2, 3])
    hedef = pd.Series([0, 1, 0, 1])
    with pytest.raises(ValueError):
        katmanli_bol(kimlikler, hedef)
