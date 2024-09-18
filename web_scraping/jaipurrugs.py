import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# options = Options()
# options.add_argument('--disable-blink-features=AutomationControlled')


def extract_first_number(input_string):
    match = re.search(r'\d+', input_string)
    if match:
        return int(match.group())
    return -1

def is_valid(size, img):
    try:
        length = extract_first_number(size.text)
        if size and img and "round" not in size.text and length > 100 and ".jpg" in img.get_attribute("src") and 'Product-Listing-Loder.jpg' not in img.get_attribute("src"):
            return True
        return False
    except Exception as e:
        print(f"Error is checking valid size: \n{e}")
        raise("Error is checking valid size")

def ext_img_urls(wd, wait_time=3, no_of_urls=100):

    img_urls = set()
    url_cnt = 0
    # load_calls = 0
    # load_more_btn = wd.find_element(By.XPATH, '//*[@id="divLoadMore"]/div/a')
    # load_more_btn = wd.find_element(By.CSS_SELECTOR, 'a.text-decoration-underline.text-uppercase.fw-400')
    # if load_more_btn:
    #     print(f"Load button exist {load_more_btn.text}")

    
    # while url_cnt < no_of_urls:
    if True:
        cards = wd.find_elements(By.CSS_SELECTOR, ".col-xl-3.col-lg-4.col-md-4.col-sm-6.col-6.mb-3.px-xl-3.px-lg-3.px-md-3.mt-3")
        print(f"No of cards: {len(cards)}")
        for i,card in enumerate(cards):
            try:
                wd.execute_script("arguments[0].scrollIntoView(true);", card)
                if i % 4 == 0:
                    time.sleep(wait_time)

                img = card.find_element(By.XPATH, ".//div[1]/a[1]/img")
                collection = card.find_element(By.XPATH, './/div[2]/a/p[1]')
                material = card.find_element(By.XPATH, './/div[2]/a/p[2]')
                size = card.find_element(By.XPATH, ".//div[2]/a/p[3]")

                if is_valid(size, img):
                    img_link = img.get_attribute('src')
                    collection_txt = collection.text
                    material_txt = material.text
                    size_txt = size.text
                    img_urls.add((img_link, collection_txt, material_txt, size_txt))
                    url_cnt = len(img_urls)

            except Exception as e:
                print(f"Error in extracting images from cards: \n{e}")
                return img_urls
        
        # print(f"No of load calls: {load_calls}")
        print(f"No of images: {url_cnt}\n")

        # try:
        #     # wd.execute_script("arguments[0].scrollIntoView(true);", load_more_btn)
        #     # wd.execute_script("arguments[0].click();", load_more_btn)
        #     popup_cancel_btn = wd.find_element(By.ID, 'wzrk-cancel')
        #     if popup_cancel_btn:
        #         popup_cancel_btn.click()
        #         time.sleep(0.5)

        #     wd.execute_script("arguments[0].style.visibility = 'visible';",load_more_btn)
        #     # ActionChains(wd).move_to_element(load_more_btn).click().perform()
        #     element = wd.find_element(By.XPATH, "//a[@onclick='FindPagingData()']")
        #     wd.execute_script("arguments[0].click();", element)
        #     # wd.execute_script("FindPagingData()")
        #     print(f"load button clicked")
        #     time.sleep(wait_time)
        # except Exception as e:
        #     print(f"Error in loading page: \n{e}")
        #     return img_urls

    return img_urls
        
    

def save_file(file:str, img_urls):
    urls_list = map(lambda x: ', '.join(x), img_urls)
    urls_str = '\n'.join(urls_list)
    try:
        with open(file, 'w') as f:
            f.write("image_urls, collection, material, size\n")
            f.write(urls_str)
    except Exception as e:
        print(f"Can't save file: \n{e}")

if __name__ == '__main__':
    urls = [
        'https://www.jaipurrugs.com/abstract-rugs?pagenumber=1&pagesize=1000&orderby=10000',
        'https://www.jaipurrugs.com/oriental-rugs?pagenumber=1&pagesize=1000&orderby=0',
        'https://www.jaipurrugs.com/moroccan-rugs?pagenumber=1&pagesize=1000&orderby=0',
        'https://www.jaipurrugs.com/distressed-rugs?pagenumber=1&pagesize=1000',
        'https://www.jaipurrugs.com/floral-rugs?pagenumber=1&pagesize=1000&orderby=10000',
        'https://www.jaipurrugs.com/geometric-rugs?pagenumber=1&pagesize=1000&orderby=10000',
        'https://www.jaipurrugs.com/solid-rugs?pagenumber=1&pagesize=1000&orderby=10000',
        'https://www.jaipurrugs.com/patchwork-rugs?pagenumber=1&pagesize=1000&orderby=0'

    ]
    file_names = [
        '../image_url_v2/abstract.csv',
        '../image_url_v2/oriental.csv',
        '../image_url_v2/moroccan_and_tribal.csv',
        '../image_url_v2/vintage_and_distressed.csv',
        '../image_url_v2/floral_and_tropical.csv',
        '../image_url_v2/geometric_and_stripes.csv',
        '../image_url_v2/solid.csv',
        '../image_url_v2/Patchwork.csv'
    ]

    # url = 'https://www.jaipurrugs.com/abstract-rugs?pagenumber=1&pagesize=1000&orderby=10000'


    for i in range(len(urls)):
        print(urls[i])
        wd = webdriver.Firefox()
        wd.get(urls[i])

        time.sleep(10)

        img_urls = ext_img_urls(wd, wait_time=3, no_of_urls=20)
        save_file(file_names[i], img_urls)

        wd.quit()
        time.sleep(5)
        del wd