# 02 · Yol Haritası

Durum işaretleri: ✅ tamam · ⏳ sürüyor · ⬜ bekliyor. Claude, adım bitince burayı günceller.
Süreler önerinin 13 haftalık çizelgesine göre **göreceli**; gerçek teslim tarihi öğrenilince yeniden dağıtılır.

## Sıkıştırılmış takvim (2026-11-20 itibarıyla; yerine geçti: 13 haftalık çizelge)

**Sunum: 7 Aralık 2026 (Pzt).** Makale sunumdan sonra teslim (tarih bilinmiyor). Sunuma kadar hedef:
çalışan sızıntısız boru hattı + 3 model + AHP-TOPSIS + RQ1 (ve mümkünse RQ2) sonuçları + literatür özeti + slaytlar.
Kapsam daraltmaları `docs/03` D31'de (🟡, öğrenci onayı bekliyor).

| Tarih | Teknik iş | Paralel: literatür / yazım |
|---|---|---|
| 20 Kas Cu | Belge paketi depoya; seviye tespiti; V2 başlangıç | L1: arama protokolü |
| 21–22 Kas | V2 kısa EDA; **V3 bölme (sıfırdan) → K-B** | L1: aramalar ve kayıt tablosu |
| 23–25 Kas | F1–F4: temizleme, oranlar, büro toplulaştırma, `Pipeline` | L2: çekirdek okuma, literatür matrisi; AHP yargıçlarına form gönder |
| 26 Kas | (tampon) | **L3 boşluk analizi + L4 ön-kayıt → K-A** (modellemeden önce) |
| 27–29 Kas | M1–M3, dar M4, M6 kalibrasyon, **M7 → K-C**, M8 SHAP | Veri ve Yöntem taslağı |
| 30 Kas–1 Ara | K1–K4: **AHP ve TOPSIS sıfırdan**, eşikler → K-D | Karar katmanı yöntemi |
| 2 Ara | E1 (RQ1), E2 (RQ2) | Bulgular tabloları/şekilleri |
| 3–4 Ara | Streamlit D1–D3 (minimal) | |
| 5 Ara | | Slaytlar (R2) |
| 6 Ara | | **Savunma provası (R3)** |
| 7 Ara | **Sunum** | |
| Sonrası | (İsteğe bağlı) kapsam genişletme: ek tablolar, RQ3 tam | Makale (R1), R4 |

## Kapı kontrolleri (geri dönüşü zor noktalar)

| Kapı | Ne zaman | Koşul |
|---|---|---|
| **K-A** Protokol | L4 sonrası, modelleme öncesi | Araştırma soruları ve deney protokolü (`docs/04`) tarihli commit ile donduruldu; mümkünse hoca onayı |
| **K-B** Bölme | V3 | Eğitim/test bölmesi bir kez yapıldı, indeksler kaydedildi; **test setine hiç bakılmadı** |
| **K-C** Model seçimi | M7 | Model seçimi **çapraz doğrulama** ile yapıldı; test kümesi yalnızca final değerlendirme için, tek seferde açıldı |
| **K-D** Karar eşikleri | K4 | Bant eşikleri ve TOPSIS referans noktaları **eğitim** (OOF) verisinde kilitlendi |
| **K-E** Deneyler | E fazı | Her deney protokole uygun; sapmalar "protokol sapması" olarak `docs/04` §10'a yazıldı |

Test kümesine kural dışı bakılırsa bu `GELISTIRME_GUNLUGU.md` içine yazılır ve ilgili sonuç "keşifsel" etiketiyle raporlanır.

---

## Faz 0 · Altyapı

| # | Adım | Çıktı | Bitti sayılır | Öğrenilen / savunma konusu |
|---|---|---|---|---|
| A1 ✅ | Proje dizini | Klasör iskeleti | `tree` çıktısı doğrulandı | `raw` değişmez, `processed` üretilebilir; `src` ≠ `notebooks` |
| A2 ✅ | Yerel Git deposu | `.git`, `.gitignore`, `.gitkeep`, README, ilk commit | `git status` temiz; `git log --oneline` 1 commit; proje OneDrive **dışında** | Neden veri Git'e girmez, `.gitignore` kodlaması |
| A3 ✅ | GitHub deposu + ilk push | Uzak depo, `main` dalı | Depo açık, README görünüyor, kimlik doğrulama çalışıyor | Uzak/yerel depo, `push`, dal kavramı |
| A4 ✅ | Python ortamı | `.venv`, `requirements.txt`, `ruff`, `pytest` | `python -m pytest` çalışıyor; `pip freeze` kaydı | Sanal ortam, bağımlılık sabitleme |
| A5 ⬜ | (Ek) CI | GitHub Actions: pytest | Yeşil rozet | Sürekli entegrasyon |

## Faz 1 · Literatür ve çerçeve (hf 1-2, Faz 2 ile paralel)

