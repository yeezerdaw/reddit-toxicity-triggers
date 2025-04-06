import re

def extract_sentences_with_keyword(df, keyword="india"):
    sentences = []
    for comment in df['clean_body'].dropna():
        for sentence in re.split(r'(?<=[.!?]) +', comment):
            if keyword in sentence.lower():
                sentences.append(sentence)
    return sentences

