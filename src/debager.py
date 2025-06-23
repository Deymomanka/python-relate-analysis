from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# ヘッドレスオプション
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

# Chrome起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Greenの検索ページを開く
driver.get("https://www.green-japan.com/search")

# 検索ボックスに"Python"を入力してEnter
# ② 検索ボックスを取得（←セレクタ変更）
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='SearchFormInput']"))
)

# ③ Pythonを入力して検索
search_box.send_keys("Python")
search_box.send_keys(Keys.RETURN)

# 結果の読み込み待ち
time.sleep(5)

# HTML取得
html = driver.page_source
driver.quit()

# 保存して後で分析
with open("green_search_result.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 検索結果ページ保存完了")
