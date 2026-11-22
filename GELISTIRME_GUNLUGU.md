# Geliştirme Günlüğü: Kredi Risk KDS Projesi

Bu dosya projenin nerede kaldığını, alınan kararları ve sıradaki adımı kaydeder.
Yeni bir Claude oturumunda önce `CLAUDE.md`, sonra bu dosya okunur (`docs/00_BASLA_BURADAN.md`).
Proje önerisi: `docs/kaynaklar/Proje_Onerisi_Kredi_Risk.docx`.

Son güncelleme: 2026-11-20

## Takvim

- **Sunum: 7 Aralık 2026 (Pzt).** Makale (akademik yayın formatı) sunumdan sonra teslim; tarihi bilinmiyor.
- Günlük plan: `docs/02_yol_haritasi.md` → "Sıkıştırılmış takvim". Kapsam daraltma önerisi: `docs/03` D31 (🟡).

## Proje özeti

- **Ders:** Karar Destek Sistemleri (KDS), dönem projesi
- **Başlık:** Makine Öğrenmesi ve Çok Kriterli Karar Analizi ile Kredi Risk Değerlendirme ve Onay Karar Destek Sistemi
- **Veri:** Kaggle Home Credit Default Risk (application_train + 6 ek tablo, ~307 bin başvuru)
- **Modeller:** Logistic Regression, Random Forest, XGBoost (ROC-AUC, F1, PR-AUC)
- **Karar katmanı:** AHP (ağırlıklar) + TOPSIS → Onayla / Şartlı Onayla / Reddet
- **Arayüz:** Streamlit dashboard, ağırlıklar kullanıcı tarafından ayarlanabilir, SHAP ile açıklama
- **Hedef:** Kod GitHub'a adım adım yüklenecek

## Çalışma şekli

