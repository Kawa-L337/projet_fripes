import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
import streamlit as st

st.title("Deuxième vie ou Dernière main ?")

with st.container():
    st.header("Calculateur")
    st.write("""
        Cet outil estime le parcours probable d'une fripe à travers le monde 
             et vous donne quelques chiffres clés de l'impact écologique de ce voyage.
    """)


import requests

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjFmNjdmMWEyZGU2ZjRkNzhiMGQ5YTcxNTEzZDg3YWYxIiwiaCI6Im11cm11cjY0In0="   # <-- remplacer ici
le_havre_port = (49.4749981,0.1333328)  # latitude, longitude
paris_airport = (49.0083899664, 2.53844117956)  # latitude, longitude
rotterdam_port = (51.885, 4.2867) # latitude, longitude


# trouve les coordonnées lat et lon d'une ville
# https://openrouteservice.org/dev/#/api-docs/directions%20service API documentation

def geocode_city(city_name):
    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": ORS_API_KEY,
        "text": city_name,
        "boundary.country": "FR"  # limité à la France
    }

    r = requests.get(url, params=params)
    data = r.json()

    if "features" not in data or len(data["features"]) == 0:
        raise ValueError("Ville introuvable")

    coords = data["features"][0]["geometry"]["coordinates"]  # lon, lat
    return coords[1], coords[0]  # lat, lon

# calcul de la distance routière

def get_distance_km(start_coords, end_coords):
    url = "https://api.openrouteservice.org/v2/directions/driving-hgv"  # trajet pour camion driving-car = voiture individuelle
    body = {
        "coordinates": [
            [start_coords[1], start_coords[0]],  # lon, lat
            [end_coords[1], end_coords[0]] 
        ]
    }

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=body, headers=headers)
    data = r.json()

    # distance en mètres
    distance_m = data["routes"][0]["summary"]["distance"]
    return distance_m / 1000  # en km

# Fonctions principales

def distance_camion_vers_rotterdam(ville):
    start_lat, start_lon = geocode_city(ville)
    distance_km_havre = get_distance_km((start_lat, start_lon), rotterdam_port)
    return distance_km_havre

def distance_camion_vers_paris(ville):
    start_lat, start_lon = geocode_city(ville)
    distance_km_paris = get_distance_km((start_lat, start_lon), paris_airport)
    return distance_km_paris

def eqco2_camion_vers_rotterdam(ville,poids):
    start_lat, start_lon = geocode_city(ville)
    distance_km = get_distance_km((start_lat, start_lon), rotterdam_port)
    eqco2 = (400 * distance_km * poids/1000000)+300 # grammesco2/g transporté * la distance * le poids en g + l'eqco2 collecte/plateforme poids lourd
    return eqco2 #en grammes equivalent carbone
def eqco2_camion_vers_paris(ville,poids):
    start_lat, start_lon = geocode_city(ville)
    distance_km = get_distance_km((start_lat, start_lon), paris_airport)
    eqco2 = (400 * distance_km * poids/1000000)+300 # grammesco2/g transporté * la distance * le poids en g + l'eqco2 collecte/plateforme poids lourd
    return eqco2 #en grammes equivalent carbone    

