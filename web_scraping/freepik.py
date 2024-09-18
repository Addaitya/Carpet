import time
from selenium import webdriver
from selenium.webdriver.common.by import By

'''
a._44sdx510._1286nb19d._1286nb12tv._1286nb119._1286nb11e._1286nb1v._1286nb19d._44sdx5j._1286nb16ru._1286nb17f3._1286nb17g9._1286nb12j7._1286nb1297._1286nb123v._1286nb12dv._1286nb12od._1286nb12rp._1286nb14kp._1286nb14m1._1286nb14nd._1286nb14op._44sdx51g._1286nb115._1286nb14gd._1286nb14hd._1286nb14id._1286nb14jd._1286nb14td._1286nb18o
'''

def ext_urls(wb, sleep_between_interactions=5, no_of_urls=100):
    image_urls = set()
    url_cnt = len(image_urls)
    curr_page = 1

    while url_cnt < no_of_urls:
        thumbnails = wb.find_elements(By.CSS_SELECTOR, "img._1286nb17:not(._1x032glf)")

        for thb in thumbnails:
            try:
                if thb.get_attribute('src') and 'http' in thb.get_attribute('src') and '.webp' not in thb.get_attribute('src'):
                        image_urls.add(thb.get_attribute('src'))
                        url_cnt = len(image_urls)
            except Exception as e:
                 print(f"Some error came: {e}")
                
        print(f"Page extracted: {curr_page}")
        print(f"url count: {url_cnt}\n")

        try:
            nxt_pg_sel = 'a._44sdx510._1286nb19d._1286nb12tv._1286nb119._1286nb11e._1286nb1v._1286nb19d._44sdx5j._1286nb16ru._1286nb17f3._1286nb17g9._1286nb12j7._1286nb1297._1286nb123v._1286nb12dv._1286nb12od._1286nb12rp._1286nb14kp._1286nb14m1._1286nb14nd._1286nb14op._44sdx51g._1286nb115._1286nb14gd._1286nb14hd._1286nb14id._1286nb14jd._1286nb14td._1286nb18o'
            nxt_pg_btn = wb.find_element(By.CSS_SELECTOR, f"{nxt_pg_sel}")
            if nxt_pg_btn:
                nxt_pg_btn.click()
                curr_page += 1
                time.sleep(sleep_between_interactions)

            else:
                print("The end")
                return image_urls
            

        except Exception as e:
            print(f"Some error occured on clicking next page: \n{e}")
    
    return image_urls


url = "https://www.freepik.com/search?query=carpet%20classic%20texture&ai=excluded&format=search&last_filter=type&type=allImages"
file = '../image_urls/classic.txt'

wb = webdriver.Firefox()
wb.get(url) 
time.sleep(2)
wb.execute_script("window.open = function() {};")
img_urls = ext_urls(wb, sleep_between_interactions=3 ,no_of_urls=1000)
wb.quit()
with open(file, 'w') as f:
     text = "\n".join(img_urls)
     f.write(text)
