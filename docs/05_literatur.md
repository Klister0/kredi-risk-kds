# 05 · Literatür

**İşaretler**
- ✅ **Doğrulandı:** Bu paket hazırlanırken (2026-11-15) web aramasıyla künye (başlık, dergi, cilt, sayfa/DOI) yayıncı, dizin ya da kütüphane kaydında görüldü.
- ◐ **Kısmen:** Varlığı görüldü, künyenin bir kısmı (yazar sırası, sayı, sayfa) teyit bekliyor.
- ⚠️ **Hafızadan:** Bilinen bir kaynak ama bu oturumda doğrulanmadı. **Rapora almadan önce DOI/yayıncı sayfasıyla doğrula.** Doğrulayamazsan alma.

Açıklamalar bu dosyada **kendi cümlelerimizle** yazılmıştır; kaynaktan metin kopyalanmamalıdır.
Atıf biçimi (APA 7 mi IEEE mi) hocaya sorulacak; künyeler bu yüzden alan alan yazıldı. Önerilen araç: Zotero + BibTeX.

> Kural: Bu dosyada yazan bir bilgi "okudum" anlamına gelmez. Bir kaynağı **okumadan** bulgusunu yazma; okunduğunda §5'teki nota işle.

---

## 1. Doğrulanmış kaynaklar (✅)

**[L-01] Lessmann, S., Baesens, B., Seow, H.-V., & Thomas, L. C. (2015).** Benchmarking state-of-the-art classification algorithms for credit scoring: An update of research.
*European Journal of Operational Research, 247*(1), 124–136. https://doi.org/10.1016/j.ejor.2015.05.030
*Ne yapıyor:* Sekiz gerçek kredi skorlama veri setinde 41 sınıflandırıcıyı karşılaştırıyor; topluluk yöntemlerinin güçlü olduğunu gösteriyor, altı farklı doğruluk göstergesini ve skor kartlarının finansal etkisini inceliyor.
*Projede:* Metrik seçimi (D11), model seçimi gerekçesi (D09), "sadece doğruluk değil" savunması.

**[L-02] Dastile, X., Celik, T., & Potsane, M. (2020).** Statistical and machine learning models in credit scoring: A systematic literature survey.
*Applied Soft Computing, 91*, 106263. https://doi.org/10.1016/j.asoc.2020.106263
*Ne yapıyor:* 2010–2018 arası 74 çalışmanın sistematik taraması; topluluk sınıflandırıcıların tekil modellerden iyi çıkma eğilimini ve iki büyük sorunu (modellerin açıklanamazlığı, dengesiz veri) öne çıkarıyor.
*Projede:* Literatür bölümü omurgası; SHAP ve dengesizlik kararlarının (D08, D15) arka planı.

**[L-03] García-Cascales, M. S., & Lamata, M. T. (2012).** On rank reversal and TOPSIS method.
*Mathematical and Computer Modelling, 56*(5–6), 123–132. https://doi.org/10.1016/j.mcm.2011.12.022
*Ne yapıyor:* TOPSIS'te yeni alternatif eklenince sıralamanın değişmesini (rank reversal) inceliyor ve algoritma için düzeltmeler öneriyor.
*Projede:* D21 (sabit referans noktası), RQ4. *(Not: dergi adı ilk hatırlamada yanlıştı, arama ile düzeltildi; bu, "hafızadan yazma" riskinin örneği.)*

**[L-04] Dal Pozzolo, A., Caelen, O., Johnson, R. A., & Bontempi, G. (2015).** Calibrating probability with undersampling for unbalanced classification.
*2015 IEEE Symposium Series on Computational Intelligence (SSCI)*, 159–166. https://doi.org/10.1109/SSCI.2015.33
*Ne yapıyor:* Undersampling'in sıralamayı korurken olasılık tahminlerini ve sınıflandırma eşiğini nasıl çarpıttığını analitik ve deneysel olarak gösteriyor; düzeltme yolunu veriyor.
*Projede:* **RQ3'ün teorik dayanağı**, D08/D13.

**[L-05] Roy, P. K., & Shaw, K. (2023).** A credit scoring model for SMEs using AHP and TOPSIS.
*International Journal of Finance & Economics, 28*(1), 372–391. https://doi.org/10.1002/ijfe.2425
*Ne yapıyor:* KOBİ kredi skorlaması için kriterleri literatür ve uzman görüşünden belirleyip AHP ile ağırlıklandırıyor, TOPSIS ile skor üretiyor.
*Projede:* En yakın "AHP-TOPSIS kredi" referansı; farkımız: ML-PD, büyük veri, gerçek etiketle doğrulama (§3).

