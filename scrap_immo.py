# -*- coding: utf-8 -*-
"""
Script to retrieve data from the site seloger.com
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import os

working_dir = "C:/Users/simplon/Desktop/scrappy_immo"
os.chdir(working_dir)

# Initialize variables
ville = []
quartier = []
price = []
room_nb = []
bedroom_nb = []
surface = []
typelogement = []
#description = []

# Create a session (to avoid redirecting loop with requests.get())
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'


# Loop over different pages
max_pages = 220
page = 1
while (page <= max_pages):
    url = ("https://www.logic-immo.com/vente-immobilier-paris-75,100_1/options/groupprptypesids=1,6,7,12,15")
    page += 1
    try:
        r = s.get(url)
    except:
        # Stop visiting pages
        break
    
    # Get information from the page
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # find all ads from the page
    annonces = soup.find_all("div", attrs={"class": "offer-list-row"})
    
    print(annonces)
    
    for annonce in annonces:
        # get properties of the appartment
        ville.append(annonce.find("span", attrs={"class": "offer-details-location--locality"}).get_text())
        quartier.append(annonce.find().get_text())
        price.append(annonce.find("p", attrs={"class": "offer-price"}).get_text())
        typelogement.append(annonce.find("span", attrs={"class": "offer-details-type"}).get_text())
        #description.append(annonce.find("div", attrs={"class": "Card__Description-sc-7insep-4 ContentZone__ClassifiedDescription-wghbmy-0 fNmvry"}).get_text())
        room = annonce.find("span", attrs={"class": "offer-details-caracterististik--rooms"})
        room_nb.append(room.find("span", attrs={"class": "offer-rooms-number"}).get_text())
        bedroom = annonce.find("span", attrs={"class": "offer-details-caracterististik--bedrooms"})
        bedroom_nb.append(bedroom.find("span", attrs={"class": "offer-rooms-number"}).get_text())
        surface.append(annonce.find("span", attrs={"class": "offer-area-number"}).get_text())


rst = pd.DataFrame({"type of logement": typelogement,
                    "ville": ville,
                    "quartier" : quartier,
                    "price": price,
                    "room_nb": room_nb,
                    "bedroom_nb": bedroom_nb,
                    "surface": surface})

new_names = rst.columns.values
new_names = [name + "_raw" for name in new_names]
rst.columns = new_names
    
# Write result to csv
rst.to_csv("immo-paris-page1-to-500_raw.csv", encoding="utf-8")