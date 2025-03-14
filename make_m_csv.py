import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up Chrome options
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
options.add_argument('--ignore-certificate-errors')  # Disable SSL verification

driver = webdriver.Chrome(service=Service(), options=options)
driver.get("https://www.flashscore.com/")
time.sleep(5)

try:

    dff = pd.read_csv('data.csv')

    # Display the DataFrame
    links = dff['link']
    nums = dff['s/n']
    teams = dff['MATCH NAME']

    cnt = len(nums)
    ii = 0

    while ii < cnt :

        num = nums[ii]
        homeTeam = teams[ii].split("-")[0]
        awayTeam = teams[ii].split("-")[1]
        url = links[ii]
        url = url.replace("match-summary", "h2h/")
        
        
        col1 = []
        col2 = []
        col3 = []
        col4 = []


        homeURL = url+"home"
        
        driver.get(homeURL)

        time.sleep(2)
        
        # scoreDiv = WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH, "//div[@class='detailScore__wrapper']")) ) 

        elements = driver.find_elements(By.CLASS_NAME, "showMore")

        if elements :
            MoreButton = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()='Show more matches']")))
            time.sleep(1)
            MoreButton.click()

        elements = driver.find_elements(By.CLASS_NAME, "showMore")

        if elements :
            MoreButton = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()='Show more matches']")))
            MoreButton.click()
        
        elements = driver.find_elements(By.CLASS_NAME, "showMore")

        if elements :
            MoreButton = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()='Show more matches']")))
            MoreButton.click()

        time.sleep(2)

        spans = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='h2h__result']")))
        
        i = 0
        lenOfSpans = 20

        if lenOfSpans > len(spans):
            lenOfSpans = len(spans)

        while i < lenOfSpans:
            
            span = spans[i]
            texts = span.text.split("\n")
            col1.append(texts[0])
            col2.append(texts[1])

            i = i + 1

        print(col1, col2)

        awayURL = url+"away"
        
        driver.get(awayURL)

        time.sleep(2)
        
        # scoreDiv = WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH, "//div[@class='detailScore__wrapper']")) ) 

        elements = driver.find_elements(By.CLASS_NAME, "showMore")

        if elements :
            MoreButton = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()='Show more matches']")))
            MoreButton.click()

        elements = driver.find_elements(By.CLASS_NAME, "showMore")

        if elements :
            MoreButton = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()='Show more matches']")))
            MoreButton.click()
        
        elements = driver.find_elements(By.CLASS_NAME, "showMore")

        if elements :
            MoreButton = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()='Show more matches']")))
            MoreButton.click()
            
        time.sleep(2)

        spans = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='h2h__result']")))
        
        i = 0
        lenOfSpans = 20

        if lenOfSpans > len(spans):
            lenOfSpans = len(spans)


        while i < lenOfSpans:
            
            span = spans[i]
            texts = span.text.split("\n")
            col3.append(texts[0])
            col4.append(texts[1])

            i = i + 1

        print(col3, col4)

        i = len(col1)
        while i < 20 :
            col1.append(" ")
            i = i + 1
        
        i = len(col2)
        while i < 20 :
            col2.append(" ")
            i = i + 1
        
        i = len(col3)
        while i < 20 :
            col3.append(" ")
            i = i + 1
        
        i = len(col4)
        while i < 20 :
            col4.append(" ")
            i = i + 1

        data = {
            homeTeam: col1,
            "_": col2,
            awayTeam: col3,
            "__": col4
        }

        fileName = "m"+str(num)+".csv"
        df = pd.DataFrame(data)
        df.to_csv(fileName, index=False)

        ii = ii + 1

finally:
    driver.quit()