**[L-06] ✅ Roy, P. K., & Shaw, K. (2021).** A multicriteria credit scoring model for SMEs using hybrid BWM and TOPSIS.
*Financial Innovation, 7*, 77. https://doi.org/10.1186/s40854-021-00295-5
*Ne yapıyor:* En iyi-en kötü yöntemiyle (BWM) ağırlıkları, TOPSIS ile skoru üretiyor; ağırlık duyarlılık analizi yapıyor.
*Projede:* D19 (BWM alternatifi), RQ2'nin yakın öncülü: onlar ağırlık duyarlılığına bakıyor, biz **karar kararlılığı ve PD baseline** ile genişletiyoruz. *(✅ 2026-11-20: Financial Innovation 7(1), Art. 77, s. 1–27, DOI yayıncı + DOAJ + RePEc ile doğrulandı; yazarlar Pranith Kumar Roy & Krishnendu Shaw.)*

**[L-07] Kou, G., Peng, Y., & Lu, C. (2014).** MCDM approach to evaluating bank loan default models.
*Technological and Economic Development of Economy, 20*(2), 292–311. https://doi.org/10.3846/20294913.2014.913275
*Ne yapıyor:* TOPSIS'i, banka kredisi temerrüt **modellerini** birden çok performans metriğine göre sıralamak için kullanıyor.
*Projede:* "MCDM'in kredide farklı kullanımı" ayrımı (§3); bizim kullanımımız *başvuruları* sıralamak.

**[L-08] Oral, N., & Engin, O. (2024).** Ticari kredilerde bulanık-AHP ve TOPSIS yardımıyla risk analizi.
*Harran Üniversitesi Mühendislik Dergisi, 9*(1), 22–38.
*Ne yapıyor:* On firma için bulanık AHP ve TOPSIS ile ticari kredi riski analizi yapıyor (Türkçe literatür).
*Projede:* Türkçe kaynak olarak ilgili çalışmalar bölümü.

