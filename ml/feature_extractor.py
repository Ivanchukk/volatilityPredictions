import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler

class FeatureExtractor:
    def __init__(self, df, seq_len):
        self.df = df
        self.seq_len = seq_len
 
        
        

    def featuresAndPredictionSelection(self):
        self.features = ['takerBaseVolume', 'qouteVolume', 'high', 'low', 'volatility']
        self.predict_field = 'volatility'
        return self.features, self.predict_field
        

    def sequence_length(self):
        self.sequenceLength = 1
        return self.sequenceLength

    def columnsLst(self):
        self.cols = self.train_ds.columns
        return self.cols
    
    def trainTest(self):
        train_data_to = int(self.df.size*0.8)
        test_data_from = 1 - train_data_to
        self.train_ds = self.df[:train_data_to][self.features]
        self.test_ds = self.df[test_data_from:][self.features]
        return self.test_ds, self.train_ds

    def predictionDataScale(self):
        yscaler = StandardScaler()
        yscaler = yscaler.fit(self.train_ds[[self.predict_field]])
        # return yscaler.mean_, yscaler.scale_ 
        return yscaler
    
    def featureDataScale(self):
        sc = StandardScaler()
        sc = sc.fit(self.train_ds)
        self.train_ds_scaled = pd.DataFrame(sc.transform(self.train_ds), columns=self.features)
        self.test_ds_scaled = pd.DataFrame(sc.transform(self.test_ds), columns=self.cols)
        return self.train_ds_scaled, self.test_ds_scaled

    def create_sequences(self, data):
        X = []
        y = []
        # seq_len = 5
        for i in range(self.seq_len, len(data)):
            X.append(data[i-self.seq_len:i])
            y.append(data[self.predict_field][i])
        X, y = np.array(X), np.array(y)
        return X, y

    def createSequences(self):
        self.featuresAndPredictionSelection()
        self.trainTest()
        self.columnsLst()
        self.sequence_length()
        self.featureDataScale()
        X_train, y_train = self.create_sequences(self.train_ds_scaled)
        X_test, y_test = self.create_sequences(self.test_ds_scaled)
        return X_train, y_train, X_test, y_test, self.predictionDataScale(), self.predict_field, self.features, self.sequence_length()

    
        # Scaling for features (X)


# a = FeatureExtractor(data).createSequences()