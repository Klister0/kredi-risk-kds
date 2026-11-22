# 07 · Veri Notları: Home Credit Default Risk

**Doğrulama durumu (2026-11-20):** §1'deki satır/sütun sayıları V1'de ham veriyle **doğrulandı** (kaynak: `data/README.md`,
SHA-256 parmak izleri orada). §3 tanımları sözlükten okundu. **V2 (2026-11-20, yalnız eğitim kümesi n=246.009):** `TARGET` oranı **%8,07**; `DAYS_EMPLOYED=365243` oranı **%17,9**.

## 1. Tablolar ve ilişkiler

| Tablo | Satır (✅) | Sütun | Anahtar | İçerik |
|---|---:|---:|---|---|
| `application_train` | 307.511 | 122 | `SK_ID_CURR` (tekil) | Başvuru bilgileri + **`TARGET`** |
| `application_test` | 48.744 | 121 | `SK_ID_CURR` | Aynı yapı, **etiketsiz** (kullanılmaz; kendi test kümemizi ayıracağız) |
| `bureau` | 1.716.428 | 17 | `SK_ID_BUREAU`; `SK_ID_CURR`'a bağlı | Diğer kurumlardaki kredi geçmişi |
| `bureau_balance` | 27.299.925 | 3 | `SK_ID_BUREAU` | Büro kredilerinin aylık durumu (`STATUS`) |
| `previous_application` | 1.670.214 | 37 | `SK_ID_PREV`; `SK_ID_CURR` | Home Credit'teki önceki başvurular |
| `POS_CASH_balance` | 10.001.358 | 8 | `SK_ID_PREV` | Önceki POS/nakit kredilerin aylık durumu |
| `credit_card_balance` | 3.840.312 | 23 | `SK_ID_PREV` | Önceki kredi kartı aylık bakiyeleri |
| `installments_payments` | 13.605.401 | 8 | `SK_ID_PREV` | Taksit ödeme geçmişi |

Veri sözlüğü `HomeCredit_columns_description.csv` **latin-1** kodlamalıdır.

İlişki: `application` (1) → (N) `bureau` → (N) `bureau_balance`; `application` (1) → (N) `previous_application` → (N) `POS_CASH_balance`,
`credit_card_balance`, `installments_payments`. **Toplulaştırma, `SK_ID_CURR` düzeyinde yapılır; sonuçta satır sayısı 307.511 kalmalıdır** (birleştirme testi).

**`TARGET` oranı:** eğitimde **%8,07** (19.860 pozitif / 246.009) ✅ V2. Tam veride ≈%8.

## 2. Bilinen anomaliler ve kararlar

| Konu | Gözlem | Karar |
|---|---|---|
| `DAYS_EMPLOYED = 365243` | **%17,9** (44.075/246.009); emekli/çalışmayan. Bu grupta temerrüt **%5,4**, normalde %8,7 → bayrak bilgi taşıyor | NaN + `ISTIHDAM_ANOMALI` bayrağı (D05) |
| `CODE_GENDER = 'XNA'` | Eğitimde **4** satır | NaN yap |
| `ORGANIZATION_TYPE = 'XNA'` | Genelde aynı emekli grubu | Kategori olarak bırak veya "Bilinmiyor" |
| Konut sütunları (`*_AVG`, `*_MODE`, `*_MEDI`) | Yüksek eksiklik; üçlü aynı bilginin özeti | Yalnız `*_AVG` tut; eksiklik göstergesi düşün |
| `FLAG_DOCUMENT_*` (20 sütun) | Çoğu neredeyse sabit | `BELGE_SAYISI` özetine indirge |
| `OBS_*_SOCIAL_CIRCLE`, `AMT_REQ_CREDIT_BUREAU_*`, `OWN_CAR_AGE` | Aşırı uç değerler | Eğitim yüzdeliğine göre kırp (LR) |
| `DAYS_*` | Başvuruya göre **negatif** (geçmiş) | Yıla çevir ve işaretini düzelt |
| `previous_application`: `DAYS_FIRST_DRAWING` vb. | `365243` yapay kodu burada da görülür | Aynı anomali kuralı |
| `bureau_balance.STATUS` | `C` kapalı, `X` bilinmiyor, `0` gecikmesiz, `1-5` gecikme kovaları (5: ≥120 gün veya silinmiş) | "Gecikme" için 1-5 al; `X`'i gecikme sayma |
| `AMT_CREDIT_MAX_OVERDUE` (bureau) | Yüksek oranda eksik | Eksik ≠ 0; kayıt yoksa ayrı bayrak |

