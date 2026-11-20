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

**[L-06] ◐ Roy, P. K., & Shaw, K. (2021).** A multicriteria credit scoring model for SMEs using hybrid BWM and TOPSIS.
*Financial Innovation, 7*, 77. https://doi.org/10.1186/s40854-021-00295-5
*Ne yapıyor:* En iyi-en kötü yöntemiyle (BWM) ağırlıkları, TOPSIS ile skoru üretiyor; ağırlık duyarlılık analizi yapıyor.
*Projede:* D19 (BWM alternatifi), RQ2'nin yakın öncülü: onlar ağırlık duyarlılığına bakıyor, biz **karar kararlılığı ve PD baseline** ile genişletiyoruz. *(Yazar sırası kaynak sayfasında farklı görünebilir; yayıncı sayfasından teyit et.)*

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
| **Önerilen boşluk** | PD'yi MCDM kriteri yapan, büyük ölçekli perakende verisinde, PD-tek baseline'a karşı eşit onay oranında karşılaştıran, ağırlık dayanıklılığı ve kalibrasyon etkisini ölçen çalışma → **§9 taramasıyla teyit edilecek** |

Bu tablo, **birkaç aramaya** dayanıyor; kesin değildir. Aynı fikri yapmış bir çalışma çıkarsa kaynak olarak ele alınıp katkı daraltılır (`docs/04` §13).

## 4. Hafızadan listelenen, doğrulanacak kaynaklar (⚠️)

**AHP / çok kriterli karar**
- Saaty, T. L. (1980). *The Analytic Hierarchy Process.* McGraw-Hill. · Saaty, T. L. (1990). How to make a decision: The analytic hierarchy process. *EJOR, 48*(1), 9–26.
- Aczél, J., & Saaty, T. L. (1983). Procedures for synthesizing ratio judgements. *J. Math. Psychol., 27*, 93–102. *(Grup AHP geometrik ortalama; D19)*
- Rezaei, J. (2015). Best-worst multi-criteria decision-making method. *Omega, 53*, 49–57. *(BWM; kısmi doğrulama: L-06 içinde anılıyor)*
- Diakoulaki, D., Mavrotas, G., & Papayannakis, L. (1995). Determining objective weights in multiple criteria problems: The CRITIC method. *Computers & Operations Research, 22*(7), 763–770.
- Opricovic, S., & Tzeng, G.-H. (2004). Compromise solution by MCDM methods: A comparative analysis of VIKOR and TOPSIS. *EJOR, 156*(2), 445–455.
- Choo, E. U., Schoner, B., & Wedley, W. C. (1999). Interpretation of criteria weights in multicriteria decision making. *Computers & Industrial Engineering, 37*(3), 527–541. *(Nominal ≠ etkin ağırlık; D18)*
- Triantaphyllou, E., & Sánchez, A. (1997). A sensitivity analysis approach for some deterministic multi-criteria decision-making methods. *Decision Sciences, 28*(1), 151–194. *(RQ2)*

**ML ve değerlendirme**
- Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5–32.
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proc. KDD '16*, 785–794.
- Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems 30.*
- Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic minority over-sampling technique. *JAIR, 16*, 321–357.
- Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE, 10*(3), e0118432.
- Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. *Proc. ICML.*
- Elkan, C. (2001). The foundations of cost-sensitive learning. *Proc. IJCAI.*
- Hand, D. J. (2009). Measuring classifier performance: a coherent alternative to the area under the ROC curve. *Machine Learning, 77*, 103–123.
- Nadeau, C., & Bengio, Y. (2003). Inference for the generalization error. *Machine Learning, 52*, 239–281.
- Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. *JMLR, 7*, 1–30. *(Tek veri setinde uygulanamaz; neden uygulamadığımızın savunması)*
- Bergstra, J., & Bengio, Y. (2012). Random search for hyper-parameter optimization. *JMLR, 13*, 281–305.
- Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on typical tabular data? *NeurIPS Datasets and Benchmarks.*
- Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. *Nature Machine Intelligence, 1*, 206–215.

**Kredi skorlama ve politika**
- Verbraken, T., Bravo, C., Weber, R., & Baesens, B. (2014). Development and application of consumer credit scoring models using profit-based classification measures. *EJOR, 238*(2), 505–513.
- Crook, J., & Banasik, J. (2004). Does reject inference really improve the performance of application scoring models? *Journal of Banking & Finance, 28*(4), 857–874. *(D29)*
- Kozodoi, N., Jacob, J., & Lessmann, S. (2022). Fairness in credit scoring: Assessment, implementation and profit implications. *EJOR, 297*(3), 1083–1094. *(RQ5)*
- Hardt, M., Price, E., & Srebro, N. (2016). Equality of opportunity in supervised learning. *NeurIPS 29.*
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
| | | | | | | |
