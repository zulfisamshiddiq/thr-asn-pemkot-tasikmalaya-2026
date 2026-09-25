# ============================================================
# Dashboard Sentimen Publik — THR ASN Pemkot Tasikmalaya 2026
# ============================================================

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import STOPWORDS, WordCloud


# ============================================================
# Konfigurasi halaman
# ============================================================

st.set_page_config(page_title="Sentimen Publik THR ASN — Kota Tasikmalaya", layout="wide",)


# ============================================================
# Path dataset dan model
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "datasets" / "05_absa.xlsx"
METRICS_PATH = BASE_DIR.parent / "models" / "metrics.json"


# ============================================================
# Stopwords
# ============================================================

BASE_STOPWORDS = set(STOPWORDS)
BASE_STOPWORDS.update({
    'bp', 'pa', 'nu', 'ge', 'anu', 'bu', 'teu', 'mah', 'weh', 'abi', 'kang',
    'si', 'krna', 'ah', 'gak', 'gk', 'atuh', 'geus', 'kan', 'jeung', 'ttp',
    'oge', 'te', 'tuh', 'yaa', 'sih', 'yang', 'lho', 'ek', 'boa', 'kn', 'di',
    'keur', 'ka', 'ari', 'da', 'wae', 'usah', 'jd', 'asa', 'ges', 'mh',
    'dong', 'tah', 'et', 'ku', 'tp', 'ti', 'aja', 'ieu', 'ke', 'pada', 'ga',
    'biar', 'pk', 'dll', 'lah', 'tos', 'tdk', 'klo', 'ya', 'itu', 'sll',
    'sblm', 'dah', 'teh', 'nya', 'sdh', 'loh', 'n', 'jas', 'rb', 'dn', 'jga',
    'jln', 'jg', 'pisan', 'cik', 'keneh', 'gening', 'deui', 'se', 'sm',
    'smg', 'skr', 'udh', 'nih', 'tgl', 'p', 'g', 'h', 'l', 'i', 'x', 'pp',
    'pw', 'ath', 'ter', 'klu', 'dr',
})

VECTORIZER_STOPWORDS = list(BASE_STOPWORDS)


# ============================================================
# Load data
# ============================================================

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH)
    return df

@st.cache_data
def load_metrics() -> dict | None:
    if not METRICS_PATH.exists():
        return None

    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        f"File dataset tidak ditemukan di `{DATA_PATH}`. "
        "Pastikan `05_absa.xlsx` ada di folder `datasets/`."
    )

    st.stop()
metrics = load_metrics()


# ============================================================
# Header
# ============================================================

st.title("Analisis Sentimen Publik — THR ASN Pemkot Tasikmalaya")
st.caption(
    "Analisis komentar publik dari Instagram, TikTok, dan Facebook terkait "
    "isu pencairan THR ASN. Dashboard ini hanya menampilkan visualisasi "
    "agregat — tidak ada tabel data mentah atau identitas penulis komentar."
)


# ============================================================
# Ringkasan jumlah data
# ============================================================

n_total = len(df)
n_positif = (df["sentiment"].str.lower() == "positif").sum()
n_negatif = (df["sentiment"].str.lower() == "negatif").sum()

col1, col2, col3 = st.columns(3)

# Mencegah pembagian dengan 0 jika data kosong (misal, file dataset baru dibuat tapi belum diisi)
if n_total > 0:
    persen_negatif = 100 * n_negatif / n_total
    persen_positif = 100 * n_positif / n_total
else:
    persen_negatif = 0
    persen_positif = 0

col1.metric("Total komentar dianalisis", f"{n_total:,}")
col2.metric("Sentimen negatif", f"{n_negatif:,}", f"{persen_negatif:.1f}%")
col3.metric("Sentimen positif", f"{n_positif:,}", f"{persen_positif:.1f}%")

st.divider()

# ============================================================
# Tabs
# ============================================================

