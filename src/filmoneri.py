import pandas as pd

# 1. Filmleri oku
film_df = pd.read_csv("../data/ml-100k/u.item", sep="|", encoding="latin-1", header=None)
film_df = film_df[[0, 1]]
film_df.columns = ["film_id", "film_adi"]

# 2. Oy verilerini oku
oy_df = pd.read_csv("../data/ml-100k/u.data", sep="\t", header=None)
oy_df.columns = ["kullanici_id", "film_id", "puan", "timestamp"]

# 3. Film isimleriyle puanları birleştir
veri = pd.merge(oy_df, film_df, on="film_id")

# 4. Kullanıcı-film puan matrisi oluştur
puan_matrisi = veri.pivot_table(index="kullanici_id", columns="film_adi", values="puan")

# 5. Film öneri fonksiyonu
def film_oner(film_adi, min_oy_sayisi=50):
    try:
        # Film için puanları al
        film_puanlari = puan_matrisi[film_adi]

        # Korelasyonu hesapla
        benzerlikler = puan_matrisi.corrwith(film_puanlari)

        # Sonuçları DataFrame'e dönüştür
        benzer_filmler = pd.DataFrame(benzerlikler, columns=["korelasyon"])
        benzer_filmler.dropna(inplace=True)

        # Puan sayılarını hesapla
        puan_sayilari = veri.groupby("film_adi")["puan"].count()
        benzer_filmler["oy_sayisi"] = puan_sayilari

        # Minimum oy filtresi uygula ve sırala
        filtreli = benzer_filmler[benzer_filmler["oy_sayisi"] >= min_oy_sayisi]
        sonuc = filtreli.sort_values("korelasyon", ascending=False)
        sonuc = sonuc[sonuc.index != film_adi]  # Seçili filmi hariç tut
        sonuc = sonuc.reset_index()

        return sonuc.head(10)
    except KeyError:
        print(f"[HATA] Seçilen film adı bulunamadı: {film_adi}")
        return pd.DataFrame()

# Film listesi
film_listesi = sorted(puan_matrisi.columns)
