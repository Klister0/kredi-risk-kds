import numpy as np
import pandas as pd

from src.kriterler import KRITERLER, KriterHazirlayici


def _df(istihdam, gecikme):
    n = len(istihdam)
    return pd.DataFrame({"KREDI_GELIR": [2.0] * n, "TAKSIT_GELIR": [0.1] * n,
                         "AMT_INCOME_TOTAL": [1e5] * n, "ISTIHDAM_YIL": istihdam,
                         "BURO_GECIKMELI_SAYISI": gecikme})


def test_kurallar_ve_egitim_medyani():
    egitim = _df([1.0, 3.0, 5.0, np.nan], [0, 1, 2, np.nan])
    kh = KriterHazirlayici().fit(egitim, [0.1, 0.2, 0.3, 0.4])
    test = _df([np.nan, 10.0], [np.nan, 4])
    M = kh.transform(test, [0.5, 0.6])
    assert M.shape == (2, len(KRITERLER))
    assert M[0, 4] == 3.0          # K5 NaN → EĞİTİM medyanı (1,3,5 → 3), test değil
    assert M[0, 5] == 0.0          # K6 NaN (kayıt yok) → 0
    assert not np.isnan(M).any()
