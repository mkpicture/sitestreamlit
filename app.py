import streamlit as st
import pandas as pd
import os
import requests as res
from bs4 import BeautifulSoup as bs

# Fonction de scraping avec Beautiful Soup
def scraper_pages(url, max_pages):
    p = 1
    data = []
    while p <= max_pages:
        response = res.get(url + f"?page={p}")
        if response.status_code != 200:
            st.warning(f"Erreur lors du chargement de la page {p}")
            break
        soup = bs(response.text, "html.parser")
        containers = soup.find_all("div", class_="col s6 m4 l3")
        
        for container in containers:
            try:
                prix = container.find("p", class_="ad__card-price").text.replace("CFA", "").strip()
                type_ = container.find("p", class_="ad__card-description").text.strip()
                adresse = container.find("p", class_="ad__card-location").span.text.strip()
                img = container.find("img", class_="ad__card-img")["src"]
                data.append({
                    "Type Chaussure": type_,
                    "Prix": prix,
                    "Adresse": adresse,
                    "Image": img
                })
            except AttributeError:
                continue
        p += 1
    return data

# URLs des catégories
base_urls = {
    "Chaussures Homme": "https://sn.coinafrique.com/categorie/chaussures-homme",
    "Chaussures Enfant": "https://sn.coinafrique.com/categorie/chaussures-enfants"
}

# Titre de l'application
st.title("🛒 Catalogue de Chaussures - CoinAfrique")

# Menu de navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Sélectionnez une page", ["Accueil", "Scraper avec BeautifulSoup", "Scraper avec WebScraper", "Formulaire Kobo", "Formulaire Google Forms"])

if page == "Accueil":
    st.subheader("Bienvenue sur l'application de scraping de CoinAfrique")
    st.write("Cette application permet de scraper des données de chaussures disponibles sur CoinAfrique et d'accéder aux fichiers CSV des données récupérées.")
elif page == "Scraper avec WebScraper":
    st.subheader("📂 Afficher les données déjà scrapées")

    # Dictionnaire des fichiers CSV
    fichier_csv = {
        "Chaussures Homme": "Lien_1.csv",
        "Chaussures Enfant": "Lien_2.csv"
    }

    choix_fichier = st.selectbox("Sélectionnez une catégorie :", list(fichier_csv.keys()))

    if os.path.exists(fichier_csv[choix_fichier]):
        df = pd.read_csv(fichier_csv[choix_fichier])
        st.write(f"📊 Aperçu des données de {choix_fichier} :")
        st.dataframe(df)  # Affichage des données sous forme de tableau

        # Bouton pour télécharger les données
        with open(fichier_csv[choix_fichier], "rb") as file:
            st.download_button(label="📥 Télécharger le fichier CSV",
                               data=file,
                               file_name=fichier_csv[choix_fichier],
                               mime="text/csv")
    else:
        st.warning(f"Aucune donnée trouvée pour {choix_fichier}. Veuillez scraper des données d'abord.")

elif page == "Scraper avec BeautifulSoup":
    st.subheader("Scraper des données avec BeautifulSoup")
    choix_url = st.selectbox("Sélectionner une catégorie", list(base_urls.keys()))
    max_pages_input = st.number_input("Nombre de pages à scraper", min_value=1, max_value=50, value=5)
    
    if st.button("Scraper"):
        url = base_urls[choix_url]
        annonces = scraper_pages(url, max_pages_input)
        df = pd.DataFrame(annonces)
        if not df.empty:
            st.write("Données extraites :")
            st.dataframe(df)
            df.to_csv(f"{choix_url}.csv", index=False)
            with open(f"{choix_url}.csv", "rb") as file:
                st.download_button(label="📥 Télécharger les données", data=file, file_name=f"{choix_url}.csv", mime="text/csv")
        else:
            st.warning("Aucune donnée extraite. Vérifiez l'URL ou le nombre de pages.")



elif page == "Formulaire Kobo":
    st.subheader("Remplir le formulaire Kobo")
    st.components.v1.iframe("https://ee.kobotoolbox.org/i/qpW8UpoY", height=800)


elif page == "Formulaire Google Forms":
    st.subheader("Remplir le formulaire Google Forms")
    st.write('<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScMYr16ZeJOpY5ZSoSYTgpFe3AK9X6SB3-QnESKYboSOuL-pA/viewform?embedded=true" width="640" height="1198" frameborder="0" marginheight="0" marginwidth="0">Chargement…</iframe>', unsafe_allow_html=True)