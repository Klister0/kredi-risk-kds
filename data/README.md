# Veri

Kaynak: [Kaggle Home Credit Default Risk](https://www.kaggle.com/competitions/home-credit-default-risk/data)
(yarışma kurallarının kabul edilmesi gerekir). CSV'ler lisans ve boyut nedeniyle depoda yer almaz;
indirilip `data/raw/` içine konmalıdır. `data/raw/` **salt okunur** kabul edilir; tüm dönüşümler koddan
`data/processed/`'e yazılır.

## Ham dosyalar

Satır/sütun sayıları Kaggle'da yayımlanan değerlerle doğrulanmıştır (2026-10-05).

| Dosya | Boyut (MB) | Satır | Sütun | SHA-256 (ilk 16) | İçerik |
|---|---:|---:|---:|---|---|
| application_train.csv | 166.1 | 307,511 | 122 | 52e96b895b1112e1 | Ana tablo: başvurular + `TARGET` |
| application_test.csv | 26.6 | 48,744 | 121 | a36161331d839150 | Kaggle test başvuruları, `TARGET` yok |
| bureau.csv | 170.0 | 1,716,428 | 17 | 9d799143423f2807 | Diğer kurumlardaki krediler |
| bureau_balance.csv | 375.6 | 27,299,925 | 3 | 33e09f06174c26f0 | Büro kredilerinin aylık durumu |
| previous_application.csv | 405.0 | 1,670,214 | 37 | 5046cd657ee04df2 | Home Credit'teki önceki başvurular |
| POS_CASH_balance.csv | 392.7 | 10,001,358 | 8 | 0e13bc573ffa8fc2 | POS/nakit kredilerin aylık bakiyesi |
| installments_payments.csv | 723.1 | 13,605,401 | 8 | 428c2e2496e4d6d6 | Taksit ödeme geçmişi |
| credit_card_balance.csv | 424.6 | 3,840,312 | 23 | a9cdc48900d55131 | Kredi kartı aylık bakiyesi |
| HomeCredit_columns_description.csv | 0.04 | 219 | 5 | eef7665398228a80 | Sütun açıklamaları (**latin-1** kodlamalı) |
| sample_submission.csv | 0.5 | 48,744 | 2 | 95258f8383ad9da4 | Kaggle gönderim örneği (kullanılmıyor) |

Parmak izini doğrulamak için (PowerShell):

```powershell
Get-FileHash data\raw\application_train.csv -Algorithm SHA256
```

## Notlar

- `application_test.csv`'de `TARGET` olmadığı için model değerlendirmesinde kullanılamaz.
  Test kümesi `application_train.csv`'den ayrılacaktır.
- Tablolar `SK_ID_CURR` (başvuru) ve `SK_ID_PREV` / `SK_ID_BUREAU` (önceki kredi) anahtarlarıyla bağlanır.
