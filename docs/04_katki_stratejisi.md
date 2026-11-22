# 04 · Literatüre Katkı Stratejisi

Hoca "literatüre katkı" bekliyor. Bu dosya, **dürüst ve savunulabilir** bir katkının nasıl kurulacağını anlatır.
Katkı iddiası, ancak §9'daki sistematik tarama yapıldıktan ve kaydedildikten sonra yazılır.

## 1. Dürüst başlangıç: neler katkı **değildir**

Bu paketi hazırlarken yapılan sınırlı literatür taraması (`docs/05`), şunları gösteriyor:

| Plan | Neden tek başına katkı değil |
|---|---|
| Home Credit üzerinde LR / RF / XGBoost karşılaştırması | Çok sayıda çalışma, preprint ve tez zaten yapmış (ör. boosting karşılaştırmaları, SHAP'lı yorumlama). Bizim için **zorunlu temel**, yeni bulgu değil. |
| SHAP ile açıklama | Aynı veri setinde zaten uygulanmış. Gerekli ama yeni değil. |
| AHP-TOPSIS ile kredi skoru | Mevcut; çoğu KOBİ/şirket kredisi, küçük örneklem, ML'siz ve uzman ağırlıklı (ör. Roy & Shaw). |
| MCDM ile **sınıflandırıcıları sıralamak** | Mevcut (Kou ve ark. 2014; García ve ark.). Bizim amacımız *başvuruları* sıralamak. |

**Sonuç:** Katkı, model karşılaştırmasında değil, **ML risk skorunun MCDM karar katmanına entegrasyonunun büyük ölçekli gerçek veride sistematik
olarak incelenmesinde** aranmalı.

## 2. Katkı çerçevesi: "Risk skoru ile politika kriterlerini birleştirmenin bedeli ve dayanıklılığı"

Tek cümle: **"Bir ML risk skorunu AHP-TOPSIS ile politika kriterleriyle birleştiren karar katmanı, yalnızca risk skoruna dayanan karardan ne kadar
farklı sonuç veriyor, bu fark neye mal oluyor ve ağırlık belirsizliği karşısında ne kadar dayanıklı?"**

Üç ana araştırma sorusu (çekirdek + hedef katman), bir ek:

| # | Soru | Katman |
|---|---|---|
| **RQ1** | Eşit onay oranında, AHP-TOPSIS kararı PD-tek eşiklemeye göre **ne kadar daha kötü/iyi** ayrıştırıyor ve politika kriterlerini (ödeme gücü) ne kadar daha iyi koruyor? (Bedel: *price of policy*) | Çekirdek |
| **RQ2** | Kriter ağırlığı belirsizliği (AHP yargı değişimi, farklı ağırlıklandırma yöntemleri) kararları ne kadar oynatıyor? **Karar kararlılığı** "Şartlı Onayla" bandını gerekçelendirmek için kullanılabilir mi? | Hedef |
| **RQ3** | Sınıf dengesizliği çözümleri (ağırlıklandırma/SMOTE/undersampling) AUC'yi korurken **olasılık kalibrasyonunu bozuyor** mu ve bu, TOPSIS kararlarını ne kadar değiştiriyor? Kalibrasyon bunu düzeltiyor mu? | Hedef |
| RQ4 | Sabit-referans TOPSIS ile batch TOPSIS arasındaki karar farkı (rank reversal) ne büyüklükte? | Ek |
| RQ5 | PD-tek ve AHP-TOPSIS onay oranları, cinsiyet/yaş gruplarında nasıl farklılaşıyor? | Ek |

**Neden bu sorular?** Her biri (a) önerideki gerçek bir zayıf noktadan doğuyor (`docs/01` §2), (b) veriyle sınanabilir, (c) sonuç ne olursa olsun
(olumlu/olumsuz/sıfır) bilgi taşıyor, (d) 13 haftaya sığıyor.

## 3. Konumlandırma ve boşluk analizi (taslak; L3'te güncellenecek)

| Çalışma türü | Örnek (✅ doğrulanmış) | Neyi yapıyor | Bizim farkımız |
|---|---|---|---|
| MCDM ile model sıralama | Kou, Peng, Lu (2014) | TOPSIS ile **modelleri** metriklerine göre sıralar | Biz **başvuruları** sıralıyoruz |
| Bağımsız MCDM skorlama (başvuran) | Roy & Shaw (2021 BWM-TOPSIS ✅, 2022 fuzzy-TOPSIS-Sort-C ✅, 2023 AHP-TOPSIS ✅); **Ignatius ve ark. (2018) bulanık AHP-TOPSIS ✅** | KOBİ/başvuranları uzman-bulanık ya da finansal-oran kriterleriyle puanlar; ticari dereceyle karşılaştırır | Biz **eğitilmiş ML PD'sini** kriter yapıyor, **büyük perakende verisinde gerçek temerrüt etiketiyle** ve **PD-tek baseline'a karşı** doğruluyoruz |
| Türkçe literatür | Oral & Engin (2024) Bulanık AHP-TOPSIS | 10 ticari firma | Ölçek ve doğrulama farkı |
| ML + AHP hibrit | AHP-SVM çalışmaları (⚠️ künye eksik) | AHP öznitelik ağırlığı, SVM sınıflandırma | Biz AHP'yi karar katmanında, ML'den sonra kullanıyoruz |
| Home Credit ML çalışmaları | arXiv 2505.20815, Coşkun & Turanlı (2023) (⚠️ teyit) | Model karşılaştırma, SHAP | Karar katmanı yok |

**Boşluk hipotezi (L1 ön taramasıyla DARALTILDI, 2026-11-20):** AHP/BWM-TOPSIS'i **başvurana** uygulamak literatürde **mevcut**
(Ignatius ve ark. 2018; Roy & Shaw 2021/2022/2023). Dolayısıyla "MCDM ile başvuru sıralamak" katkı değildir. Geriye kalan, taradığımız kayıtlarda
rastlamadığımız boşluk: *(i) bir TOPSIS kriteri olarak **eğitilmiş ML temerrüt olasılığı** (bu çalışmalar uzman/bulanık ya da finansal-oran kriterleri kullanıyor);
(ii) **büyük ölçekli gerçek perakende verisi + gözlenen temerrüt etiketi** (bunlar KOBİ/küçük örneklem, ticari dereceyle karşılaştırıyor);
(iii) **PD-tek baseline'a karşı eşit onay oranında** "politika bedeli"; (iv) **ağırlık dayanıklılığı + kalibrasyonun karara etkisi**.*
Bu dar iddiayı yazmadan önce §9 tam taraması gerekir.

## 4. RQ1 deney tasarımı: PD-tek vs AHP-TOPSIS

**Skorlar.** `s_PD = 1 − PD` (yüksek = iyi). `s_MCDM = C*` (TOPSIS yakınlık katsayısı).
**Onay oranı ızgarası.** a ∈ {10, 20, …, 90}%: her skor için en iyi a% onaylanır.
**Birincil çıktı.** Her a'da onaylananlar içinde **kötü oranı** (TARGET=1 oranı); fark = MCDM − PD-tek. Eğri altındaki alan a ∈ [0,2; 0,8].
**İkincil çıktılar.**
- **Swap-set:** PD-tek onaylayıp MCDM'in reddettiği (ve tersi) başvurular; bunların kötü oranı ve kriter profili.
- **Politika ihlali:** Onaylananlar içinde taksit/gelir veya kredi/gelir oranı eğitim yüzdeliğinin (ör. p90) üzerinde olanların payı.
- **Ağırlık taraması:** `w_PD` 0 → 1 değişirken (diğerleri orantılı), kötü oranı ile politika ihlali arasındaki **Pareto eğrisi**.
- **Ablation:** `politika-kör PD` (kriter özelliklerinden arındırılmış model), `ext-siz PD`.
**İstatistik.** Test kümesi üzerinde 1000 bootstrap, eşleştirilmiş fark için %95 güven aralığı. Çoklu a için düzeltme yok, tek birincil metrik (alan farkı) belirlenir.
**Beklenen / olası sonuçlar (hipotez, ön-kayıt):**
- H1a: PD-tek, kötü oranında MCDM'den daha iyi veya eşit (çünkü PD doğrudan hedefe optimize). Fark = "bedel".
- H1b: MCDM, politika ihlalini PD-tek'e göre azaltır.
- H1c: `w_PD` orta/yüksek olduğunda bedel küçük, ihlal kazancı belirgindir (Pareto'da "diz" noktası).
**Yorum kuralları.** H1a doğrulanırsa **bu bir başarısızlık değil bulgudur**: MCDM'in katma değeri ayırt edicilikte değil şeffaflık, kontrol ve politika uyumundadır; bedeli ölçtük.
H1a yanlışlanırsa (MCDM daha iyi ayırıyorsa) önce nedeni araştır: sızıntı, çift sayım, referans noktası hatası?

## 5. RQ2 deney tasarımı: ağırlık dayanıklılığı

- **Temel ağırlık** `w0` (D19'dan). **Rastgele ağırlıklar:** `w ~ Dirichlet(α·w0)`; α ∈ {10, 50, 200} (düşük α = geniş belirsizlik), N = 1000 çekim.
- **Eşikler:** (i) çekim başına eşit onay oranı (nicel eşik) → yalnız *yeniden sıralama* etkisi; (ii) `w0` ile kilitli mutlak eşik → ağırlık+ölçek etkisi. İkisi de raporlanır.
- **Karar kararlılık indeksi** `S_i = max_k P(karar_i = k)` (1 = her çekimde aynı karar).
- **Sorular:** (a) S dağılımı nasıl? (b) Düşük-S başvurular eşiğe yakın mı? (c) Düşük-S onaylananların kötü oranı, yüksek-S onaylananlardan farklı mı? (d) Ağırlıklandırma yöntemleri (AHP, eşit, entropi, CRITIC) arasında sıralama uyumu (Kendall τ) ve karar uyumu (Cohen κ).
- **Tasarım önerisi (hipotez):** "Şartlı Onayla" bandı, *ağırlık-hassas (düşük S)* başvurulara karşılık gelsin; bu bandın riski gerçekten daha belirsiz olup olmadığı test edilir.
- **Ek duyarlılık:** Tek tek ağırlığı ±%20 oynatma (OAT; ⚠️ Triantaphyllou & Sánchez 1997).
- **Not:** Düşük S ile yüksek kötü oran arasında ilişki **bulunmayabilir**; bu durumda "S, risk için değil yalnızca karar belirsizliği için bilgi taşır" diye raporlanır.

## 6. RQ3 deney tasarımı: dengesizlik ve kalibrasyon → karar

- **Varyantlar:** yok / `class_weight` / SMOTE / undersampling; her biri ham ve kalibre (isotonic, Platt, prior-shift) olarak. Aynı model ve hiperparametreler.
- **Model düzeyi:** AUC, PR-AUC, Brier, ECE, güvenilirlik eğrisi. **Beklenti (⚠️ literatür):** AUC ≈ sabit; Brier/ECE bozuluyor (Dal Pozzolo ve ark. 2015 ✅).
- **Karar düzeyi:** PD'nin farklı varyantları aynı AHP-TOPSIS'e verilir. Çıktılar: (i) karar değişim oranı (referans = kalibre model), (ii) eşit onay oranında kötü oranı, (iii) **mutlak PD eşikli** politika (ör. "PD > %X ise reddet") altında hatalı onay/ret.
- **İlk kanıt (M4/M6, 2026-11-22, model düzeyi):** XGB'de sınıf ağırlığı AUC'yi ~0,003 değiştirirken ortalama PD'yi ~4,5 kat şişirdi (ECE 0,0025→0,286). Model-düzeyi beklenti doğrulandı; **karar düzeyi** etkisi E3'te (aynı AHP-TOPSIS'e farklı PD varyantları).
- **Hipotez H3:** Sıralamaya dayalı karar (eşit onay oranı) kalibrasyona az duyarlı; **mutlak eşikli** ve **TOPSIS (doğrusal olmayan birleştirme)** kararları duyarlı. Yani AUC'ye göre model seçmek, olasılığı karar girdisi yapan sistemler için yetersiz kalabilir.

## 7. RQ4/RQ5 (ek)

- **RQ4:** n ∈ {100, 1000, 10000} büyüklüğünde rastgele gruplarda batch-TOPSIS C* ile sabit-referans C*'ı karşılaştır; karar uyumu ve rank korelasyonu. (D21)
- **RQ5:** Onay oranı farkı (cinsiyet, yaş bandı), PD-tek vs AHP-TOPSIS; eşit fırsat farkı (⚠️ Hardt ve ark. 2016), AUC maliyeti. (D16)

## 8. Deney protokolü ön-kaydı (şablon: L4'te doldurulacak)

```
Protokol sürümü: v1   Tarih: ____   Commit: ____   Hoca onayı: evet/hayır/tarih
1. Veri ve bölme: (tohum, oranlar, indeks dosyası yolu)
2. PD modeli: (özellik seti, model, dengesizlik stratejisi, kalibrasyon)  ← K-C sonrası kilit
3. Karar katmanı: (kriterler, yönler, AHP yargıları ve CR, referans noktaları, hedef onay oranları)  ← K-D sonrası kilit
4. RQ1..RQ3: hipotez, birincil/ikincil metrik, istatistik, yorum kuralı
5. Analiz kapsamı: hangi alt analizler "doğrulayıcı", hangileri "keşifsel" (etiketlenecek)
6. Durdurma/değişiklik kuralı: sapma → §10'a kayıt
```

Neden ön-kayıt? Sonuçları gördükten sonra hipotez veya metrik değiştirmek (p-hacking) savunmada en kolay yıkılan noktadır.
Ön-kayıt, "bu soruları sonuçları görmeden sorduk" diyebilmektir.

## 9. Sistematik literatür tarama protokolü (L1, öğrenci yapar)

- **Veritabanları:** Google Scholar, Scopus/Web of Science (üniversite erişimi/VPN), IEEE Xplore, ScienceDirect, SpringerLink, DergiPark (Türkçe), arXiv (preprint, ayrı işaretle).
- **Başlangıç dizgileri** (İngilizce; varyantları dene, her sorgu ve sonuç sayısını kaydet):
  - `("credit scoring" OR "credit risk" OR "loan approval") AND (TOPSIS OR AHP) AND ("machine learning" OR "probability of default")`
  - `("probability of default" AND TOPSIS)`; `("decision support" AND "credit" AND AHP AND XGBoost)`
  - `("weight sensitivity" OR "robustness") AND MCDM AND credit`
  - `("Home Credit Default Risk")`
  - `calibration AND "class imbalance" AND "credit scoring"`; `"rank reversal" AND TOPSIS`
  - Türkçe: `"kredi risk" AND TOPSIS`, `"kredi skorlama" AND "AHP"`, `"makine öğrenmesi" AND "çok kriterli karar"`
- **Dahil etme:** hakemli (ya da etiketli preprint), kredi/borç riski + MCDM ya da ML-PD kesişimi; **dışlama:** yalnızca model sıralaması (not et, bağlam kaynağı olarak tut).
- **Kayıt tablosu (`docs/05`'e):** tarih · veritabanı · dizgi · sonuç sayısı · taranan · seçilen · gerekçe.
- **Karar kuralı:** İlk 100 sonucun başlık/özet taraması + atıf zinciri (ileri/geri). Boşluk iddiası için "bulamadık" yerine "[tarih, veritabanları, dizgiler] ile taradığımız kayıtlarda ... rastlamadık" yaz.

## 10. Protokol sapmaları günlüğü

| Tarih | Sapma | Neden | Etkisi |
|---|---|---|---|
| | | | |

## 11. Katkı iddiası cümle şablonları (dikkatli)

- ✅ "Taradığımız çalışmalarda (Ek A: arama kaydı), ML tabanlı PD'yi AHP-TOPSIS kriteri olarak kullanıp, gerçek temerrüt etiketleriyle PD-tek eşiklemeye karşı eşit onay oranında doğrulayan bir çalışmaya rastlamadık."
- ✅ "Sonuçlarımız, politika kriterlerini eklemenin kötü oranında X puanlık (%95 GA: ...) bir bedeli olduğunu ve politika ihlalini Y oranında azalttığını gösteriyor."
- ❌ "İlk kez ..." / "Literatürde bir ilk ..." / "Üstün" / "Devrim niteliğinde".
- ✅ Sınırlılıklar: tek veri seti, booked popülasyon, zaman bazlı doğrulama yok, AHP yargıları sınırlı sayıda kişiden, maliyet varsayımları.

## 12. Çıktılar

1. Rapor: **Katkılar** ve **Sınırlılıklar** bölümleri (ayrı, açık).
2. Açık kaynak, tekrarlanabilir GitHub deposu (deney betikleri, ön-kayıt commit'i, sonuç CSV'leri; veri hariç).
3. (Opsiyonel; **hocayla konuş**) Kısa bildiri/öğrenci sempozyumu özeti. Hangi mecra uygun olduğunu hoca ve tez danışmanı bilir; burada mecra adı uydurmuyoruz.

## 13. Riskler

| Risk | Önlem |
|---|---|
| Sonuçlar "sıkıcı" çıkar (fark yok) | Sıfır sonuç da bulgudur; güven aralığıyla raporla, "farkı tespit edemedik (GA: ...)" |
| Zaman yetmez | Çekirdek (RQ1) tamamlanmadan RQ2/RQ3'e geçme; RQ3 dar tutulabilir (yalnız XGBoost, 3 varyant) |
| AHP yargıcı bulunamaz | Literatür temelli ağırlık + RQ2 geniş duyarlılık; sınırlılık olarak yaz |
| Boşluk iddiası çürür (benzer çalışma bulunur) | **Kısmen gerçekleşti (L1, 2026-11-20):** MCDM-başvuran mevcut (Ignatius 2018, Roy & Shaw). İddia **daraltıldı**: ML-PD kriteri + büyük gerçek veri + PD-tek baseline + kalibrasyon. Bulunanlar yakın kaynak olarak ele alınıyor |
| Sızıntı ya da hata iyi sonucu üretir | Beklenmedik derecede iyi sonuçta önce hata ara (`docs/07` §4) |
| Hoca beklentisi daha geniş | §3 sorusu (`docs/01` §6) ile erkenden netleştir |

## 14. Hocaya sorulacak netleştirme soruları (kopyala)

1. "Literatüre katkı" için hangi düzey bekleniyor: yeni yöntem mi, yeni karşılaştırmalı analiz mi, yeni uygulama bağlamı mı?
2. Ders sonunda yayın/bildiri hedefi var mı, yoksa rapor içinde bir "katkı" bölümü yeterli mi?
3. AHP yargıları için dış uzman (bankacı) kullanmak uygun mu? Öğrenci yargıları yeterli kabul edilir mi?
4. Önerdiğimiz karşılaştırma (PD-tek vs AHP-TOPSIS, ağırlık dayanıklılığı, kalibrasyon) yeterli katkı çerçevesi mi?
