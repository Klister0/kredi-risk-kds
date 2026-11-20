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
- **2026-11-20'den itibaren (belge paketiyle):** Claude öğretmen-eş çalışan rolünde (`CLAUDE.md` §3). Komutları öğrenci
  kendi makinesinde çalıştırır; kritik parçaları (bölme, AHP, TOPSIS, bootstrap, kalibrasyon grafiği) öğrenci sıfırdan yazar.
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
| | | | |

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

## Sıradaki adım

1. Belge paketinin commit'i: `docs: proje belge paketi ve sıkıştırılmış takvim`.
2. Seviye tespiti (5 kısa soru), ardından **V2:** `notebooks/01_kesif.ipynb` — `application_train` yapısı, sütun tipleri,
   eksik oranları, `TARGET` oranı (≈%8 beklenir, doğrula), `DAYS_EMPLOYED` anomalisi, bellek. Paralelde **L1** arama protokolü.

## Değişiklik kaydı

| Tarih | Değişiklik |
|---|---|
| 2026-10-05/06 | Adım 1–5 (iskelet, Git, GitHub, venv, veri) |
| 2026-11-20 | Belge paketi depoya alındı; takvim (sunum 7 Aralık) eklendi; çalışma biçimi öğretmen-eş çalışan olarak güncellendi |
