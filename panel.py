"""Kredi Onay Karar Destek Sistemi — Streamlit paneli (AKADEMİK PROTOTİP).

Çalıştırma (proje kökünden):
    .\\.venv\\Scripts\\python.exe -m streamlit run panel.py
Önkoşul: data/processed/model/final_model.joblib ve data/processed/karar_katmani.joblib
         (deneyler/final_model.py ve deneyler/karar_katmani_hazirla.py ile üretilir).
"""
from __future__ import annotations

from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import shap
import streamlit as st

from src.karar import KRITER_ADLARI, degerlendir, katman_kur, shap_katkilari
from src.kriterler import KRITERLER

KOK = Path(__file__).resolve().parent
RENK = {"Onayla": "#2E7D32", "Şartlı Onayla": "#EF8F00", "Reddet": "#C62828"}

st.set_page_config(page_title="Kredi Onay KDS", layout="wide")


@st.cache_resource
def yukle():
    model = joblib.load(KOK / "data/processed/model/final_model.joblib")
    katman = joblib.load(KOK / "data/processed/karar_katmani.joblib")
    aciklayici = shap.TreeExplainer(model["boru"].named_steps["model"])
    return model, katman, aciklayici


@st.cache_resource
def katman_onbellek(w_tuple, red, sartli):
    _, paket, _ = yukle()
    return katman_kur(paket["M_egitim"], np.array(w_tuple), red, sartli)


model, paket, aciklayici = yukle()
boru, kalibrator, kh = model["boru"], model.get("kalibrator"), paket["kh"]

# --- Kenar çubuğu: ağırlıklar ve bant oranları ---
st.sidebar.header("Kriter ağırlıkları")
w_vars = paket["w_ahp"] if paket["w_ahp"] is not None else np.ones(6) / 6
st.sidebar.caption("Varsayılan: AHP (uzman yargısı)" if paket["w_ahp"] is not None
                   else "Varsayılan: eşit ağırlık (AHP yargıları henüz yok)")
ham = np.array([st.sidebar.slider(KRITER_ADLARI[k], 0.0, 1.0, float(round(w_vars[i], 3)), 0.01, key=k)
                for i, k in enumerate(KRITERLER)])
if ham.sum() == 0:
    st.sidebar.error("En az bir ağırlık sıfırdan büyük olmalı."); st.stop()
w = ham / ham.sum()
st.sidebar.caption("Normalize: " + ", ".join(f"{k.split('_')[0]} {v:.2f}" for k, v in zip(KRITERLER, w)))
st.sidebar.header("Portföy politikası")
red = st.sidebar.slider("Reddet bandı (eğitimdeki en kötü %)", 5, 40, 15) / 100
sartli = st.sidebar.slider("Şartlı Onayla bandı (%)", 0, 40, 15) / 100
katman = katman_onbellek(tuple(np.round(w, 6)), red, sartli)

# --- Ana alan ---
st.title("Kredi Onay Karar Destek Sistemi")
st.caption("Akademik prototiptir; gerçek kredi kararı için kullanılamaz. Model: XGBoost (cinsiyet kullanılmaz), "
           "karar katmanı: AHP ağırlıklı, eğitimden sabit referanslı TOPSIS.")

havuz = paket["havuz"]
kimlik = st.selectbox("Başvuru (eğitim örnek havuzundan)", havuz["SK_ID_CURR"].tolist())
satir = havuz[havuz["SK_ID_CURR"] == kimlik].copy()

with st.expander("Başvuru bilgilerini düzenle (ne-olursa senaryosu)"):
    c1, c2, c3 = st.columns(3)
    satir["AMT_INCOME_TOTAL"] = c1.number_input("Gelir", 0.0, value=float(satir["AMT_INCOME_TOTAL"].iloc[0]), step=1000.0)
    satir["AMT_CREDIT"] = c2.number_input("Kredi tutarı", 0.0, value=float(satir["AMT_CREDIT"].iloc[0]), step=1000.0)
    taksit0 = satir["AMT_ANNUITY"].iloc[0]
    satir["AMT_ANNUITY"] = c3.number_input("Taksit", 0.0, value=float(0 if np.isnan(taksit0) else taksit0), step=100.0)
    emekli0 = satir["DAYS_EMPLOYED"].iloc[0] == 365243
    emekli = c1.checkbox("Emekli / çalışmıyor", value=bool(emekli0))
    yil0 = 0.0 if emekli0 else -satir["DAYS_EMPLOYED"].iloc[0] / 365.25
    yil = c2.number_input("İstihdam süresi (yıl)", 0.0, 60.0, float(round(yil0, 1)), 0.5, disabled=emekli)
    satir["DAYS_EMPLOYED"] = 365243 if emekli else -yil * 365.25

if satir["AMT_INCOME_TOTAL"].iloc[0] <= 0:
    st.error("Gelir sıfırdan büyük olmalı."); st.stop()

r = degerlendir(satir, boru, kh, katman, kalibrator)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Temerrüt olasılığı (PD)", f"{r['PD']:.1%}")
m2.metric("TOPSIS yakınlık C*", f"{r['C*']:.3f}", help=f"Eğitimdeki başvuruların %{r['c_yuzdelik']*100:.0f}'inden yüksek")
m3.markdown(f"**AHP-TOPSIS kararı**<br><span style='font-size:1.6em;color:{RENK[r['karar']]}'>{r['karar']}</span>",
            unsafe_allow_html=True)
m4.markdown(f"**Yalnız PD'ye göre**<br><span style='font-size:1.6em;color:{RENK[r['karar_pd_tek']]}'>{r['karar_pd_tek']}</span>",
            unsafe_allow_html=True)
if r["karar"] != r["karar_pd_tek"]:
    st.info("İki politika bu başvuruda farklı karar veriyor: AHP-TOPSIS, PD'nin yanında politika kriterlerini de tartıyor.")

sol, sag = st.columns(2)
with sol:
    st.subheader("Kriterler (karar katmanı)")
    st.dataframe(r["kriterler"], hide_index=True, width="stretch",
                 column_config={"Değer": st.column_config.NumberColumn(format="%.3f"),
                                "Ağırlık": st.column_config.NumberColumn(format="%.2f"),
                                "İdeale yakınlık (0–1)": st.column_config.ProgressColumn(min_value=0, max_value=1, format="%.2f")})
    st.caption("İdeale yakınlık: 0 = eğitimdeki en kötü uç (p1/p99), 1 = en iyi uç. TOPSIS bu konumları ağırlıklarla birleştirir.")
with sag:
    st.subheader("PD neden bu? (SHAP)")
    katki = shap_katkilari(satir, boru, aciklayici)[::-1]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(katki.index, katki.values, color=["#C44E52" if v > 0 else "#4C72B0" for v in katki.values])
    ax.axvline(0, color="k", lw=0.8); ax.set_xlabel("Katkı (log-odds): kırmızı riski artırır, mavi azaltır")
    fig.tight_layout(); st.pyplot(fig)
    st.caption("SHAP nedensellik değildir; ilişkili değişkenlerde katkı paylaşımı kararsız olabilir.")
