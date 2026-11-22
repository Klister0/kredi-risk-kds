"""F4 · Sızıntısız ön işleme boru hattı (sklearn Pipeline).

Tasarım: durumsuz özellik türetme (F1+F2) önce; sonra imputer/encoder/scaler.
KİLİT NOKTA: imputer medyanı, scaler ortalama/std'si, encoder kategorileri YALNIZ
`fit` sırasında (yani yalnız eğitim katında) öğrenilir. Böylece CV ve test'te sızıntı olmaz.

Büro özellikleri (F3) sızıntısızdır (TARGET kullanmaz, durumsuz toplulaştırma), bu yüzden
bölmeden önce birleştirilebilir; bu boru hattı başvuru + büro sütunlu X üzerinde çalışır.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.oran_ozellikleri import oran_ozellikleri_ekle
from src.veri_hazirlama import temizle_basvuru

BIRAKILACAK = ["SK_ID_CURR", "TARGET"]


class OzellikTuretici(BaseEstimator, TransformerMixin):
    """Durumsuz özellik türetme (F1 temizleme + F2 oranlar). fit hiçbir şey öğrenmez."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = temizle_basvuru(X)
        X = oran_ozellikleri_ekle(X)
        return X.drop(columns=[c for c in BIRAKILACAK if c in X.columns])


def on_isleme_boru_hatti(olcekle: bool = True) -> Pipeline:
    """Ön işleme Pipeline'ı döndürür. Sütun tipleri fit anında dtype ile seçilir.

    olcekle=True (LR için): sayısalları StandardScaler ile ölçekler.
    olcekle=False (ağaçlar için): ölçekleme yok (ağaçlar tekdüze dönüşüme duyarsız).
    """
    sayisal_adimlar = [("imputer", SimpleImputer(strategy="median"))]
    if olcekle:
        sayisal_adimlar.append(("olcek", StandardScaler()))
    sayisal = Pipeline(sayisal_adimlar)

    kategorik = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    sutunlar = ColumnTransformer([
        ("sayisal", sayisal, make_column_selector(dtype_include=np.number)),
        ("kategorik", kategorik, make_column_selector(dtype_exclude=np.number)),
    ], remainder="drop")

    return Pipeline([
        ("ozellik", OzellikTuretici()),
        ("sutunlar", sutunlar),
    ])
