import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/review_final.csv')
df.info()
print(df.head())

df_stopwords = pd.read_csv('./stopwords.csv', index_col=0)
stopwords = list(df_stopwords['stopword'])
stopwords = stopwords + ['안나', '제니퍼', '미국', '중국', '영화', '감독', '리뷰', '연출',
                         '장면', '주인공', '되어다', '출연', '싶다', '올해', '엘사']
okt = Okt()
df['clean_reviews'] = None
count = 0
for idx, review in enumerate(df.reviews):
    count += 1
    if count % 10 == 0:
        print('.', end='')
    if count % 1000 == 0:
        print()
    review = re.sub('[^가-힣 ]', ' ', review)
    df.loc[idx, 'clean_reviews'] = review
    token = okt.pos(review, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_token = df_token[(df_token['class']=='Noun') |
                        (df_token['class']=='Verb') |
                         (df_token['class']=='Adjective')]
    words = []
    for word in df_token.word:
        if len(word) > 1:
            if word not in list(df_stopwords.stopword):
                words.append(word)
    cleaned_sentence = ' '.join(words)
    df.loc[idx, 'clean_reviews'] = cleaned_sentence
print(df.head(30))
df.dropna(inplace=True)
df.to_csv('./crawling_data/cleaned_reviews_2016_2022.csv', index=False)


























