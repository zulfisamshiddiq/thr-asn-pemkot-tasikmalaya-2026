# **research-refactored**

Versi **refactor** dari analisis sentimen publik terhadap pencairan THR ASN
Pemkot Tasikmalaya. Dibuat menggunakan dataset mentah yang sama dengan
[`../research-original/`](../research-original/README.md), tetapi dengan pipeline
yang dipecah menjadi notebook bernomor, terstruktur, dan (sebagian besar) reproducible
dalam satu environment.

**Versi ini tidak diperuntukan menggantikan publikasi resmi** — hasil yang sudah dipublikasikan
tetap versi `research-original`. Folder ini dibuat untuk dasar pengembangan lanjutan dan sebagai
salah satu referensi dari sisi teknis atau pipeline. Namun, apabila pembaca memiliki kritik dan saran
dapat disampaikan kepada peneliti dan atau jika ingin mengembangnkan lebih lanjut untuk kebutuhan
yang serupa dapat didonwload langsung.

## Isi folder

```
research-refactored/
├── notebooks/
│   ├── 01_eda.ipynb              # Load 3 dataset mentah + hasil gabungan manual,
│   │                             # missing value & duplikat check, distribusi platform,
│   │                             # analisis kata kunci awal
│   ├── 02_preprocessing.ipynb    # Cleaning (URL/HTML/emoji/simbol/username),
│   │                             # case folding, normalisasi kata tidak baku
│   │                             # (kamus GitHub + tambahan manual), tokenizing,
│   │                             # stopword removal, stemming (Sastrawi)
│   ├── 03_labeling.ipynb         # Labeling LAXICON (kamus InSet positif/negatif),
│   │                             # BUKAN IndoBERT — lihat catatan metodologi di bawah
│   ├── 04_visualization.ipynb    # Wordcloud, frekuensi unigram & trigram per sentimen
│   ├── 05_absa.ipynb             # Aspect-Based Sentiment Analysis sederhana
│   │                             # (rule-based keyword matching: THR, ASN,
│   │                             # Kinerja Pemkot, Infrastruktur, Lainnya)
│   └── 06_modeling.ipynb         # Klasifikasi teks: SVM, KNN, Naive Bayes,
│                                 # Random Forest, Decision Tree, Neural Network (MLP),
│                                 # Logistic Regression — dievaluasi terhadap label
│                                 # hasil laxicon (lihat catatan di bawah)
├── datasets/                     # Checkpoint data antar tahap (01_eda.xlsx →
│                                 # 02_preprocessing.xlsx → 03_labeling.xlsx →
│                                 # 05_absa.xlsx), plus dataset mentah asli
└── img/                          # Semua output visualisasi bernomor sesuai notebook
                                  # asalnya (mis. "04 wc_positif.png")
```

Penamaan `01_eda` → `06_modeling` mengikuti urutan tahapan pipeline data science
standar (EDA → preprocessing → labeling → visualisasi → analisis lanjutan →
modeling). Pola ini supaya lebih mudah dipahami oleh pembaca pemula seperti peneliti
dengan background non IT yang sempat mengalami kendala cara memahami tahapan pipline data science.

## Perbedaan Metodologis dari _research-original_ — WAJIB dibaca

**Perbedaan hasil antara versi original dan refactored tidak hanya terletak pada jumlah kelas (3→2).**
Ada dua perubahan besar:

1. **Jumlah kelas**: 3 kelas (positif/negatif/netral) → 2 kelas (positif/negatif).
   Pada _research-original_ peneliti mendapatkan arahan dari manajemen tidak menggunakan
   kelas netral pada analisis. Dengan demikian, hasil risetnya menggunakan data sentimen
   positif dan negatif. Pada _research-refactored_ ini peneliti melakukan labeling 2 kelas
   (positif/negatif) berdasarkan kebutuhan pada _research-originial_.
