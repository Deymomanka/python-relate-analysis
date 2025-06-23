from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_job_cards(soup):
    job_list = []

    job_cards = soup.find_all('div', class_='css-1scr8qj')
    print(f"見つかったjobカードの数: {len(job_cards)}")

    for card in job_cards:
        try:
            job_title_tag = card.find('div', class_='css-9rsp2i') 
            job_title = job_title_tag.text.strip() if job_title_tag else ''

            # 勤務地（もしあれば）
            location_tag = card.find('div', class_='css-kc5p0c') 
            location = location_tag.text.strip() if location_tag else ''

            # 想定年収
            income_tag = card.find('div', class_='css-1l7aayo') 
            income = income_tag.text.strip() if income_tag else ''

            # 関連スキル
            skill_tag = card.find('div', class_='css-16au6i3') 
            skill = skill_tag.text.strip() if skill_tag else ''

            job_list.append({
                'job_title': job_title,
                'location': location,
                'income': income,
                'skill': skill
            })

        except Exception as e:
            print(f"❌ エラー: {e}")
            continue

    return job_list


def get_jobs_with_selenium(query="python", pages=77):

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
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    all_jobs = []

    for page in range(pages):
        print(f"Fetching page {page+1}")
        try:
            # 検索結果読み込みを待つ
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "css-1scr8qj"))
            )
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            jobs = extract_job_cards(soup)
            all_jobs.extend(jobs)

            # 次のページへ（ページネーションの"次へ"リンクをクリック）
            # next_button = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(8)")
            # next_button.click()
            # time.sleep(3)

            # BeautifulSoupで次ページリンクのaタグを取得
            next_svg = soup.find("svg", attrs={"data-testid": "NavigateNextIcon"})
            if next_svg:
                next_a_tag = next_svg.find_parent("a")
                if next_a_tag and next_a_tag.has_attr("href"):
                    next_url = "https://www.green-japan.com" + next_a_tag["href"]
                    driver.get(next_url)
                    page += 1
                    time.sleep(3)
                else:
                    print("✅ 最終ページに到達（リンクなし）")
                    break
            else:
                print("✅ 最終ページに到達（アイコンなし）")
                break




        except Exception as e:
            print(f"❌ ページ {page+1} の取得に失敗: {e}")
            break


    driver.quit()
    return all_jobs


# スクレイピング実行
jobs = get_jobs_with_selenium(query="python", pages=77)
# DataFrameに変換
df = pd.DataFrame(jobs)
# CSVとして保存
df.to_csv("green_python_jobs.csv", index=False, encoding="utf-8-sig")