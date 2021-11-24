import re
import requests
import os
from PIL import Image
from selenium import webdriver

class Browser():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('/home/ubuntu/PycharmProjects/search_by_photo/chromedriver', options=options)

    def upload_photo(self,path):
        self.driver.get('https://www.google.com.ua/imghp?hl=ru&ogbl')
        button_photo = self.driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[3]/div[2]/span')
        button_photo.click()
        input_photo = self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[2]/form/div[2]/div[2]/input')
        input_photo.send_keys(path)
        select_image = self.driver.find_element_by_xpath(
            '/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/g-section-with-header/div[1]/title-with-lhs-icon/a/div[2]/h3')
        select_image.click()
        current_url = self.driver.current_url.replace('simg','isz:l%2Csimg')
        self.driver.get(current_url)
        return self.driver.page_source

    def urls_photo(self,page):
        res = []
        urls = re.findall(r'http[s]?:\/(?:\/[^\/]+){1,}(?:\/[А-Яа-яёЁ\w ]+\.[a-z]{3,5}(?![\/]|[\wА-Яа-яёЁ]))',page)
        for url in urls:
            if url.startswith('https:'):
                if url.startswith('https://www.google.com') == False or url.startswith('https://www.gstatic.com') == False:
                    print(url)
                    if url.endswith('jpg') or url.endswith('jpeg'):
                        res.append(url)
        return res

    def download_image(self,url,name,folder):
        img = requests.get(url,verify=False)
        type_file = url.split('.')[-1]
        path = f'{folder}/{name}.{type_file}'
        img_file = open(path, 'wb')
        img_file.write(img.content)
        self.resize_image(path)
        img_file.close()

    def resize_image(self,image_path):
        size = (1000,500)
        original_image = Image.open(image_path)
        width, height = original_image.size
        resized_image = original_image.resize(size)
        width, height = resized_image.size
        resized_image.save(image_path)
