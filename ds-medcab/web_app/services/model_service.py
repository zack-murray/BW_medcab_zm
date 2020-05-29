# web_app/services/model_services.py

import pandas as pd
import os
from os import getenv
from sqlalchemy import create_engine
import dotenv
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from json import loads,dumps
from pandas.io.json import json_normalize
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier

import pickle

class Transformer():
    def __init__(self):
        self.load_data()
        self.tokenizer = Tokenizer(num_words=1000, lower=True)
        return

    def load_data(self):
        """A function that takes the DATABASE_URL and fetches the contents of the
        strain_info table then saves it to a df
        """
        dotenv.load_dotenv()
        alt = 'DATABASE_URL'
        db_url = getenv("DATASOURCE", default=alt)

        engine = create_engine(db_url)
        df = pd.read_sql("SELECT * FROM strain_info", engine)
        self.df = df
        return df

    def transform(self, document: pd.DataFrame, ignore: list,
                  negitive: list) -> pd.DataFrame:
        """A function that takes the document input and transforms it into a MinMax
        scaled DataFrame that represents the term frequency matrix.
        this method adds the dtm's for each feature then subtracts the neg feature's dtm
        then scales the data with a MinMaxScalar from sklearn.preprocessing
        Arguments:
        -------------
        document {list} : An array like list of strings representing a document to be transformed
        negitive {list} : the list of negitive features to use in calculating the dtm products
        ignore {list} : a list of features to ignore in the dtm product
        Returns:
        -------------
        combined_scaled {pd.DataFrame} : A dataframe of the transformed document's tfidf
        """

        dtm = [0] * 1000

        for i in document.columns:
            if i in ignore:
                pass
            else:
                # takes the document term frequency and if it is
                # a neg feature then we want to subtract  it from the combined dtm
                if i in negitive:
                    dtm -= self.find_dtm(self.df[i])
                # otherwise i want to add it to the combined dtm
                else:
                    dtm += self.find_dtm(self.df[i])

        mm = MinMaxScaler()
        combined_scaled_values = mm.fit_transform(dtm)
        combined_scaled_columns = dtm.columns.tolist()
        combined_scaled = pd.DataFrame(combined_scaled_values,
                                       columns=combined_scaled_columns)
        combined_scaled.fillna(0, inplace=True)
        return combined_scaled, self.df.index.tolist()

    def find_dtm(self, feature):
        """A function to take a feature and tokenize then return a tfidf df of that input
        """
        self.tokenizer.fit_on_texts(feature)
        a = self.tokenizer.texts_to_matrix(feature, mode='tfidf')
        config = self.tokenizer.get_config()
        feature_names = json_normalize(loads(
            config['word_index'])).columns.tolist()
        dtm = pd.DataFrame(a, columns=feature_names[:1000])
        return dtm

class Model():

    def __init__(self):
        self.knn = KNeighborsTransformer(n_neighbors=5,n_jobs=-1)

    def fit(self, dtm):
        self.knn.fit(dtm, dtm.index.tolist())

    def predict(self):
        pass

if __name__ == "__main__":
    tr = Transformer()
    negative = ['negative']
    ignore = []
    user_transformed, y = tr.transform(
        pd.DataFrame({'name': "blue berry kush",
                      'race': 'sativa',
                      'flavors': ['blueberry', 'sweet'],
                      'negative': ['dry mouth', 'dry eyes'],
                      'positive': ['creativity', 'stress'],
                      'medical': ['ptsd', 'stress'],
                      'description': "blueberry kush my dude blueberry_kush:10, whitewhidow:10 ",
                      }), negative, ignore)
    model = Model()