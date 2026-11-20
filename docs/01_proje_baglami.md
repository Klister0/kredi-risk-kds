# 01 · Proje Bağlamı

## 1. Önerinin özeti (hocaya sunulan belge)

**Problem.** Kredi başvurusu değerlendirme, hem kayıpları sınırlamak hem de hacmi büyütmek için kritik bir karar
problemi. Yalnızca risk skoru yetmez; karar verici skoru gelir, borçluluk ve ödeme davranışıyla birlikte
değerlendirip Onayla / Şartlı Onayla / Reddet kararına varabilmeli.

**Amaç.** Büyük bir kredi başvuru veri setinde temerrüt olasılığını ML ile tahmin etmek ve bunu AHP/TOPSIS ile
birleştirip karar önerisi üreten bir KDS kurmak.

**Önerideki taahhütler (sapma = gerekçeli kayıt):**

| # | Taahhüt | Öneri bölümü |
|---|---|---|
| T1 | Veri: Kaggle Home Credit Default Risk (7 tablo, ≈307 bin başvuru) | §4 |
| T2 | Veri hazırlama: eksik değer, aykırı değer, kodlama, ek tabloların başvuru düzeyinde toplulaştırılması, oran değişkenleri | §6.1 |
| T3 | Modeller: Logistic Regression, Random Forest, XGBoost; aynı çapraz doğrulama şeması | §6.2 |
| T4 | Metrikler: ROC-AUC, F1, PR-AUC (yalnızca doğruluk değil) | §4, §6.2, §7 |
| T5 | Sınıf dengesizliği: sınıf ağırlıklandırma veya yeniden örnekleme denenecek | §6.2 |
| T6 | Karar kriterleri (6): temerrüt olasılığı, kredi/gelir, taksit/gelir, gelir, istihdam süresi, geçmiş gecikme | §5 |
| T7 | AHP ile ağırlık, TOPSIS ile ideal çözüme yakınlık; puan eşiklerine göre Onayla/Şartlı Onayla/Reddet | §6.3 |
| T8 | Ağırlıkları karar verici değiştirebilsin (interaktif dashboard) | §2, §6.3 |
| T9 | Streamlit dashboard: risk skoru, karar, gerekçe; feature importance ve mümkünse SHAP | §6.4 |
| T10 | Ayrılmış test kümesinde değerlendirme; karar katmanını gerçek etiketlerle karşılaştırma (Onayla ve Reddet gruplarının temerrüt oranları ayrışıyor mu?) | §7 |
| T11 | Literatür: **en az 8-10 akademik kaynak**, atıflı; kaynakça APA/IEEE | §3, §10 |
| T12 | Sistem akademik prototip, gerçek karar için değil | §2 |

**Önerinin zaman çizelgesi (toplam 13 hafta):** literatür+indirme+EDA 2 hf → veri temizleme/özellik 2 hf → modeller 3 hf
→ AHP/TOPSIS 2 hf → dashboard 2 hf → test/rapor 2 hf. (Gerçek teslim tarihi bilinmiyor, §6.)

## 2. Önerinin içerdiği bilinen zayıf noktalar

Bunlar öneriyi yazarken görülmeyen, savunmada sorulma ihtimali yüksek noktalar. Her biri
`docs/03_karar_gunlugu.md` içinde bir karar maddesine bağlı.

1. **Çift sayım (D18):** PD modeli gelir, kredi/gelir, istihdam gibi kriterleri zaten girdi olarak kullanıyor;
   aynı bilgi karar katmanında yeniden ağırlıklandırılıyor.
2. **AHP yargıcı (D19):** İkili karşılaştırmaları kim yapıyor? Öğrencinin kişisel görüşü "banka uzmanı" değildir.
3. **TOPSIS tek başvuruda tanımsız (D21):** İdeal/anti-ideal nokta, başvuru kümesine bağlı. Dashboard'da tek başvuru
   girildiğinde referans nereden gelecek? Ayrıca küme değişince sıralama değişebilir (rank reversal).
4. **Döngüsel doğrulama (D23):** PD, gerçek etikete göre eğitilmiş; PD'yi içeren karar skorunun etiketle ilişkili
   çıkması şaşırtıcı değil. Anlamlı soru "PD tek başına eşikleme yapılsa ne olurdu?" karşılaştırmasıdır.
5. **Seçim yanlılığı (D29):** Veri, kredi verilmiş başvuruların sonuçlarını içerir; reddedilenler yok.
   "Reddet" grubunun gerçek temerrüt oranı, *booked* popülasyon için ölçülür.
6. **"Temerrüt" etiketi:** `TARGET`, resmi anlamda temerrüt değil, ilk taksitlerde belirli gün üzeri gecikme
   (ödeme güçlüğü) tanımına dayanır (`docs/07` §3). Terminolojide dikkat.
7. **Gelir ve taksit dönemselliği:** Önerideki "yıllık gelir" ve "aylık taksit" ifadeleri veri sözlüğüyle
   doğrulanmadı; ikisi de belirsiz (`docs/07` §3).
