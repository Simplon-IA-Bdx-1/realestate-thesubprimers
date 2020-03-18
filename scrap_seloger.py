# -*- coding: utf-8 -*-
"""
Script to retrieve data from the site seloger.com
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs4
import re
import time
import random

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
max_pages = 1
page = 1
while (page <= max_pages):
    url = ("http://www.seloger.com/list.htm?org=advanced_search&idtt=2&idtypebien=2,1&cp=75&tri=initial&LISTING-LISTpg=" +
           str(page) + "&naturebien=1,2,4")
    page += 1
    try:
        r = s.get(url)
        soup = bs4(r.text, 'html.parser')

        annonces = soup.find_all("div", attrs={"class": "Card__ContentZone-sc-7insep-3 cKGHWc"})

        if len(annonces) > 0:
            for annonce in annonces:
                # get properties of the appartment
                locality_list = (annonce.find("div", attrs={"class": "Card__LabelGap-sc-7insep-5 ContentZone__Address-wghbmy-2 eAcNsS"}).find_all("span"))
                if (len(locality_list)==2):
                    ville.append(locality_list[0].get_text())
                    quartier.append(locality_list[1].get_text())
                    price.append(annonce.find("div", attrs={"class": "Price__Label-sc-1g9fitq-1 kYWVBR"}).get_text())
                    typelogement.append(annonce.find("div", attrs={"class": "Card__LabelGap-sc-7insep-5 ContentZone__Title-wghbmy-6 hXERKq"}).get_text())
                    #description.append(annonce.find("div", attrs={"class": "Card__Description-sc-7insep-4 ContentZone__ClassifiedDescription-wghbmy-0 fNmvry"}).get_text())

                    property_list = annonce.find("ul", attrs={"class": "ContentZone__Tags-wghbmy-7 fNlgGF"}).find_all("li")
                    if (len(property_list) == 3):
                        room_nb.append(property_list[0].get_text())
                        bedroom_nb.append(property_list[1].get_text())
                        surface.append(property_list[2].get_text())
                    else:
                        room_nb.append("")
                        bedroom_nb.append("")
                        surface.append("")
            print("enregistré")
        else:
            print("captcha")
            pass

        time.sleep(random.randrange(5,10))
    except:
        # Stop visiting pages
        break
    
    

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
rst.to_csv("./test_uno.csv", sep=";", encoding="utf-8")
