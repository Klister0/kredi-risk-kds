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
İskelet: ≈%8 pozitifte "herkes öder" ≈%92 doğruluk; AUC/PR-AUC/KS/Brier (D11). `[KANIT: kendi sınıf oranı, dummy model]`

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
İskelet: Tüm dönüşümler `Pipeline` içinde, yalnız eğitime fit; SMOTE/kalibrasyon yalnız CV/OOF içinde; test kilit noktalarda açıldı (K-B/K-C); sızıntı testi. Bölme EDA'dan önce yapıldı (D33), indeksler commit'li. `[KANIT: boru hattı testi; data/processed/bolme/ commit'i]`

**S9. Ek tabloları neden bu şekilde toplulaştırdınız? Başka özellik olabilirdi.** ⬜
İskelet: Sayı/oran/maksimum özetleri, "kayıt yok" ≠ 0 (F3). Alternatif: zaman pencereli özellikler, daha fazla agregasyon; zaman kısıtı.

**S10. `EXT_SOURCE` değişkenleri ne? Çıkarsanız ne olur?** ⬜
İskelet: Dış kaynaklı normalize skorlar, en güçlü sinyaller (D17). `ext-siz` sürüm sonucu. `[KANIT]`

**S11. Cinsiyet ve yaş modelde mi? Adil mi?** ⬜
İskelet: D16: cinsiyet dışlandı/test edildi; yaş için adalet analizi. Hukuki çerçeve tartışması. `[KANIT: AUC maliyeti]`

## C. Modelleme

**S12. Neden bu üç model? LightGBM/CatBoost/sinir ağı neden değil?** ⬜
İskelet: D09: baseline + bagging + boosting; LightGBM ≈ XGBoost beklenir; tabular veride ağaçlar güçlü. Duyarlılık olarak eklenebilir.

**S13. AUC'niz 0,7x. Düşük değil mi?** ⬜
İskelet: Bu veri setinde literatürde ≈0,76–0,80 aralığı (bir doğrulanmış gösterge: LightGBM ≈0,79, `docs/05` §2); kredi riskinde AUC 0,9 şüphelidir (sızıntı). Hedef modelin mutlak skoru değil karar katmanının incelenmesi.

**S14. Hiperparametreleri nasıl seçtiniz? Aşırı uyum yok mu?** ⬜
İskelet: Rastgele arama, eşit bütçe, CV, test kilitli (D10). `[KANIT: CV-test farkı]`

**S15. Modeller arasındaki fark istatistiksel olarak anlamlı mı?** ⬜
İskelet: Bootstrap GA + eşleştirilmiş fark; Friedman/Nemenyi tek veri setinde uygulanamaz (D14). `[KANIT: GA'lar]`

**S16. Sınıf dengesizliği için ne yaptınız? SMOTE neden/neden değil?** ⬜
İskelet: D08, RQ3: ağırlıklandırma/SMOTE/undersampling karşılaştırması; AUC'yi koruyup kalibrasyonu bozar (Dal Pozzolo 2015 ✅). `[KANIT: Brier/ECE tablosu]`

**S17. Olasılıklarınız kalibre mi? Neden önemli?** ⬜
İskelet: TOPSIS PD'nin değerini kullanır; mutlak eşikli politikalar da. Güvenilirlik eğrisi + Brier/ECE (D13). `[KANIT: eğri]`

**S18. F1 eşiğini nasıl seçtiniz?** ⬜
İskelet: Test üzerinde seçilmedi; eğitim OOF'unda, maliyet senaryolarıyla (D12). `[KANIT]`

**S19. Modeliniz hangi özelliklere bakıyor? Neden güvenmeliyiz?** ⬜
İskelet: Önem + SHAP (D15); LR katsayılarıyla tutarlılık; SHAP nedensellik değildir, korele özelliklerde kararsızlık (Rudin 2019 ⚠️: yorumlanabilir model tartışması).

## D. Karar katmanı

**S20. Neden AHP? Eşit ağırlık ya da entropi neden olmasın?** ⬜
İskelet: Politika önceliklerini yansıtır (karar verici müdahalesi); entropi/CRITIC veriden gelir ama politikayı bilmez. RQ2 ile karşılaştırdık (D19). `[KANIT: τ/κ]`

**S21. AHP ikili karşılaştırmalarını kim yaptı? Banka uzmanı mıydı?** ⬜
İskelet: Dürüst cevap: yargıçlar `[... ]`, CR `[...]`, geometrik ortalama; uzman olmayan yargı sınırlılık; bu yüzden ağırlık duyarlılığını (RQ2) ana deney yaptık. Uydurma "uzman" yok.

**S22. Neden TOPSIS? VIKOR/PROMETHEE/SAW olsaydı?** ⬜
İskelet: D20: bağımsız başvuru puanı, sezgisel. Alternatifler farklı telafi varsayımları; "ek" duyarlılık karşılaştırması `[KANIT, varsa]`.

**S23. TOPSIS'te rank reversal sorunu yok mu? Tek başvuruda nasıl çalışıyor?** ⬜
İskelet: Eğitimden **sabit** ideal/anti-ideal; García-Cascales & Lamata 2012 ✅; batch'e karşı fark RQ4 (D21).

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

- "Test setine kaç kez baktınız?" → Sayıyı bil: `GELISTIRME_GUNLUGU.md`'de kayıtlı olmalı (hedef: final değerlendirmede tek sefer).
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
