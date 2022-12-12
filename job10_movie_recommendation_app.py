import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
import pandas as pd
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import linear_kernel


form_window = uic.loadUiType('./movie_recommendation_app.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')

        self.df_reviews = pd.read_csv('./crawling_data/one_sentences.csv')
        self.titles = self.df_reviews['titles']
        self.titles = sorted(self.titles)
        for title in self.titles:
            self.combo_box.addItem(title)

        model = QStringListModel()
        model.setStringList(self.titles)
        completer = QCompleter()
        completer.setModel(model)
        self.line_edit.setCompleter(completer)

        self.combo_box.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommend.clicked.connect(self.btn_slot)

    def recommendation_by_movie_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        cosin_sim = linear_kernel(self.tfidf_matrix[movie_idx], self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)
        recommendation = '\n'.join(list(recommendation[1:]))
        self.lbl_recommend.setText(recommendation)

    def btn_slot(self):
        key_word = self.line_edit.text()
        if key_word in self.titles:
            self.recommendation_by_movie_title(key_word)
        elif key_word in list(self.embedding_model.wv.index_to_key):
            embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
            sim_word = embedding_model.wv.most_similar(key_word, topn=10)
            words = [key_word]
            for word, _ in sim_word:
                words.append(word)
            print(words)
            sentence = []
            count = 11
            for word in words:
                sentence = sentence + [word] * count
                count -= 1
            sentence = ' '.join(sentence)
            print(sentence)
            sentence_vec = self.tfidf.transform([sentence])
            cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
            recommendation = self.getRecommendation(cosin_sim)
            recommendation = '\n'.join(list(recommendation[1:]))
            self.lbl_recommend.setText(recommendation)

    def combobox_slot(self):

        title = self.combo_box.currentText()
        self.recommendation_by_movie_title(title)

    def getRecommendation(self, cosin_sim):
        simScore = list(enumerate(cosin_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        movie_idx = [i[0] for i in simScore]
        print(len(movie_idx))
        recMovieList = self.df_reviews.iloc[movie_idx, 0]
        print(recMovieList)
        return recMovieList


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
