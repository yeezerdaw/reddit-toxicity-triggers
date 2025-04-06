import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

def plot_top_words(df, top_n=20):
    stop_words = set(stopwords.words('english'))
    words = ' '.join(df['clean_body'].dropna()).split()
    filtered = [w for w in words if w not in stop_words and len(w) > 2]
    word_freq = Counter(filtered)
    top_words = word_freq.most_common(top_n)

    words, freqs = zip(*top_words)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(freqs), y=list(words), palette="magma")
    plt.title("Top Common Words (Excluding Stopwords)")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.tight_layout()
    plt.show()

    wc = WordCloud(width=1000, height=500, background_color='white').generate_from_frequencies(word_freq)
    plt.figure(figsize=(15, 7))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title("Word Cloud")
    plt.show()

