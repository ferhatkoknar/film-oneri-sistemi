# Film Öneri Sistemi

Bu proje, kullanıcıların seçtiği bir filme benzeyen filmleri öneren bir Streamlit uygulaması sunar. Uygulama, film açıklamaları, posterleri ve Türkçe çevirileri ile kullanıcı deneyimini zenginleştirir.

## Kurulum

Bu projeyi çalıştırabilmek için aşağıdaki adımları takip edin:

1. **Gerekli Kütüphaneleri Yükleyin:**

    Projeyi çalıştırmak için gerekli olan Python kütüphanelerini yüklemek için şu komutu kullanın:

    ```bash
    pip install -r requirements.txt
    ```

2. **Uygulamayı Çalıştırın:**

    Streamlit uygulamasını başlatmak için aşağıdaki komutu kullanın:

    ```bash
    streamlit run src/app.py
    ```

3. **Veri Seti:**

    Veri seti, [MovieLens 100k](https://grouplens.org/datasets/movielens/100k/) veri setinden alınmıştır. Lütfen bu veriyi indirip `data/ml-100k/` klasörüne yerleştirin.

## Kullanım

- İzlediğiniz bir filmi seçin.
- **Benzer Filmleri Göster** butonuna tıklayın.
- Sistem, seçtiğiniz filme benzeyen filmleri önerir ve posterlerle birlikte gösterir.

## Lisans

MIT Lisansı
