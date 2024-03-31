from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from models import Tovari, Category
import json

driver = webdriver.Chrome()
driver.get(
    "https://www.mvideo.ru/noutbuki-planshety-komputery-8/planshety-195?f_brand=xiaomi&f_tolko-v-nalichii=da&from=hb")
products = []
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

elements_price = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'pricemain-value')))
elements_title = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-titletext')))
elements_image = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-picture__img')))

for element in elements_price:
    products.append({'price': element.text})

i = 0
for element in elements_title:
    products[i]['title'] = element.text
    i += 1

i = 0
for element in elements_image:
    if i == 3:
        break
    products[i]['images'] = element.get_attribute('src')
    i += 1

data = json.encoder(products)
print(data)

# for product in products:
#     t = Tovari()
#     t.title = product['title']
#     t.description = product['title']
#     t.price = int(product['price'].replace('₽', '').replace(' ', ''))
#     cat = Category.objects.filter(name='Планшеты').first()
#     t.category = cat
#     t.count = 10
#     t.image = product['image']
#     t.save()

driver.quit()
