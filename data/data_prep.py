import pandas as pd
import re

keywords_job = {
    "Pythonエンジニア": "Pythonエンジニア",
    "Python": "Pythonエンジニア",
    "データエンジニア": "データエンジニア",
    "バックエンド": "バックエンドエンジニア",
    "フロントエンド": "フロントエンドエンジニア",
    "開発": "開発エンジニア",
    "AI": "AIエンジニア",
    "Web": "Webエンジニア",
    "WEB": "Webエンジニア",
    "アプリケーション": "アプリケーションエンジニア",
    "システム": "システムエンジニア",
    "セキュリティ": "セキュリティエンジニア",
    "データサイエンティスト": "データサイエンティスト",
    "アナリスト": "データアナリスト",
    "サーバー":"サーバーエンジニア",
    "機械学習":"機械学習エンジニア",
    "クラウドエンジニア": "クラウドエンジニア",
    "AWS": "クラウドエンジニア",
    "リーダー":"PM",
    "PM": "PM",
    "テックリード": "PM",
    "チームリーダー": "PM",
    "プロダクトマネージャー": "PM",
    "プロジェクトマネージャー":"PM",
    "フルスタック": "フルスタックエンジニア",
    "ソフトウェア":"ソフトウェアエンジニア",
    "SRE":"SRE"

}

def change_title(title):
    for keyword, label in keywords_job.items():
        if keyword in title:
            return label
    return "その他エンジニア"


def has_db_skill(text):
    db_keywords = ["sql", "postgresql", "mysql"]
    text = text.lower() 
    return int(any(keyword in text for keyword in db_keywords))

def has_aws_skill(text):
    aws_keywords = ["aws"]
    text = text.lower() 
    return int(any(keyword in text for keyword in aws_keywords))

def has_ml_skill(text):
    ml_keywords = ["scikit-learn", "scikitlearn", "tensorflow", "pytorch"]
    text = text.lower() 
    return int(any(keyword in text for keyword in ml_keywords))

def has_webfm_skill(text):
    webfm_keywords = ["flask", "django"]
    text = text.lower() 
    return int(any(keyword in text for keyword in webfm_keywords))

def has_bunseki_skill(text):
    bunseki_keywords = ["pandas", "numpy", "tableau", "power"]
    text = text.lower() 
    return int(any(keyword in text for keyword in bunseki_keywords))

def extract_income_range(income_text):
    if isinstance(income_text, str):
        numbers = re.findall(r'\d+', income_text)
        if len(numbers) == 2:
            return int(numbers[0]), int(numbers[1])
    return None, None

def data_preprocess(df):
    df = df.copy()

    df = df[df["skill"].notna() & df["skill"].str.contains("Python", na=False)]
    df["job_title"] = df["job_title"].astype(str).apply(change_title)
    df["Data_base"] = df["skill"].apply(has_db_skill)
    df["AWS"] = df["skill"].apply(has_aws_skill)
    df["ML"] = df["skill"].apply(has_ml_skill)
    df["WebFM"] = df["skill"].apply(has_webfm_skill)
    df["data_analysis"] = df["skill"].apply(has_bunseki_skill)
    df[["min_income", "max_income"]] = df["income"].apply(lambda x: pd.Series(extract_income_range(x)))
    df["avg_income"] = ((df["max_income"] + df["min_income"]) / 2).round(2)


    return df


if __name__ == "__main__":
    df = pd.read_csv("../src/python_jobs.csv")
    df_processed = data_preprocess(df)
    df_processed.to_csv("processed_data.csv", index=False, encoding="utf-8-sig")
    print("✅ 保存完了：processed_data.csv")

