import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up Chrome options
options = Options()
options.add_argument('--user-data-dir=/home/leo/.config/google-chrome')
options.add_argument('--profile-directory=Default')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
options.add_argument('--ignore-certificate-errors')  # Disable SSL verification
 
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.flashscore.com/")
time.sleep(20)

try:

    df = pd.read_csv('data.csv')

    # Display the DataFrame
    links = df['link']
    scores = []

    i = 1

    for link in links:

        driver.get(link)

        time.sleep(3)
        
        scoreDiv = WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'detailScore__wrapper')]")) )
        text = scoreDiv.text
        arr = text.split("\n")

        print(i)

        score = ""

        if len(arr) < 3 :
            score = " - " 
        
        else :
            score = arr[0] + ":" + arr[2]

        scores.append(score)
        
        i = i + 1
 
    print(scores)
    df['Results'] = scores
    df.to_csv('updated_data.csv', index=False)

finally:
    driver.quit()