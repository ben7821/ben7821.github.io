import os
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

script_dir = os.path.dirname(os.path.abspath(__file__))

main_url = "https://www.ste-sidam.fr/marques/"
login_url = "https://www.ste-sidam.fr/login/"

username = "..."
password = "..."

options = webdriver.FirefoxOptions()
options.add_argument('--headless') 

parser = argparse.ArgumentParser(description="Script de scraping pour récupérer des informations sur des produits.")
parser.add_argument("--browser", choices=["firefox", "chrome"], default="firefox", help="Choix du navigateur (firefox par défaut)")
args = parser.parse_args()

if args.browser == "firefox":
    driver = webdriver.Firefox(options=options)
elif args.browser == "chrome":
    driver = webdriver.Chrome(options=options)
else:
    raise ValueError("Navigateur non pris en charge.")

with tqdm(total=6, desc="Connexion", unit="s") as pbar:
    driver.get(login_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_pass")))
    pbar.update(2)

    password_field = driver.find_element(By.ID, "user_pass")
    username_field = driver.find_element(By.ID, "user_login")

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = driver.find_element(By.ID, "wp-submit")
    login_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    pbar.update(4)

    driver.get(main_url)
    pbar.update(2)

def extract_product_info(product_url):
    try:
        driver.get(product_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        product_title = driver.find_element(By.TAG_NAME, 'h1').text.strip()
        product_price = driver.find_element(By.CSS_SELECTOR, 'div.product-detail__price').text.strip()
        product_stock = driver.find_element(By.CSS_SELECTOR, 'div.sticker').text.strip()
        product_descr = driver.find_element(By.CSS_SELECTOR, 'div.product-detail-desc').text.strip()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        product_details_div = soup.find('div', class_="product-detail-info product-detail-info--carac")
        if product_details_div:
            characteristics = product_details_div.find_all('strong')
            product_characteristics = {char.text.strip().split(':')[0]: char.find_next('span').text.strip() for char in characteristics}

            return {'Title': product_title, 'Price': product_price, **product_characteristics, 'Stock': product_stock, 'Description': product_descr}
        else:
            return None
    except Exception as e:
        print(f"Exception: {e} for URL: {product_url}")
        return None

def get_brand_urls(main_url):
    driver.get(main_url)
    brand_items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.brand-content-item')))
    return [item.get_attribute('href') for item in brand_items]

def get_product_urls(brand_urls):
    all_product_urls = []
    for brand_url in tqdm(brand_urls, desc="Product URLs"):
        driver.get(brand_url)
        brand_texts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.brand-card__text')))
        all_product_urls += [text.find_element(By.TAG_NAME, 'a').get_attribute('href') for text in brand_texts]
    return all_product_urls

def get_product_urls(brand_urls):
    all_product_urls = []
    for brand_url in tqdm(brand_urls, desc="Product URLs"):
        driver.get(brand_url)
        pagination = driver.find_elements(By.CSS_SELECTOR, 'nav.woocommerce-pagination')
        last_page_number = 1
        if pagination:
            pagination_links = pagination[0].find_elements(By.CSS_SELECTOR, 'a.page-numbers')
            last_page_number = len(pagination_links) if pagination_links else 1
        for page_number in tqdm(range(1, last_page_number + 1), desc=f"Marque : {brand_url}", leave=False):
            page_url = f"{brand_url}page/{page_number}/"
            driver.get(page_url)
            brand_texts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.brand-card__text')))
            for brand_text in brand_texts:
                product_link = brand_text.find_element(By.TAG_NAME, 'a').get_attribute('href')
                all_product_urls.append(product_link)

    return all_product_urls

all_brand_urls = get_brand_urls(main_url)
# Filtre for dev_mod (test)
filtered_brand_urls = ["https://www.ste-sidam.fr/marques/aselkon/"]
all_product_urls = get_product_urls(filtered_brand_urls if filtered_brand_urls else all_brand_urls)

all_product_info = [extract_product_info(url) for url in tqdm(all_product_urls, desc="Extracting Product Info")]
df = pd.DataFrame([info for info in all_product_info if info])

excel_path = os.path.join(script_dir, "results_scraper.xlsx")
df.to_excel(excel_path, index=False)

print(f"Results saved to '{excel_path}'.")
