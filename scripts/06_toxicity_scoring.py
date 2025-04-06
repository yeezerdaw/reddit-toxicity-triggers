import requests
from tqdm import tqdm

def get_toxicity(text, api_key):
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}}
    }
    try:
        response = requests.post(url, json=data)
        result = response.json()
        return result['attributeScores']['TOXICITY']['summaryScore']['value']
    except:
        return None

def add_toxicity_scores(df, api_key, n=200):
    df_sample = df.sample(n=n)
    df_sample["toxicity"] = [get_toxicity(text, api_key) for text in tqdm(df_sample["clean_body"])]
    return df_sample

