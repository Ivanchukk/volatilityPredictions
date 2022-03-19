from keras.layers import *
from keras import layers, Sequential
import pandas as pd
import numpy as np

class Model:
    def __init__(self, X_train, y_train, X_test, y_test, yscaler, predict_fields, sequence_length, features, neurons, activefunc, numEpochs, batchSize, optimizer):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.yscaler = yscaler
        self.neurons = neurons
        self.activefunc = activefunc
        self.numEpochs = numEpochs
        self.batchSize = batchSize
        self.optimizer = optimizer
        print("*****")
        print(predict_fields)
        self.predict_fields = predict_fields
        self.features = features
        self.sequence_length = sequence_length
        self.createModel()
        self.trainModel()
        self.predict()


    def createModel(self):
        neurons = 16
        self.model = Sequential(
            [layers.LSTM(units=self.neurons, input_shape=(self.X_train.shape[1:]), return_sequences=True, activation=self.activefunc),
            Dense(units=8),
            layers.LSTM(units=4, input_shape=(self.X_train.shape[1:]), return_sequences=False, activation=self.activefunc),
            
            Dense(units=1)]
        )
        return self.model

    def modelSummery(self):
        return self.model.summary()

    def trainModel(self, losss='mean_squared_error'):
        self.model.compile(optimizer=self.optimizer, loss=losss) #adam , mean_squared_error
        self.model.fit(self.X_train, self.y_train, epochs=self.numEpochs, batch_size=self.batchSize, validation_data=(self.X_test, self.y_test))
        return self.model


    def predict(self):
        self.predicted = self.yscaler.inverse_transform(self.model.predict(self.X_test))
        self.test = self.yscaler.inverse_transform(self.y_test.reshape(-1,1))
        return self.predicted, self.test

        # run model prediction on received data
    
    def evaluate(self, checkpoint=None):
        print("111111")
        print(self.predict_fields)
        print(f"Results for  volatility prediction")
        print(f"Predict_field: {self.predict_fields}, sequence_len: {self.sequence_length}, features: {self.features}\n\n")
        # Run code that prints evaluation for the model (accuracy, scores, errors, etc) 
        preds_list = self.predicted.reshape((self.predicted.shape[0],))
        real_vals_list = self.test.reshape((self.test.shape[0],))
        diff = preds_list - real_vals_list  
        diff_percent = np.round((diff / real_vals_list) * 100, 1)
        pd.DataFrame(data={'predictions': preds_list, 
                    'true_values': real_vals_list,
                    'diff': diff,
                    'diff %': diff_percent})


        # resultMAE = f"Mean absolute error: {np.average(np.abs(diff))}\n"
        # resultMAEstd = f"Mean absolute error std: {np.std(np.abs(diff))}\n"

        # resultMAE = f"% Mean absolute error: {np.round(np.average(np.abs(diff_percent)), 1)}%\n"
        # resultMAEstd = f"% Mean absolute error std: {np.round(np.std(np.abs(diff_percent)), 1)}%\n"

        resultMAE = f"{np.round(np.average(np.abs(diff_percent)), 1)}%\n"
        resultMAEstd = f"{np.round(np.std(np.abs(diff_percent)), 1)}%\n"

        print(resultMAE)
        print(resultMAEstd)
        return diff_percent, preds_list, real_vals_list, resultMAE, resultMAEstd



    def _load_model(self):
        # load model from the checkpoint and assign in to self.my_model
        print(f"Model loaded")

# data = pd.read_pickle("data_processing/rawDataFolder/KNCUSDT/1h/KNCUSDT_1hfull.pkl")
# md = Model(FeatureExtractor(data).createSequences())
