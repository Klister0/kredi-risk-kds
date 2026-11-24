"""Tek başvuru değerlendirme testleri (sentetik model ve kriter matrisi)."""
import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

xgb = pytest.importorskip("xgboost")
pytest.importorskip("shap")

from src.boru_hatti import on_isleme_boru_hatti
from src.karar import degerlendir, katman_kur, kriter_konumlari, shap_katkilari
from src.kriterler import KriterHazirlayici
from src.oran_ozellikleri import oran_ozellikleri_ekle
from src.veri_hazirlama import temizle_basvuru


def _kurulum(n=800):
    rng = np.random.default_rng(0)
    X = pd.DataFrame({
        "SK_ID_CURR": np.arange(n), "AMT_INCOME_TOTAL": rng.uniform(5e4, 3e5, n),
        "AMT_CREDIT": rng.uniform(1e5, 1e6, n), "AMT_ANNUITY": rng.uniform(5e3, 5e4, n),
        "AMT_GOODS_PRICE": rng.uniform(1e5, 1e6, n), "CNT_FAM_MEMBERS": rng.integers(1, 5, n).astype(float),
        "DAYS_BIRTH": -rng.uniform(7000, 25000, n), "DAYS_EMPLOYED": -rng.uniform(100, 10000, n),
        "BURO_GECIKMELI_SAYISI": rng.integers(0, 3, n).astype(float),
    })
    y = (rng.uniform(size=n) < 0.08 + 0.2 * (X["AMT_CREDIT"] > 7e5)).astype(int)
    boru = Pipeline([("on", on_isleme_boru_hatti(olcekle=False)),
                     ("model", xgb.XGBClassifier(n_estimators=30, max_depth=3, random_state=0))]).fit(X, y)
    pd_ = boru.predict_proba(X)[:, 1]
    df = oran_ozellikleri_ekle(temizle_basvuru(X))
    kh = KriterHazirlayici().fit(df, pd_)
    return boru, kh, kh.transform(df, pd_), X


def test_degerlendir_ciktilari_tutarli():
    boru, kh, M, X = _kurulum()
    katman = katman_kur(M, np.ones(6) / 6)
    r = degerlendir(X.iloc[[5]], boru, kh, katman)
    assert 0 <= r["PD"] <= 1 and 0 <= r["C*"] <= 1
    assert r["karar"] in ("Reddet", "Şartlı Onayla", "Onayla")
    assert len(r["kriterler"]) == 6 and np.isclose(r["kriterler"]["Ağırlık"].sum(), 1)
    assert ((r["kriterler"]["İdeale yakınlık (0–1)"] >= 0) & (r["kriterler"]["İdeale yakınlık (0–1)"] <= 1)).all()


def test_bant_oranlari_egitimde_tutar():
    _, _, M, _ = _kurulum()
    k = katman_kur(M, np.ones(6) / 6, red=0.2, sartli=0.1)
    assert abs((k["c_egitim"] < k["esik"][0]).mean() - 0.2) < 0.01


def test_konum_yonu():
    _, _, M, _ = _kurulum()
    t = katman_kur(M, np.ones(6) / 6)["topsis"]
    en_iyi = np.where(t.yon_ == 1, t.ust_, t.alt_)       # fayda: üst, maliyet: alt
    assert np.allclose(kriter_konumlari(en_iyi, t), 1)


def test_shap_katkilari_toplami():
    boru, _, _, X = _kurulum()
    s = shap_katkilari(X.iloc[[3]], boru, k=3)
    assert len(s) == 4 and "Diğer değişkenler" in s.index