## 3. Tanım belirsizlikleri (savunmada sorulur; sözlükten teyit et)

1. **`TARGET` (sözlükten okundu ✅):** Sözlük tanımı özetle: 1 = örneklemdeki kredinin **ilk Y taksitinden en az birinde X günden
   fazla gecikmiş** (ödeme güçlüğü yaşayan) müşteri; 0 = diğer tüm durumlar. **X ve Y sözlükte açıklanmıyor.** Bu yüzden raporda
   gün/taksit sayısı yazılmaz; "ilk taksitlerde belirli bir gün eşiğini aşan gecikme" denir ve bu bir sınırlılık olarak belirtilir.
   Rapor terminolojisi: **temerrüt/ödeme güçlüğü**.
2. **`AMT_INCOME_TOTAL` dönemselliği (sözlükten okundu ✅):** Sözlük yalnızca "müşterinin geliri" diyor; **dönem belirtilmemiş**.
   Önerideki "yıllık gelir" ifadesi veriyle desteklenmiyor → raporda "gelir (dönem belirtilmemiş)"; oran kriterleri göreli gösterge.
   *(Öneriden sapma: `docs/03` D32.)*
3. **`AMT_ANNUITY` dönemselliği (sözlükten okundu ✅):** Sözlük yalnızca "kredi anüitesi" diyor; "aylık" olduğu **yazılı değil**.
   `taksit/gelir` oranı **mutlak ödeme yükü** değil, başvurular arası **karşılaştırmalı** göstergedir. TOPSIS için sıralama/yön önemli olduğundan
   karar katmanı etkilenmez; ama eşik tanımlarken (ör. "taksit/gelir > %40") mutlak yorum yapma.
4. **"Geçmiş temerrüt/gecikme" kriteri:** Öneri "kredi bürosu kayıtlarındaki gecikme sayısı" diyor. `bureau`'da gecikme **üç farklı kaynaktan** gelebilir (`CREDIT_DAY_OVERDUE`, `AMT_CREDIT_MAX_OVERDUE`, `bureau_balance.STATUS`).
   Tanım bir karar (D18/K1): önerilen "bu üç kaynaktan en az birinde gecikme izi olan büro kredisi sayısı". Alternatif tanımı (Home Credit'in kendi taksit gecikmesi) önerideki kapsamdan farklıdır.

## 4. Veri sızıntısı tuzakları (bu projede özellikle)

| # | Tuzak | Doğru yol |
|---|---|---|
| 1 | Eksik doldurma / ölçekleme / kırpma / kodlamayı **tüm veride** yapıp bölmek | `Pipeline` içinde, yalnız eğitim katına fit |
| 2 | Target encoding / WoE'yi tüm veride | Yalnız CV katı içinde |
| 3 | SMOTE'u CV'den **önce** uygulamak | İmblearn `Pipeline` ile yalnız eğitim katında |
| 4 | Özellik seçimini tüm veride yapmak | CV içinde |
| 5 | Eşik / kalibrasyon / TOPSIS referans noktasını test üzerinde seçmek | Eğitim OOF'unda kilitle (K-D) |
| 6 | XGBoost'ta erken durdurmayı test setiyle yapmak | Eğitimden ayrılmış doğrulama katı |
| 7 | Test kümesine tekrar tekrar bakıp ince ayar | Kapılar K-B/K-C; sayısını günlüğe yaz |
| 8 | Ek tablolarda `TARGET`'ten türeyen bir şeyin sızması | Toplulaştırma yalnız tablo içeriğinden; `TARGET` sütunu hiçbir yerde kullanılmaz |
| 9 | "Beklenmedik derecede iyi" sonucu kutlamak | Önce hata ara: AUC > ≈0,85 şüphelidir |

## 5. Özellik kataloğu (öneri; öğrenciyle birlikte karar verilir)

- **Türetilmiş (başvuru):** `YAS_YIL`, `ISTIHDAM_YIL`, `ISTIHDAM_YAS_ORANI`, `KREDI_GELIR`, `TAKSIT_GELIR`, `ODEME_ORANI` (annuity/credit), `KREDI_MAL_ORANI` (credit/goods price), `KISI_BASI_GELIR`, `EXT_ORT`, `EXT_STD`, `EXT_EKSIK_SAYISI`.
- **Büro:** kayıt sayısı, aktif sayısı, gecikmeli kredi sayısı, gecikmeli ay sayısı, maks. gecikme tutarı, toplam kredi/borç, borç oranı, son kredi gün, uzatma sayısı; `BURO_KAYDI_VAR`.
- **Önceki başvuru:** sayı, onay/ret sayısı ve oranı, ortalama tutar, verilen/istenen oranı, son karar günü; `ONCEKI_BASVURU_VAR`.
- **Taksit:** geç ödeme oranı, ortalama/maks. gecikme günü, eksik ödeme oranı.
- **POS / kart:** gecikmeli ay oranı, maks. DPD, kart kullanım oranı.
- **V2/F2 bulgusu (2026-11-20/22, eğitim):** `KREDI_GELIR` medyan 3,27 (p99≈13), `TAKSIT_GELIR` medyan 0,163, `ODEME_ORANI` 0,05, `KREDI_MAL_ORANI` 1,12, `EXT_ORT` 0,52. **Önemli:** `KREDI_GELIR`/`TAKSIT_GELIR`'in TARGET ile korelasyonu ≈0 (−0,009 / +0,013); `EXT_ORT` −0,221 (en güçlü). Yorum: kredi/gelir, taksit/gelir bu booked popülasyonda **tek başına risk tahmin etmiyor** → bunlar "politika/ödeme gücü" kriteri, "istatistiksel risk" değil (D18 çift sayım savunmasını **destekler**: MCDM'in kattığı şey ayırt edicilik değil politika kısıtı).
- **Kural:** sayım türü sütunlarda "kayıt yok" = 0; oran/ortalama sütunlarında "kayıt yok" = NaN (+ varlık bayrağı). Gerekçesini `docs/03` içine yaz.

