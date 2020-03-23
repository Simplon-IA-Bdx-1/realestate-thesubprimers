from selenium import webdriver
import re
import csv
import argparse
import time

scrapper = {
        "ville": "offer-details-location--locality",
        "price": "offer-price",
        "room_nb": "offer-rooms-number",
        "bedroom_nb": "offer-details-caracteristik--bedrooms",
        "surface": "offer-area-number",
        "quartier": "offer-details-location--sector"
    }

def get_infos(annonce, scrapper):
    result = {}
    for k, v in scrapper.items():
        try:
            result[k] = annonce.find_element_by_class_name(v).text
        except:
            result[k] = ""
    print("Annonce analysée")
    return result

parser = argparse.ArgumentParser(
    description='Logic-immo scrapper',
    usage=
    '''
    python app.py [<pages range>]
    '''
)
parser.add_argument('--range', '-r', help='Number of pages to crawl (default 10)', default=10)
args = parser.parse_args()

for page in range(1,int(args.range),1):

    driver = webdriver.Firefox(executable_path='C:/ProgramData/geckodriver.exe')
    resp = driver.get(f'https://www.logic-immo.com/vente-immobilier-paris-75,100_1/options/groupprptypesids=1,6/page={page}')
    
    liste = driver.find_element_by_class_name('offer-list')
    annonces = liste.find_elements_by_class_name('offer-details')

    with open("my_csv.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=scrapper.keys())
        for annonce in annonces:
            result = get_infos(annonce, scrapper)
            writer.writerow(result)
            print("Annonce enregistrée")

    driver.close()
    print(f"Page {int(page)}")
    time.sleep(2)