tab_names = [
    "Distribusi Platform",
    "Distribusi Sentimen",
    "Wordcloud",
    "Frekuensi Kata",
    "Sentimen per Aspek",
]

if metrics is not None:
    tab_names.append("Performa Model")

tabs = st.tabs(tab_names)


# ============================================================
# TAB 1: Distribusi Platform
# ============================================================

with tabs[0]:
    st.subheader("Distribusi Komentar per Platform")
    platform_counts = df["platform"].value_counts()
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie(
        platform_counts.values,
        labels=platform_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        textprops={"fontsize": 11},
    )

    ax.set_title("Proporsi Sumber Komentar", fontweight="bold")
    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# TAB 2: Distribusi Sentimen
# ============================================================

with tabs[1]:
    st.subheader("Distribusi Sentimen Komentar")
    sentiment_counts = df["sentiment"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        hue=sentiment_counts.index,
        palette={
            "Negatif": "#d62728",
            "Positif": "#2ca02c"
        },

        legend=False,
        ax=ax,
    )

    total = sentiment_counts.sum()

    for i, count in enumerate(sentiment_counts.values):
        pct = 100 * count / total
        ax.text(
            i,
            count + total * 0.01,
            f"{count}\n({pct:.1f}%)",
            ha="center",
            fontsize=10,
        )

    ax.set_xlabel("Sentimen")
    ax.set_ylabel("Jumlah Komentar")
    ax.set_title("Distribusi Sentimen Komentar", fontweight="bold")

    # Beri ruang untuk angka di atas batang
    ax.set_ylim(0, max(sentiment_counts.values) * 1.15)
    st.pyplot(fig)
    plt.close(fig)
    st.caption(
        "Catatan: kelas netral sudah dikeluarkan dari data ini mengikuti "
        "arahan pemilik perusahaan — lihat README repo untuk detail."
    )


# ============================================================
# TAB 3: Wordcloud
# ============================================================