- Proje adım adım ve her adımın **nedeni** açıklanarak ilerliyor; amaç olabildiğince çok şey öğrenmek.
- Her adımda tek bir konu ele alınıyor.
- Kod ve klasör adları Türkçe (ör. `veri_hazirlama.py`, `rapor/sekiller`).
- **Adım 2–5 Claude Code ile yapıldı** (komutları Claude çalıştırdı, açıkladı).
- **2026-11-20'den itibaren (belge paketiyle):** Claude öğretmen-eş çalışan rolünde (`CLAUDE.md` §3).
  **Öğrencinin tercihi (2026-11-20):** kodu çoğunlukla **Claude yazar**; öğrenci sunumda savunabilmek için her parçayı anlar.
  Bu yüzden Claude her kod parçasının yanına "sunumda şunu söyle" notu verir ve savunma kartlarını (`docs/06`) doldurur.
  Komutları (git, pytest, python) öğrenci kendi makinesinde çalıştırır (Claude'un yerel kabuğu yok; dosya okuyup yazabilir).
  Her adım: amaç → neden → alternatifler → uygulama → doğrulama → savunma kartı (`docs/06`) → kayıt (`docs/03`, bu günlük) → commit.
- Günlük her adımın sonunda güncellenir ve commit'e dahil edilir.
- **Obsidian notları (2026-10-06'dan itibaren):** Günlüğün bağlantılı, öğrenmeye yönelik hâli Obsidian kasasında
  tutuluyor: `C:\Users\Egemen\OneDrive\Belgeler\Obsidian Vault\Kredi Risk KDS\`. İçinde ana sayfa
  (`Kredi Risk KDS.md`) ve `Adımlar/`, `Kavramlar/`, `Veri/`, `Kararlar/` klasörleri var. Her adımın sonunda
  yeni bir adım notu açılır, yeni kavramlar için kavram notları yazılır, ana sayfadaki tablo güncellenir.
  Asıl kaynak bu günlüktür, Obsidian ondan türetilir. Kasa depo dışında olduğu için Git'e girmez.

## Ortam

- **İşletim sistemi:** Windows, PowerShell
- **Proje yolu:** `C:\Users\Egemen\Projeler\kredi-risk-kds` (OneDrive dışına taşındı, bkz. Adım 2)
- **Araçlar:** Git 2.56, Python 3.13
- **GitHub:** Klister0

## Klasör yapısı

```
kredi-risk-kds/
├── data/raw/          Kaggle CSV'leri (Git'e girmez)
├── data/processed/    kodun ürettiği veri (Git'e girmez)
├── notebooks/         keşif defterleri
├── src/               yeniden kullanılan kod
├── tests/             testler
├── rapor/sekiller/    rapor grafikleri
├── docs/              belge paketi (kararlar, plan, literatür, savunma)
└── CLAUDE.md          Claude oturumları için kurallar ve bağlam
```

## Test kümesi erişim sayacı (sızıntı disiplini)

Test kümesi henüz oluşturulmadı. Her açılış buraya yazılır: tarih · neden · hangi kapı (K-B/K-C/...) · sonuç.

| Tarih | Neden | Kapı | Not |
|---|---|---|---|
| 2026-11-20 | Bölme üretimi: SK_ID_CURR'lar teste atandı | K-B | Yalnız SK_ID_CURR+TARGET okundu; test ÖZELLİKLERİNE bakılmadı. n_test=61502 |
| 2026-11-22 | M7: üç modelin test değerlendirmesi (tek sefer) | K-C | XGB AUC 0,777. İlk deneme test kimlik dosyası eksik olduğu için veri okunmadan durdu (açılış sayılmaz). Kilit dosyası `deneyler/m7_test_sonuc.json`. Test tahminleri E1 için `data/processed/test_tahmin/` |

## Tamamlanan adımlar

### Adım 1: Proje dizini ✅
Klasör yapısı oluşturuldu ve `tree` ile doğrulandı.
Öğrenilenler: ham veri değiştirilmez, `processed/` koddan yeniden üretilebilir olmalı (tekrarlanabilirlik);
kalıcı kod `src/`'de, denemeler `notebooks/`'ta tutulur.

### Adım 2: Git deposu (yerel) ✅
- Proje OneDrive dışına taşındı (OneDrive senkronizasyonu büyük veri, sanal ortam ve `.git` klasörüyle çakışır).
- `git init`, `.gitignore`, `.gitkeep` dosyaları, README, günlük; ilk commit:
  `chore: proje iskeleti, .gitignore ve README` (Conventional Commits kullanılıyor).
- Öğrenilenler:
  - `.gitignore` UTF-8 olmalı; PowerShell 5.1'de `>` ile yazılan dosya UTF-16 olur ve Git okuyamaz.
  - Git boş klasörleri izlemez; `.gitkeep` klasörü depoda tutmak için kullanılan boş dosyadır (bir gelenek, Git özelliği değil).
  - `data/raw/*` + `!data/raw/.gitkeep`: önce her şeyi dışla, sonra tek dosyaya istisna tanı.
    (`data/raw/` yazılsaydı klasörün tamamı dışlanır ve istisna çalışmazdı.)
  - `notebooks/`, `src/`, `tests/` henüz boş olduğu için depoda görünmez; içlerine ilk dosya eklenince görünecekler.

### Adım 3: GitHub deposu ✅
- GitHub CLI (`gh` 2.102) kuruldu, `gh auth login` ile giriş yapıldı.
- Public depo: https://github.com/Klister0/kredi-risk-kds
- Tek komut: `gh repo create kredi-risk-kds --public --source=. --remote=origin --push`
- Öğrenilenler:
  - `gh repo create` üç işi birden yapar: GitHub'da depo açar, `git remote add origin <url>`, `git push -u origin main`.
  - `remote`: yerel deponun bildiği uzak adres; `origin` geleneksel addır (`git remote -v` ile görülür).
  - `-u` (upstream): `main`'i `origin/main`'e bağlar; sonrasında yalnızca `git push` / `git pull` yeterli.
  - Public depo güvenli çünkü veri `.gitignore` ile dışarıda; ama `.env` gibi gizli bilgiler asla commit edilmemeli.
  - Yeni kurulan program "bulunamadı" derse terminal eski PATH'i kullanıyordur; terminali yeniden açmak yeterli.

### Adım 4: Python sanal ortamı ✅
- `py -3.13 -m venv .venv` ile projeye özel ortam; paketler `requirements.txt`'de sürümleri sabitlenerek tutuluyor.
- Kurulu: pandas 3.0, numpy 2.5, scikit-learn 1.9, xgboost 3.4, matplotlib, seaborn, jupyterlab, ipykernel, pytest.
  `shap` ve `streamlit` ilgili adımlarda eklenecek.
- Komutlar ortamı etkinleştirmeden, doğrudan `.\.venv\Scripts\python.exe` ile çalıştırılıyor.
  (PowerShell'de `.\.venv\Scripts\Activate.ps1` "running scripts is disabled" hatası verebilir; bu bir güvenlik ayarıdır,
  etkinleştirme şart değil.)
- Öğrenilenler:
  - Sanal ortam: her projenin paketleri ayrı; biri bozulursa silinip `requirements.txt`'den yeniden kurulur.
  - `requirements.txt`'ye `pip freeze`'in tamamı (110 satır, dolaylı bağımlılıklar dahil) değil,
    yalnızca doğrudan kurulan paketler `==` ile yazıldı: okunabilir, platformdan bağımsız, tekrarlanabilir.
  - Doğrulama: `pip install -r requirements.txt --dry-run` (dosya ortamla uyumlu mu) ve `pip check` (çakışma var mı).
  - İçe aktarma adı ile paket adı farklı olabilir: `pip install scikit-learn` ama `import sklearn`.
  - **pandas 3.0 notu:** Copy-on-Write varsayılan ve metin sütunları artık `str` tipinde. Önceki sohbetteki
    (pandas 2 ile yazılmış) referans koddan parça alınırsa zincirleme atama (`df[a][b] = ...`) çalışmaz, `.loc` kullanılmalı.

### Adım 5: Kaggle verisi ✅
- 10 CSV (2.5 GB) Downloads'tan `data/raw/`'a taşındı (aynı disk: taşıma anlık, kopya 2.5 GB israf olurdu).
- 8 tablonun satır/sütun sayısı Kaggle değerleriyle birebir doğrulandı; SHA-256 parmak izleri `data/README.md`'de.
- Öğrenilenler:
  - Veri Git'e girmez ama verinin kimliği (kaynak, boyut, parmak izi) girer: başkası doğru veriyi indirdiğini doğrulayabilir.
  - `HomeCredit_columns_description.csv` latin-1 kodlamalı: `pd.read_csv(..., encoding="latin-1")`.
  - `application_test.csv`'de `TARGET` yok (Kaggle'ın gizli test kümesi); bizim test kümemiz
    `application_train`'den ayrılacak.
  - Büyük dosyalar `chunksize` ile parça parça okunabilir; bellek yetmezse bu yöntem kullanılır.

### Adım 6: Belge paketi depoya alındı (2026-11-20)
- `CLAUDE.md` köke, `docs/00–07` ve öneri (`docs/kaynaklar/`) depoya eklendi. Paket daha önce OneDrive'da ayrı duruyordu;
  karar geçmişinin tarihli commit'lerle izlenebilmesi için depoya taşındı (ön-kayıt K-A bunu gerektirir).
- Paketteki eski durum bilgileri gerçek duruma göre güncellendi (A1–A4, V1 ✅; `docs/02`, `docs/07` §1).
- Veri sözlüğünden okunanlar (`docs/07` §3, `docs/03` D32): `TARGET` tanımındaki gün (X) ve taksit (Y) sayıları sözlükte **yok**;
  `AMT_INCOME_TOTAL` ve `AMT_ANNUITY` için **dönem belirtilmemiş** (öneri "yıllık/aylık" diyor → öneride ifade hatası).
- Yeni kararlar: D31 (kapsam daraltma, 🟡), D32 (öneri hataları, 🟢).

### Adım 7: V3 Bölme ✅
- `src/bolme.py`: katmanlı holdout **sıfırdan** (`katmanli_bol`), bölmeyi kaydetme (`bolmeyi_kaydet`), `__main__` ile gerçek veri koşusu.
- `src/__init__.py` (boş, paket olsun diye). `tests/test_bolme.py`: 7 test (ayrıklık, bütünlük, oran koruma, belirlenircilik, sıralılık, sklearn ile sınıf bazında uyum, tekil-olmayan kimlik hatası).
- Claude ortamında 7/7, öğrencinin makinesinde `python -m pytest` 7/7 **yeşil**.
- Gerçek veri (kapı K-B): `python -m src.bolme` → `data/processed/bolme/` (n_egitim=246009, n_test=61502, tohum=42, %20). 246009+61502=307511 ✓.
- **Karar verildi:** bölme indeksleri commit'lenir; `.gitignore`'a `!data/processed/bolme/` istisnası eklendi (D03 🟢).
- **D33 (🟢):** EDA bölmeden sonra, yalnız eğitim kümesinde (sızıntı).

### Adım 8: V2 EDA (yalnız eğitim kümesi) ✅
- `notebooks/01_kesif.py`: eğitim kimlikleriyle `application_train`; konsol özeti + 3 grafik (`rapor/sekiller/`).
- **Doğrulanan sayılar (n=246.009):** `TARGET` %8,07 (19.860 pozitif); `DAYS_EMPLOYED=365243` %17,9 (bu grupta temerrüt %5,4 < normal %8,7);
  >%50 eksik 41 sütun (çoğu konut `*_AVG/*_MODE/*_MEDI` üçlüsü → yalnız `*_AVG` tutma kararını destekler); `EXT_SOURCE_1/2/3` TARGET ile en güçlü korelasyonlar.
  Eğitim belleği 426 MB (float32 ile 362 MB).
- `docs/07` §1-§2 bu sayılarla güncellendi.

### Adım 9: F1 Başvuru temizleme ✅
- `src/veri_hazirlama.py`: `istihdam_anomalisini_isaretle` (365243→NaN + bayrak, idempotent), `cinsiyet_xna_nan`, `gunleri_yila_cevir` (negatif gün → pozitif yıl), `temizle_basvuru` (orkestratör, satır sayısını assert'ler). Durumsuz dönüşümler → sızıntı yok.
- `tests/test_veri_hazirlama.py`: 5/5 yeşil. Gerçek eğitim verisinde: 44.075 anomali, 4 cinsiyet NaN, YAS_YIL 20,5–69,1, satır 246.009 korundu.

### Adım 10: L1 literatür ön taraması ⏳
- Web araması (ön katman) ile 5 dizgi; doğrulanan künyeler `docs/05`'e işlendi:
  - **L-06** Roy & Shaw 2021 (Financial Innovation 7(1), Art.77) ✅ tam doğrulandı; **Rezaei 2015** (Omega 53, 49–57) ✅.
  - Yeni: **L-14** Ignatius ve ark. 2018 (NCAA 29(10)) — bulanık AHP-TOPSIS ile **başvuran** sıralama; **L-15** Roy & Shaw 2022 (Complex & Intelligent Systems).
- **ÖNEMLİ (kural 4 bildirimi):** AHP/TOPSIS'i kredi **başvurusuna** uygulamak literatürde zaten var (Ignatius 2018; Roy & Shaw). "Başvuru sıralamak" tek başına katkı değil.
  Katkı **daraltıldı** (`docs/04` §3/§13, `docs/05` §3, `docs/06` S29): eğitilmiş **ML PD'sini** TOPSIS kriteri yapmak + **büyük gerçek veri + gerçek etiket** + **PD-tek baseline (eşit onay oranı)** + kalibrasyon.
- **Kalan iş (öğrenci):** `docs/04` §9 sistematik tarama (Scopus/WoS/IEEE/ScienceDirect + atıf zinciri). Ön tarama boşluğu "kanıtlamaz", daraltır.

### Adım 11: F2 Oran/türev özellikler ✅
- `src/oran_ozellikleri.py`: `KREDI_GELIR`, `TAKSIT_GELIR`, `ODEME_ORANI`, `KREDI_MAL_ORANI`, `KISI_BASI_GELIR`, `EXT_ORT/STD/EKSIK_SAYISI`. Sıfıra bölme güvenli (payda 0/NaN → NaN, inf yok). `tests/test_oran_ozellikleri.py` 4/4.
- Gerçek veride (eğitim): medyanlar makul, inf yok, eksik <%0,2. **Bulgu:** `KREDI_GELIR`/`TAKSIT_GELIR` TARGET ile korelasyon ≈0; `EXT_ORT` −0,221. → politika kriterleri risk sinyali değil (D18 savunmasını destekler). `docs/07` §5, `docs/03` D18 güncellendi.

### Adım 12: F3 bureau toplulaştırma ◐ (bureau ✅, bureau_balance bekliyor)
- `src/ek_tablolar.py`: `buro_ozellikleri` (SK_ID_CURR düzeyinde: kayıt/aktif/gecikmeli/uzatma sayısı, maks gecikme gün/tutar, toplam borç/kredi, borç oranı, son kredi günü), `basvuruya_birlestir` ("kayıt yok" kuralı: sayım 0, oran/tutar NaN, `BURO_KAYDI_VAR`). `tests/test_ek_tablolar.py` 4/4.
- Gerçek veri: büro özet 305.811 başvuru; eğitime birleşince **246.009 satır korundu**. **Başvuruların %14,3'ü büro kaydı yok** (35.244). Gecikme izi **%23,6** (düzeltildi: ilk kayıttaki %0,2 bir yazdırma hatasıydı, `docs/07`), borç oranı medyan 0,22.
- bureau_balance (aylık STATUS/DPD) sunum kapsamında **opsiyonel**; zaman kalırsa eklenir (D31).

### Adım 13: F4 sızıntısız Pipeline ✅
- `src/boru_hatti.py`: `OzellikTuretici` (durumsuz F1+F2) → `ColumnTransformer` [sayısal: median impute (+ opsiyonel StandardScaler); kategorik: most_frequent impute + OneHotEncoder(handle_unknown='ignore')]. `olcekle` paramı (LR=True, ağaçlar=False).
- `tests/test_boru_hatti.py` 3/3. **Sızıntı kanıtı:** imputer istatistiği eğitim medyanı (test değil) — sayısal test yeşil; görülmemiş kategori patlamıyor.
- Gerçek veri (büro birleşik, iç doğrulama bölmesi): 267 özellik, çıktıda NaN/inf yok, ölçekli ortalama~0/std~1, test sütunları eğitimle hizalı.

### Adım 14: M1 Dummy + Logistic Regression baseline ✅
- `src/veri_yukle.py` (`egitim_matrisi`: app+bureau birleşik eğitim X/y, `ornek` ile hızlı mod) + `deneyler/m1_baseline.py` (Dummy + LR, 5 katlı StratifiedKFold, boru hattı CV içinde → sızıntısız).
- **Sonuç (tam veri 246.009, temel+büro):** LR **ROC-AUC 0,7526 ± 0,0022**, PR-AUC 0,235; Dummy 0,499 / 0,081. Beklenen aralıkta (0,74–0,76), sızıntı işareti yok.
- Sonuç `deneyler/m1_baseline_2026-11-22_tam.json`. Test kümesine BAKILMADI.

### Adım 15: M2 Random Forest + M3 XGBoost ✅
- `deneyler/m2_m3_agaclar.py`: M1 ile aynı 5 katlı CV, `olcekle=False`, sabit parametreler, erken durdurma yok, eğitim skoru da kaydediliyor.
- **Sonuç (tam veri):** XGB **0,769 ± 0,002** (PR-AUC 0,257) > LR 0,753 > RF 0,749. RF'nin LR'nin altında kalması kısıtlı ayardan (derinlik 12, max_samples 0,3); gizlenmedi. XGB eğitim-CV farkı 0,10 (aşırı uyum → M5).
- Beklenen aralık (0,77–0,80) alt sınırında: yalnız temel+büro özellikleri (diğer 4 tablo kapsam dışı, D31). Sızıntı işareti yok.

### Adım 16: M4 (dar) + M6 kalibrasyon ✅
- `src/kalibrasyon.py`: `ece` (eşit frekanslı), `prior_duzeltme`, `cv_isotonic` (sızıntısız); `tests/test_kalibrasyon.py` 5/5 (bilinen sonuçlarla).
- `deneyler/m4_m6_kalibrasyon.py`: XGB {ağırlık yok, scale_pos_weight≈11,4} × {ham, prior, isotonic}, 5 katlı OOF.
- **Bulgu (RQ3 model düzeyi):** ağırlık AUC'yi ~0,003 değiştiriyor, ortalama PD'yi 0,080→0,367 şişiriyor (ECE 0,003→0,286). Prior düzeltme aşırı düzeltiyor (0,068). Ağırlıksız ham model zaten kalibre (ECE 0,0025).
- Kararlar: **D08 🟢** (ağırlıklandırma yok), **D13 🟡** ön-belirlenmiş kural (ECE<0,01 → ham, aksi isotonic).
- OOF tahminleri `data/processed/oof/xgb_oof_tam.csv` (git dışı; betikle yeniden üretilir). Şekil `rapor/sekiller/04_guvenilirlik_egrisi.png`.

### Adım 17: M5 eşit bütçeli arama — betik hazır, tam koşu öğrencinin makinesinde ⏳
- `deneyler/m5_arama.py`: LR/RF/XGB, 12 aday × 3 kat (eşit bütçe) → en iyiler 5 katlı CV'de yeniden ölçülür. Seçim kuralı arama öncesi yazıldı (D10): en yüksek 5-kat CV AUC.
- Claude ortamında 20 bin satır × 2 adayla duman testi geçti (kod çalışıyor; sayılar anlamsız).
- Tam koşu öğrencinin makinesinde (12 iş parçacığı); tahmini süre kaba olarak 1–3 saat. Çıktı `deneyler/m5_arama_<tarih>_tam.json`.

### Adım 18: K1 kriter tablosu (öneri) + K2 AHP sıfırdan ✅
- **Düzeltme:** F3'te başvuru düzeyi gecikme izi %0,2 yazılmıştı; doğrusu **%23,6** (yazdırma hatası). `docs/07` düzeltildi. 6. kriter gerçekten ayırt edici.
- `src/ahp.py`: matris doğrulama, üst üçgenden matris, kuvvet yinelemesiyle ağırlık + λmax, CI/CR (RI web'de doğrulandı), geometrik ortalama grup birleştirme. `tests/test_ahp.py` 7/7 (numpy.linalg.eig ile çapraz doğrulama dahil).
- **D34 (🟡):** 6 kriter, yönler, eksik kuralları (K5 emekli → eğitim medyanı; K6 kayıtsız → 0; tümü eğitim p1–p99 kırpma).
- `docs/ahp_yargi_formu.md` (15 ikili karşılaştırma) + `docs/kaynaklar/ahp_yargilar_sablon.csv`.
- **D19 (🟡):** Birincil yargıç öğrencinin babası (bankacı); mümkünse 1–2 meslektaşı. Bağımsız doldurma; CR>0,10 ise yeniden değerlendirme.

### Adım 19: K3 TOPSIS sıfırdan + K1 kriter hazırlayıcı ✅
- `src/topsis.py`: `batch_topsis` (klasik) + `SabitTopsis` (eğitimden kırpma/norm/ideal; tek başvuruda tanımlı, rank reversal yok). `tests/test_topsis.py` 7/7, **pymcdm 1.4 ile çapraz doğrulama** dahil.
- `src/kriterler.py`: D34 kuralları (K5 eksik → eğitim medyanı, K6 kayıt yok → 0), fit yalnız eğitimde; `tests/test_kriterler.py`.
- `src/ahp.py::en_tutarsiz_ciftler` (yargıca yeniden sorulacak çiftler). Öğrenilen: n=3'te tutarsızlığın yeri tespit edilemez (tek döngü); n=6'da edilir — testli.
- Gerçek veride uçtan uca sağlama (eşit ağırlık, **raporlanmaz**): boru hattı çalışıyor, C* ile PD negatif ilişkili. Tüm testler: 45.

### Adım 20: M5 eşit bütçeli arama ✅
- Tam eğitim, öğrencinin makinesi (~35 dk). LR 0,7528 · RF 0,7503 · **XGB 0,7704 ± 0,001** → kurala göre **XGBoost seçildi**. XGB eğitim-CV farkı 0,10→0,06. RF ayarlı hâliyle de LR'nin altında.
- Protokol sapması kaydı: K-A ön-kaydı modellemeden sonra, karar katmanı deneylerinden önce (`docs/04` §10).

### Adım 21: Final model + ön-kayıt (K-A) taslağı
- `deneyler/final_model.py`: M5 parametreleri JSON'dan okunur; 5 katlı OOF (AUC 0,7705, Brier 0,0671, **ECE 0,0023 → D13 kuralı: ham PD**); tüm eğitimle final fit. Model `data/processed/model/final_model.joblib`, OOF `data/processed/oof/final_oof.csv` (git dışı, betikle yeniden üretilir). Test açılmadı.
- `docs/08_on_kayit_v1.md`: E1 (RQ1, doğrulayıcı: birincil Δ = ortalama kötü oranı farkı a∈0,2–0,8, eşleştirilmiş bootstrap B=1000), E2 (RQ2, keşifsel), E3-dar (RQ3, eğitim OOF). Bantlar %15/%15/%70 (politika parametresi). **Öğrenci onayı + commit = K-A.**

### Adım 22: K-A ✅ + M7 test değerlendirmesi (K-C) ✅
- Ön-kayıt `docs/08_on_kayit_v1.md` commit'lendi (3a6c1ee) → **K-A**.
- `src/degerlendirme.py` (KS, eşleştirilmiş bootstrap sıfırdan; `tests/test_degerlendirme.py`), `deneyler/m7_test.py` (deneme modu + ikinci açılışı engelleyen kilit).
- **Test (n=61.502):** XGB AUC **0,777 [0,770–0,784]**, Gini 0,554, KS 0,417, PR-AUC 0,265, Brier 0,0667, ECE 0,0032. LR 0,757, RF 0,756. XGB−LR +0,019 [+0,017; +0,022] → anlamlı. CV→test 0,770→0,777.
- `commit_bekleyen.cmd`: Claude push edemiyor (izin reddedildi); öğrenci bu betikle commit'liyor.

### Adım 23: M8 SHAP ✅ + D16 cinsiyet bulgusu
- `src/aciklama.py` + testler (toplanabilirlik, XGBoost `pred_contribs` ile uyum); `deneyler/m8_shap.py` → şekiller 05 (global), 06 (dağılım), 07 (iki örnek başvuru). LR–SHAP yön uyumu %100, önem sırası ρ=0,41.
- **CODE_GENDER 4. en önemli değişken.** Cinsiyetsiz modelin CV maliyeti AUC −0,0016 (yalnız eğitim).
- **D16 kararı (öğrenci): cinsiyetsiz final model.** `on_isleme_boru_hatti(dislanan=...)` parametresi (varsayılan boş → M1–M5 değişmez). Final OOF AUC 0,7689, ECE 0,0023 → ham PD. SHAP yeniden üretildi (cinsiyetli şekiller `*_cinsiyetli.png` olarak saklı). Cinsiyetli kayıtlar: eksiz JSON'lar + `*_cinsiyetli.png` + yerel `*_cinsiyetli_m7.*`. Sapma `docs/04` §10; cinsiyetsiz modelin test AUC'si E1'de bir kez.

## Açık konular / kararlar

- **TOPSIS tek başvuruda tanımsız:** İdeal/anti-ideal noktalar eğitim verisinden (ör. %5 ve %95 yüzdelikleri)
  sabitlenip yeni başvurular bu referansa göre puanlanacak. (Önerildi, karar katmanında uygulanacak.)
- **Çift sayım riski:** Gelir, kredi/gelir gibi değişkenler hem modelde hem TOPSIS'te yer alıyor.
  Raporda gerekçe: model "istatistiksel riski", diğer kriterler "banka politikasını" temsil eder.
- **Veri sızıntısı:** Eksik doldurma, ölçekleme ve kodlama yalnızca eğitim kümesine göre (sklearn Pipeline) yapılacak.
- Önceki sohbette bitmiş bir veri hazırlama + EDA sürümü üretildi (`kredi-risk-kds.zip`).
  Proje sıfırdan yeniden kuruluyor; o sürüm yalnızca başvuru kaynağı.
- **Literatür:** Hoca makalede "literatürde X vardı, bu çalışma Y'yi ekledi" yapısını istiyor → sistematik tarama (`docs/04` §9) L1'de başlıyor.
- **Kararlar ve ayrıntılar:** `docs/03` (D01–D32). Bilinen zayıf noktalar: `docs/01` §2.
- **Sorulacaklar:** makale şablonu/dili/tarihi, değerlendirme kriterleri, AHP yargıçları, cinsiyet değişkeni (D16), RAM (`docs/01` §6).

## Sıradaki adım — güncel plan (2026-11-22, sunum 7 Aralık Pzt)

Sahip: **Sen** = Egemen · **Ben** = Claude · **Birlikte**. Kritik yol kalın.

| # | Ne zaman | İş | Sahip | Kapı / not |
|---|---|---|---|---|
| 1 | 22 Kas | Bekleyen commit'ler + `m5_arama_*_tam.json` commit | Sen | — |
| 2 | 22–23 Kas | **AHP formunu babana ver** (bağımsız doldursun; mümkünse 1–2 meslektaş) | Sen | Dönüş hedefi 25 Kas |
| 3 | 22 Kas ✅ | **L4 ön-kayıt** `docs/08_on_kayit_v1.md` commit'lendi | Ben → Sen | **K-A** ✅ |
| 4 | 22 Kas ✅ | Final XGB OOF (AUC 0,7705, ECE 0,0023 → ham PD) + tüm eğitimle final fit | Ben | Test açılmadı |
| 5 | 22 Kas ✅ | **M7: test kümesi TEK SEFER** — XGB AUC 0,777 [0,770–0,784] | Ben | **K-C** ✅ |
| 6 | 22 Kas ✅ | M8 SHAP (global + yerel); D16: final model cinsiyetsiz | Ben | T9 ✅, D16 ✅ |
| 7 | 25 Kas | AHP yargıları → ağırlıklar, CR; gerekirse en tutarsız çiftler yeniden sorulur | Birlikte | D19 |
| 8 | 25–26 Kas | **K4 bantlar/eşikler** (Onayla/Şartlı/Reddet) eğitim OOF'unda | Ben | **K-D** |
| 9 | 26–27 Kas | **E1 (RQ1)**: eşit onay oranında PD-tek vs AHP-TOPSIS; swap-set; politika ihlali; w_PD taraması; bootstrap | Ben | Çekirdek katkı |
| 10 | 28–29 Kas | E2 (RQ2) ağırlık dayanıklılığı (Dirichlet MC, karar kararlılığı); zaman kalırsa E3 dar | Ben | Hedef katman |
| 11 | 30 Kas–2 Ara | Streamlit dashboard D1–D3 (tek başvuru, ağırlık kaydırıcı, SHAP + kriter katkısı) | Ben | T8/T9 |
| 12 | 23 Kas–2 Ara (günde ~1 sa) | **L2 sistematik literatür taraması** (Scopus/WoS/IEEE + atıf zinciri), `docs/05` §7 | Sen | Katkı cümlesinin dayanağı |
| 13 | 3–4 Ara | Sonuç tabloları/şekilleri, literatür + katkı slaytları | Birlikte | — |
| 14 | 5 Ara | Slaytlar (R2) | Birlikte | — |
| 15 | 6 Ara | **Savunma provası** (R3): ben hoca rolünde | Birlikte | `docs/06` |
| 16 | 7 Ara | **Sunum** | Sen | — |
| 17 | Sunum sonrası | Makale (R1), kapsam genişletme (ek tablolar, bureau_balance, RQ3 tam), R4 | Birlikte | — |

Tampon: 3–4 Aralık kısmen tampondur; gecikme olursa önce #10 (RQ2) daraltılır, #9 (RQ1) ve #11 (dashboard) düşmez.

## Değişiklik kaydı