import pandas as pd
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'u/\w+', '', text)
    text = re.sub(r'r/\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_and_clean(path):
    df = pd.read_csv(path)
    df.drop_duplicates(subset=["comment_id"], inplace=True)
    df.dropna(subset=["body"], inplace=True)
    df['clean_body'] = df['body'].apply(clean_text)
    return df

def save_cleaned(df, path="data/cleaned_indian_comments.csv"):
    df.to_csv(path, index=False)

