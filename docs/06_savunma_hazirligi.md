# 06 · Savunma Hazırlığı

Hoca her şeyi soracak. Bu dosya canlı bir belgedir: **her adım sonunda** ilgili soruların cevabı öğrenciyle birlikte
doldurulur. Cevap iskeletleri başlangıçtır; **`[KANIT]` yerine gerçek sonuç yazılmadan cevap hazır sayılmaz.**

**Cevap formatı (her soruda):** (1) tek cümlelik cevap, (2) gerekçe, (3) alternatif ve neden seçmedik, (4) kanıt/şekil, (5) dürüst sınırlılık.
**Altın kural:** Bilmediğini kabul et, sınırı söyle, nasıl test edeceğini anlat. "Bilmiyorum, ama şöyle test ederdim" iyi cevaptır; uydurmak değildir.

Hazırlık durumu: ⬜ boş · 🟨 iskelet · ✅ öğrenci kendi kelimeleriyle ve kanıtla cevapladı

---

## A. Problem ve veri

**S1. Neden kredi riski? Neden bu veri seti?** ⬜
İskelet: Büyük ölçek, çok tablolu ilişkisel yapı, gerçek kurum verisi (D01). Alternatif: German Credit (küçük, 1000 satır). Sınırlılık: tek veri seti.

**S2. "Temerrüt" dediğiniz şey tam olarak ne?** ⬜
İskelet: `TARGET` resmî temerrüt değil, ilk taksitlerde belirli gün üzeri gecikme (ödeme güçlüğü) tanımı (`docs/07` §3; sözlük dosyasından teyit et). Raporda "temerrüt/ödeme güçlüğü".

**S3. Veride sınıf dengesizliği var; doğruluk neden kullanmadınız?** ⬜
İskelet: ≈%8 pozitifte "herkes öder" ≈%92 doğruluk; AUC/PR-AUC/KS/Brier (D11). Dummy (stratified) CV ROC-AUC ≈0,50, PR-AUC ≈0,08 (taban oran) → baseline anlamsızlığı gösterildi. `[KANIT: m1_baseline json; TARGET %8,07]`

**S4. Veri kimlerden oluşuyor? Reddedilenler yok mu?** ⬜
İskelet: Kredisi verilmiş (booked) başvuruların sonuçları; reject inference yapmadık (D29). Sonuçlar bu popülasyon için. Sınırlılık olarak yazılı.

**S5. Zaman bazlı değerlendirme neden yok?** ⬜
İskelet: Başvuru tarihi veride yok; rastgele katmanlı bölme (D03). Sınırlılık: dağılım kayması ölçülemedi.

## B. Veri hazırlama

**S5b. Bölmeyi nasıl yaptınız? Neden kimlikle sakladınız, katmanlama gerekli miydi?** 🟨
İskelet: `src/bolme.py` katmanlı holdout (sıfırdan, sklearn ile doğrulandı); `SK_ID_CURR` sabit kimlik, satır sırası kırılgan;
katmanlama 61 bin satırlık holdout'ta kozmetik ama 5 katlı CV'de gerçekten gerekli (küçük katlarda azınlık oranı sapar).
Bölme bir kez yapıldı, indeksler commit'lendi (tohum 42). `[KANIT: test_bolme.py 7/7; bolme_meta.json]`
*(Öğrenci kendi kelimeleriyle yazacak → ✅)*

**S6. `DAYS_EMPLOYED = 365243` ile ne yaptınız, neden?** ⬜
İskelet: NaN + bayrak (D05). Alternatifler: sil, medyanla doldur. `[KANIT: anomali oranı, gruba göre temerrüt oranı]`

**S7. Eksik değerleri neden böyle doldurdunuz? MICE neden değil?** ⬜
İskelet: D04. Eksikliğin kendisi bilgi taşıyor; XGB yerel NaN; maliyet. `[KANIT: strateji karşılaştırması]`

