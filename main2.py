from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv
import math
import re
import random
options = Options()
options.headless = True
driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
#driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.set_window_size(1920, 1080)

#Random times between actions, so it looks like human)
def random_sleep():
    _sleep = random.randint(1, 3)
    time.sleep(_sleep)

def setup():
    driver.get("https://en.aruodas.lt/butai/")
    # driver.get("https://en.aruodas.lt/namai/")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Sutinku"]'))).click()
    random_sleep()

def adclicker():
    num_apartments = 100
    # num_apartments = int(input("Enter the number of apartments to scrape: "))
    count = 0
    with open('apartments.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'City', 'District', 'Street', 'House_No','Flat_No', 'Area', 'Rooms', 'Floor','No_of_floors', 'Year', 'Building Type', 'Heating','Furnishing', 'EnergyClass', "Price", 'Description', 'Additional_premises', 'Nearest_kindergarten','Nearest_shool', 'Nearest_shop','Nearest_busstop', 'About']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        while count < num_apartments:
            ads = driver.find_elements(By.CSS_SELECTOR, "div.list-adress-v2 a")
            if not ads:
                break
            for ad in ads:
                #Find all the ads on current page, scrolls until other ad is found, gets url, clicks it.
                try:
                    row = ad.find_element(By.XPATH, "../../..")
                    driver.execute_script("arguments[0].scrollIntoView();", row)
                    driver.execute_script("window.scrollBy(0, -50);")
                    ad_url = ad.get_attribute("href")
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(ad_url)
                    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
                    random_sleep()

                    # Define the pattern
                    pattern = r'^(.*?),\s*(.*?),\s*(.*?)\s*,\s*(.*)$'

                    title = driver.find_element(By.CLASS_NAME, "obj-header-text").text

                    # Match the pattern with title text
                    match = re.match(pattern, title)

                    # Extract the relevant parts from the match
                    if match:
                        city = match.group(1)
                        district = match.group(2)
                        street = match.group(3)
                    else:
                        # Handle the case where the pattern does not match
                        city = math.nan
                        district = math.nan
                        street = math.nan
                        print("Failed to extract city, district, street, and apartment type from title text")

                    #if value is not found, replace it with NaN

                    try:
                        house_no = driver.find_element(By.XPATH, '//dt[normalize-space()="House No.:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        house_no = math.nan

                    try:
                        flat_no = driver.find_element(By.XPATH, '//dt[normalize-space()="Flat No.:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        flat_no = math.nan

                    try:
                        description = driver.find_element(By.XPATH, '//dt[normalize-space()="Description:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        description = math.nan

                    try:
                        area = driver.find_element(By.XPATH, '//dt[normalize-space()="Area:"]/following-sibling::dd[1]').text.split()[0]
                        area = area.replace('"', '') + "m2"
                    except NoSuchElementException:
                        area = math.nan

                    try:
                        rooms = driver.find_element(By.XPATH, '//dt[normalize-space()="Number of rooms :"]/following-sibling::dd[1]').text.split()[0]
                    except NoSuchElementException:
                        rooms = math.nan

                    try:
                        floor = driver.find_element(By.XPATH, '//dt[normalize-space()="Floor:"]/following-sibling::dd[1]').text.split()[0]
                    except NoSuchElementException:
                        floor = math.nan

                    try:
                        no_of_floors = driver.find_element(By.XPATH, '//dt[normalize-space()="No. of floors:"]/following-sibling::dd[1]').text.split()[0]
                    except NoSuchElementException:
                        no_of_floors = math.nan

                    try:
                        year = driver.find_element(By.XPATH, '//dt[normalize-space()="Build year:"]/following-sibling::dd[1]').text.split()[0]
                    except NoSuchElementException:
                        year = math.nan

                    try:
                        building_type = driver.find_element(By.XPATH,'//dt[normalize-space()="Building type:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        building_type = math.nan

                    try:
                        heating = driver.find_element(By.XPATH, '//dt[normalize-space()="Heating system:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        heating = math.nan

                    try:
                        furnishing = driver.find_element(By.XPATH, '//dt[normalize-space()="Equipment:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        furnishing = math.nan

                    try:
                        additional_premises = driver.find_element(By.XPATH, '//dt[normalize-space()="Additional premises:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        additional_premises = math.nan

                    try:
                        energy_class = driver.find_element(By.XPATH,'//dt[normalize-space()="Building Energy Efficiency Class:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        energy_class = math.nan

                    # atstumas nuo darzelio
                    try:
                        dis_element = driver.find_elements_by_class_name('statistic-info-cell-main')
                        if len(dis_element)==4:
                            dis_element1 = dis_element[0]
                            # Get the distance from the span element with the class "cell-data"
                            distance_element = dis_element1.find_element_by_class_name('cell-data')
                            dist_kindergarten = distance_element.text.split('~ ')[1]
                        else:
                            dist_kindergarten = math.nan
                    except NoSuchElementException:
                        dist_kindergarten = math.nan

                    # atstumas nuo mokyklos
                    try:
                        # dis_element = driver.find_elements_by_class_name('statistic-info-cell-main')
                        if len(dis_element)==4:
                            dis_element2 = dis_element[1]
                            # Get the distance from the span element with the class "cell-data"
                            distance_element2 = dis_element2.find_element_by_class_name('cell-data')
                            dist_shool = distance_element2.text.split('~ ')[1]
                        else:
                            dist_shool = math.nan
                    except NoSuchElementException:
                        dist_shool = math.nan

                    # atstumas nuo parduotuves
                    try:
                        # dis_element = driver.find_elements_by_class_name('statistic-info-cell-main')
                        if len(dis_element)==4:
                            dis_element3 = dis_element[2]
                            # Get the distance from the span element with the class "cell-data"
                            distance_element3 = dis_element3.find_element_by_class_name('cell-data')
                            dist_shop = distance_element3.text.split('~ ')[1]
                        else:
                            dist_shop = math.nan
                    except NoSuchElementException:
                        dist_shop = math.nan
                    # atstumas nuo viesojo transporto stoteles
                    try:
                        # dis_element = driver.find_elements_by_class_name('statistic-info-cell-main')
                        if len(dis_element)==4:
                            dis_element4 = dis_element[3]
                            # Get the distance from the span element with the class "cell-data"
                            distance_element4 = dis_element4.find_element_by_class_name('cell-data')
                            dist_busstop = distance_element4.text.split('~ ')[1]
                        else:
                            dist_busstop = math.nan
                    except NoSuchElementException:
                        dist_busstop = math.nan


                    try:
                        price_element = driver.find_element(By.CLASS_NAME, "price-eur")
                        price_text = price_element.text.strip()
                        price = int(''.join(filter(str.isdigit, price_text)))
                    except NoSuchElementException:
                        price = math.nan

                    try:
                        about_element = driver.find_element_by_id('collapsedText')
                        about = about_element.text
                    except NoSuchElementException:
                        about = math.nan

                    writer.writerow({'title': title, 'City': city, 'District': district, 'Street': street, 'House_No': house_no, 'Flat_No': flat_no, 'Area': area, 'Rooms': rooms,
                                     'Floor': floor, 'No_of_floors': no_of_floors, 'Year': year, 'Building Type': building_type, 'Heating': heating,
                                     'Furnishing': furnishing, 'EnergyClass': energy_class, 'Price': price, 'Description': description,'Additional_premises': additional_premises, 'Nearest_kindergarten': dist_kindergarten, 'Nearest_shool': dist_shool, 'Nearest_shop': dist_shop,'Nearest_busstop': dist_busstop, 'About': about})
                    print(str(count+1) +") ", title, house_no, flat_no, area, year, price)
                finally:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                count += 1
                if count >= num_apartments:
                    break
            try:
                next_page = driver.find_element(By.XPATH, "//a[@class='page-bt' and contains(text(),'»')]")
                next_page.click()
                time.sleep(3)
            except NoSuchElementException:
                break
setup()
adclicker()
