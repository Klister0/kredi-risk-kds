# 03 · Karar Günlüğü

Hoca "neden bunu seçtin, başkasını seçseydin ne olurdu?" diye soracak. Bu dosya o cevapların **kaynağıdır**.

**Durumlar**
- 🟢 **Karar verildi:** öneride taahhüt edilmiş ya da öğrenciyle kesinleşmiş.
- 🟡 **Önerilen:** makul varsayılan; öğrenci (gerekirse hoca) onayı bekliyor.
- 🔴 **Açık:** deneyle ya da bilgiyle belirlenecek.

**Kural:** "Kanıt" alanı boşsa karar savunulabilir değildir. Kanıt yazılana kadar 🟡/🔴 kalır.
Karardan dönülürse eski kayıt silinmez; "Yerine geçti: Dxx-v2" notu eklenir.

**Kayıt şablonu**

```
### Dxx · Başlık   [🟢/🟡/🔴]
Bağlam: sorun nedir?
Seçenekler: A (seçilen) / B / C ...
Gerekçe: neden A?
Alternatif seçilseydi: B ile ne olurdu? (sonuç, risk, maliyet)
Kanıt: (deney/test/kaynak, dosya yolu) ← boşsa doldurulacak
Riskler / sınırlılık:
```

---

## A. Veri ve bölme

### D01 · Veri seti: Home Credit Default Risk   [🟢]
**Bağlam:** Öneri T1. **Seçenekler:** Home Credit (seçilen) / German Credit (1000 satır) / Taiwan Credit Card / Give Me Some Credit / Lending Club.
**Gerekçe:** Büyük ölçek (≈307 bin başvuru), çok tablolu ilişkisel yapı (ek tabloların toplulaştırılması gerçek bir veri mühendisliği işi), ve
gerçek bir kredi veren kurumdan. **Alternatif seçilseydi:** German Credit çok küçük, MCDM literatüründe zaten yaygın (küçük örneklem, genelleme zayıf);
Lending Club'da zaman değişkeni var, ancak veri erişimi ve kullanım koşulları ayrıca kontrol gerektirir.
**Kanıt:** `docs/05` boşluk analizi: MCDM'li çalışmalar çoğunlukla küçük veri setlerinde. **Sınırlılık:** Tek veri seti → genelleme iddiası zayıf; Demšar tipi çoklu veri seti testleri uygulanamaz.

### D02 · Problem tanımı: ikili sınıflandırma, hedef `TARGET`   [🟢]
**Seçenekler:** İkili PD (seçilen) / sağkalım analizi (zamana bağlı temerrüt) / LGD-EAD modelleme / çok sınıflı risk notu.
**Gerekçe:** Veride tek bir ikili etiket var, başvuru tarihi yok (zaman modeli kurulamaz). **Alternatif:** Sağkalım modeli daha zengin ama gerekli zaman bilgisi yok.
**Kanıt:** `docs/07` §3. **Sınırlılık:** `TARGET` resmi temerrüt değil, ilk taksitlerde gecikme (ödeme güçlüğü); raporda "temerrüt/ödeme güçlüğü" ifadesi ve tanım açıkça verilir.

### D03 · Bölme: %80/%20 katmanlı holdout + eğitim üzerinde 5 katlı katmanlı CV   [🟢]
**Seçenekler:** Katmanlı holdout + CV (seçilen) / iç içe (nested) CV / tekrarlı CV / bootstrap / zaman bazlı bölme.
**Gerekçe:** Kaggle `test.csv` etiketsiz olduğu için kendi test kümemiz gerekir. Katmanlama %8'lik azınlığın her parçada korunmasını sağlar.
**Alternatif seçilseydi:** Nested CV tahminleri daha tarafsız ama maliyeti ~5× (tam veride pahalı); zaman bazlı bölme için tarih yok.
**Kanıt:** `src/bolme.py` (sıfırdan katmanlı bölme) + `tests/test_bolme.py` (7 test, sklearn ile sınıf bazında uyum dahil, 2026-11-20 yeşil);
gerçek veri bölmesi `data/processed/bolme/` (n_egitim=246009, n_test=61502, tohum=42, %20), **commit'lendi** (`.gitignore` istisnası).
**Sınırlılık:** Aynı test kümesi birden fazla deneyde kullanılır → çoklu karşılaştırma uyarısı; kilit noktalar K-B/K-C.

