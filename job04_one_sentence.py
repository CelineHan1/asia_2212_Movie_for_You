import pandas as pd

df = pd.read_csv('./crawling_data/cleaned_reviews_2016_2022.csv')
df.dropna(inplace=True)
df.info()
one_sentences = []
for title in df['titles'].unique():
    temp = df[df['titles']==title]
    if len(temp) > 30:
        temp = temp.iloc[:30, :]
    one_sentence = ' '.join(temp['clean_reviews'])
    one_sentences.append(one_sentence)
df_one = pd.DataFrame({'titles':df['titles'].unique(), 'reviews':one_sentences})
print(df_one.head())
df_one.to_csv('./crawling_data/one_sentences.csv', index=False)