**S8. Veri sızıntısı olmadığını nasıl biliyorsunuz?** ⬜
İskelet: Tüm dönüşümler `Pipeline` içinde, yalnız eğitime fit; SMOTE/kalibrasyon yalnız CV/OOF içinde; test kilit noktalarda açıldı (K-B/K-C); sızıntı testi. Bölme EDA'dan önce yapıldı (D33), indeksler commit'li. Boru hattı `src/boru_hatti.py`: imputer/scaler/encoder yalnız fit'te öğrenir; `test_boru_hatti.py::test_sizinti_imputer_egitimden` imputer istatistiğinin **eğitim medyanı** olduğunu sayısal kanıtlar. `[KANIT: sızıntı testi yeşil; data/processed/bolme/ commit'i]`

**S9. Ek tabloları neden bu şekilde toplulaştırdınız? Başka özellik olabilirdi.** ⬜
İskelet: Sayı/oran/maksimum özetleri, "kayıt yok" ≠ 0 (F3). Alternatif: zaman pencereli özellikler, daha fazla agregasyon; zaman kısıtı.

**S10. `EXT_SOURCE` değişkenleri ne? Çıkarsanız ne olur?** ⬜
İskelet: Dış kaynaklı normalize skorlar, en güçlü sinyaller (D17). `ext-siz` sürüm sonucu. `[KANIT]`

**S11. Cinsiyet ve yaş modelde mi? Adil mi?** ⬜
İskelet: D16: cinsiyet dışlandı/test edildi; yaş için adalet analizi. Hukuki çerçeve tartışması. `[KANIT: AUC maliyeti]`

## C. Modelleme

**S12. Neden bu üç model? LightGBM/CatBoost/sinir ağı neden değil?** ⬜
İskelet: D09: baseline + bagging + boosting; LightGBM ≈ XGBoost beklenir; tabular veride ağaçlar güçlü. **Sonuç:** XGB 0,769 > LR 0,753 > RF 0,749 (CV). RF'nin LR'yi geçememesi dürüstçe raporlanır; M5'te eşit bütçeli aramadan sonra da sonuç aynı (RF 0,750 < LR 0,753) → bu özellik setinde bagging'in doğrusal modele üstünlüğü yok. XGB ayarlı 0,770 (seçilen). `[KANIT: deneyler/m2_m3_*_tam.json]`

**S13. AUC'niz 0,7x. Düşük değil mi?** ⬜
İskelet: Bu veri setinde literatürde ≈0,76–0,80 aralığı (LightGBM ≈0,79, `docs/05` §2); kredi riskinde AUC 0,9 şüphelidir (sızıntı). **Bizim M1 LR CV AUC = 0,753 ± 0,002** (temel+büro), beklenen aralıkta → sağlama tuttu. **Test (M7): XGB 0,777 [0,770–0,784], Gini 0,554, KS 0,417.** Hedef modelin mutlak skoru değil karar katmanı. `[KANIT: deneyler/m1_baseline_*_tam.json]`

**S14. Hiperparametreleri nasıl seçtiniz? Aşırı uyum yok mu?** ⬜
İskelet: Rastgele arama, eşit bütçe, CV, test kilitli (D10). Aşırı uyum göstergesi eğitim-CV farkı: XGB ayarsız 0,10 → ayarlı 0,06 (L2, min_child_weight, düşük öğrenme hızı). Seçim kuralı aramadan ÖNCE commit'lendi. `[KANIT: CV-test farkı M7]`

**S15. Modeller arasındaki fark istatistiksel olarak anlamlı mı?** ⬜
İskelet: Eşleştirilmiş bootstrap (B=1000; her yeniden örneklemde aynı başvurular üç modele) → XGB−LR AUC +0,019 [+0,017; +0,022], XGB−RF +0,021 [+0,018; +0,024]: GA'lar 0'ı içermiyor → fark anlamlı. Friedman/Nemenyi tek veri setinde uygulanamaz (D14). LR ile RF arasında fark yok. `[KANIT: deneyler/m7_test_sonuc.json]`

**S16. Sınıf dengesizliği için ne yaptınız? SMOTE neden/neden değil?** ⬜
İskelet: D08, RQ3. Ölçtük: `scale_pos_weight` AUC 0,769→0,766 (≈aynı), ortalama PD 0,08→0,37, ECE 0,003→0,286. Yani ağırlık sıralamayı korudu, olasılığı bozdu (Dal Pozzolo 2015 ✅). TOPSIS değeri kullandığı için ağırlıksız model seçildi. SMOTE kapsam dışı (D31). `[KANIT: m4_m6 json, şekil 04]`

**S17. Olasılıklarınız kalibre mi? Neden önemli?** ⬜
İskelet: TOPSIS PD'nin değerini kullanır; mutlak eşikli politikalar da. Ağırlıksız XGB OOF'ta ECE 0,0025 (ort. tahmin 0,080, gözlenen 0,081) → kalibre. Kural ön-belirlendi: ECE<0,01 ise ham, değilse isotonic (D13). `[KANIT: şekil 04_guvenilirlik_egrisi.png]`

**S18. F1 eşiğini nasıl seçtiniz?** ⬜
İskelet: Test üzerinde seçilmedi; eğitim OOF'unda, maliyet senaryolarıyla (D12). `[KANIT]`

**S19. Modeliniz hangi özelliklere bakıyor? Neden güvenmeliyiz?** ⬜
İskelet: Önem + SHAP (D15); LR katsayılarıyla tutarlılık; SHAP nedensellik değildir, korele özelliklerde kararsızlık (Rudin 2019 ⚠️: yorumlanabilir model tartışması).

## D. Karar katmanı

**S20. Neden AHP? Eşit ağırlık ya da entropi neden olmasın?** ⬜
İskelet: Politika önceliklerini yansıtır (karar verici müdahalesi); entropi/CRITIC veriden gelir ama politikayı bilmez. RQ2 ile karşılaştırdık (D19). `[KANIT: τ/κ]`

**S20b. AHP ağırlığı nasıl hesaplanıyor? CR ne demek?** 🟨
İskelet: İkili karşılaştırma matrisinin en büyük özdeğerine ait özvektör = ağırlıklar (kuvvet yinelemesiyle hesapladık, numpy ile doğruladık). Tam tutarlı yargıda a_ij = w_i/w_j ve λmax = n olur; tutarsızlık λmax'ı n'nin üstüne çıkarır. CI = (λmax−n)/(n−1); CR = CI/RI, RI rastgele doldurulmuş matrislerin ortalama CI'sı (n=6 → 1,24). CR < 0,10 → yargılar rastgeleye göre yeterince tutarlı. `[KANIT: test_ahp.py]`

**S21. AHP ikili karşılaştırmalarını kim yaptı? Banka uzmanı mıydı?** ⬜
İskelet: Dürüst cevap: yargıçlar `[... ]`, CR `[...]`, geometrik ortalama; uzman olmayan yargı sınırlılık; bu yüzden ağırlık duyarlılığını (RQ2) ana deney yaptık. Uydurma "uzman" yok.

**S22. Neden TOPSIS? VIKOR/PROMETHEE/SAW olsaydı?** ⬜
İskelet: D20: bağımsız başvuru puanı, sezgisel. Alternatifler farklı telafi varsayımları; "ek" duyarlılık karşılaştırması `[KANIT, varsa]`.

**S23. TOPSIS'te rank reversal sorunu yok mu? Tek başvuruda nasıl çalışıyor?** ⬜
İskelet: Eğitimden **sabit** ideal/anti-ideal; García-Cascales & Lamata 2012 ✅; batch'e karşı fark RQ4 (D21). Testle gösterdik: klasik TOPSIS'te kümeye aşırı iyi bir alternatif eklenince diğerlerinin puanı değişiyor; sabit referansta bir başvurunun puanı yanında kim olursa olsun aynı. Tek başvuru (dashboard) böylece tanımlı. Kodu pymcdm ile çapraz doğruladık. `[KANIT: test_topsis.py]`

**S24. PD zaten gelir, kredi/gelir vb. özellikleri kullanıyor; aynı bilgiyi ikinci kez saymıyor musunuz?** ⬜
İskelet: Evet, risk. Gerekçe: PD "istatistik", kriterler "politika". Ablation: politika-kör PD; nominal-etkin ağırlık analizi (D18). **Bu savunmanın en önemli sorusudur.** `[KANIT]`

**S25. Eşikleri nasıl belirlediniz? Bu eşikler keyfî değil mi?** ⬜
İskelet: Hedef onay oranından, eğitim OOF'unda (D22); dashboard'da ayarlanabilir. Keyfîlik: hedef onay oranı politika kararıdır, biz sabitlemedik, eğri raporladık.

**S26. Karar katmanının işe yaradığını nasıl kanıtlıyorsunuz? PD zaten etiketle ilişkili, bu döngüsel değil mi?** ⬜
İskelet: Döngüselliği biz de gördük; bu yüzden PD-tek baseline ve **eşit onay oranında** karşılaştırma (D23). Bedel ve politika kazancı ölçüldü. `[KANIT: RQ1 eğrisi]`

**S27. "Şartlı Onayla" ne demek? Nasıl belirlendi?** ⬜
İskelet: Bant tanımı (D22); varsa ağırlık-hassas başvurular (RQ2). `[KANIT: S ile kötü oran ilişkisi, bulunamadıysa söyle]`

**S28. Karar verici ağırlıkları değiştirirse ne olur? Güvenilir mi?** ⬜
İskelet: Dirichlet MC, karar kararlılık indeksi, flip oranı (RQ2). Dashboard'da karar belirsizliği gösterimi (varsa).

## E. Katkı ve genel

**S29. Literatüre katkınız nedir?** ⬜
İskelet (`docs/04` §11): "AHP/TOPSIS'i kredi başvurusuna uygulamak literatürde **var** (Ignatius ve ark. 2018 bulanık AHP-TOPSIS; Roy & Shaw 2021/2022 BWM/fuzzy-TOPSIS). Bizim farkımız ve [tarih/dizgi] ile taradığımız kayıtlarda rastlamadığımız: **eğitilmiş bir ML temerrüt olasılığını** TOPSIS kriteri yapıp **büyük gerçek veride gerçek etiketle**, **PD-tek baseline'a karşı eşit onay oranında** bedelini ve ağırlık dayanıklılığını ölçmek." **"İlk" deme.** Sınırlılıklar: tek veri seti, booked popülasyon, ön tarama (tam tarama öğrenci tarafından).

**S30. Bu sonuçlar gerçek bankada geçerli olur mu?** ⬜
İskelet: Hayır, iddia etmiyoruz; akademik prototip, tek veri seti, zaman doğrulaması yok, reject inference yok, adalet/yasal gereksinimler eksik.

**S31. Sonuç beklediğinizden farklı çıktı mı? Hipoteziniz yanlış çıktıysa?** ⬜
İskelet: Ön-kayıt var (K-A); sapmalar kayıtlı (`docs/04` §10); negatif sonuç da bulgu.

**S32. Sistemi neden Streamlit ile yaptınız?** ⬜
İskelet: D24 (hızlı prototip). Üretim için FastAPI+React; kapsam dışı.

**S33. Çalışma tekrarlanabilir mi?** ⬜
İskelet: Tohum, kayıtlı bölme, `requirements.txt`, deney CSV'leri, temiz klon testi (R4).

**S34. Etik/yasal: otomatik karar, açıklanabilirlik, ayrımcılık?** ⬜
İskelet: İnsan-karar-verici merkezli KDS (otomatik karar değil, öneri); açıklama (SHAP); adalet analizi (RQ5, varsa); yasal çerçeve doğrulanmadan iddia yok (`docs/05` §4).

**S35. Bu projede en çok neyi öğrendiniz, ne yapardınız farklı?** ⬜
İskelet: Öğrenci kendi cümleleriyle (adım günlüğünden). Gerçek, kişisel, somut örnek.

## F. Tuzak ve zorlayıcı sorular

- "Test setine kaç kez baktınız?" → Bölmede kimlik ataması (K-B, özelliklere bakılmadı) + M7'de bir kez (K-C, betikte ikinci açılışı engelleyen kilit dosyası var). E1/E2 ön-kayıtlı son analizler. Sayaç: `GELISTIRME_GUNLUGU.md`.
- "AUC farkı 0,002; neden XGBoost?" → GA'lara bak; fark anlamsızsa dürüstçe söyle ve yorumlanabilirlik/maliyet gibi ikincil kriterlere dayan.
- "SHAP yanlış olabilir mi?" → Evet: korele özelliklerde, bağımlılık varsayımlarında; nedensellik iddia etmiyoruz.
- "Ağırlıkları değiştirince karar değişiyorsa sistem güvenilmez" → Bu RQ2: değişimin boyutu ölçüldü; kararsız başvurular işaretleniyor (varsa).
- "Neden PD'yi doğrudan eşiklemiyorsunuz? MCDM gereksiz" → RQ1 tam bu: bedeli ölçtük; MCDM'in değeri şeffaflık, politika uyumu ve kontrol; ayırt edicilik değil.
- "Bu kod senin mi?" → Öğrenci kendi yazdığı bölümleri (AHP, TOPSIS, bölme, bootstrap) ekranda açıklayabilmeli; bu yüzden "sıfırdan yaz" kuralı (`CLAUDE.md` §3).

## G. Savunma provası protokolü (R3)

1. Claude "hoca" rolüne geçer; yukarıdan **rastgele sırayla**, öğrenci kaynağa bakmadan cevaplar.
2. Her cevap 1-4 puan (1: bilmiyor, 4: kanıtla savunuyor). 3'ün altı olanlar ilgili adıma geri dönülüp güçlendirilir.
3. Sürpriz soru: projede yer almayan bir alternatif yöntem sor ("ya LightGBM kullansaydınız?"); amaç "bilmiyorum ama şöyle test ederdim" refleksi.
4. Son prova: 10 dakikalık sunum + 10 dakikalık soru-cevap, süre tutarak.
