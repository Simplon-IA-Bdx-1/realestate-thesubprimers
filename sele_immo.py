from selenium import webdriver
import re

ville = []
quartier = []
price = []
room_nb = []
bedroom_nb = []
surface = []

driver = webdriver.Firefox(executable_path='C:/ProgramData/geckodriver.exe')

resp = driver.get('https://www.logic-immo.com/vente-immobilier-paris-75,100_1/options/groupprptypesids=1,6')

liste = driver.find_element_by_class_name('offer-list')
annonces = liste.find_elements_by_class_name('offer-details')

for annonce in annonces[1:-1]:
    ville.append(annonce.find_element_by_class_name("offer-details-location--locality").text)
    # if annonce.find_element_by_class_name("offer-details-location--city") > 0:
    #     quartier.append(annonce.find_element_by_class_name("offer-details-location--city").text)
    # else:
    #     quartier.append("")
    price.append(annonce.find_element_by_class_name("offer-price").text)
    room_nb.append(annonce.find_element_by_class_name("offer-rooms-number").text)
    bedroom_nb.append(annonce.find_element_by_class_name("offer-rooms-number").text)
    surface.append(annonce.find_element_by_class_name("offer-area-number").text)
    print("OK")

print(room_nb[0])
print(bedroom_nb[0])
print(ville[0])
print(price[0])