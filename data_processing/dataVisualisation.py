import dtale
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
class Visualisation:
    def __init__(self):
        pass

    def dtal(self, df):
        # df = pd.read_pickle("./data_processing/results/.pkl")
        d = dtale.show(df, subprocess=False)
        # print(dtale.instances())
        # print(d.link())
        # d.open_browser()

    def plotLine(self, x, y):
        plt.figure(figsize=(20,15))
        plt.plot(x, y)

        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)

        fig.savefig('WebExample/static/charts/lineChart.png')        



    def plot_predictions(self, test, predicted):

        plt.plot(test, color='red',label=f"Real  volatility")
        plt.plot(predicted, color='blue',label=f"Predicted  volatility")
        plt.title(f" Volatility Prediction")
        plt.xlabel('Time')
        plt.ylabel(f" Volatility")
        plt.legend()
        plt.show(block=True)

        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)

        fig.savefig('WebExample/static/charts/foo.png')





# a = Visualisation()

# data = pd.read_pickle("./rawDataFolder/LINKUSDT/LINKUSDTfull.pkl")

# a.dtal(data)
