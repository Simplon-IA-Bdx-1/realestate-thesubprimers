from selenium import webdriver
import re

ville = []
quartier = []
price = []
room_nb = []
bedroom_nb = []
surface = []

driver = webdriver.Firefox(executable_path='C:/ProgramData/geckodriver.exe')
# driver = webdriver.Chrome(executable_path='C:/ProgramData/chromedriver.exe')

resp = driver.get('http://www.seloger.com/list.htm?org=advanced_search&idtt=2&idtypebien=2,1&cp=75&tri=initial&LISTING-LISTpg=2&naturebien=1,2,4')

elem = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/div[2]')

infos = elem.find_elements_by_class_name('fNlgGF')
locations = elem.find_elements_by_class_name('eAcNsS')
prices = elem.find_elements_by_class_name('kYWVBR')
locaprices = list(zip(locations, prices))

def append_info(infos, locaprices):
    print(infos.find_elements_by_tag_name('li'))
    room_nb.append(re.match(r'\d', infos.find_elements_by_tag_name('li')[0].text).group())
    bedroom_nb.append(re.match(r'\d', infos.find_elements_by_tag_name('li')[1].text).group())
    surface.append(re.match(r'\d', infos.find_elements_by_tag_name('li')[2].text).group())
    ville.append(locaprices[0].find_elements_by_tag_name('span')[0].text)
    if len(locaprices[0].find_elements_by_tag_name('span')) > 1:
        quartier.append(locaprices[0].find_elements_by_tag_name('span')[1].text)
    else:
        quartier.append("NA")
    price.append(locaprices[1].text)
    return room_nb, bedroom_nb, surface, ville, quartier, price

result = map(append_info, infos, locaprices)

print(result.values)
# print(room_nb[0])
# print(bedroom_nb[0])
# print(ville[0])
# print(price[0])