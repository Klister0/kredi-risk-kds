# AHP Yargı Formu: Kredi Onay Kriterlerinin Göreli Önemi

**Amaç.** Bir kredi başvurusunu değerlendirirken aşağıdaki 6 kriterin birbirine göre ne kadar önemli olduğunu
belirlemek. Cevaplarınız yalnızca akademik bir ders projesinde (KDS dersi, Muğla Sıtkı Koçman Üniversitesi)
kriter ağırlıklarını hesaplamak için kullanılacaktır. Doğru ya da yanlış cevap yoktur; kendi deneyiminize göre
yanıtlayın. Süre: yaklaşık 10 dakika.

## Kriterler

| Kod | Kriter | Açıklama |
|---|---|---|
| K1 | Temerrüt olasılığı (PD) | Makine öğrenmesi modelinin tahmin ettiği ödeme güçlüğü olasılığı |
| K2 | Kredi / gelir oranı | İstenen kredi tutarının başvuranın gelirine oranı |
| K3 | Taksit / gelir oranı | Taksit tutarının gelire oranı (ödeme yükü) |
| K4 | Gelir | Başvuranın beyan ettiği gelir |
| K5 | İstihdam süresi | Mevcut işte çalışılan yıl |
| K6 | Geçmiş gecikme | Kredi bürosu kayıtlarında gecikme izi olan kredi sayısı |

## Ölçek (Saaty 1–9)

| Değer | Anlamı |
|---|---|
| 1 | İkisi eşit önemde |
| 3 | Biri diğerinden biraz daha önemli |
| 5 | Biri diğerinden belirgin şekilde daha önemli |
| 7 | Biri diğerinden çok daha önemli |
| 9 | Biri diğerinden kesinlikle daha önemli |
| 2, 4, 6, 8 | Ara değerler |

## Karşılaştırmalar (15 çift)

Her satırda **hangisinin daha önemli olduğunu** işaretleyin ve **ne kadar** daha önemli olduğunu 1–9 arasında yazın.
İkisi eşitse "Eşit" yazın ve değer olarak 1 verin.

| # | Sol | Sağ | Daha önemli olan (Sol / Sağ / Eşit) | Değer (1–9) |
|---|---|---|---|---|
| 1 | K1 Temerrüt olasılığı | K2 Kredi/gelir | | |
| 2 | K1 Temerrüt olasılığı | K3 Taksit/gelir | | |
| 3 | K1 Temerrüt olasılığı | K4 Gelir | | |
| 4 | K1 Temerrüt olasılığı | K5 İstihdam süresi | | |
| 5 | K1 Temerrüt olasılığı | K6 Geçmiş gecikme | | |
| 6 | K2 Kredi/gelir | K3 Taksit/gelir | | |
| 7 | K2 Kredi/gelir | K4 Gelir | | |
| 8 | K2 Kredi/gelir | K5 İstihdam süresi | | |
| 9 | K2 Kredi/gelir | K6 Geçmiş gecikme | | |
| 10 | K3 Taksit/gelir | K4 Gelir | | |
| 11 | K3 Taksit/gelir | K5 İstihdam süresi | | |
| 12 | K3 Taksit/gelir | K6 Geçmiş gecikme | | |
| 13 | K4 Gelir | K5 İstihdam süresi | | |
| 14 | K4 Gelir | K6 Geçmiş gecikme | | |
| 15 | K5 İstihdam süresi | K6 Geçmiş gecikme | | |

**Yargıç bilgisi (isim yazmanız gerekmez):** Görev/uzmanlık (ör. bankacı, finans akademisyeni, finans öğrencisi): ______
Kredi değerlendirme deneyimi (yıl): ______

---
*Projeye giriş notu (öğrenci için):* Sol daha önemliyse `deger`, sağ daha önemliyse `1/deger` olarak
`docs/kaynaklar/ahp_yargilar.csv` dosyasına satır sırasıyla girilir (`src/ahp.py::ust_ucgenden_matris`).
