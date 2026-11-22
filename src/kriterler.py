"""K1 · Karar kriterleri matrisi (D34).

Sıra: K1 PD (maliyet), K2 kredi/gelir (maliyet), K3 taksit/gelir (maliyet), K4 gelir (fayda),
K5 istihdam yılı (fayda), K6 geçmiş gecikme sayısı (maliyet).
Öğrenilen tek parametre eksik-değer medyanlarıdır; fit YALNIZ eğitimde (sızıntısız).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.topsis import FAYDA, MALIYET

KRITERLER = ["K1_PD", "K2_KREDI_GELIR", "K3_TAKSIT_GELIR", "K4_GELIR", "K5_ISTIHDAM_YIL", "K6_GECIKME"]
YONLER = np.array([MALIYET, MALIYET, MALIYET, FAYDA, FAYDA, MALIYET])
_KAYNAK = {"K2_KREDI_GELIR": "KREDI_GELIR", "K3_TAKSIT_GELIR": "TAKSIT_GELIR",
           "K4_GELIR": "AMT_INCOME_TOTAL", "K5_ISTIHDAM_YIL": "ISTIHDAM_YIL",
           "K6_GECIKME": "BURO_GECIKMELI_SAYISI"}


class KriterHazirlayici:
    """df: temizlenmiş + oranları eklenmiş + büro birleşik çerçeve; pd_: aynı sıradaki PD değerleri."""

    def _ham(self, df, pd_):
        M = pd.DataFrame({k: df[s].to_numpy(dtype=float) for k, s in _KAYNAK.items()})
        M.insert(0, "K1_PD", np.asarray(pd_, dtype=float))
        return M[KRITERLER]

    def fit(self, df, pd_):
        M = self._ham(df, pd_)
        self.medyan_ = M.median()                 # K5: emekli (anomali) grubu için eğitim medyanı
        return self

    def transform(self, df, pd_) -> np.ndarray:
        M = self._ham(df, pd_)
        M["K6_GECIKME"] = M["K6_GECIKME"].fillna(0.0)   # büro kaydı yok → gecikme kanıtı yok (D34)
        M = M.fillna(self.medyan_)
        return M.to_numpy()
