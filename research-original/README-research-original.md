# **research-original**

Versi riset **asli** analisis sentimen publik terhadap pencairan THR ASN
Pemkot Tasikmalaya. Versi ini yang sudah di-ACC oleh tim manajemen, diunggah ke Instagram
dan dimuat di media priangan.com.

File ini disimpan apa adanya untuk transparansi/audit trail — **bukan** rekomendasi
metodologi untuk dikembangkan lebih lanjut. Untuk pipeline yang lebih rapi dan
terdokumentasi, lihat [`../research-refactored/`](../research-refactored/README.md).

## Isi Folder

```
research-original/
├── main.ipynb             # Seluruh pipeline: EDA, preprocessing, labeling, visualisasi,
│                          # ASBA sederhana, DAN riset lain (kepuasan kinerja Pemkot/Pemda)
│                          # yang tercampur dalam satu notebook
├── data/
│   ├── dataset_facebook-comments-scraper_2026-03-18_21-19-55-636.xlsx        # Hasil scraping komentar facebook
│   ├── dataset_instagram-comment-scraper_2026-03-18_22-30-04-045.xlsx        # Hasil scraping komentar instagram
│   ├── dataset_tiktok-comments-scraper_2026-03-18_21-17-10-607.xlsx          # Hasil scraping komentar tiktok
│   ├── dataset_thr.xlsx                                                      # Gabungan 3 platform + data tambahan hasil
│   │                                                                         # copy-paste manual pada data instagram (digabung & dibersihkan di Excel,
│   │                                                                         # bukan di notebook)
│   ├── thr_stemming.xlsx                                                     # Hasil setelah stemming
│   ├── df_clean_thr.xlsx                                                     # Data bersih siap label
│   ├── df_labeled_thr.xlsx                                                   # Data setelah diberi label sentimen (IndoBERT)
│   ├── df_labeled_thr (1).xlsx                                               # Duplikat/versi lain hasil labeling
│   ├── df_labeled_thr_2.xlsx                                                 # Duplikat/versi lain hasil labeling
│   └── text_stemming.csv
├── image_thr/                                                                # Output visualisasi (pie chart platform, distribusi sentimen,
│                                                                             # wordcloud positif/negatif/netral, wordcloud kata "lari")
└── *.jpg (1.jpg–14.jpg)                                                      # Bahan konten instagram perusahaan
```

## Dampak & Publikasi

Hasil riset ini dipresentasikan ke manajemen perusahaan dan diliput oleh media
regional:

