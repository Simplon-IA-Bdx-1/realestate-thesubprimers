import pandas as pd
import time
import bs4
import random
import requests
# !pip install fake-useragent
from fake_useragent import UserAgent
import itertools as it

# Initialize variables
ville = []
quartier = []
price = []
room_nb = []
bedroom_nb = []
surface = []
typelogement = []

def get_pages(nb):
    pages = []
    token1 = "http://www.seloger.com/list.htm?org=advanced_search&idtt=2&idtypebien=2,1&cp=75&tri=initial&LISTING-LISTpg="
    token2 = "&naturebien=1,2,4"
    for i in range(1,nb+1):
        j = token1 + str(i) + token2
        pages.append(j)
    return pages

pages = get_pages(3)
print(pages)

def get_proxies():
    r = requests.get("https://www.proxy-list.download/HTTPS")
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    print(soup.select("#txta1"))


# https://www.proxy-list.download/HTTPS
proxies = pd.read_csv('http_proxies.txt', header = None)
proxies = proxies.values.tolist()
proxies = list(it.chain.from_iterable(proxies))

def get_data(pages,proxies):
    
    ua = UserAgent()
    proxy_pool = it.cycle(proxies)
    
    while len(pages) > 0:
        for i in pages:
        # itération dans un liste de proxies    
            proxy = next(proxy_pool)
        # essai d'ouverture d'une page   
            try:
                print("essai connection")
                r = requests.get(i,proxies={"http": proxy, "https": proxy}, headers={'User-Agent': ua.random},timeout=5)
                print(r.reason)
        # lecture du code html et la recherche des balises <em>
                soup = bs4.BeautifulSoup(r.text, 'html.parser')

                annonces = soup.find_all("div", attrs={"class": "Card__ContentZone-sc-7insep-3 cKGHWc"})
                print(annonces)
                print(soup.p)

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

                    pages.remove(i)
                    print(len(pages))
                else:
                    print("captcha")
                    pass
                time.sleep(random.randrange(5,10))
            except:
                print("Skipping. Connnection error")

get_data(pages,proxies)

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
rst.to_csv("test_scrap.csv", sep=";", encoding="utf-8")