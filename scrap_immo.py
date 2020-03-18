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
import time

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

# Loop over different pages
max_pages = 2
page = 0
while (page <= max_pages):
    print("hey")
    url = ("https://www.logic-immo.com/vente-immobilier-paris-75,100_1/options/groupprptypesids=1,6")
    page += 1
    try:
        print("connection")
        r = s.get(url)
        # Get information from the page
        soup = BeautifulSoup(r.text, 'html.parser')

        # find all ads from the page
        annonces = soup.find_all("div", attrs={"class": "offer offer-list"})
        
        for annonce in annonces:
            # get properties of the appartment
            ville.append(annonce.find("span", attrs={"class": "offer-details-location--locality"}).get_text())
            if annonce.find("a", attrs={"class": "offer-details-location--city"}):
                quartier.append(annonce.find("a", attrs={"class": "offer-details-location--city"}).get_text())
            else:
                quartier.append("")
            price.append(annonce.find("p", attrs={"class": "offer-price"}).get_text())
            typelogement.append(annonce.find("span", attrs={"class": "offer-details-type"}).get_text())
            #description.append(annonce.find("div", attrs={"class": "Card__Description-sc-7insep-4 ContentZone__ClassifiedDescription-wghbmy-0 fNmvry"}).get_text())
            # room = annonce.find("span", attrs={"class": "offer-details-caracterististik--rooms"})
            # room_nb.append(room.find("span", attrs={"class": "offer-rooms-number"}).get_text())
            # bedroom = ("span", attrs={"class": "offer-details-caracterististik--bedrooms"})
            bedroom_nb.append(annonce.find("span", attrs={"class": "offer-rooms-number"}).get_text())
            surface.append(annonce.find("span", attrs={"class": "offer-area-number"}).get_text())
            print("OK")

        time.sleep(5)
    except:
        print("raté")
        # Stop visiting pages
        break
    


rst = pd.DataFrame({"type of logement": typelogement,
                    "ville": ville,
                    "quartier" : quartier,
                    "price": price,
                    # "room_nb": room_nb,
                    "bedroom_nb": bedroom_nb,
                    "surface": surface})

new_names = rst.columns.values
new_names = [name + "_raw" for name in new_names]
rst.columns = new_names
    
# Write result to csv
rst.to_csv("testos.csv", encoding="utf-8")