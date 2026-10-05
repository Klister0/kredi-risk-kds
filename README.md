# Kredi Risk Karar Destek Sistemi

Makine Öğrenmesi ve Çok Kriterli Karar Analizi ile Kredi Risk Değerlendirme ve Onay Karar Destek Sistemi.
Karar Destek Sistemleri dersi dönem projesi.

> Akademik bir prototiptir; gerçek kredi kararlarında kullanılmak üzere tasarlanmamıştır.

## Yaklaşım

1. **Veri hazırlama:** Kaggle Home Credit Default Risk veri seti (~307 bin başvuru + 6 ek tablo)
2. **Risk modelleme:** Logistic Regression, Random Forest, XGBoost (ROC-AUC, F1, PR-AUC)
3. **Karar katmanı:** AHP ile kriter ağırlıkları + TOPSIS ile Onayla / Şartlı Onayla / Reddet
4. **Sunum:** Streamlit dashboard, ayarlanabilir ağırlıklar ve SHAP ile açıklama

## Klasör yapısı

```
data/raw/          Kaggle CSV'leri (Git'e girmez)
data/processed/    kodun ürettiği veri (Git'e girmez)
notebooks/         keşif defterleri
src/               yeniden kullanılan kod
tests/             testler
rapor/sekiller/    rapor grafikleri
```

## Veri

Veri lisans ve boyut nedeniyle depoda yer almaz.
[Kaggle Home Credit Default Risk](https://www.kaggle.com/competitions/home-credit-default-risk/data)
sayfasından indirilip `data/raw/` içine açılmalıdır.

Geliştirme süreci ve alınan kararlar için: [GELISTIRME_GUNLUGU.md](GELISTIRME_GUNLUGU.md)
