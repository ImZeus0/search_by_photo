import os
from parser import Browser


PATH_PHOTO = os.path.abspath('photo.jpg')





if __name__ == '__main__':
    browser = Browser()
    page = browser.upload_photo(PATH_PHOTO)
    urls = browser.urls_photo(page)
    count = 0
    for url in urls:
        browser.download_image(url,f'{count}')
        count+=1