## 6. Önceki referans sürümden doğrulanmış çıkarımlar

Önceki sohbette üretilen referans sürüm (`kredi-risk-kds.zip`), **sentetik** veriyle sınandı: 8 test geçti (pandas 2.2 ve 3.0, uyarısız),
EDA defteri hatasız çalıştı. Bu şunu gösterir: **kod mantığı ve birleştirme kuralları tutarlı**; **gerçek veri sonucu hakkında hiçbir şey söylemez.**
Oradan alınabilecek ders: (i) Büyük tablolarda yalnız gereken sütunları oku (`usecols`) ve tipleri küçült; (ii) `category` sütunlarında `groupby(observed=True)`; (iii) sürüm farkı uyarıları (`replace` ile aşağı tip dönüşümü) testle yakalandı; (iv) birleştirme sonrası `len(df) == len(app)` ve `SK_ID_CURR` tekilliği assert'i.
Öğrenci bu parçaları **kendi yazacak**; referans kodu yapıştırmak amaç değildir.

## 7. Performans ve bellek

- Tam veri için ≥ 8 GB RAM önerilir (en büyük tablo ≈27 milyon satır). Önce 20-50 bin başvurulu örnek.
- `pd.read_csv(..., usecols=[...], dtype=...)`; sayısal sütunları `float32`/küçük `int`; metin sütunlarını `category`.
- Büyük tabloları (özellikle `bureau_balance`, `installments_payments`) **parça parça** toplulaştır ve `data/processed/` altına Parquet olarak yaz; sonraki koşularda yeniden hesaplama.
- Kaggle indirmesi ≈0,7 GB (zip), açılınca ≈2,5 GB; Git'e girmez.

## 8. Beklenen büyüklükler (mantık kontrolü, doğrulanacak)

| Gösterge | Beklenti | Kaynak |
|---|---|---|
| `TARGET` oranı | ≈%8 | Bu belge §1 (doğrula) |
| Yalnız `application` + LR | AUC ≈0,74–0,76 | Yazarın hatırası (⚠️ doğrula) |
| Tüm tablolar + GBDT | AUC ≈0,77–0,80 | Bir doğrulanmış gösterge: LightGBM ≈0,79 (`docs/05` §2); yarışma üst skorları ≈0,80 civarı (⚠️ doğrula) |
| `EXT_SOURCE`'suz model | Belirgin düşüş bekleniyor | Ölçülecek (D17). V2: `EXT_SOURCE_1/2/3` TARGET ile en güçlü korelasyonlar (−0,155 / −0,161 / −0,177); eksik %56 / %0,2 / %20 |

Beklentiden **çok iyi** çıkarsa sızıntıdan şüphelen; **çok kötü** çıkarsa ön işleme/birleştirme hatasından şüphelen.
