import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_reviews = pd.read_csv('./crawling_data/one_sentences.csv')
df_reviews.info()

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df_reviews['reviews'])
print(tfidf_matrix[0].shape)
with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(tfidf, f)
mmwrite('./models/tfidf_movie_review.mtx', tfidf_matrix)