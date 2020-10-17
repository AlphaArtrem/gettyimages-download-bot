import requests
import os 
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Connect to chrome driver 
driver = webdriver.Chrome() 
# Current woking directory
current_path = os.getcwd()
# Website url
URL = "https://dam.gettyimages.com/ufc/"
# User agent to mask script as device
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent" : USER_AGENT}
# Sending request to google
resp = requests.get(URL, headers=headers)

# If the request was successfull
if resp.status_code == 200:
    soup = BeautifulSoup(resp.content, "html.parser")
    # Find links with class noline
    for a in soup.find_all('a', class_ = 'noline'):
        # Get path for current directory
        path = current_path + "/imgs/" + ''.join(e for e in a.text if e.isalnum())
        # If direcry exists skip
        if os.path.isdir(path):
            continue
        # Else open page
        driver.get("https://dam.gettyimages.com" + a['href'])
        # Wait for agree button to become clickable
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div[4]/div[2]/div[4]/div[1]/div[1]/div/div/div[3]/button')))
        agree_button = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[4]/div[2]/div[4]/div[1]/div[1]/div/div/div[3]/button")
        # Click agree button
        agree_button.click()
        # Get page after clicking button
        image_catalogue = BeautifulSoup(driver.page_source, "html.parser")
        # Create directory for album
        os.mkdir(path)
        # Find all images from page
        for img in image_catalogue.find_all('img', class_ = 'image-div'):
            # Get image
            img_data = requests.get(img["src"][:-len("element.jpg")] + "original/" + img["alt"]).content
            # Remove special characters from image
            img_path = path + "/" + ''.join(e for e in img["alt"] if e.isalnum()) 
            # Add image extension
            img_path = img_path[:-len("jpg")] + img_path[len(img_path) - len("jpg"):]
            # Create image file
            with open(img_path, "wb") as local_img_file:
                # Add image to local storage
                local_img_file.write(img_data)
else:
    # Give proper error code if can't connect
    print("Request denied with error code : " + str(resp.status_code))