### D04 · Eksik değer stratejisi: modele göre   [🟡]
**Seçenekler:** XGBoost yerel NaN + LR/RF için medyan + "eksik" göstergesi (seçilen) / MICE / KNN imputer / satır silme / tek tip sabit doldurma.
**Gerekçe:** Eksikliğin kendisi bilgi taşıyabilir (`EXT_SOURCE_*`, konut sütunları); satır silmek veri ve temsil kaybı. **Alternatif:** MICE/KNN yavaş (307 bin × 100+ sütun) ve kazanç belirsiz.
**Kanıt:** F4 `src/boru_hatti.py` SimpleImputer(median) `Pipeline` içinde, yalnız eğitime fit (sızıntı testi yeşil). (V2 eksik/temerrüt ilişkisi; M-fazı strateji karşılaştırması.) **Not:** RandomForest yerel NaN desteği sklearn 1.9'da doğrulanacak; şimdilik imputer kullanılıyor.

### D05 · `DAYS_EMPLOYED = 365243` anomalisi: NaN + bayrak   [🟢]
**Seçenekler:** NaN + `ISTIHDAM_ANOMALI` bayrağı (seçilen) / satırı sil / medyanla doldur / olduğu gibi bırak.
**Gerekçe:** Değer ≈1000 yıllık yapay kod (çoğunlukla emekli/çalışmayan); silmek yüzde ≈18'lik bir grubu kaybettirir; olduğu gibi bırakmak doğrusal modelleri bozar.
**Kanıt:** V2 (anomali %17,9, bu grupta temerrüt %5,4 < normal %8,7); `src/veri_hazirlama.py` + `tests/test_veri_hazirlama.py` (5/5, 2026-11-20); gerçek veride 44.075 satır işaretlendi, satır sayısı korundu.

### D06 · Kategorik kodlama   [🟡]
**Seçenekler:** One-hot (LR/RF) + yerel/sıralı kodlama (XGB) (seçilen) / target encoding / WoE / frekans kodlaması.
**Gerekçe:** One-hot sızıntısızdır ve basittir. Target encoding ve WoE hedefi kullandığı için **yalnızca CV katları içinde** güvenli.
**Alternatif:** WoE klasik skor kartlarının dilidir (yorumlanabilirlik artar) ama sızıntı riski ve ek karmaşıklık getirir.
**Kanıt:** (M-fazı).

### D07 · Ölçekleme ve aykırı değer   [🟡]
**Seçenekler:** LR için log dönüşümü + eğitimin yüzdeliklerine göre kırpma (winsorize), ağaçlar için yok (seçilen) / tümünde robust scaler / hiçbir şey.
**Gerekçe:** Ağaçlar tekdüze dönüşümlere duyarsız; LR uç değerlere duyarlı. Kırpma sınırları **yalnızca eğitimden** öğrenilir.
**Kanıt:** (V2 aykırı değer analizi; M1 sonuçları).

### D08 · Sınıf dengesizliği   [🟢] (sunum kapsamı: ağırlıklandırma yok)
**Seçenekler:** Yok / `class_weight`·`scale_pos_weight` / SMOTE / rastgele undersampling / eşik kaydırma.
**Gerekçe (neden açık):** Öneri T5 "denenecek" der. Bu seçim **AUC'yi neredeyse değiştirmez ama olasılık ölçeğini bozar** (Dal Pozzolo ve ark. 2015: undersampling sıralamayı korur, kalibrasyonu bozar); TOPSIS ise PD'nin değerini kullanır. Bu yüzden RQ3 konusu.
**Alternatif seçilseydi:** SMOTE yüksek boyutlu, karma tipli tabloda ağaç modellerinde çoğu zaman kazanç getirmez; sentetik örnekler kategorik/anomali kodlarıyla uyumsuz olabilir.
**Kanıt (M4/M6, 2026-11-22, XGBoost OOF, tam eğitim):** `scale_pos_weight`≈11,4 AUC'yi neredeyse değiştirmiyor (0,769→0,766) ama ortalama PD'yi 0,080'den **0,367**'ye şişiriyor (gözlenen 0,081); ECE 0,0025→**0,286**, Brier 0,067→0,170. → Ağırlıklandırma ayırt edicilik kazandırmıyor, olasılığı bozuyor (Dal Pozzolo ve ark. 2015 ✅ ile tutarlı). **Karar:** TOPSIS'e giden PD **ağırlıklandırmasız** modelden. SMOTE/undersampling sunum kapsamı dışı (D31). `deneyler/m4_m6_kalibrasyon_*_tam.json`, `rapor/sekiller/04_guvenilirlik_egrisi.png`

