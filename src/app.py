import streamlit as st

# Sayfa ayarları (ilk Streamlit komutu olmak zorunda)
st.set_page_config(page_title="Film Öneri Sistemi", page_icon="🎬", layout="wide")

# imports
import pandas as pd
import requests
from urllib.parse import quote
from filmoneri import film_oner, film_listesi  # Senin kendi modülün
from googletrans import Translator  # Google Translate kütüphanesi

from dotenv import load_dotenv
import os

# .env 
load_dotenv()

OMDB_API_KEY = os.getenv('OMDB_API_KEY')

# API anahtarını kontrol et
if not OMDB_API_KEY:
    print("API Anahtarı bulunamadı!")

# ------------------ ÜST BANNER ve AÇIKLAMA ------------------ #
st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #1f1f2e; border-radius: 10px; margin-bottom: 30px;">
        <h1 style="color: #f8f9fa;">🎬 Film Öneri Sistemi</h1>
        <p style="color: #d3d3d3; font-size: 18px;">
            İzlediğiniz bir filmi seçin, sistem size o filme benzeyen önerilerde bulunsun. <br>
            Posterler, açıklamalar ve Türkçe çevirilerle zenginleştirilmiş bu sistem sayesinde, klasik film keşifleriniz artık çok daha kolay!
        </p>
    </div>
""", unsafe_allow_html=True)

# Yardım kutucuğu
with st.expander("ℹ️ Nasıl kullanılır?"):
    st.markdown("""
    1. Aşağıdan bir film seçin.
    2. **🎯 Benzer Filmleri Göster** butonuna tıklayın.
    3. Sistem, seçtiğiniz filme benzeyen filmleri analiz ederek öneriler sunar.
    4. Her öneri, görsel ve Türkçe açıklama ile birlikte gösterilir.
    5. Gerekirse açıklamaları genişleterek tamamını okuyabilirsiniz.
    """)

# ------------------ YARDIMCI FONKSİYONLAR ------------------ #
def temizle_film_adi(film_adi):
    import re
    return re.sub(r"\s*\(.*?\)", "", film_adi).strip()

def turkceye_cevir(text):
    if text:
        translator = Translator()
        try:
            translation = translator.translate(text, src='en', dest='tr')
            return translation.text
        except Exception as e:
            st.warning(f"[ÇEVİRME HATASI] Türkçeye çevirme işlemi yapılamadı: {e}")
            return text
    return ""

def poster_getir(film_adi):
    try:
        if not isinstance(film_adi, str):
            st.warning(f"'film_adi' bir string değil: {film_adi} ({type(film_adi)})")
            return "https://via.placeholder.com/150x220?text=YOK", ""

        temiz_ad = temizle_film_adi(film_adi)
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={quote(temiz_ad)}"

        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True":
            poster_url = data.get("Poster", "https://via.placeholder.com/150x220?text=YOK")
            film_aciklama = data.get("Plot", "")
            return poster_url, film_aciklama
        else:
            st.warning(f"[!] Poster veya açıklama bulunamadı: {film_adi}. Hata: {data.get('Error')}")
            return "https://via.placeholder.com/150x220?text=YOK", ""
    except Exception as e:
        st.error(f"[HATA] {film_adi} için poster alınamadı: {e}")
        return "https://via.placeholder.com/150x220?text=YOK", ""

# ------------------ ARAYÜZ ------------------ #

# Film seçimi
film_sec = st.selectbox("🎞️ Bir film seçin:", film_listesi)

# Butona tıklanınca benzer filmleri getir
if st.button("🎯 Benzer Filmleri Göster"):
    benzer_filmler = film_oner(film_sec)
    st.markdown(f"### 🎥 **'{film_sec}'** filmine benzer öneriler:")

    for i in range(0, len(benzer_filmler), 2):
        col1, col2 = st.columns(2)

        for j, col in zip(range(i, min(i + 2, len(benzer_filmler))), [col1, col2]):
            film_adi = str(benzer_filmler.iloc[j]["film_adi"])

            poster_url, film_aciklama = poster_getir(film_adi)
            aciklama_turkce = turkceye_cevir(film_aciklama)

            with col:
                st.image(poster_url, width=200)
                st.markdown(f"**{film_adi}**")
                if aciklama_turkce:
                    with st.expander("📖 Açıklamayı Göster"):
                        st.markdown(aciklama_turkce)

# ------------------ TEST BUTONU ------------------ #
if st.checkbox("🔍 Test Et (Inception)"):
    test_poster, test_aciklama = poster_getir("Inception")
    test_aciklama_turkce = turkceye_cevir(test_aciklama)
    st.image(test_poster, caption="Test: Inception")
    if test_aciklama_turkce:
        st.markdown(f"**Açıklama:** {test_aciklama_turkce[:300]}...")
