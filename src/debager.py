from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("URL")

search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='SearchFormInput']"))
)

search_box.send_keys("Python")
search_box.send_keys(Keys.RETURN)

time.sleep(5)

html = driver.page_source
driver.quit()

with open("search_result.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 検索結果ページ保存完了")