8. **Zamansal doğrulama yok:** Veride başvuru tarihi bulunmuyor; zaman bazlı bölme yapılamaz.
9. **Dengesizlik çözümü olasılığı bozar (D8, D13):** Sınıf ağırlığı/yeniden örnekleme, AUC'yi bozmadan olasılık
   ölçeğini bozar; TOPSIS ise PD'nin *değerini* kullanır, sıralamasını değil.

## 3. Hedefin üç katmanı

- **Zorunlu (ders):** T1-T12'yi sağlayan çalışır prototip, rapor, sunum.
- **Savunma:** her seçimin alternatif + kanıtla savunulabilirliği.
- **Katkı (hoca beklentisi):** `docs/04` içindeki araştırma soruları. Gerçekçi hedef, devrim değil;
  **iyi tanımlanmış, tekrarlanabilir ve dürüstçe raporlanmış bir ampirik katkı**.

## 4. Mevcut durum (2026-11-20)

- A1–A4 ve V1 tamam (Git + GitHub + venv + doğrulanmış ham veri). Kod yok. Güncel ayrıntı: `GELISTIRME_GUNLUGU.md`.
- Önceki referans sürüm (`kredi-risk-kds.zip`): yalnızca başvuru kaynağı; öğrenci sıfırdan yazıyor.

## 5. Kapsam katmanları

| Katman | İçerik | Kural |
|---|---|---|
| **Çekirdek** (ders için şart) | T1-T12; RQ1 (PD-tek vs AHP-TOPSIS); temel sızıntısız boru hattı; 3 model; kalibrasyon kontrolü; SHAP; Streamlit | Bitmeden diğerine geçme |
| **Hedef** (katkı için) | RQ2 (ağırlık dayanıklılığı), RQ3 (dengesizlik/kalibrasyon → karar), grup-AHP, `EXT_SOURCE` ablation | Çekirdekten sonra |
| **Ek** (zaman kalırsa) | RQ4 (TOPSIS referans/rank reversal), adalet analizi, LightGBM/CatBoost duyarlılık, MLflow, CI | İsteğe bağlı |

## 6. Bilinmeyenler: öğrenciye sorulacaklar

**Cevaplananlar (2026-11-20):** Sunum **7 Aralık 2026**; makale "akademik yayın formatında", sunumdan sonra teslim.
Hoca, makalede "literatürde X vardı, bu çalışma Y'yi kazandırdı" yapısını açıkça istiyor; literatür taraması sağlam olmalı.
Ayrıca kısa bir sunum slaytı hazırlanacak. Ortam: Windows, Python 3.13, Git 2.56, `gh` CLI.

**Açık kalanlar:**
1. Makalenin teslim tarihi, şablonu (IEEE/dergi/serbest), dili (TR/EN), sayfa sınırı, atıf biçimi (APA/IEEE)?
2. Değerlendirme kriterleri (rapor, kod, sunum, demo ağırlıkları)? Sunum süresi?
3. "Katkı"nın düzeyi: yeni karşılaştırmalı analiz yeterli mi? Bildiri/yayın hedefi var mı? (`docs/04` §14)
4. Çalışma bireysel mi?
5. RAM (tam veri için ≥ 8 GB önerilir).
6. AHP için **uzman yargısı** toplayabileceği biri var mı?

## 7. Sözlük

| Terim | Anlam |
|---|---|
| PD | Probability of Default, temerrüt (burada: ödeme güçlüğü) olasılığı |
| ROC-AUC | Rastgele bir "kötü" başvurunun "iyi"den yüksek skor alma olasılığı; eşikten bağımsız ayırt edicilik |
| Gini | 2·AUC − 1; kredi skorlamada yaygın rapor biçimi |
| KS | Kötü/iyi birikimli dağılımlar arasındaki en büyük fark; skorlamada yaygın |
| PR-AUC | Precision-Recall eğrisi altındaki alan; dengesiz veride bilgilendirici |
| Kalibrasyon | Tahmin edilen olasılığın gerçek sıklıkla örtüşmesi (%10 dediğin grupta %10 mu kötü?) |
| Brier / ECE | Olasılık hatası ölçüleri (Brier: karesel hata; ECE: beklenen kalibrasyon hatası) |
| AHP | Analytic Hierarchy Process; ikili karşılaştırmalardan kriter ağırlığı türetir; tutarlılık oranı (CR) < 0,10 beklenir |
| TOPSIS | Alternatifleri ideal ve anti-ideal çözüme uzaklığa göre sıralar; çıktı "yakınlık katsayısı" C* ∈ [0,1] |
| Rank reversal | Alternatif kümesi değişince sıralamanın değişmesi |
| Swap-set analizi | İki politikanın farklı karar verdiği başvuruların karşılaştırılması |
| Booked popülasyon | Kredisi fiilen verilmiş başvurular (sonucu gözlenenler) |
| Reject inference | Reddedilenlerin sonucunu tahmin ederek seçim yanlılığını azaltma girişimi |
| Veri sızıntısı | Test bilgisinin eğitime karışması; sonuçları olduğundan iyi gösterir |