### D29 · Reject inference uygulanmaz   [🟡]
**Seçenekler:** Uygulama / parseling / augmentation / kapsam dışı bırak (seçilen).
**Gerekçe:** Reddedilenlerin sonucu hiçbir veride yok; yöntemler ek varsayım ister ve literatürde faydası tartışmalı. **Etkisi:** Sonuçlar "kredisi verilmiş (booked) popülasyon" için geçerli; "Reddet" grubunun gerçek temerrüt oranı, tüm başvuru havuzunda farklı olabilir.
**Kanıt:** Raporda **Sınırlılıklar** bölümü; `docs/05` içinde Crook & Banasik (⚠️ doğrulanacak).

---

## B. Modelleme

### D09 · Model seti: LR, RF, XGBoost   [🟢]
**Seçenekler:** LR+RF+XGB (öneri, seçilen) / LightGBM / CatBoost / SVM / sinir ağı / WoE-LR skor kartı / EBM (açıklanabilir boosting).
**Gerekçe:** Yorumlanabilir baseline + bagging + boosting üçlüsü; öneride taahhüt. **Alternatif seçilseydi:** LightGBM ile XGBoost benzer sonuçlar verir (Home Credit çalışmalarında ikisi de en iyi model olarak raporlanabiliyor),
CatBoost kategorik veride avantajlı; ikisi de "ek" katmanda duyarlılık olarak eklenebilir. Tabular veride ağaç tabanlı modeller sinir ağlarına çoğu zaman üstün (⚠️ Grinsztajn ve ark. 2022, doğrulanacak).
**Kanıt (2026-11-22, temel+büro, 5 katlı CV, sabit hiperparametre):**
| Model | CV ROC-AUC | PR-AUC | Eğitim AUC | Süre (2 çekirdek) |
|---|---|---|---|---|
| Dummy | 0,499 ± 0,002 | 0,081 | – | – |
| LR | 0,753 ± 0,002 | 0,235 | – | – |
| RF | 0,749 ± 0,002 | 0,235 | 0,790 | 148 sn |
| XGBoost | **0,769 ± 0,002** | **0,257** | 0,869 | 165 sn |
Gözlem: XGB > LR ≈ +0,017 AUC (CV std'nin ~8 katı; resmî test M7 bootstrap). **RF, LR'nin biraz altında** (kısıtlı ayar: derinlik 12, max_samples 0,3) — gizlenmez, M5'te eşit bütçeli aramayla yeniden bakılacak. XGB eğitim-CV farkı 0,10 → düzenlileştirme M5. `deneyler/m1_*`, `deneyler/m2_m3_*`

### D10 · Hiperparametre arama   [🟢]
**Seçenekler:** Rastgele arama (seçilen) / grid / Optuna (Bayes) / elle ayar.
**Gerekçe:** Eşit bütçeyle adil karşılaştırma; rastgele arama grid'e göre geniş uzayda daha verimli (⚠️ Bergstra & Bengio 2012, doğrulanacak). **Alternatif:** Optuna daha az denemede iyi sonuç verir; öğrenme açısından "ek".
**Tasarım (2026-11-22, arama ÖNCESİ yazıldı):** `deneyler/m5_arama.py` — her model 12 aday × 3 katlı CV (eşit bütçe), ölçüt ROC-AUC; en iyi parametreler M1–M3 ile aynı 5 katlı CV'de yeniden ölçülür. **Seçim kuralı:** en yüksek 5 katlı CV ROC-AUC. Test kümesi seçime karışmaz. Uzaylar betikte kayıtlı (LR: C; RF: ağaç sayısı/derinlik/yaprak/özellik/örnek oranı; XGB: ağaç, öğrenme hızı, derinlik, min_child_weight, subsample, colsample, L1/L2).
**Sonuç (M5, 2026-11-22, tam eğitim, öğrencinin makinesi ~35 dk):** LR 0,7528±0,002 (C≈0,031; aday aralığı 0,7518–0,7526) · RF 0,7503±0,002 (aday 0,7467–0,7498) · **XGB 0,7704±0,001** (aday 0,7509–0,7692; lr≈0,024, derinlik 6, 754 ağaç, min_child_weight 15, L2≈4,6). Kurala göre **XGBoost seçildi**. Ayar kazancı küçük (XGB +0,001) ama eğitim-CV farkı 0,10→0,06. RF ayarlı hâliyle de LR'nin altında → ilk bulgu ayar eksikliğinden değil. `deneyler/m5_arama_2026-11-22_tam.json`
**Önceki not:** M2/M3 şimdilik **sabit, makul** parametrelerle (betikte kayıtlı); erken durdurma kullanılmadı (ayrı doğrulama katı gerektirir, sızıntı riski). Arama M5'te eşit bütçeyle. (M5: bütçe, aranan uzay, CV skor dağılımı.)

### D11 · Metrik seti   [🟢]
**Seçenekler:** ROC-AUC (+Gini), PR-AUC, KS, Brier, ECE, F1@eşik, beklenen maliyet (seçilen) / doğruluk.
**Gerekçe:** %8 pozitif oranında "herkes ödeyecek" modeli ≈%92 doğruluk alır; doğruluk anlamsız. AUC eşikten bağımsız ayırt edicilik, PR-AUC dengesiz veri duyarlılığı (⚠️ Saito & Rehmsmeier 2015), KS/Gini sektör dili, Brier/ECE kalibrasyon (karar katmanı için kritik).
**Kanıt:** (M7 tablosu).

### D12 · F1 eşiği ve maliyet varsayımı   [🔴]
**Seçenekler:** 0,5 sabit / F1'i maksimize eden eşik / maliyet duyarlı eşik (FN maliyeti ≫ FP maliyeti).
**Gerekçe:** F1 eşiğe bağımlı; eşik **test üzerinde seçilmez**, eğitim OOF tahminlerinde seçilir. Maliyet oranı (ör. 5:1, 10:1) **varsayımdır**; tek bir sayı yerine senaryo aralığı raporlanır (⚠️ Elkan 2001; Verbraken ve ark. 2014).
**Kanıt:** (M7/E1 duyarlılık tablosu).

### D13 · Kalibrasyon yöntemi   [🟡] (ön-belirlenmiş kural)
**Seçenekler:** Isotonic / Platt (sigmoid) / prior-shift düzeltmesi (undersampling için analitik) / kalibrasyonsuz.
**Gerekçe:** TOPSIS PD'yi doğrudan kullanır → olasılıkların güvenilir olması gerekir. **Alternatif:** Isotonic esnek ama az veride aşırı uyum; Platt basit ama tek parametreli biçim varsayar. Veri büyük olduğu için isotonic beklenir.
**Kanıt (M6):** Ağırlıksız XGB ham OOF zaten kalibre (ECE 0,0025, ort. tahmin 0,080 vs 0,081). Isotonic (CV'li) ECE'yi 0,0006'ya indiriyor, AUC'yi 0,0007 düşürüyor (bağ/tie etkisi). Ağırlıklı modelde analitik **prior düzeltme** ECE'yi 0,286→0,013'e indiriyor ama **aşırı düzeltiyor** (ort. 0,068 < 0,081): ağırlıklandırma, düzenlileştirilmiş ağaçlarda tam olarak yeniden örneklemeye denk değil. Isotonic her iki durumda ECE≈0,001.
**Ön-belirlenmiş kural (K-C öncesi yazıldı):** Seçilen final modelin OOF ECE'si < 0,01 ise **ham** PD kullanılır; değilse **isotonic**, tüm eğitim OOF'una fit edilip teste uygulanır. Sızıntısız: kalibrasyon yalnız OOF'tan öğrenilir.

### D14 · Modeller arası istatistiksel karşılaştırma   [🟡]
**Seçenekler:** Bootstrap %95 GA + eşleştirilmiş fark (seçilen) / DeLong AUC testi / katlar üzerinde eşleştirilmiş t-testi (düzeltmeli) / Friedman+Nemenyi (çoklu veri seti).
**Gerekçe:** Tek veri setinde Friedman/Nemenyi uygulanamaz; test kümesi büyük (≈61 bin) olduğundan bootstrap ve DeLong uygulanabilir. Kat bazlı t-testi bağımsızlık varsayımını ihlal eder (⚠️ Nadeau & Bengio 2003).
**Kanıt:** (M7).

### D15 · Açıklanabilirlik   [🟢]
**Seçenekler:** SHAP (TreeExplainer) + permutation importance (seçilen) / LIME / PDP-ICE / karşıolgusal açıklamalar (DiCE) / içsel yorumlanabilir model (EBM, skor kartı).
**Gerekçe:** Öneri T9. SHAP ağaç modellerinde hızlı ve tutarlı yerel/global açıklama verir. **Sınırlılık:** SHAP nedensellik değildir; korele özelliklerde katkı paylaşımı kararsızdır; yüksek riskli kararlar için "post-hoc açıklama yerine doğası gereği yorumlanabilir model" tartışması var (⚠️ Rudin 2019).
**Kanıt:** (M8; LR katsayıları ile SHAP tutarlılığı kontrolü).

### D16 · Korunan nitelikler (cinsiyet, yaş)   [🔴]
**Seçenekler:** Cinsiyeti modelden çıkar, yaşı tut + adalet analizi / ikisini de çıkar / hepsini tut.
**Gerekçe (öneri):** Birçok hukuk düzeninde cinsiyetin kredi kararında kullanılması sorunlu (⚠️ yasal çerçeve doğrulanacak: AB, KVKK/BDDK, ABD ECOA). Akademik prototip de olsa savunmada sorulur. Çıkarmanın AUC maliyeti ölçülmeli.
**Kanıt:** (F5/M-fazı: `CODE_GENDER`'lı/siz CV; E4 adalet metrikleri). **Hocayla konuşulacak.**

### D17 · `EXT_SOURCE_1/2/3` kullanımı   [🟡]
**Seçenekler:** Tut (seçilen) / çıkar / hem tam hem `ext-siz` sürüm raporla.
**Gerekçe:** Bu üç skor veri setindeki en güçlü sinyaller (kaynakları belirsiz, dış skorlar). Gerçek bankada karşılığı bürodan gelen skor olabilir; ama yorumlanabilirlik ve genellenebilirlik sorusu doğar.
**Alternatif:** Çıkarılırsa AUC belirgin düşer; bu düşüşü raporlamak, modelin diğer değişkenlerden ne kadar öğrendiğini gösterir (savunma kartı).
**Kanıt:** (F5 `ext-siz` sürümü, M7).

---

## C. Karar katmanı

### D18 · Karar kriterleri ve çift sayım   [🔴]
**Seçenekler:** Öneri Tablo 5'teki 6 kriter (seçilen, T6) / PD'siz politika kriterleri / PD'yi politika-kör özelliklerle eğitmek / kriterleri PD'ye ortogonalleştirmek.
**Bağlam:** PD modeli gelir, kredi/gelir, istihdam ve gecikme bilgisini zaten kullanıyor. Aynı bilgi ikinci kez ağırlıklanıyor; bu da *nominal* AHP ağırlığı ile *etkin* ağırlığın farklı olmasına yol açar (⚠️ Choo ve ark. 1999: ağırlıkların yorumu).
**Gerekçe (savunma):** PD "istatistiksel risk", diğer kriterler "banka politikası/ödeme gücü" kısıtını temsil eder; amaç tam da bu iki dilin birleşiminin bedelini ölçmek (RQ1).
**Kanıt:** F2 (2026-11-22): `KREDI_GELIR`/`TAKSIT_GELIR` TARGET ile korelasyon ≈0 (−0,009/+0,013) → politika kriterleri risk sinyali taşımıyor, ayrı dil oldukları savunmasını destekler. (Ek: kriter korelasyon matrisi, "politika-kör PD" ablation, etkin-nominal ağırlık analizi — model fazında.)

### D19 · Ağırlıklandırma: AHP, yargıçlar kim?   [🟡]
**Güncelleme (2026-11-22):** Birincil yargıç: **bir banka çalışanı** (öğrencinin babası; kredi değerlendirme deneyimi formda kayıt altına alınacak). Mümkünse 1–2 meslektaşı da eklenecek → grup AHP (geometrik ortalama). Yargıç **bağımsız** doldurur: model sonuçları ve öğrencinin görüşü önceden paylaşılmaz. CR > 0,10 ise en tutarsız çiftler gösterilip yeniden değerlendirme istenir (standart AHP uygulaması). Raporda yargıcın rolü ve deneyimi yazılır; yakınlık ilişkisi sorulursa açıkça belirtilir. Tek yargıç kalırsa RQ2 ağırlık dayanıklılığı bu sınırlılığı telafi eden ana analizdir.
**Seçenekler:** AHP, grup yargısı (seçilen) / tek kişilik AHP / eşit ağırlık / entropi / CRITIC / BWM (en iyi-en kötü).
**Gerekçe:** Öneri T7 AHP der. AHP öznel yargı ister; "banka uzmanı" yoksa vekil gerekir: ≥ 3 yargıç (bankacı, finans öğretim üyesi, finans öğrencisi), geometrik ortalamayla birleştirme (⚠️ Aczél & Saaty 1983), CR < 0,10 koşulu. Yargı toplanamazsa literatür temelli ağırlıklar + geniş duyarlılık analizi, ve bu açıkça sınırlılık yazılır.
**Alternatif seçilseydi:** Entropi/CRITIC objektif (veriden) ama "politika önceliklerini" yansıtmaz; BWM daha az karşılaştırma ister (⚠️ Rezaei 2015) ve KOBİ kredi literatüründe kullanıldı (Roy & Shaw ✅).
**Kanıt:** `src/ahp.py` sıfırdan (kuvvet yinelemesi özvektör, CI/CR, geometrik ortalama grup birleştirme), `tests/test_ahp.py` 7/7: tutarlı matristen ağırlığı geri verir (CR=0, λmax=n), `numpy.linalg.eig` ile aynı özvektör, döngüsel yargıda CR>0,10. RI değerleri web'de doğrulandı (n=6 → 1,24). Yargı formu `docs/ahp_yargi_formu.md`. **Yargıçlar henüz belirlenmedi.** (Yargı tabloları, CR değerleri, RQ2 karşılaştırması.)

### D20 · MCDM yöntemi: TOPSIS   [🟢]
**Seçenekler:** TOPSIS (öneri, seçilen) / VIKOR / PROMETHEE / ELECTRE / SAW (ağırlıklı toplam) / MARCOS.
**Gerekçe:** Mesafe tabanlı, sezgisel, her alternatifi bağımsız bir puana indirgiyor (başvuru bazlı puan lazım). **Alternatif seçilseydi:** SAW şeffaf ve rank reversal'a daha az açık ama uç değerlerde telafi edici (bir kriterin kötülüğü diğeriyle kapanır); VIKOR "uzlaşı çözümü" ve grup faydası/pişmanlık kavramıyla sınırlı telafiye izin verir (⚠️ Opricovic & Tzeng 2004).
**Kanıt:** (RQ2'de SAW/VIKOR duyarlılık karşılaştırması "ek").

### D21 · TOPSIS referans noktaları ve normalizasyon   [🟢]
**Seçenekler:** Vektör normalizasyon + **eğitim verisinden sabitlenmiş** ideal/anti-ideal (eğitim yüzdelikleri) (önerilen) / batch min-max / vektör normalizasyon (batch).
**Gerekçe:** Dashboard tek başvuru değerlendirir; batch TOPSIS tek alternatifte tanımsızdır. Küme değişince sıralamanın değişmesi (rank reversal; ✅ García-Cascales & Lamata 2012) bağımsız karar için istenmez. Sabit referans bu sorunu yok eder ama referans seçimi (p1/p99 mu, p5/p95 mi?) yeni bir parametre.
**Alternatif seçilseydi:** Batch TOPSIS aynı başvuruya farklı grupta farklı puan verir; bunu RQ4'te ölçmek mümkün.
**Karar:** Vektör normalizasyonu; kırpma sınırları (p1/p99), normalizasyon paydası ve A+/A− **yalnız eğitimden** (`src/topsis.py::SabitTopsis`).
**Kanıt:** `tests/test_topsis.py` 7/7: (i) baskın alternatif C*=1, baskın olunan C*=0; (ii) klasik TOPSIS **pymcdm 1.4** ile aynı (korelasyon > 0,999, sıralama uyumu > %99); (iii) eğitim kümesinde SabitTopsis = batch TOPSIS (kırpılmış); (iv) sabit referansta başvuru tek tek ya da toplu puanlansa da aynı puan (rank reversal yok); (v) batch TOPSIS'te yeni alternatif eklenince mevcut puanlar değişiyor (rank reversal var). Gerçek veride uçtan uca çalıştı (kriter hazırlayıcı + SabitTopsis). (E4 batch-vs-sabit deneyi: ek kapsam.)

### D22 · Karar bantları ve eşikler   [🔴]
**Seçenekler:** Hedef onay oranına göre eğitim OOF C* niceliklerinden eşik (önerilen) / sabit puan eşikleri (örn. 0,6/0,4) / maliyet tabanlı eşik / karar vericinin dashboard'da ayarladığı eşikler.
**Gerekçe:** Sabit puan eşikleri ağırlık değişince anlamını yitirir; onay oranı bazlı eşik, ağırlık/dağılım değişse de "portföy politikasını" sabit tutar ve PD-tek ile **eşit onay oranında** karşılaştırmaya izin verir (D23).
**Kanıt:** (K4).

### D23 · Karar katmanı doğrulama tasarımı   [🟡]
**Seçenekler:** Eşit onay oranında kötü oranı eğrisi + swap-set + politika-ihlal oranı + PD-tek baseline (seçilen) / yalnızca bant bazlı temerrüt oranları (önerideki ham hâl).
**Gerekçe:** Önerideki doğrulama (Onayla/Reddet gruplarının temerrüt oranı ayrışıyor mu?) PD içerdiği için neredeyse garanti sonuç verir (döngüsellik). PD-tek baseline olmadan MCDM'in katma değeri ölçülemez.
**Kanıt:** (E1).

---

## D. Sunum, süreç, altyapı

### D24 · Arayüz: Streamlit   [🟢]
**Seçenekler:** Streamlit (öneri, seçilen) / Gradio / Dash / Flask+React / FastAPI+React.
**Gerekçe:** Python-yerli, ağırlık kaydırıcıları ve canlı sonuç için hızlı. **Alternatif:** FastAPI+React ölçeklenebilir ve üretime yakın ama tek öğrenci/13 hafta için kapsam dışı.

### D25 · Deney takibi   [🟡]
**Seçenekler:** Tarihli CSV/JSON + sabit tohum (seçilen) / MLflow / Weights & Biases.
**Gerekçe:** Basit ve görünür; öğrenme için önce elle yapılır. **Alternatif:** MLflow "ek" katmanda.

### D26 · Ortam ve Git stratejisi   [🟡]
**Seçenekler:** `venv` + `requirements.txt` (seçilen) / `uv` / conda / poetry. **Git:** `main` + kısa ömürlü dallar + Conventional Commits (Türkçe) / doğrudan `main`.
**Gerekçe:** Windows'ta en az sürpriz; GitHub'da okunaklı geçmiş.

### D27 · Ara veri formatı: Parquet   [🟢]
**Seçenekler:** Parquet (seçilen) / CSV / Feather / DuckDB.
**Gerekçe:** Tip korur, sıkıştırır, hızlı okur (CSV'ye göre tip bilgisi kaybolmaz).

### D28 · Dil politikası   [🟢]
Türkçe kod/klasör adları, Türkçe commit, Türkçe rapor. **Gerekçe:** Öğrencinin ve hocanın dili; tutarlılık.
**Not:** Kütüphane çağrıları İngilizce kalır (`fit`, `predict_proba`).

### D30 · Maliyet varsayımları   [🔴]
FN/FP maliyet oranları ve gelir/zarar varsayımları literatür ve makul aralıklarla senaryo olarak raporlanır; tek bir sayıya dayanılmaz (bkz. D12).

---

### D31 · Sunum takvimine göre kapsam daraltma   [🟡]
**Bağlam:** Sunum 7 Aralık 2026; 2026-11-20 itibarıyla 17 gün var. Önerinin 13 haftalık çizelgesi uygulanamaz (`docs/02` "Sıkıştırılmış takvim").
Makale sunumdan sonra teslim edileceği için bazı işler sunum sonrasına kayabilir.
**Seçenekler:** A (önerilen) sunuma kadar çekirdek + dar kapsam, sonrası genişletme / B tüm öneri kapsamı sunuma kadar / C model kısmını küçültüp yalnız karar katmanına odaklanmak.
**A'nın içeriği:**
- Ek tablolar: sunuma kadar yalnız `bureau` + `bureau_balance` (6. kriter "geçmiş gecikme" bunlara bağlı). Diğer 4 tablo sunum sonrası "tam" özellik seti olarak eklenebilir. → T2'den **kısmi sapma**.
- Dengesizlik (T5): {yok, `class_weight`/`scale_pos_weight`}; SMOTE sunuma kadar yok (gerekçe: Dal Pozzolo ve ark. 2015 ✅ + süre). RQ3 dar: yalnız XGBoost × {yok, ağırlık} × {ham, isotonic}.
- Hiperparametre: küçük rastgele arama, üç modele eşit bütçe.
- Düşen (ek katman): RQ4, RQ5, LightGBM/CatBoost, CI, MLflow.
**Alternatif seçilseydi:** B ile her adım yüzeysel kalır ve savunulabilirlik (hedef 2) düşer; C ile öneri T3/T4 taahhüdü zayıflar.
**Kanıt:** Takvim (`docs/02`). **Sınırlılık:** Sunumdaki sonuçlar "temel + büro" özellik setine aittir; makalede genişletilirse sayılar değişebilir ve bu açıkça belirtilir.

### D32 · Öneride bulunan ifade hataları (bildirim)   [🟢]
**Bağlam:** `CLAUDE.md` §4 kural 4: önerideki hatalar sessizce düzeltilmez.
1. **Gelir ve taksit dönemselliği:** Öneri §5 "yıllık gelir" ve "aylık taksit" diyor; veri sözlüğü `AMT_INCOME_TOTAL` için yalnız "gelir", `AMT_ANNUITY` için yalnız "anüite" diyor, **dönem belirtmiyor** (`docs/07` §3). Raporda "gelir" ve "taksit/anüite" kullanılır; oranlar göreli göstergedir.
2. **`TARGET` tanımı:** Sözlük, eşik gün (X) ve taksit sayısını (Y) **vermiyor**. Raporda sayı yazılmaz; "temerrüt/ödeme güçlüğü" terimi ve bu belirsizlik sınırlılık olarak verilir.
3. **Metrik tablosu tutarsızlığı:** Öneri §6.2 tablosunda LR ve RF yalnız ROC-AUC/F1, XGBoost ek olarak PR-AUC ile değerlendirilecek gibi yazılmış. Adil karşılaştırma için üç model **aynı metrik setiyle** değerlendirilir (D11).
**Kanıt:** `data/raw/HomeCredit_columns_description.csv` (latin-1), okunma tarihi 2026-11-20; öneri belgesi.

---

### D33 · EDA, bölmeden SONRA ve yalnız eğitim kümesinde   [🟢]
**Bağlam:** `docs/02` sıralaması V2 (EDA) → V3 (bölme) idi. Tüm veride EDA, test kümesinin dağılımını görmemize yol açar;
sonra eksik doldurma/aykırı değer kararlarını farkında olmadan bu bilgiye göre veririz (araştırmacı kaynaklı sızıntı).
**Seçenekler:** Önce böl, EDA'yı yalnız eğitimde yap (seçilen) / tüm veride EDA (önerideki örtük sıra) / EDA'yı tümden atla.
**Gerekçe:** Kapı K-B koşulu "test setine hiç bakılmadı"; dürüst kalabilmek için bölme EDA'dan önce gelir. Fark küçük olsa da savunulabilir tek sıra budur.
**Alternatif seçilseydi:** Tüm veride EDA sonuçları biraz daha "temiz" görünür ama "test setine baktınız mı?" sorusuna dürüst cevap "evet" olur.
**Kanıt:** V3 bölme (D03) EDA'dan (V2) önce tamamlandı. **Sınırlılık:** Eğitimdeki aykırı/eksik desenleri tüm veriyi temsil etmeyebilir; test dağılımı final değerlendirmede görülür.

### D34 · Karar kriterleri tablosu (K1)   [🟡]
**Bağlam:** T6'daki 6 kriterin koddan türetilmesi, yönü ve eksik değer kuralı. TOPSIS'te yön ve aykırı değerler sonucu doğrudan etkiler.

| Kod | Kriter | Sütun (kod) | Yön | Eksik / özel durum kuralı (önerilen) |
|---|---|---|---|---|
| K1 | Temerrüt olasılığı | seçilen modelin PD'si (eğitimde OOF) | maliyet | yok |
| K2 | Kredi/gelir | `KREDI_GELIR` | maliyet | eksik yok (eğitimde %0) |
| K3 | Taksit/gelir | `TAKSIT_GELIR` | maliyet | eksik ≈0; kalırsa eğitim medyanı |
| K4 | Gelir | `AMT_INCOME_TOTAL` | fayda | eksik yok |
| K5 | İstihdam süresi | `ISTIHDAM_YIL` | fayda | **anomali grubu (%17,9, emekli/çalışmayan) → eğitim medyanı** |
| K6 | Geçmiş gecikme | `BURO_GECIKMELI_SAYISI` | maliyet | **büro kaydı yok (%14,3) → 0** |

**Ek kural:** Her kriter TOPSIS öncesi **eğitimin p1–p99** aralığına kırpılır (sınırlar eğitimden, D21 sabit referansın temeli).
Gerekçe: gelirde aşırı uçlar var; vektör normalizasyonu uçlara duyarlı, tek bir aşırı gelir tüm diğerlerini sıkıştırır.
**Gerekçe (K5):** Emekli grubu verinin gösterdiği gibi daha **düşük** riskli (temerrüt %5,4 vs %8,7, V2). 0 yıl vermek onları cezalandırır ve kanıtla çelişir; medyan "ne ödül ne ceza"dır.
**Gerekçe (K6):** Politika kriteri olarak "gözlenmiş gecikme yok" ile "kayıt yok" ikisi de gecikme kanıtı içermez; kanıt olmadan ceza verilmez. Not: **model** tarafında bu iki durum ayrı tutulur (`BURO_KAYDI_VAR`, F3); karar katmanında ayrım PD üzerinden zaten yansır.
**Alternatifler:** K5 için 0 (cezalandırıcı) / ayrı "emekli" kriteri; K6 için kayıtsızlara medyan ya da ceza; kırpma yerine log dönüşümü.
**Kanıt:** V2/F3 bulguları (`docs/07`). Duyarlılık: RQ2'de bu kurallar değiştirilerek karar değişim oranı ölçülebilir.

## Bilinen açık sorular (hocaya/öğrenciye)

1. Hoca "literatüre katkı"yı nasıl tanımlıyor? (→ `docs/04` kapsamı)
2. AHP için uzman yargısı toplanabilir mi? (→ D19)
3. Cinsiyet değişkeni modelde kalsın mı? (→ D16)
4. Test kümesini tüm deneyler için ortak kullanma konusunda hocanın görüşü? (→ D03)