2. **Metode labeling berubah total, secara sengaja**: _original_ memakai
   **IndoBERT** (model klasifikasi berbasis transformer, dilatih pada korpus
   besar, menghasilkan 3 kelas); _refactored_ memakai **pendekatan laxicon**
   (kamus InSet — menghitung selisih jumlah kata positif dan kata negatif per
   komentar). Ini bukan "versi rapi" dari metode yang sama — dua metode ini
   punya asumsi dan sumber error yang berbeda sama sekali.

   Pemilihan metode laxicon ini adalah **keputusan sadar**, bukan akibat
   hilangnya kode IndoBERT dari `research-original` (kode itu memang hilang
   karena dikerjakan di Colab dan sesinya ter-reset, tapi itu bukan alasan
   penggantian metode). Metode laxicon dipilih berdasarkan referensi yang
   merekomendasikannya untuk kasus klasifikasi 2 kelas — sejalan dengan arahan
   dari manajemen supaya hasil akhir hanya memuat sentimen positif dan negatif.

   Meski demikian, bagi siapa pun yang ingin membandingkan performa
   "before/after refactor", **perbandingan ini tetap tidak apple-to-apple**:
   perbedaan distribusi sentimen dan akurasi antar kedua versi mencerminkan
   gabungan dari
   (a) penyederhanaan 3→2 kelas
   (b) perbedaan metode labeling — bukan murni efek "merapikan kode dengan metode yang sama".

## Ringkasan Pipeline

1. **EDA** (`01_eda.ipynb`): load dataset scraping mentah per platform + dataset
   gabungan hasil edit manual di Excel (`dataset_thr.xlsx` — sama seperti yang
   dipakai di `research-original`), cek missing value & duplikat, distribusi
   komentar per platform, analisis kemunculan kata kunci awal.
2. **Preprocessing** (`02_preprocessing.ipynb`): pipeline cleaning teks lengkap
   → normalisasi kata tidak baku (kamus dari GitHub `analisis25/data_kamus_tb`,
   ~8.867 entri, plus tambahan manual untuk istilah lokal Sunda) → tokenizing →
   stopword removal (NLTK Indonesian) → stemming (Sastrawi).
3. **Labeling** (`03_labeling.ipynb`): Laxicon InSet (`fajri91/InSet`),
   `skor = jumlah kata positif − jumlah kata negatif`
   skor ≤ 0 = Negatif
   skor > 0 = Positif
4. **Visualisasi** (`04_visualization.ipynb`): wordcloud per sentimen, frekuensi
   unigram & trigram per sentimen.
5. **ABSA** (`05_absa.ipynb`): pelabelan aspek berbasis keyword-matching manual
   (5 aspek: THR, ASN, Kinerja Pemkot, Infrastruktur, Lainnya), lalu distribusi
   sentimen per aspek.
6. **Modeling** (`06_modeling.ipynb`): 7 algoritma klasik dibandingkan
   (CountVectorizer + SVM/KNN/Naive Bayes/Random Forest/Decision
   Tree/MLP/Logistic Regression), evaluasi via accuracy, classification report,
   confusion matrix. Model terbaik (dipilih berdasarkan macro F1, bukan
   accuracy — lihat "Model artifacts & portability" di bawah) disimpan sebagai
   satu `Pipeline` (vectorizer + classifier) di folder `models/`.

## Model Artifacts & Portability

Model hasil training disimpan di `models/sentiment_pipeline_<nama_model>.joblib`
sebagai satu `sklearn.pipeline.Pipeline` (`CountVectorizer` + classifier
terpilih), bukan file model dan vectorizer terpisah — ini supaya vocabulary
yang dipakai saat inference selalu konsisten dengan saat training.

**Model ini TIDAK dirancang untuk portable ke dataset atau domain lain.**
Ini bukan keterbatasan implementasi yang bisa diperbaiki dengan mudah,
tapi sifat dasar dari pendekatan Bag-of-Words:

- `CountVectorizer` membangun vocabulary hanya dari data training. Kata yang
  tidak ada di vocabulary tersebut akan diabaikan (tidak error) saat `transform()`
  dipanggil pada teks baru — artinya model bisa tetap menghasilkan prediksi meski
  sebenarnya "buta" terhadap sebagian besar isi teks baru tersebut.
- Model dilatih pada domain sangat spesifik: isu THR ASN Tasikmalaya, bahasa
  campuran Indonesia-Sunda, periode Maret 2026. Pergeseran domain (topik lain,
  wilayah lain, rentang waktu lain) kemungkinan besar menurunkan performa
  signifikan meski sama-sama "analisis sentimen Bahasa Indonesia".
- Untuk peneliti lain yang ingin memakai pendekatan serupa pada dataset
  berbeda: yang portable adalah **pipeline/metodologisnya** (notebook
  01–06), bukan file `.joblib` yang sudah dilatih — model perlu dilatih ulang
  dari data yang dipakai.