| # | Adım | Çıktı | Bitti sayılır | Öğrenilen / savunma konusu |
|---|---|---|---|---|
| L1 ⏳ | Arama protokolü | `docs/05` içinde veritabanı, arama dizgisi, dahil etme/dışlama, tarih, sonuç sayısı kaydı | Protokol tekrarlanabilir | Sistematik tarama mantığı |
| L2 | Literatür matrisi | ≥ 25 kaynak taranmış, **≥ 12 çekirdek kaynak** okunmuş; her biri 3 satır not (ne yaptı, veri, bulgu/sınır) | Tablo dolu; her künye doğrulanmış | Kaynak okuma, atıf disiplini |
| L3 | Boşluk analizi + RQ kesinleştirme | `docs/04` §3'ün güncel hâli; hocayla görüşme notu | Boşluk, kaynaklarla gerekçeli; hocanın "katkı" beklentisi netleşti | Katkı iddiasının sınırı |
| L4 | **Deney protokolü ön-kaydı** → **K-A** | `docs/04` §8 şablonu dolduruldu, tarihli commit | Hipotezler, metrikler, istatistiksel plan yazılı | Ön-kayıt, p-hacking'den kaçınma |

## Faz 2 · Veri (hf 1-2)

| # | Adım | Çıktı | Bitti sayılır | Öğrenilen / savunma konusu |
|---|---|---|---|---|
| V1 ✅ | Veri indirme + veri sözlüğü | `data/raw/*.csv`; `docs/07` §1 doğrulandı (satır/sütun) | 7 dosya mevcut, boyutlar `docs/07` ile karşılaştırıldı | Kaggle kuralları, lisans |
| V2 ✅ | `application_train` EDA | Defter + `rapor/sekiller/` | Hedef dağılımı, eksiklik, anomali, aykırı değer, hedefe göre dağılımlar | Sınıf dengesizliği, eksiklik mekanizması |
| V3 ✅ | **Bölme** → **K-B** | `src/bolme.py`, kayıtlı indeksler, testler | %80/%20 katmanlı bölme; sınıf oranları iki tarafta eşit; test indeksleri dosyada, kimse açmadı | Neden katmanlı, neden zaman bazlı değil |
| V4 | Ek tabloların EDA'sı | Tablo başına özet | İlişkiler (SK_ID_CURR/PREV/BUREAU), anahtar tekilliği ve anomaliler not edildi | İlişkisel veri, 1-N ilişki |

## Faz 3 · Özellik mühendisliği (hf 3-4)

| # | Adım | Çıktı | Bitti sayılır | Öğrenilen / savunma konusu |
|---|---|---|---|---|
| F1 ✅ | Başvuru temizleme | `src/veri_hazirlama.py` | Anomali kodları düzeltilmiş (`docs/07` §2), birim testli | Anomali ≠ eksik; bayrak değişkeni |
| F2 ✅ | Oran/türev özellikler | Kredi/gelir, taksit/gelir vb. | Sıfıra bölme güvenli; testli | Oran değişkenlerinin anlamı |
| F3 ◐ | Ek tablo toplulaştırma | Her tablo için ayrı fonksiyon + test | Satır sayısı değişmedi; kayıt yoksa 0/NaN kuralı kayıtlı | Toplulaştırma, "kayıt yok" ≠ "0 gecikme" |
| F4 ✅ | sklearn `Pipeline` | `src/boru_hatti.py` | Imputer/encoder/scaler yalnızca eğitime fit; testli sızıntı kontrolü | Veri sızıntısı |
| F5 | Özellik seti sürümleri | `temel` (yalnız application), `tam` (+ ek tablolar), `politika-kör`, `ext-siz` | Her sürüm adlandırılmış ve yeniden üretilebilir | Ablation mantığı (RQ1/D17 için) |

## Faz 4 · Modelleme (hf 5-7)

| # | Adım | Çıktı | Bitti sayılır | Öğrenilen / savunma konusu |
|---|---|---|---|---|
| M1 | Dummy + Logistic Regression | Baseline sonuçları (CV) | CV AUC ± std kaydedildi | Baseline neden gerekli |
| M2 | Random Forest | CV sonuçları | Aynı CV şeması | Bagging, aşırı uyum |
| M3 | XGBoost | CV sonuçları | Aynı CV şeması, erken durdurma doğru kullanıldı (sızıntısız) | Boosting, hiperparametreler |
| M4 | Dengesizlik stratejileri | Yok / `class_weight` / SMOTE / undersampling karşılaştırması | SMOTE yalnızca CV içinde; olasılık kalibrasyonu da raporlandı | Neden AUC kalibrasyonu göstermez |
| M5 | Hiperparametre arama | Arama bütçesi + sonuçlar | Aynı bütçe tüm modellere; en iyi parametreler kayıtlı | Aşırı uyum, arama stratejisi |
| M6 | Kalibrasyon | Güvenilirlik eğrileri, Brier/ECE; isotonic/Platt/prior-shift | Kalibrasyon **OOF tahmin** üzerinde öğrenildi | Kalibrasyon ≠ ayırt edicilik |
| M7 | Test değerlendirmesi → **K-C** | AUC, Gini, KS, PR-AUC, Brier, F1@eşik, maliyet; bootstrap %95 GA | Model seçimi CV'ye göre, test tek sefer | Güven aralığı, model karşılaştırma testi |
| M8 | Açıklanabilirlik | Önem sıralaması, permutation importance, SHAP (global + yerel) | SHAP sınırlamaları yazıldı (korele özellikler, nedensellik değil) | Açıklanabilirlik ≠ nedensellik |

