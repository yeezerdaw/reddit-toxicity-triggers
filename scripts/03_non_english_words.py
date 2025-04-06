from nltk.corpus import words, stopwords
from collections import Counter
import nltk
nltk.download('words')
nltk.download('stopwords')

def get_non_english_words(df):
    english_vocab = set(words.words())
    stop_words = set(stopwords.words('english'))

    all_words = ' '.join(df['clean_body'].dropna()).split()
    filtered = [w.lower() for w in all_words if w.isalpha() and w.lower() not in stop_words]
    non_english = [w for w in filtered if w not in english_vocab]

    return Counter(non_english).most_common(50)

