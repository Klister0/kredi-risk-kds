# 08 · Deney Protokolü Ön-Kaydı (v1)

**Tarih:** 2026-11-22 · **Commit:** bu dosyanın ilk commit'i (tarih kanıtı) · **Hoca onayı:** yok (sunumda belirtilecek)
**Kapsam:** Karar katmanı deneyleri E1 (RQ1), E2 (RQ2), E3-dar (RQ3). Bu dosya commit'lenmeden E-fazı analizleri koşulmaz.
**Sapma:** Ön-kayıt modelleme SONRASI, karar katmanı deneyleri ÖNCESİ yapılıyor (`docs/04` §10). Model düzeyi seçimler
yine sonuç görülmeden yazılmıştı: D10 seçim kuralı, D13 kalibrasyon kuralı (tarihli commit'ler).

## 1. Veri ve bölme
- `application_train` (307.511), katmanlı %80/%20, tohum 42. Eğitim 246.009 / test 61.502. İndeksler `data/processed/bolme/` (commit'li).
- Özellik seti: temel + büro (D31). Diğer 4 ek tablo kapsam dışı.

## 2. PD modeli (K-C ile kilitlenir)
- XGBoost, M5 parametreleri (`deneyler/m5_arama_2026-11-22_tam.json`), sınıf ağırlıklandırması yok (D08).
- Kalibrasyon: D13 kuralı (OOF ECE < 0,01 → ham; değilse tüm OOF'a fit isotonic). Sonuç `deneyler/final_model_*.json`.
- Eğitim tarafı PD = 5 katlı OOF; test tarafı PD = tüm eğitimle fit edilmiş final model.

## 3. Karar katmanı (K-D ile kilitlenir)
- 6 kriter, yönler ve eksik kuralları D34; kırpma sınırları (p1/p99), normalizasyon ve ideal/anti-ideal **eğitim OOF kriterlerinden** (`SabitTopsis`, D21).
- Ağırlıklar (w0): AHP; yargıç(lar) D19, birden fazlaysa geometrik ortalama. Kabul CR < 0,10; aşılırsa en tutarsız çiftler yargıca yeniden sorulur, **ilk ve son CR kaydedilir**. Yargıçlara model sonuçları gösterilmez. **w0 dondurulmadan E1/E2'nin test analizleri koşulmaz.**
- Bantlar (dashboard ve bant tabloları için): eğitim OOF C* niceliklerinden **Reddet = alt %15, Şartlı Onayla = sonraki %15, Onayla = üst %70**. PD-tek için aynı nicelikler (1 − PD) üzerinde. Bu oranlar politika parametresidir; ana sonuçlar onay oranı eğrisi üzerinden raporlanır ve bantlara bağlı değildir.
- Test kümesinde hiçbir karar katmanı parametresi (ağırlık, eşik, kırpma, referans) ayarlanmaz.

## 4. RQ1 · Politika bedeli (E1) — DOĞRULAYICI
- Skorlar (test): s_PD = 1 − PD, s_MCDM = C*.
- Onay oranı ızgarası a ∈ {0,10; 0,20; …; 0,90}; her a'da skora göre üst a onaylanır (test içinde sıralama; etiket kullanılmaz).
- **Birincil metrik:** Δ = ortalama_{a ∈ {0,2…0,8}} [BR_MCDM(a) − BR_PD(a)]; BR = onaylananlarda TARGET=1 oranı.
- İstatistik: test üzerinde eşleştirilmiş bootstrap, B = 1000, tohum 42, %95 yüzdelik güven aralığı. Tek birincil metrik; çoklu karşılaştırma düzeltmesi yok.
- **H1a:** Δ > 0 (AHP-TOPSIS'in kötü oranı PD-tek'ten yüksek = politika bedeli). Δ'nin GA'sı tamamen 0'ın altında çıkarsa önce sızıntı / çift sayım / referans hatası aranır.
- **H1b (ikincil, doğrulayıcı):** Politika ihlali oranı = onaylananlar içinde TAKSIT_GELIR > eğitim p90 **veya** KREDI_GELIR > eğitim p90 olanların payı. Hipotez: ihlal_MCDM < ihlal_PD, a = 0,70'te ve a ∈ {0,2…0,8} ortalamasında; aynı bootstrap.
- Keşifsel (etiketli): swap-set (a = 0,70'te iki politikanın farklı karar verdiği başvurular; kötü oranı ve kriter profili), w_PD taraması (w_PD ∈ {0; 0,1; …; 1}, diğer ağırlıklar w0 oranlarıyla ölçeklenir; her noktada Δ ve ihlal → Pareto eğrisi; **H1c:** eğride belirgin bir "diz" noktası var).

## 5. RQ2 · Ağırlık dayanıklılığı (E2) — KEŞİFSEL (betimsel)
- w ~ Dirichlet(α · w0), α ∈ {10, 50, 200}, N = 1000 çekim, tohum 42.
- Her çekimde bant eşikleri eğitim OOF C* niceliklerinden yeniden hesaplanır (%15/%15/%70), test başvurularına uygulanır.
- Karar kararlılık indeksi S_i = max_k P(karar_i = k). Raporlanan: S dağılımı (medyan, S < 0,8 payı); düşük-S başvuruların Şartlı bandıyla örtüşmesi; düşük-S ve yüksek-S onaylananların kötü oranı.
- Zaman kalırsa: ağırlık yöntemleri (AHP, eşit, entropi, CRITIC) arası Kendall τ (sıralama) ve Cohen κ (karar).

## 6. RQ3-dar · Kalibrasyonun karara etkisi (E3) — DOĞRULAYICI (yalnız eğitim OOF)
- PD varyantları (`deneyler/m4_m6_*`): ağırlıksız ham (referans), sınıf ağırlıklı ham, sınıf ağırlıklı isotonic. Aynı w0 ve aynı SabitTopsis.
- Metrikler: (i) karar değişim oranı (referansa göre, bantlar), (ii) a = 0,70'te kötü oranı, (iii) **mutlak eşikli politika** "PD > 0,15 ise reddet" altında ret oranı.
- **H3:** Eşit onay oranlı (sıralama temelli) kararlar az değişir; mutlak PD eşikli politika ve TOPSIS bant kararları belirgin değişir.

## 7. Test kümesi kullanımı
- K-C (M7): model metrikleri, bir kez. E1/E2: dondurulmuş boru hattıyla son analizler. Her açılış `GELISTIRME_GUNLUGU.md` sayacına yazılır. Açılıştan sonra hiçbir parametre değişmez.

## 8. Değişiklik kuralı
- Her sapma `docs/04` §10'a tarih, neden ve etkiyle yazılır. Bu dosya düzenlenmez; değişiklik gerekirse `08_on_kayit_v2.md` açılır.