## Faz 5 · Karar katmanı (hf 8-9)

| # | Adım | Çıktı | Bitti sayılır | Öğrenilen / savunma konusu |
|---|---|---|---|---|
| K1 | Kriter tablosu | 6 kriter: tanım, yön, ölçek, eksik değer kuralı | Her kriter koddan türetildi ve doğrulandı | Fayda/maliyet kriteri |
| K2 | **AHP sıfırdan** | `src/ahp.py`: özvektör yöntemi, CR, grup birleştirme (geometrik ortalama) | Saaty örneğiyle ve bir kütüphaneyle (ör. `pymcdm`) çapraz doğrulandı; CR < 0,10 | AHP matematiği, tutarlılık |
| K3 | **TOPSIS sıfırdan** | `src/topsis.py`: normalizasyon, ağırlıklı matris, ideal/anti-ideal, C* | Kitap örneği ve kütüphane ile aynı sonuç; **sabit referans** (eğitimden) desteği | TOPSIS adımları, rank reversal |
| K4 | Bantlar ve eşikler → **K-D** | Onayla/Şartlı Onayla/Reddet tanımı | Eşikler eğitim OOF'unda kilitli; hedef onay oranı parametrik | Eşik seçimi, maliyet |
| K5 | Karar gerekçesi | Kriter katkıları + SHAP özeti | Her karar için "neden" metni üretilebiliyor | Açıklama biçimi |

## Faz 6 · Deneyler (hf 9-11)

Ayrıntı: `docs/04_katki_stratejisi.md` §4-§8.

| # | Adım | Çıktı | Bitti sayılır |
|---|---|---|---|
| E1 | **RQ1** PD-tek vs AHP-TOPSIS | Onay oranı - kötü oran eğrisi, swap-set, politika-ihlal oranı, bootstrap GA | Protokole uygun, `deneyler/` altında kayıtlı |
| E2 | **RQ2** Ağırlık dayanıklılığı | Dirichlet MC, karar kararlılık indeksi, ağırlık yöntemleri karşılaştırması | Aynı |
| E3 | **RQ3** Dengesizlik/kalibrasyon → karar | Varyant başına AUC, Brier, karar değişim oranı | Aynı |
| E4 | (Ek) RQ4 referans noktası, adalet | Batch vs sabit TOPSIS; onay oranı eşitsizliği | Zaman kalırsa |
| E5 | Sonuç yazımı | Tablolar/şekiller, negatif sonuçlar dahil | Her iddia bir tablo/şekle bağlı |

## Faz 7 · Dashboard (hf 10-12)

| # | Adım | Bitti sayılır |
|---|---|---|
| D1 | Streamlit iskelet, model + referans yükleme, girdi formu | Tek başvuru girilince PD ve C* hesaplanıyor |
| D2 | Ağırlık kaydırıcıları, canlı karar | Ağırlıklar toplamı 1; AHP ikili karşılaştırma girişi opsiyonel |
| D3 | Açıklama paneli | SHAP waterfall + kriter katkıları |
| D4 | Hata durumları, README, ekran görüntüleri | Geçersiz girdi çökmüyor; temiz kurulumda çalışıyor |

## Faz 8 · Rapor ve savunma (hf 12-13)

| # | Adım | Bitti sayılır |
|---|---|---|
| R1 | Rapor | Giriş, literatür, veri, yöntem, deney, bulgular, **sınırlılıklar**, sonuç; ≥ 8-10 doğrulanmış kaynak (hedef ≥ 20) |
| R2 | Sunum | Her slayt bir savunma sorusuna bağlı |
| R3 | **Savunma provası** | Claude "hoca" rolünde `docs/06`'dan sürpriz sorular sorar; öğrenci kaynağa bakmadan cevaplar |
| R4 | Tekrarlanabilirlik | Temiz klonda README adımlarıyla baştan çalışıyor; `v1.0` etiketi |

## Zaman yönetimi kuralları

- Her faz sonunda "bitti mi, yoksa yeterince iyi mi?" kararı; mükemmeliyetçilik kapsam kaybettirir.
- Sıkışırsan **ek** katman düşer, **çekirdek** düşmez (`docs/01` §5).
- Tam veri koşuları uzun sürer: arama bütçesini ve örnek boyutunu planla; gece koşusu için betik, defter değil.
