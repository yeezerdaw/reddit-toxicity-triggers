from collections import Counter
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

def get_context_words(df, target="india"):
    before_words, after_words = [], []
    stop_words = set(stopwords.words('english'))

    for comment in df['clean_body'].dropna():
        tokens = comment.split()
        for i, word in enumerate(tokens):
            if word.lower() == target:
                if i > 0 and tokens[i-1].lower() not in stop_words:
                    before_words.append(tokens[i-1].lower())
                if i < len(tokens)-1 and tokens[i+1].lower() not in stop_words:
                    after_words.append(tokens[i+1].lower())

    return Counter(before_words).most_common(20), Counter(after_words).most_common(20)