########################################
if __name__ == "__main__":
    # ville de départ
    ville_depot = st.text_input("Entrez la ville de dépot : ") 
    # poids du vêtement estimé par catégorie
    option = st.selectbox(label="Type de vêtements",options=("T-Shirt","Pull","Sweat-Shirt","Short","Pantalon","Jean","Chemise","Robe","Manteau","Veste"))
    if option == "T-Shirt":
        poids=200
    elif option == "Pull":
        poids = 800  
    elif option == "Sweat-Shirt":
        poids = 400 
    elif option == "Pantalon":
        poids = 500           
    elif option == "Jean":
        poids = 800 
    elif option == "Chemise":
        poids = 300     
    elif option == "Robe":
        poids = 500     
    elif option == "Manteau":
        poids = 1000     
    elif option == "Veste":
        poids = 700
    elif option == "Short":
        poids = 300 
    if option in ("Chemise","Robe","Veste"):
        article = "Cette" 
    else :
        article = "Ce"
    if article =="Cette":
        pronom = "Elle"   
    else :
        pronom = "Il"                
    # prix évident ou pas suivant "Marque" 
    marque=st.checkbox("Marque ?")
    # selection d'une ou plusieurs matière
    matiere=st.multiselect(label="Matière", options= ("Lin","Viscose","Coton","Laine","Soie","Cuir","Nylon","Polyester","Acrylique"), placeholder = "Choisissez une ou plusieurs matières")
    # biodégradable ou pas
    
    statut=""
    for mat in matiere :      
        if mat in ("Nylon","Polyester","Acrylique"):
            statut = "Non-Biodégradable"
        else : 
            statut = "Biodégradable" 
    # estimation temps de décomposition        
    for mat in matiere :
        if mat in ("Lin","Viscose"):
            duree = "de 2 à 5 semaines"
        elif mat == "Coton":
            duree = "de 2 semaines à 1 an (suivant les traitements chimiques)"
        elif mat == "Laine" :
            duree = "de 1 à 5 ans (suivant les traitements chimiques)"
        elif mat == "Soie":
            duree = "4 ans"
        elif mat in ("Nylon","Cuir") :
            duree = "40 ans"
        elif mat in ("Polyester","Acrylique"):
            duree = "200 ans" 
    # recyclage ?        
    if len(matiere)==1 :
        for mat in matiere :
            if mat in ("Polyester","Coton"):
                recyclage = f"Si {article.lower()} {option} en {matiere[0]} avait été détecté suffisamment tôt, ce vêtement aurait pu être recyclé."
            else :
                recyclage =""
    else:
        recyclage=""                                 
        #####       
    etat=st.segmented_control(label="Etat du vêtement", options=("Abimé","Bon état","Presque neuf"))   
    distance_mer_mombasa = 4400 # distance mombasa / karachi
    eqco2_mombasa = (40 * distance_mer_mombasa * poids/1000000)+200
    distance_mer = 20000 #distance rotterdam / karachi
    eqco2_mer = (40 * distance_mer * poids/1000000) +200
    distance_air = 6126 # distance paris / karachi
    eqco2_air = 2500 * distance_air * poids/1000000
    if st.button("Valider") :
        if marque == True:
            if etat == "Presque neuf":               
                d = distance_camion_vers_rotterdam(ville_depot)*2
                e = (eqco2_camion_vers_rotterdam(ville_depot,poids))*2
                st.write(f"La distance parcourue par {article.lower()} {option} déposé à {ville_depot} est de: :red[{d:.2f} km], l'impact écologique de ce parcours est de :red[{e/1000:.2f}kg] équivalent carbone.")     
                st.write(f"{pronom} a de grandes chances de finir dans une friperie européenne de ce type :")
                st.image("https://images.lanouvellerepublique.fr/image/upload/t_1020w/f_auto/640af03fe1f5b42d518b456b.jpg")              
            elif etat == "Bon état":
                d_mer = distance_camion_vers_rotterdam(ville_depot)*2+distance_mer*2
                d_air = distance_camion_vers_rotterdam(ville_depot)*2+distance_mer+distance_air
                e_mer = (eqco2_camion_vers_rotterdam(ville_depot,poids))*2+eqco2_mer*2
                e_air = (eqco2_camion_vers_rotterdam(ville_depot,poids))*2+eqco2_mer+eqco2_air
                st.write(f"La distance parcourue par {article.lower()} {option} déposé à {ville_depot} est de: :red[{d_mer:.2f} km], l'impact écologique de ce parcours est de :red[{e_mer/1000:.2f}kg] équivalent carbone.")
                st.write(f"{pronom} a :red[5%] de chance d'effectuer une partie de son trajet en avion, dans ce cas il parcourt :red[{d_air:.2f}] km et rejette :red[{e_air/1000:.2f}kg] équivalent carbone.")
                st.write(f"{pronom} a des chances de finir dans une friperie européenne de ce type :")
                st.image("https://images.lanouvellerepublique.fr/image/upload/t_1020w/f_auto/640af03fe1f5b42d518b456b.jpg") 
            elif etat == "Abimé":
                d = distance_camion_vers_rotterdam(ville_depot)+distance_mer+distance_mer_mombasa
                e = (eqco2_camion_vers_rotterdam(ville_depot,poids))+eqco2_mer+eqco2_mombasa
                st.write(f"La distance parcourue par {article.lower()} {option} déposé à {ville_depot} est de: :red[{d:.2f}] km, l'impact écologique de ce parcours est de :red[{e/1000:.2f}kg] équivalent carbone.")
                st.write(f"{pronom} a :red[30%] de chance de finir immédiatement dans une décharge à ciel ouvert de ce type:")
                st.image("https://i.la-croix.com/836x/smart/2023/02/15/1301255513/decharge-ouvert-Dandora-portes-Nairobi-24-juillet-2021-Kenya_0.jpg")
                if statut != "":
                    st.write(f"{article} {option} est :red[{statut}] et mettra :red[{duree}] à se dégrader dans une décharge.")
                    st.write(f":green[{recyclage}]")
            else :
                st.write("Veuillez définir un état général du vêtement.")
        else :
            if etat == "Presque neuf":               
                d = distance_camion_vers_rotterdam(ville_depot)+distance_mer+distance_mer_mombasa
                e = (eqco2_camion_vers_rotterdam(ville_depot,poids))+eqco2_mer+eqco2_mombasa
                st.write(f"La distance parcourue par {article.lower()} {option} déposé à {ville_depot} est de: :red[{d:.2f} km], l'impact écologique de ce parcours est de :red[{e/1000:.2f}kg] équivalent carbone.")
                st.write(f"{pronom} a de grandes chances de finir sur un marché local de ce type :")  
                st.image("https://www.jobboom.com/carriere/wp-content/uploads/2012/01/Fripier-Banfora.jpg")                             
            elif etat == "Bon état":
                d = distance_camion_vers_rotterdam(ville_depot)+distance_mer+distance_mer_mombasa
                e = (eqco2_camion_vers_rotterdam(ville_depot,poids))+eqco2_mer+eqco2_mombasa
                st.write(f"La distance parcourue par {article.lower()} {option} déposé à {ville_depot} est de: :red[{d:.2f} km], l'impact écologique de ce parcours est de :red[{e/1000:.2f}kg] équivalent carbone.")
                st.write(f"{pronom} a :red[30%] de chance de finir immédiatement dans une décharge à ciel ouvert de ce type:")
                st.image("https://i.la-croix.com/836x/smart/2023/02/15/1301255513/decharge-ouvert-Dandora-portes-Nairobi-24-juillet-2021-Kenya_0.jpg")
                if statut != "":
                    st.write(f"{article} {option} est :red[{statut}] et mettra :red[{duree}] à se dégrader dans une décharge.")
                    st.write(f":green[{recyclage}]")
            elif etat == "Abimé":
                d = distance_camion_vers_rotterdam(ville_depot)+distance_mer+distance_mer_mombasa
                e = (eqco2_camion_vers_rotterdam(ville_depot,poids))+eqco2_mer+eqco2_mombasa
                st.write(f"La distance parcourue par {article.lower()} {option} déposé à {ville_depot} est de: :red[{d:.2f} km], l'impact écologique de ce parcours est de :red[{e/1000:.2f}kg] équivalent carbone.")
                st.write(f"{pronom} a de très grandes chances de finir :red[immédiatement] dans une décharge à ciel ouvert de ce type:")
                st.image("https://i.la-croix.com/836x/smart/2023/02/15/1301255513/decharge-ouvert-Dandora-portes-Nairobi-24-juillet-2021-Kenya_0.jpg")        
                if statut != "":
                    st.write(f"{article} {option} est :red[{statut}] et mettra :red[{duree}] à se dégrader dans une décharge.")
                    st.write(f":green[{recyclage}]")
                
            else :
                st.write("Veuillez définir un état général du vêtement.")    
        
    if st.button("") :
        st.image("https://i.postimg.cc/V6vc2fPW/MERCI.png")  
            