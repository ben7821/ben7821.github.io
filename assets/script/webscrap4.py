import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import zipfile

# Fonction optimisée pour télécharger un fichier
def optimized_download_file(driver, download_url, download_dir):
  driver.execute_script(f"window.location = '{download_url}'")
  num_files_before = len(os.listdir(download_dir))
  WebDriverWait(driver, 30).until(lambda d: len(os.listdir(download_dir)) > num_files_before)
  
  for file in os.listdir(download_dir):
    if file.endswith('.zip'):
      file_path = os.path.join(download_dir, file)
      with zipfile.ZipFile(file_path, 'r') as zip_file:
        zip_file.extractall(download_dir)
      os.remove(file_path)

with open('url.json') as f:
  sites = json.load(f)

options = webdriver.FirefoxOptions() 
options.add_argument('--headless')
script_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(script_dir)
options.set_preference("browser.download.dir", download_dir)
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")

parser = argparse.ArgumentParser(description="Script de scraping pour récupérer des informations sur des produits.")
parser.add_argument("--browser", choices=["firefox", "chrome"], default="firefox", help="Choix du navigateur (firefox par défaut)")
args = parser.parse_args()

if args.browser == "firefox":
  driver = webdriver.Firefox(options=options)
elif args.browser == "chrome":
  driver = webdriver.Chrome(options=options)
else:
  raise ValueError("Navigateur non pris en charge.")
  
# Boucle sur les sites  
for site in sites:
  driver.get(site['url'])
  
  username_input = driver.find_element(By.ID, site['username_field_id'])
  username_input.send_keys(site['username'])

  password_input = driver.find_element(By.ID, site['password_field_id'])
  password_input.send_keys(site['password'])

  login_button = driver.find_element(By.CLASS_NAME, site['submit_class'])
  login_button.click()
  
  optimized_download_file(driver, site['download_url'], download_dir)

  driver.delete_all_cookies()
  
driver.quit()