**[L-09] Baesens, B., Van Gestel, T., Viaene, S., Stepanova, M., Suykens, J., & Vanthienen, J. (2003).** Benchmarking state-of-the-art classification algorithms for credit scoring.
*Journal of the Operational Research Society, 54*(6), 627–635.
*(Künye, L-01'in kaynakçasından doğrulandı.)* Kredi skorlamada klasik karşılaştırma çalışması; L-01 bunu günceller.

**[L-10] ◐ Thomas, L. C. (2000).** A survey of credit and behavioural scoring: forecasting financial risk of lending to consumers.
*International Journal of Forecasting, 16*(2), 149–172. https://doi.org/10.1016/S0169-2070(00)00034-0
*(DOI ve ilk sayfa doğrulandı; sayı ve son sayfa teyit edilsin.)* Tüketici kredisi skorlamasının klasik derlemesi.

**[L-11] ◐ Louzada, F., Ara, A., & Fernandes, G. B. (2016).** Classification methods applied to credit scoring: Systematic review and overall comparison.
*Surveys in Operations Research and Management Science, 21*(2), 117–134.
*(Dergi, cilt ve ilk sayfa doğrulandı; yazar sırası, sayı ve son sayfa teyit edilsin.)*

**[L-12] ◐ Hwang, C.-L., & Yoon, K. (1981).** *Multiple Attribute Decision Making: Methods and Applications.* Springer.
*(Varlığı L-03'ün kaynakçasında görüldü; yayıncı/yıl teyit edilsin.)* TOPSIS'in orijinal kaynağı.

**[L-13] ◐** *Machine learning-driven credit risk: a systemic review.* *Neural Computing and Applications, 34*(17), 14327–14339 (2022).
*(Dergi, cilt, sayı, sayfa ve yıl görüldü; **yazarlar ve DOI teyit edilsin**.)* 76 çalışmanın taraması; topluluk yöntemleri, dengesiz veri ve şeffaflık sorunları.

**[L-14] Ignatius, J., Hatami-Marbini, A., Rahman, A., Dhamotharan, L., & Khoshnevis, P. (2018).** A fuzzy decision support system for credit scoring.
*Neural Computing and Applications, 29*(10), 921–941. https://doi.org/10.1007/s00521-016-2592-1  (✅ 2026-11-20: NCAA 29(10), DOI yayıncı sayfasından; sayfa aralığı teyit edilebilir ~921–941)
*Ne yapıyor:* Kriter ağırlıklarını **bulanık AHP** ile üretip TOPSIS'le başvuranları risk uzaklığına göre sıralayan bir KDS kuruyor (FICO bağlamı), duyarlılık analizi dahil.
*Projede:* **En yakın çalışma.** AHP-TOPSIS'i model sıralamaya değil **başvuranlara** uyguluyor → "biz başvuranları sıralıyoruz" ayrımı artık tek başına katkı değil. Farkımız: ML tabanlı PD'yi kriter yapmak, büyük gerçek veri + gerçek temerrüt etiketi, PD-tek baseline, kalibrasyon. Katkı buna göre daraltıldı (`docs/04` §3, §13).

**[L-15] Roy, P. K., & Shaw, K. (2022).** An integrated fuzzy credit rating model using fuzzy-BWM and new fuzzy-TOPSIS-Sort-C.
*Complex & Intelligent Systems, 8*(4), 3581–3600. https://doi.org/10.1007/s40747-022-00823-5  (✅ 2026-11-20)
*Ne yapıyor:* Bulanık-BWM ağırlık + fuzzy-TOPSIS-Sort-C ile firmaları sınıflandırıyor; TOPSIS-Sort'un rank reversal'ı ele aldığını belirtiyor; sonuçları ticari derecelerle karşılaştırıyor.
*Projede:* MCDM-kredi ailesinin güncel hâli; rank reversal (D21) ve sınıflandırma bandı tartışmasına yakın.

## 2. Yakın çalışmalar, künyesi eksik (⚠️/◐): bağlam kaynağı olarak tut, eksik alanları tamamla

| Kısa ad | Gördüğümüz | Eksik |
|---|---|---|
| García, Sánchez, Marqués, "Synergetic Application of Multi-Criteria Decision-Making Models to Credit Granting Decision Problems" | TOPSIS ve PROMETHEE ile **sınıflandırıcıları** metriklerine göre sıralıyor | Dergi, yıl, cilt, sayfa, DOI |
| AHP-SVM, 5C kriterleri ("Creditworthiness Classification Utilizing AHP-SVM Based on 5C Criteria") | AHP ile öznitelik ağırlığı, SVM ile sınıflandırma | Yazarlar, dergi, yıl, DOI |
| Entropi + MARCOS, German Credit (Statlog) üzerinde kredi riski önceliklendirme | 1000 başvuranlık veri, entropi ağırlığı + MARCOS sıralaması | Yazarlar, dergi/yıl, DOI |
| arXiv:2505.20815 (Home Credit; LR, RF, SVM, KNN, NB, MLP, AdaBoost, CatBoost, LightGBM, XGBoost; SMOTE, SHAP) | Home Credit üzerinde çok modelli karşılaştırma + SHAP; **preprint** | Başlık/yazar teyidi (SHAP başlıklı bir derleme sayfası aynı çalışmayı anlatıyor gibi görünüyor); hakemli yayın var mı |
| Coşkun, S. B., & Turanlı, M. (2023), JAMSI (DOI: 10.2478/jamsi-2023-0001) | Home Credit üzerinde XGBoost, CatBoost, LightGBM karşılaştırması (Türk yazarlar) | Başlık, cilt, sayfa |
| Home Credit + LR/RF/XGBoost/LightGBM üzerine Yunanca bir çalışma (Pire Üniversitesi, UNIPI açık deposunda görüldü) | LightGBM için ROC-AUC ≈ 0,7865 bildirilmiş | Yazar, yıl, belge türü (tez mi?) teyit edilmeli; alıntılamadan önce |

**Home Credit'te beklenen AUC için tek doğrulanmış gösterge:** yukarıdaki tezde LightGBM ≈ 0,79. Bu, kendi sonuçlarımız için **mantık kontrolü**:
çok farklı çıkarsa (ör. > 0,85) önce sızıntı ara.

## 3. Boşluk analizi (✅'lerle desteklenen kısım)

| Alan | Gözlem |
|---|---|
| Home Credit + ML | Çok sayıda çalışma, preprint ve tez; model karşılaştırması ve SHAP yaygın → **katkı alanı değil** |
| AHP/BWM + TOPSIS ile kredi skorlama | Çoğu KOBİ/ticari kredi, küçük örneklem, uzman ağırlıklı, ML-PD yok; doğrulama genelde vaka sınırlı |
| MCDM'in ML ile birlikte kullanımı | Ağırlıklı olarak **model seçimi** (sınıflandırıcıları sıralama) ve **öznitelik ağırlıklandırma** (AHP→SVM) |
| Kalibrasyon ve dengesizlik | Teorik sonuç var (L-04); **karar katmanı etkisi** bizim aradığımız bağlantı |
| MCDM'i **başvurana** uygulama | **Mevcut** (Ignatius ve ark. 2018 bulanık AHP-TOPSIS; Roy & Shaw 2021/2022 BWM/fuzzy-TOPSIS) → "başvuru sıralamak" tek başına katkı **değil** |
| **Daraltılmış boşluk** | Bu çalışmalar uzman/bulanık ya da finansal-oran kriterleri kullanır, **eğitilmiş ML PD'sini bir TOPSIS kriteri yapmaz**; çoğu KOBİ/küçük örneklem, ticari dereceyle karşılaştırır, **gerçek temerrüt etiketi + PD-tek baseline + eşit onay oranı** kurgusu yoktur. Boşluk: ML-PD'yi kriter yapıp büyük gerçek veride PD-tek'e karşı ölçmek, ağırlık dayanıklılığı + kalibrasyon → **§9 tam taramasıyla teyit edilecek** |

Bu tablo, **birkaç aramaya** dayanıyor; kesin değildir. Aynı fikri yapmış bir çalışma çıkarsa kaynak olarak ele alınıp katkı daraltılır (`docs/04` §13).

## 4. Hafızadan listelenen kaynaklar — 2026-11-24 itibarıyla çoğu ✅ (kalan ⚠️: Saaty 1980 kitap, Altman 1968, yasal metinler)

**AHP / çok kriterli karar**
- Saaty, T. L. (1980). *The Analytic Hierarchy Process.* McGraw-Hill. ⚠️ · **✅ Saaty, T. L. (1990).** How to make a decision: The analytic hierarchy process. *EJOR, 48*(1), 9–26. https://doi.org/10.1016/0377-2217(90)90057-I *(2026-11-24: RePEc + Scilit)*
- **✅ Aczél, J., & Saaty, T. L. (1983).** Procedures for synthesizing ratio judgements. *Journal of Mathematical Psychology, 27*(1), 93–102. https://doi.org/10.1016/0022-2496(83)90028-7 *(2026-11-24: Crossref atıf kaydı + Springer kaynakçası; bir dizinde yalnız Aczél görünüyor, iki yazarlı künye Crossref'te)* — Grup AHP'de geometrik ortalamanın gerekçesi (homojenlik/karşılıklılık koşulları; D19).
- Rezaei, J. (2015). Best-worst multi-criteria decision-making method. *Omega, 53*, 49–57. https://doi.org/10.1016/j.omega.2014.11.009 *(✅ 2026-11-20: Omega 53(C) 49–57, DOI RePEc/Elsevier ile doğrulandı)*
- **✅ Diakoulaki, D., Mavrotas, G., & Papayannakis, L. (1995).** Determining objective weights in multiple criteria problems: The CRITIC method. *Computers & Operations Research, 22*(7), 763–770. https://doi.org/10.1016/0305-0548(94)00059-H *(2026-11-24: Scilit + makale PDF'i)* — RQ2 ağırlık yöntemi karşılaştırması.
- **✅ Opricovic, S., & Tzeng, G.-H. (2004).** Compromise solution by MCDM methods: A comparative analysis of VIKOR and TOPSIS. *EJOR, 156*(2), 445–455. https://doi.org/10.1016/S0377-2217(03)00020-1 *(2026-11-24: RePEc + MaRDI)*
- **✅ Choo, E. U., Schoner, B., & Wedley, W. C. (1999).** Interpretation of criteria weights in multicriteria decision making. *Computers & Industrial Engineering, 37*(3), 527–541. https://doi.org/10.1016/S0360-8352(00)00019-X *(2026-11-24: Scilit + kütüphane kaydı)* — Ağırlıkların anlamı birleştirme kuralına bağlı (nominal ≠ etkin; D18).
- **✅ Triantaphyllou, E., & Sánchez, A. (1997).** A sensitivity analysis approach for some deterministic multi-criteria decision-making methods. *Decision Sciences, 28*(1), 151–194. https://doi.org/10.1111/j.1540-5915.1997.tb01306.x *(2026-11-24: ISI kaydı + kütüphane)* — RQ2.

**ML ve değerlendirme**
- **✅ Breiman, L. (2001).** Random forests. *Machine Learning, 45*(1), 5–32. https://doi.org/10.1023/A:1010933404324 *(2026-11-24: Springer DOI + makale PDF)*
- **✅ Chen, T., & Guestrin, C. (2016).** XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794. https://doi.org/10.1145/2939672.2939785 *(2026-11-24: arXiv + researchr + bibbase)*
- **✅ Lundberg, S. M., & Lee, S.-I. (2017).** A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems 30*, 4765–4774. arXiv:1705.07874 *(2026-11-24: NeurIPS bildiri sayfası + meta veri)*
- **✅ Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002).** SMOTE: Synthetic minority over-sampling technique. *Journal of Artificial Intelligence Research, 16*, 321–357. https://doi.org/10.1613/jair.953 *(2026-11-24: JAIR + arXiv)*
- **✅ Saito, T., & Rehmsmeier, M. (2015).** The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE, 10*(3), e0118432. https://doi.org/10.1371/journal.pone.0118432 *(2026-11-24: DOAJ + PMC)*
- **✅ Niculescu-Mizil, A., & Caruana, R. (2005).** Predicting good probabilities with supervised learning. *Proceedings of the 22nd International Conference on Machine Learning (ICML '05).* *(2026-11-24: mlanthology + yazar PDF; sayfa numarası görülmedi)* — Boosting'in olasılıkları sigmoid biçimde bozduğunu gösterir; bizim log-loss XGB'miz ise kalibre (ECE 0,002) → tartışma.
- **✅ Elkan, C. (2001).** The foundations of cost-sensitive learning. *Proceedings of the 17th International Joint Conference on Artificial Intelligence (IJCAI)*, 973–977. *(2026-11-24: IJCAI resmî sayfası 973–977 diyor; bazı dizinler 973–978 — resmî kaynak esas)*
- **✅ Hand, D. J. (2009).** Measuring classifier performance: a coherent alternative to the area under the ROC curve. *Machine Learning, 77*(1), 103–123. https://doi.org/10.1007/s10994-009-5119-5 *(2026-11-24: Springer + dblp)*
- **✅ Nadeau, C., & Bengio, Y. (2003).** Inference for the generalization error. *Machine Learning, 52*(3), 239–281. https://doi.org/10.1023/A:1024068626366 *(2026-11-24: mlanthology + MaRDI)*
- **✅ Demšar, J. (2006).** Statistical comparisons of classifiers over multiple data sets. *Journal of Machine Learning Research, 7*, 1–30. *(2026-11-24: JMLR resmî sayfası)* — Çoklu veri seti testleri; tek veri setinde uygulanamadığının savunması (D14).
- **✅ Bergstra, J., & Bengio, Y. (2012).** Random search for hyper-parameter optimization. *Journal of Machine Learning Research, 13*, 281–305. *(2026-11-24: JMLR resmî sayfası + PDF)* — D10.
- **✅ Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022).** Why do tree-based models still outperform deep learning on typical tabular data? *Advances in Neural Information Processing Systems 35* (Datasets and Benchmarks Track). arXiv:2207.08815 *(2026-11-24: NeurIPS poster sayfası + dblp; sayfa numarası yok)*
- **✅ Rudin, C. (2019).** Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. *Nature Machine Intelligence, 1*(5), 206–215. https://doi.org/10.1038/s42256-019-0048-x *(2026-11-24: Duke Scholars + PMC)*

**Kredi skorlama ve politika**
- **✅ Verbraken, T., Bravo, C., Weber, R., & Baesens, B. (2014).** Development and application of consumer credit scoring models using profit-based classification measures. *EJOR, 238*(2), 505–513. https://doi.org/10.1016/j.ejor.2014.04.001 *(2026-11-24: RePEc + Southampton deposu)*
- **✅ Crook, J., & Banasik, J. (2004).** Does reject inference really improve the performance of application scoring models? *Journal of Banking & Finance, 28*(4), 857–874. https://doi.org/10.1016/S0378-4266(03)00203-6 *(2026-11-24: RePEc + econbiz)* — D29.
- **✅ Kozodoi, N., Jacob, J., & Lessmann, S. (2022).** Fairness in credit scoring: Assessment, implementation and profit implications. *EJOR, 297*(3), 1083–1094. https://doi.org/10.1016/j.ejor.2021.06.023 *(2026-11-24: RePEc + arXiv)* — D16/RQ5 (adalet; cinsiyet çıkarma tartışması).
- **✅ Hardt, M., Price, E., & Srebro, N. (2016).** Equality of opportunity in supervised learning. *Advances in Neural Information Processing Systems 29*, 3315–3323. *(2026-11-24: NeurIPS meta verisi)*
- Altman, E. I. (1968). Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. *Journal of Finance, 23*(4), 589–609. *(Tarihsel arka plan)*

**Yasal/düzenleyici (içerik doğrulanmadan iddia etme)**
- AB Yapay Zekâ Tüzüğü (Regulation (EU) 2024/1689): kredi değerlendirme sistemlerinin yüksek riskli sınıfta olduğu hükmü, GDPR m. 22 (otomatik karar), KVKK m. 11 (otomatik analiz sonucuna itiraz). *Madde numaralarını ve metni resmi kaynaktan doğrula; hukuk görüşü değildir.*

**Veri seti**
- Home Credit Group. (2018). *Home Credit Default Risk* [Kaggle yarışması]. https://www.kaggle.com/competitions/home-credit-default-risk *(Erişim tarihini raporda yaz.)*

## 5. Kaynak not şablonu (her okunan kaynak için)

```
[L-xx] Künye (doğrulandı ✅ tarih)
Soru / amaç:
Veri ve yöntem:
Ana bulgular (kendi cümlenle):
Sınırlılıklar:
Bizim projeyle ilişkisi: (D?? / RQ?)
Bir cümlelik atıf: "X (yıl), ... gösterdi."
Okuma durumu: özet / tam metin
```

## 6. Çekirdek okuma sırası (≥ 12; öneri T11 için ≥ 8-10 kaynak yeterli, hedef ≥ 20 kaynakça)

1. L-02 Dastile (harita) → 2. L-01 Lessmann (ölçüt/model) → 3. L-05 Roy & Shaw 2023 → 4. L-06 Roy & Shaw 2021 → 5. L-07 Kou 2014 →
6. L-03 García-Cascales → 7. L-04 Dal Pozzolo → 8. Chen & Guestrin (XGBoost) → 9. Lundberg & Lee (SHAP) → 10. Saaty 1990 (AHP) →
11. Opricovic & Tzeng 2004 → 12. Rudin 2019 → +L-08 (Türkçe) ve L-11 (derleme).

## 7. Sistematik tarama kaydı (L1; `docs/04` §9 dizgileriyle doldur)

| Tarih | Veritabanı | Dizgi | Sonuç sayısı | Taranan | Seçilen | Not |
|---|---|---|---|---|---|---|
| 2026-11-20 | Web (genel arama, Claude oturumu — ön tarama) | "probability of default" TOPSIS credit scoring machine learning | ~10 görüldü | 10 | L-07, García | Çoğu model sıralama; García ve ark. sınıflandırıcı sıralıyor |
| 2026-11-20 | Web (ön tarama) | Home Credit Default Risk AHP TOPSIS | ~10 | 10 | — | Home Credit'e özgü AHP-TOPSIS karar katmanı görülmedi (teyit: tam tarama) |
| 2026-11-20 | Web (ön tarama) | fuzzy AHP TOPSIS credit scoring (Ignatius) | ~10 | 10 | L-14 | Bulanık AHP-TOPSIS başvuran sıralama (FICO) — en yakın çalışma |
| 2026-11-20 | Web (ön tarama) | BWM TOPSIS SME credit scoring (Roy & Shaw) | ~10 | 10 | L-06, L-15 | BWM/fuzzy-TOPSIS KOBİ skorlama |
| 2026-11-20 | Web (ön tarama) | Rezaei best-worst method Omega 2015 | ~10 | 10 | Rezaei 2015 | BWM temel kaynağı doğrulandı |

**Not (dürüstlük):** Bunlar Claude oturumunda yapılan **ön** web aramalarıdır. Katkı iddiası için `docs/04` §9'daki
sistematik tarama (Scopus/WoS/IEEE/ScienceDirect + atıf zinciri) **öğrenci tarafından** yapılıp buraya eklenmelidir.