with tabs[2]:
    st.subheader("Wordcloud")
    pilihan = st.selectbox(
        "Tampilkan wordcloud untuk:",
        ["Semua (General)", "Positif", "Negatif"],
    )
    if pilihan == "Semua (General)":
        text_data = (df["normalisasi_kata"].dropna().astype(str))
        colormap = "viridis"
    else:
        text_data = (df.loc[df["sentiment"].str.lower() == pilihan.lower(),"normalisasi_kata"].dropna().astype(str))
        colormap = ( "Greens" if pilihan == "Positif" else "Reds")

    teks_gabungan = " ".join(text_data)

    if teks_gabungan.strip():
        wc = WordCloud(
            width=1400,
            height=500,
            background_color="white",
            stopwords=BASE_STOPWORDS,
            max_words=1000,
            colormap=colormap,
            prefer_horizontal=0.9,
            relative_scaling=0.5,
            min_font_size=8,
            max_font_size=120,
        ).generate(teks_gabungan)

        fig, ax = plt.subplots(figsize=(14, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Tidak ada data untuk kategori ini.")


# ============================================================
# TAB 4: Frekuensi Kata
# ============================================================

with tabs[3]:
    st.subheader("Frekuensi Kata")
    col_a, col_b = st.columns(2)
    with col_a:
        sentimen_pilihan = st.selectbox(
            "Sentimen:",
            ["Semua (General)", "Positif","Negatif"],
            key="freq_sent",
        )
    with col_b:
        ngram_pilihan = st.radio(
            "Jenis n-gram:",
            ["Unigram", "Trigram"],
            horizontal=True,
        )

    top_n = st.slider("Jumlah kata teratas:", 5, 25, 15)

    # Filter berdasarkan sentimen
    if sentimen_pilihan == "Semua (General)":
        text_data = (df["normalisasi_kata"].dropna().astype(str))
    else:
        text_data = (
            df.loc[df["sentiment"].str.lower() == sentimen_pilihan.lower(), "normalisasi_kata"
            ].dropna().astype(str)
        )

    # N-gram
    if ngram_pilihan == "Unigram":
        ngram_range = (1, 1)
        token_pattern = (r"(?u)\b[a-zA-Z][a-zA-Z]+\b")
    else:
        # Trigram
        ngram_range = (3, 3)
        token_pattern = None

    vec_kwargs = dict(
        ngram_range=ngram_range,
        stop_words=VECTORIZER_STOPWORDS,
    )

    if token_pattern:
        vec_kwargs["token_pattern"] = token_pattern

    # Proses frekuensi
    if (
        not text_data.empty
        and text_data.str.strip().any()
    ):

        vectorizer = CountVectorizer(**vec_kwargs)
        X = vectorizer.fit_transform(text_data)
        if len(vectorizer.get_feature_names_out()) > 0:
            # Semua frekuensi kata
            all_freq_df = pd.DataFrame({
                "kata": vectorizer.get_feature_names_out(),
                "frekuensi": X.sum(axis=0).A1,
            }).sort_values("frekuensi", ascending=False,)
            # Ambil Top N
            freq_df = all_freq_df.head(top_n).copy()
            # Persentase (berdasarkan total frekuensi seluruh kata)
            total_frekuensi = (all_freq_df["frekuensi"].sum())
            freq_df["persentase"] = (freq_df["frekuensi"] / total_frekuensi * 100)


            # Grafik
            fig, ax = plt.subplots(figsize=(11, max(4, top_n * 0.40)))
            bars = ax.barh(freq_df["kata"], freq_df["frekuensi"], color="steelblue",)
            ax.invert_yaxis()

            # Label di ujung batang (angka dan persen)
            labels = [
                f"{int(freq)} ({pct:.1f}%)"
                for freq, pct
                in zip(freq_df["frekuensi"], freq_df["persentase"],)
            ]

            ax.bar_label(
                bars,
                labels=labels,
                padding=5,
                fontsize=9,
            )

            ax.set_xlabel("Frekuensi")
            ax.set_ylabel("Kata / N-gram")
            ax.set_title(
                f"Top {top_n} {ngram_pilihan} — "
                f"{sentimen_pilihan}",
                fontweight="bold"
            )

            # Beri ruang di sebelah kanan
            max_freq = freq_df["frekuensi"].max()
            ax.set_xlim(0,max_freq * 1.20)

            # Grid horizontal agar lebih mudah dibaca
            ax.grid(axis="x", linestyle="--", alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info(
                "Tidak ada kata informatif "
                "untuk kombinasi ini."
            )
    else:
        st.info("Tidak ada data untuk kombinasi ini.")


# ============================================================
# TAB 5: Sentimen per Aspek (ABSA)
# ============================================================

with tabs[4]:
    st.subheader("Distribusi Sentimen per Aspek")
    if "keyword" in df.columns:
        # Jumlah komentar berdasarkan aspek dan sentimen
        pivot = (df.groupby(["keyword", "sentiment"]).size().unstack(fill_value=0))
        # Pastikan urutan kolom sentimen konsisten
        kolom_sentimen = [
            kolom for kolom in ["Negatif", "Positif"]
            if kolom in pivot.columns
        ]

        pivot = pivot[kolom_sentimen]

        # Grafik
        fig, ax = plt.subplots(figsize=(11, 6))
        pivot.plot(
            kind="bar",
            ax=ax,
            color=[
                "#d62728",
                "#2ca02c"
            ],
        )

        # Tambahkan jumlah dan persentase
        for container in ax.containers:
            labels = []

            for bar in container:
                tinggi = bar.get_height()
                if tinggi > 0:
                    # Posisi aspek pada sumbu X
                    posisi = int(round(bar.get_x() + bar.get_width() / 2))
                    # Total komentar pada aspek
                    total_aspek = (pivot.iloc[posisi].sum())
                    # Persentase sentimen
                    persentase = (tinggi / total_aspek * 100)
                    labels.append(
                        f"{int(tinggi)}\n"
                        f"({persentase:.1f}%)"
                    )
                else:
                    labels.append("")
            ax.bar_label(
                container,
                labels=labels,
                padding=4,
                fontsize=8,
            )

        # Pengaturan grafik
        ax.set_title("Distribusi Sentimen berdasarkan Aspek", fontweight="bold")
        ax.set_xlabel("Aspek")
        ax.set_ylabel("Jumlah Komentar")
        plt.xticks(rotation=30,ha="right")
        ax.legend(title="Sentimen")
        # Beri ruang untuk label di atas batang
        nilai_maksimum = (pivot.max().max())
        ax.set_ylim(0,nilai_maksimum * 1.18)
        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.3,
        )
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info(
            "Kolom `keyword` (hasil ABSA) "
            "tidak ditemukan di dataset."
        )


# ============================================================
# TAB 6: Performa Model
# ============================================================

if metrics is not None:
    with tabs[5]:
        st.subheader("Perbandingan Performa Model")
        st.caption(
            "Model dipilih berdasarkan macro F1, bukan accuracy — data "
            "sentimen ini imbalanced (kelas negatif jauh lebih banyak), "
            "sehingga accuracy tinggi bisa menutupi performa buruk pada "
            "kelas positif."
        )

        # Data performa model
        metric_df = (
            pd.DataFrame(metrics).T
            .sort_values("macro_f1", ascending=False)
        )

        # Grafik
        fig, ax = plt.subplots(figsize=(11, 6))
        x = range(len(metric_df))
        width = 0.35

        # Bar Accuracy
        bars_accuracy = ax.bar(
            [i - width / 2 for i in x],
            metric_df["accuracy"],
            width,
            label="Accuracy",
        )

        # Bar Macro F1
        bars_macro_f1 = ax.bar(
            [i + width / 2 for i in x],
            metric_df["macro_f1"],
            width,
            label="Macro F1",
        )

        # Label Accuracy
        labels_accuracy = [
            f"{value:.1%}"
            for value
            in metric_df["accuracy"]
        ]

        ax.bar_label(
            bars_accuracy,
            labels=labels_accuracy,
            padding=4,
            fontsize=9,
        )

        # Label Macro F1
        labels_macro_f1 = [
            f"{value:.1%}"
            for value
            in metric_df["macro_f1"]
        ]

        ax.bar_label(
            bars_macro_f1,
            labels=labels_macro_f1,
            padding=4,
            fontsize=9,
        )

        # Pengaturan sumbu X dan y
        ax.set_xticks(list(x))
        ax.set_xticklabels(metric_df.index, rotation=30, ha="right",)
        ax.set_ylim(0, 1.18)
        ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0,])
        ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%",])
        ax.set_ylabel("Persentase")
        ax.set_xlabel("Model")
        ax.legend(title="Metrik")
        ax.set_title("Accuracy vs Macro F1 per Model", fontweight="bold")

        # Grid horizontal
        ax.grid(axis="y", linestyle="--", alpha=0.3,)

        # Layout agar tidak terpotong
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # Model terbaik berdasarkan Macro F1
        best_model = (metric_df["macro_f1"].idxmax())
        best_macro_f1 = (metric_df.loc[best_model,"macro_f1"])
        best_accuracy = (metric_df.loc[best_model,"accuracy"])
        st.success(
            f"Model dengan macro F1 tertinggi: "
            f"{best_model} — "
            f"Macro F1: {best_macro_f1:.1%}, "
            f"Accuracy: {best_accuracy:.1%}"
        )



# ============================================================
# Footer
# ============================================================

st.divider()
st.caption(
    "Model klasifikasi sentimen di repo ini dilatih khusus untuk komentar "
    "terkait THR ASN Kota Tasikmalaya (Bahasa Indonesia dengan campuran Sunda). "
    "Prediksi untuk topik atau domain lain kemungkinan tidak akurat — lihat "
    "penjelasan lengkap soal keterbatasan portability disetiap readme"
)