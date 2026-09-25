# THR ASN Pemkot/Pemda Tasikmalaya — Analisis Sentimen Publik

Repository ini berisi riset analisis sentimen publik terhadap isu pencairan THR ASN
di lingkungan Pemkot Tasikmalaya dan pemerintah daerah sekitarnya (Priangan Timur),
berdasarkan komentar warganet di Instagram, TikTok, dan Facebook.

Repo ini punya **dua versi riset** yang disimpan terpisah dengan sengaja — **keduanya
dipertahankan, tidak ada yang dihapus/ditimpa** — supaya jejak proses (audit trail)
tetap terbuka:

| Folder                                                    | Status                                                                                                                                                                                | Deskripsi singkat                                                                                                                                                                                                                     |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`research-original/`](./research-original/README.md)     | Riset asli, sudah dipublikasikan (di-ACC oleh manajemen, diunggah ke Instagram perusahaan, dan dimuat di media priangan.com)                                                          | 3 kelas sentimen (positif/negatif/netral), labeling pakai IndoBERT, sebagian data dikumpulkan manual (copy-paste), workflow tersebar di Jupyter Lab + Google Colab                                                                    |
| [`research-refactored/`](./research-refactored/README.md) | Refactor internal, **tidak dipublikasikan** — dibuat untuk pengembangan pipeline yang lebih terstruktur supaya menjadi salah satu referensi jika melakukan penelitian hal yang serupa | 2 kelas sentimen (positif/negatif saja, sesuai arahan manajemen), labeling pakai metode laxicon (InSet), pipeline dipecah jadi 6 notebook bernomor, seluruh proses ada jejaknya di satu environment (tidak lagi lintas Colab/Jupyter) |

## Alasan dua Verrsi

Riset original dikerjakan sebagai proyek kerja nyata pertama penulis di bidang ini
(non-IT background, belajar pemrograman otodidak), dengan sejumlah keterbatasan teknis dan SDM
di lapangan: sebagian scraping gagal/tidak stabil sehingga sebagian data
diambil manual, labeling dilakukan di Google Colab dan sesi Colab ter-reset, serta dua topik riset
yang berbeda (THR ASN dan kepuasan kinerja Pemkot/Pemda) tercampur dalam satu notebook (`main.ipynb`).

Refactor tidak untuk mengganti hasil yang sudah publish, tapi untuk

- (a) membuat pipeline yang bisa direproduksi dan dikembangkan orang lain, dan
- (b) menjadi bahan portofolio yang lebih dipertanggungjawabkan secara
  metodologis.

> **Catatan penting soal validitas perbandingan kedua versi**
> Perbedaan hasil antara `research-original` dan `research-refactored` **tidak hanya**
> disebabkan oleh perubahan jumlah kelas (3 → 2). Metode labeling-nya juga **berbeda
> total**: original memakai model IndoBERT (klasifikasi berbasis transformer),
> sedangkan refactored memakai pendekatan leksikon (kamus InSet, skor kata
> positif−negatif). Ini dua metode yang secara mendasar berbeda, bukan versi
> "rapi" dari metode yang sama. Siapa pun yang membaca/mengembangkan repo ini
> perlu tahu bahwa kedua hasil **tidak apple-to-apple** — lihat detail di README
> masing-masing folder.

## Struktur folder

```
.
├── research-original/       # Riset asli (sudah publish) — lihat README di dalamnya
├── research-refactored/     # Refactor untuk keterbacaan — lihat README di dalamnya
├── requirements.txt         # Dependency gabungan untuk kedua versi
└── README.md                # File ini
```

## Environment & dependency

Lihat [`requirements.txt`](./requirements.txt). File ini disusun berdasarkan
import yang benar-benar dipakai di kedua notebook, **bukan** hasil `pip freeze`
langsung dari environment asli — silakan jalankan:

```bash
python --version
pip freeze > requirements.txt
```

## Disclaimer

- Riset ini bersifat eksploratif, menggunakan data komentar publik dari media
  sosial (bukan survei terstruktur), dan **bukan** riset akademik peer-reviewed.
- Keterbatasan metodologis masing-masing versi dijelaskan lengkap di README
  masing-masing folder — dibaca dulu sebelum mengutip angka dari repo ini.