> [89% Sentimen Negatif Soal THR ASN, Wali Kota Tasikmalaya Disorot Tajam di
> Media Sosial](https://priangan.com/89-sentimen-negatif-soal-thr-asn-wali-kota-tasikmalaya-disorot-tajam-di-media-sosial/) —
> Priangan.com, 20 Maret 2026.

> ⚠️ **Catatan penting soal angka di artikel vs. angka di notebook ini**
> Artikel menyebut **89,1% negatif, 10,9% positif**. Notebook `main.ipynb` di
> folder ini menghasilkan distribusi **3 kelas**: negatif 1.087 (61,8%), netral
> 540 (30,7%), positif 133 (7,6%) dari 1.760 komentar berlabel. Kedua angka ini
> **tidak langsung sebanding** karena basis perhitungannya berbeda: angka di
> artikel didapat dengan **mengeluarkan kelas netral** dari data lalu menghitung
> ulang proporsi hanya dari sisa data negatif+positif:
>
> - 1.087 ÷ (1.087 + 133) = 89,1% → negatif
> - 133 ÷ (1.087 + 133) = 10,9% → positif
>
> Kelas netral dikeluarkan dari analisis atas arahan dari manajemen
> bukan keputusan teknis peneliti. Perlu ditekankan juga publikasi
> ini bukan sebagai referensi teknis yang dijadikan landasan untuk mengembangkan
> riset yang serupa di tempat dan di waktu yang berbeda. Hasil publikasi ini
> bertujuan untuk memberitahukan kepada para pemangku kebijakan bahwa terdapat masyarakat
> yang terdampak terhadap kebijakan yang diambil. Dengan demikian, hasil riset
> ini dapat menjadi penyampaian kritik dan saran dari publik kepada para
> pemangku kebijakan sebagai salah satu bahan evaluasi dengan harapan publik untuk
> kebijakan selanjutnya disesuaikan dengan kebutuhan dan keadaan publik
> dan dilaksanakan secara transparan.
> Informasi tambahan, antara notebook dengan hasil publikasi keduanya konsisten,
> hanya basis pembaginya berbeda (1.760 data vs. 1.220 data setelah kelas netral dibuang).
> Total komentar yang disebut di artikel (~1.854) merujuk pada jumlah data
> mentah hasil scraping (`data/dataset_thr.xlsx`, sebelum pembersihan missing
> value), bukan jumlah data yang akhirnya diberi label sentimen (1.760).

## Ringkasan Pipeline

1. **Load & cleaning**: baca `dataset_thr.xlsx`, hapus missing value.
2. **Preprocessing teks**: cleaning regex (mention, hashtag, URL, karakter
   non-alfabet) → case folding → normalisasi slang (kamus manual campuran
   Indonesia/Sunda) → tokenisasi → stopword removal (Sunda-aware, negasi
   dipertahankan) → stemming (Sastrawi).
3. **Labeling**: dilakukan **di luar notebook ini**, di Google Colab, menggunakan
   model **IndoBERT**. Hasil label di-export ke `df_labeled_thr.xlsx` lalu
   di-import kembali ke Jupyter Lab. **Kode labeling di Colab tidak tersedia
   di repo ini** — sesi Colab ter-reset dan tidak sempat disimpan.
4. **Visualisasi**: distribusi platform (pie chart), distribusi sentimen (bar
   chart, 3 kelas: positive/neutral/negative), wordcloud per kelas sentimen,
   pencarian frekuensi kata kunci manual (mis. "lari", "run", "jogging").
5. **Analisis topik per wilayah**: n-gram (bigram/trigram) per wilayah pemerintahan
   — bagian ini sebenarnya termasuk proyek riset lain (lihat catatan di bawah).

## Keterbatasan & Catatan Metodologis (penting dibaca)

Pada saat melakukan riset, SDM belum memenuhi standard kelayakan hail riset
untuk bisa dijadikan sebagai referensi metodologis. Seperti yang disampaikan diatas,
hasil riset ini bertujuan untuk menyampaikan kepada pemangku kebijakan bahwa dari
kebijakan pencairann THR ASN ini terdapat kritik dan saran (Hasil riset berada dibagian bawah).
Namun untuk meningkatkan keterbacaan, peneliti melakukan refactore proyek dengan tujuan apabila
peneliti atau pembaca melakukan riset hal yang serupa, hasil refactor ini bisa menjadi salah satu
referensi metodologis.

- **Dua proyek riset tercampur dalam satu notebook.** `main.ipynb` menggabungkan
  analisis THR ASN dengan analisis terpisah soal tingkat kepuasan publik terhadap
  kinerja Pemkot/Pemda se-Priangan Timur (kode dengan variabel `df_fix`,
  `data_wakil/df_labeled_fix_wakil.xlsx`, analisis per `government`/wilayah).
  Ini dua unit analisis yang berbeda dan seharusnya tidak berbagi notebook yang sama.
- **Sebagian data dikumpulkan manual (copy-paste ke Excel)**, bukan hasil scraping
  otomatis penuh — berpotensi bias seleksi (komentar mana yang dipilih untuk
  di-copy tidak mengikuti kriteria sampling yang terdokumentasi).
- **Penggabungan & pembersihan 3 dataset platform dilakukan manual di Excel**
  (drop kolom, merge), bukan di notebook — sehingga langkah ini tidak reproducible
  dari kode yang ada di repo.
- **Kode labeling (IndoBERT) hilang.** Karena dikerjakan di Colab dan sesinya
  ter-reset, tidak ada cara memverifikasi ulang bagaimana IndoBERT dipakai
  (prompt/threshold/preprocessing sebelum masuk model tidak terdokumentasi).
- **IndoBERT dilatih untuk teks berbahasa Indonesia, sedangkan dataset ini
  campuran Indonesia dan Sunda.** Penulis sendiri meragukan hal ini saat
  proses berjalan. Potensi mislabeling pada komentar berbahasa Sunda cukup
  yakin dan tidak divalidasi lebih lanjut (mis. lewat validasi manual/human
  annotation pada sampel).
- **Klasifikasi 3 kelas (positif/negatif/netral) diragukan validitasnya oleh
  penulis sendiri** saat riset dilakukan, tidak ada validasi independen
  (misalnya inter-annotator agreement atau spot-check manual) terhadap hasil
  IndoBERT untuk mengonfirmasi batas antar kelas, khususnya netral vs negatif.
- **Tidak ada train/test split atau model evaluation** pada tahap sentimen di
  notebook ini — labeling sepenuhnya bergantung pada output model eksternal
  (IndoBERT) tanpa lapisan verifikasi tambahan yang terlihat di kode.
- Hasil riset ini **sudah dipublikasikan secara publik** (Instagram perusahaan,
  priangan.com)

## Cara Menjalankan (jika ingin reproduksi sebagian)

Notebook ini **tidak dapat direproduksi penuh** karena:

1. Sebagian input data (`data/dataset_thr.xlsx`) sudah merupakan hasil edit manual
   di Excel, bukan output scraping mentah.
2. Tahap labeling (IndoBERT, di Colab) tidak ada kodenya di repo ini.

## Hasil Riset

Analisis ini mengkaji persepsi publik terhadap isu pemerintahan dan sosial di kota Tasikmalya berdasarkan percakapan
warganet yang dihimpun dari tiga media sosial, yaitu Facebook, Instagram, dan Tiktok yang berjumlah 1.854 data komentar.
Media sosial menjadi ruang evaluasi terbuka tempat masyarakat menyampaikan aspirasi sekaligus kritik dan saran terhadap
kebijakan dan realisasi program pemerintah. Dalam periode pengamatan, diskusi publik berfokus pada persoalan THR
(Tunjangan Hari Haraya) idulfitri yang belum didistribusikan secara menyeluruh. Secara umum percakapan publik mencerminkan
tingginya perhatian masyarakat terhadap isu yang berdampak langsung pada kehidupan dan kebutuhan sehari-hari, sekaligus
menunjukkan ekspektasi yang kuat terhadap kesejahteraan dan hak sebagai ASN terpenuhi.

#### Wordcloud Sentimen Positif

- Kata “thr”, “gaji”, “cair”, “rakyat”, “hak”, “asn”, “paruh” dan “masyarakat” sebagai fokus utama pada pencairan hak ASN dan melibatkan masyarakat secara inklusif.
- Kemudian kata “moga”, “allah”, “amin”, dan “alhamdulillah” mengekspresikan doa dan harapan serta rasa syukur atas adanya THR meskipun dicicil atau bahkan telat dalam pencairan.
- Kemunculan kata “walikota”, “wali”, dan “pimpin” menunjukkan perhatian publik sekaligus harapan terhadap peran wali kota untuk segera mengatasi isu-isu ini.
- Kata “nikmat”, “syukur”, dan “hati” mencerminkan adanya rasa penerimaan atas isu pencairan THR meskipun belum dilakukan secara merata dan dicicil. Masyarakat masih memiliki harapan dan kepercayaan terhadap tindakan responsif dari wali kota.

#### Wordcloud Sentimen Negatif

- Kata “thr”, “belum”, “tidak”, dan “cair” menunjukkan dominasi keluhan terkait THR yang belum dibayarkan atau mengalami keterlambatan.
- Kemunculan kata “kota”, “tasik”, “pemda”, “daerah”, serta nama wali kota “viman”/”alfarizi” menunjukkan kritik yang diarahkan kepada wali kota secara langsung sebagai pihak yang bertanggung jawab.
- Kata “tidak”, “adil”, “jangan”, dan “parah” mencerminkan persepsi ketidakadilan serta kekecewaan masyarakat terhadap kebijakan pencairan THR. - Meskipun ada kata “adil”, bisa terklarifikasi sebagai potongan kalimat dari tidak adil atau yang lainnya.
- Kemunculan kata “bohong”, “lucu”, “rusak”, serta “nakes” dan “rsud” menunjukkan adanya sentimen negatif yang meluas, baik berupa ketidakpercayaan, sindiran, maupun keluhan dari publik yang memerhatikan kepada golongan tenaga kesehatan.

Secara umum publik mengeluhkan terkait pendistribusian THR ASN yang telat dan dilakukan secara bertahap. Hal ini berdampak langsung terhadap keadaan sosial dan ekonomi pegawai ASN karena menjelang Hari Raya Idul Fitri kebutuhan semakin meningkat. Ditengah-tengah isu THR ASN, sebagian masyarakat juga menyentuh pembahasan mengenai fasilitas atau kondisi fisik infrastruktur kota Tasikmalaya yang berfokus pada keadaan jalan sebagai jalur akomodasi masyarakat demi kelancaran melaksanakan aktivitas sehari-hari yang dapat mempengaruhi keadaan ekonomi dan pendidikan di kota Tasikmalaya.

Pada dasarnya, sentimen publik tidak mempermasalahkan terkait aktivitas atau hobi yang dilakukan oleh wali kota. Namun sebaliknya, masyarakat justru menyindir salah satu aktivitas wali kota sebagai pelari karena publik menilai wali kota terlalu sibuk lari atau bahkan mengikuti event-event lari. Jika dapat diseimbangi dengan manajerial kepemimpinan yang transparan dan berdampak terhadap masayarakat, aktivitas wali kota yang seringkali melakukan olahraga lari begitupun dengan masyarakat kota Tasikmalaya yang banyak memiliki hobi olahraga serupa, seharusnya ini menjadi momentum untuk meningkatkan humanisme dan keakraban antara wali kota dengan masyarakat sehingga akan tercipta pembanguan daerah yang saling menguntungkan bagi pemerintah dan masyarakat itu sendiri.

#### Harapan konektivitas vs kepercayaan publik: transparansi dan jadwal pendistribusian yang konkret

Keterlambatan pendistribusian THR memicu dinamika persepsi di ruang publik. Kebutuhan masyarakat menjelang Hari Raya Idul Fitri meningkat dan tidak selaras dengan pendistribusinya THR yang belum jelas kapan didistribusikan secara menyeluruh.

#### Pandangan penerimaan

Sebagian memilih bersabar dan menunggu kejelasan bahkan tidak terlalu mempermasalahkan pendistribusian THR, yang penting 100% didistribusikan meskipun secara bertahap

#### Pandangan penolakan

Publik menolak pendistribusian THR secara bertahap dan distribusikan sepenuhnya setelah Hari Raya Idul Fitri karena kebutuhan sebelum Hari Raya meningkat.

#### Dampak

- Kehilangan Kepercayaan Publik: Ketidakjelasan pendistribusian THR ini memicu reaksi publik terhadap transparansi wali kota sebagai figur pemimpin yang bertanggung jawab secar langsung.
- Reputasi Pemerintah Lokal: Tanpa adanya transparansi yang konkret, publik memberikan sentimen yang mayoritas kecewa kepada wali kota
- Preseden Tata Kelola: Kekhawatiran bahwa masalah transparansi yang berimplikasi kepada kepercayaan masyarakat pada program yang akan dilaksanakan
