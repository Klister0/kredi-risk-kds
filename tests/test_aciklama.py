"""SHAP açıklama testleri: toplanabilirlik, XGBoost yerleşik SHAP ile uyum, toplama korunumu."""
import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

xgb = pytest.importorskip("xgboost")
pytest.importorskip("shap")

from src.aciklama import degiskene_topla, global_onem, shap_hesapla
from src.boru_hatti import on_isleme_boru_hatti


def _veri(n=600, tohum=0):
    rng = np.random.default_rng(tohum)
    X = pd.DataFrame({
        "SK_ID_CURR": np.arange(n), "AMT_INCOME_TOTAL": rng.uniform(5e4, 3e5, n),
        "AMT_CREDIT": rng.uniform(1e5, 1e6, n), "AMT_ANNUITY": rng.uniform(5e3, 5e4, n),
        "DAYS_BIRTH": -rng.uniform(7000, 25000, n), "DAYS_EMPLOYED": -rng.uniform(100, 10000, n),
        "CODE_GENDER": rng.choice(["M", "F"], n), "NAME_CONTRACT_TYPE": rng.choice(["Cash", "Revolving", "X"], n),
    })
    y = (rng.uniform(size=n) < 0.1 + 0.2 * (X["AMT_CREDIT"] > 6e5)).astype(int)
    boru = Pipeline([("on", on_isleme_boru_hatti(olcekle=False)),
                     ("model", xgb.XGBClassifier(n_estimators=30, max_depth=3, random_state=0))]).fit(X, y)
    return boru, X


def test_toplanabilirlik_ve_xgboost_yerlesik_shap():
    boru, X = _veri()
    S, taban, Z, adlar, kaynak = shap_hesapla(boru, X)
    marj = boru.named_steps["model"].predict(Z, output_margin=True)
    assert np.allclose(taban + S.sum(axis=1), marj, atol=1e-4)          # taban + Σ SHAP = log-odds
    yerlesik = boru.named_steps["model"].get_booster().predict(xgb.DMatrix(Z), pred_contribs=True)
    assert np.allclose(S, yerlesik[:, :-1], atol=1e-4)                     # XGBoost'un kendi TreeSHAP'i ile aynı


def test_degiskene_toplama_korunum():
    boru, X = _veri()
    S, _, _, adlar, kaynak = shap_hesapla(boru, X)
    Sd = degiskene_topla(S, kaynak)
    assert np.allclose(Sd.sum(axis=1), S.sum(axis=1), atol=1e-9)
    assert "CODE_GENDER" in Sd.columns and "CODE_GENDER=M" not in Sd.columns
    onem = global_onem(Sd)
    assert onem.is_monotonic_decreasing