- Pendekatan yang secara umum lebih transferable ke domain baru adalah model
  pretrained berbasis transformer (mis. IndoBERT, yang justru dipakai di
  `research-original` tapi kodenya tidak tersimpan) — representasi bahasanya
  dipelajari dari korpus besar sehingga fine-tuning ke domain baru biasanya
  membutuhkan data lebih sedikit dibanding melatih BoW+classical ML dari nol.

Cara memuat ulang model untuk inference:

```python
import joblib
pipeline = joblib.load('models/sentiment_pipeline_<nama_model>.joblib')
prediksi = pipeline.predict(["contoh teks baru di sini"])
```

## Keterbatasan Lain (di luar perbedaan dengan versi original)

- **Aturan tie-breaking condong ke Negatif.** Skor 0 (netral secara leksikal —
  jumlah kata positif dan negatif sama, termasuk komentar tanpa kata sentimen
  sama sekali) dikategorikan sebagai **Negatif**, bukan dipisah atau dibuang.
  Ini artinya distribusi kelas Negatif kemungkinan lebih besar dari yang
  "sebenarnya" secara leksikal murni, semata karena aturan threshold ini.
- **Circularity evaluasi model.** Label `sentiment` yang dipakai untuk
  melatih dan mengevaluasi model klasifikasi (tahap 06) adalah hasil dari
  laxicon InSet, bukan anotasi manusia. Artinya angka akurasi (mis. 90.9%
  untuk SVM) mengukur seberapa baik model "meniru" aturan laxicon, bukan
  seberapa akurat model terhadap sentimen sebenarnya. Untuk klaim yang lebih
  kuat, idealnya sebagian data diberi label manual oleh human annotator sebagai
  ground truth independen (dan idealnya dihitung inter-annotator agreement bila
  lebih dari satu annotator).
- **Recall kelas Positif rendah di hampir semua model** (0.15–0.69) sementara
  precision/recall kelas Negatif tinggi (>0.9) — konsisten dengan pola data
  imbalanced (Negatif jauh lebih banyak) yang tidak ditangani dengan teknik
  balancing (class weighting, oversampling/undersampling, dsb). Accuracy
  sebagai metrik utama berisiko menyesatkan di sini; macro F1 atau F1 per
  kelas lebih representatif — dan berdasarkan classification report yang sudah
  ada, macro F1 lebih rendah dari accuracy pada semua model.
- **Tools NLP berbahasa Indonesia (NLTK stopwords, Sastrawi stemmer) dipakai
  pada dataset campuran Indonesia-Sunda**, sama seperti pada versi original —
  potensi under-stemming/salah stopword-removal pada token Sunda tetap ada
  meski sudah ditambah stopword kustom Sunda secara manual.
- **ABSA berbasis keyword-matching manual**, bukan model ABSA yang dilatih —
  cukup untuk eksplorasi awal, tapi rentan terhadap keyword yang tidak lengkap
  atau ambigu (mis. kata "kota" dalam daftar keyword "Kinerja Pemkot" berpotensi
  menangkap konteks yang tidak relevan dengan kinerja pemerintah).
- **Single train/test split** (80/20, `random_state=42`), tanpa cross-validation

## Cara Menjalankan

```bash
pip install -r ../requirements.txt
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords')"
jupyter lab notebooks/
```

Jalankan notebook secara berurutan (01 → 06); setiap notebook membaca output
`.xlsx` dari notebook sebelumnya di folder `datasets/`.

## Hasil Riset

Analisis ini mengkaji persepsi publik terhadap isu pemerintahan dan sosial di kota Tasikmalya berdasarkan percakapan
warganet yang dihimpun dari tiga media sosial, yaitu Facebook, Instagram, dan Tiktok yang berjumlah 1.854 data komentar.
Media sosial menjadi ruang evaluasi terbuka tempat masyarakat menyampaikan aspirasi sekaligus kritik dan saran terhadap
kebijakan dan realisasi program pemerintah. Dalam periode pengamatan, diskusi publik berfokus pada persoalan THR
(Tunjangan Hari Haraya) idulfitri yang belum didistribusikan secara menyeluruh. Secara umum percakapan publik mencerminkan
tingginya perhatian masyarakat terhadap isu yang berdampak langsung pada kehidupan dan kebutuhan sehari-hari, sekaligus
menunjukkan ekspektasi yang kuat terhadap kesejahteraan dan hak sebagai ASN terpenuhi.
Anda dapat melihat dashboard hasil riset ini di streamlit melalui url berikut :
https://thr-asn-pemkot-tasikmalaya-2026.streamlit.app/
