# 00 · Başla Buradan

Bu paket, kredi risk KDS projesini **yeni bir Claude oturumunda** kesintisiz sürdürebilmek için hazırlandı.
Projeyi yapan öğrenci **Egemen**; Claude'un işi onunla birlikte, öğretirken ve savunmaya hazırlarken ilerlemek.

## Okuma sırası

| # | Dosya | Okuma amacı | Ne zaman |
|---|---|---|---|
| 1 | `CLAUDE.md` | Kurallar, rol, hedefler | Her zaman, ilk |
| 2 | `GELISTIRME_GUNLUGU.md` | Nerede kaldık? | Her zaman |
| 3 | `docs/02_yol_haritasi.md` | Plan ve sıradaki adım | Her zaman |
| 4 | `docs/03_karar_gunlugu.md` | Verilmiş kararlar ve açık sorular | Karar gerektiren her adımda |
| 5 | `docs/04_katki_stratejisi.md` | Araştırma soruları ve deney protokolü | Literatür, model, karar katmanı, deney fazları |
| 6 | `docs/01_proje_baglami.md` | Önerinin özeti, kapsam, bilinmeyenler | İlk oturum ve belirsizlik çıkınca |
| 7 | `docs/05_literatur.md` | Kaynaklar, boşluk analizi | Literatür ve rapor yazımı |
| 8 | `docs/06_savunma_hazirligi.md` | Hoca soruları | Her adım sonunda, son aşamada prova |
| 9 | `docs/07_veri_notlari.md` | Veri tuzakları | Veri, özellik, model fazları |

## Sohbet (claude.ai) ile kullanırsan

Dosya sayısı/boyutu sınırı olabilir. Öncelik sırasıyla yükle: `CLAUDE.md`, `GELISTIRME_GUNLUGU.md`,
`docs/02`, `docs/03`, `docs/04`. Diğerlerini ilgili faza gelince ekle. Oturum uzayıp bağlam dolarsa
`GELISTIRME_GUNLUGU.md` ve değişen `docs/03`, `docs/06` dosyalarının **güncel hâlini** yeni oturuma
taşı; paketin geri kalanı değişmez.

Claude Code ile kullanırsan: `CLAUDE.md` depo kökündeyse otomatik okunur; diğer dosyaları
"docs/00'dan başla" diyerek okutursun.

## Oturumu başlatan ilk mesaj (kopyala-yapıştır)

```
Merhaba Claude, ben Egemen. KDS dersi için kredi risk projesini yapıyorum; sen bu projede öğretmen-eş
çalışan olacaksın. Ekteki belgeleri oku (CLAUDE.md, GELISTIRME_GUNLUGU.md, docs/00-07 ve öneri).
Sonra şunları yap:
1. Projeyi ve nerede kaldığımızı 5 satırda özetle.
2. Ortam/teslim tarihi/hoca beklentisi hakkında bana sormak zorunda olduğun soruları sor (en fazla 6).
3. Hazır olunca tek bir sonraki adımı öner.
Kod yazmadan önce her adımın nedenini ve alternatiflerini anlat. Kodun önemli kısımlarını ben yazacağım,
sen yönlendir. Hoca her şeyi soracak, o yüzden her karar için "başka yol izlesek ne olurdu?" cevabını
birlikte hazırlayalım.
```

## Her adımın sonunda (Claude'un kontrol listesi)

- [ ] Doğrulama yapıldı (test, sağlama kontrolü ya da bilinen sonuçla karşılaştırma)
- [ ] Öğrenci 2-3 savunma sorusunu kendi kelimeleriyle cevapladı → `docs/06` güncellendi
- [ ] Karar verildiyse `docs/03` güncellendi (alternatifler + kanıt)
- [ ] `docs/02` içinde adım işaretlendi, `GELISTIRME_GUNLUGU.md` güncellendi
- [ ] Commit atıldı (Conventional Commits, Türkçe)
- [ ] Bir sonraki **tek** adım önerildi

## Bu paketin sınırları (dürüstlük notu)

- Literatür taraması bu paket hazırlanırken **sınırlı** yapıldı (yaklaşık 8 web araması). `docs/05` içinde
  hangi kaynakların doğrulandığı (✅) ve hangilerinin doğrulanması gerektiği (⚠️) işaretli. Katkı iddiası
  için sistematik tarama (`docs/04` §9) öğrenci tarafından yapılmalı.
- Veri seti üzerinde henüz **hiçbir sonuç** yok; `docs/07` içindeki sayılar ve beklenen AUC aralıkları
  indirme sonrası doğrulanacak.
- `docs/03` içindeki bazı kararlar "Önerilen" durumunda: öğrenci ve gerekirse hoca onayı bekliyor.
