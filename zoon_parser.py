
from importlib.resources import path
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
import re 
import random
import json

headers ={
    "accept":"*/*",
    "user-agent":"user-agent"
}


def get_source_html(url):
    driver = webdriver.Chrome(
        executable_path="../chromedriver"
    )
    driver.maximize_window()
    try:
        driver.get(url=url)
        time.sleep(5)

        while True:
            find_more_element = driver.find_element(By.CLASS_NAME, "catalog-button-showMore")


            if driver.find_elements(By.CLASS_NAME, "hasmore-text"):
                with open("..html","w") as file:
                    file.write(driver.page_source)
                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()
                time.sleep(3)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def get_items_urls(file_path):
    with open(file_path) as file:
        src = file.read()

    urls = []
    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("h2", class_="minicard-item__title")

    for item in items_divs:
        item = item.find("a").get("href")
        urls.append(item)

    with open("item_urls.txt", "w") as file:
        for url in urls:
            file.write(f"{url}\n")
        return "[INFO] Urls collected successfully"


def get_data(file_path):
    with open(file_path) as file:
        urls_list = file.readlines()
        clear_urls_list=[]
        for url in urls_list:
            url = url.strip()
            clear_urls_list.append(url)

    result_list = []
    urls_count = len(urls_list)
    count = 0


    for url in clear_urls_list[:9]:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text,'lxml')

        try:
            item_name = soup.find("span", {"itemprop":"name"}).text
        except Exception as ex:
            item_name = None


        item_phones_list = []
        try:
            item_phones = soup.find("div", class_="service-phones-list").find_all("a", class_="js-phone-number")
            for phone in item_phones:
                phone = phone.get("href")
                item_phones_list.append(phone)
        except Exception as ex:
            item_phones_list = None

        try:
            item_adress = soup.find("address",class_="iblock").text                
        except Exception as ex:
            item_adress = None
        
        try:
            item_website = soup.find(text=re.compile("Компания в сети")).find_next().text.strip()             
        except Exception as ex:
            item_website= None


        result_list.append(
            {
                "name":item_name,
                "url":url,
                "phone":item_phones_list,
                "adress":item_adress,
                "item website":item_website

            }
        )
        time.sleep(random.randrange(2,5))
        
        if count%10 == 0:
            time.sleep(random.randrange(2,5))

        print(f"[+] Processed: {count}/{urls_count}")
        count+=1

    with open("06.08.json", 'w') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    return "[INFO] Data collected"

                
def main():
    # get_source_html("https://spb.zoon.ru/medical/?search_query_form=1&m[5200e522a0f302f066000055]=1")

    get_data(file_path="../item_urls.txt")
if __name__=="__main__":
    main()
