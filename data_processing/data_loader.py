from datetime import datetime, timedelta, date
# from msilib.schema import CreateFolder
import time
from http import client
import pandas as pd
from binance.client import Client
import numpy as np
from data_processing.googleCloud import GgCloud
from data_processing.folderManager import FolderManger 
import os



class DataLoader:

    def __init__(self, market, minutesToRecord, candleKind):
        self.market = market
        self.minutesToRecord = minutesToRecord
        self.candleKind = candleKind

    def load_cloud_pkl(self, blob_name ,bucket_name):
        # here add some logic that loads the data (from local file / cloud storage / url / etc)
        # inheritance can be handy here
        FolderManger().createFolder(self.market)
        pathh = f'data_processing/rawDataFolder/{self.market}/{self.market}1mCandle.pkl'
        file_path = os.path.join(os.getcwd(), pathh)

        GgCloud.download_bucket(blob_name, file_path, bucket_name)
        df = pd.read_pickle(file_path)
        # df = pd.read_pickle(f"./data_processing/rawDataFolder/{self.market}1mCandle.pkl") # lets say it was loaded from local csv
        return df

    def load_multi_pkl(self):
        path = f"./data_processing/rawDataFolder/{self.market}/{self.candleKind}/"
        dir_list = os.listdir(path)
        df = pd.DataFrame()
        for f in dir_list:
            if f[-3:] == 'pkl' and f[-5:] != '_.pkl':
                df = pd.concat([df, pd.read_pickle(path + f'/{f}')])
            else:
                pass
        df.to_pickle(path + self.market + self.candleKind +"full.pkl")

    # def save_full_pkl(self, df, path):
    #     df.to_pickle(path + self.market + "full.pkl")

    def load_full_pkl(self, raw_path):
        print("o"*20)
        # path = os.path.join(os.getcwd(), f'data_processing/rawDataFolder/{self.market}/{self.market}full.pkl')
        path = f"{raw_path}/{self.market}{self.candleKind}full.pkl"
        print(path)
        df = pd.read_pickle(path) 
        return df
        

    def load_local_pkl(self):
        df = pd.read_pickle(f"./data_processing/rawDataFolder/{self.market}1mCandle.pkl") # lets say it was loaded from local csv
        return df

    def connect_to_binance(self):
        api_key = ''
        api_secret = ''
        return Client(api_key, api_secret)
        

    def get_candles_by_date(self, startDate, endDate):
        # reload data from the internet and store it locally
        if self.candleKind == '1m':
            ck = Client.KLINE_INTERVAL_1MINUTE
        elif self.candleKind == '5m':
            ck = Client.KLINE_INTERVAL_5MINUTE
        elif self.candleKind == '15m':
            ck = Client.KLINE_INTERVAL_15MINUTE
        elif self.candleKind == '30m':
            ck = Client.KLINE_INTERVAL_30MINUTE
        elif self.candleKind == '1h':
            ck = Client.KLINE_INTERVAL_1HOUR
        elif self.candleKind == '1d':
            ck = Client.KLINE_INTERVAL_1DAY

        client = self.connect_to_binance()
        klines = client.get_historical_klines("{}".format(self.market.upper()), ck, str(startDate), str(endDate))
        dfKline = pd.DataFrame(klines)
        lst = []
        for i in klines:
            datee = datetime.fromtimestamp(i[0] / 1000)
            lst.append(str(datee))

        dfKline['date'] = lst
        try:
            dfKline.columns = ['unixDate', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'qouteVolume', 'numberOfTrades', 'takerBaseVolume', 'takerQuoteVolume', 'ignore', 'date']
            return dfKline
        except ValueError:
            print("=" * 20)
            print("Candle data is up to date")
        # print(f"DataLoader: Loaded data from {url} and stored it to {target_path}")
        

    def record_candles_to_pkl_full(self, startDate='2022-01-01', mnt=1440):
        # This function will record 1m candles 8 hours from activation. In the next day it will start from last minute recorded
        # In the first ever itteration we will need an emppty DataFrame
        print("Starting recording")
        mm = self.market
        print(mm)
        path = f"data_processing/rawDataFolder/{self.market}/{self.candleKind}/{self.market}_{self.candleKind}full.pkl"
        print('The path is ', path)
        startDate = datetime.strptime(startDate, "%Y-%m-%d")
        df = pd.DataFrame()
        i = 0
        print(self.minutesToRecord * 20)
        while i < int(self.minutesToRecord):
            print("record iteretion number ", i)
            print("enter while")
            try:
                #If it not the firs iteration we will load data from previues itterations 
                df = pd.read_pickle(path)
            except:
                df = pd.DataFrame()

            print('before first if')
            if df.size == 0:
                df_ = self.get_candles_by_date(startDate, startDate+timedelta(minutes=mnt))
            else:
                startDate = df.tail(1)['date'].iloc[0]
                startDate = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S")
                
                if i == 0:
                    endDate = date.today()
                    df_ = self.get_candles_by_date(startDate, endDate)
                else:
                    df_ = self.get_candles_by_date(startDate, startDate+timedelta(minutes=mnt))

            try:
                # FolderManger().createFolder(self.market)
                df_ = df_.reset_index()
                df = pd.concat([df, df_], axis=0)
                df = df.drop_duplicates()
                df.to_pickle(path)
                i += 1
                time.sleep(5)
            except AttributeError:
                i+=1000000
                print("=" * 20)
                print("Candle data is up to date")
        return path
    
    def record_candles_to_pkl(self, startDate='2022-01-01', mnt=1440):
        # This function will record 1m candles 8 hours from activation. In the next day it will start from last minute recorded
        # In the first ever itteration we will need an emppty DataFrame
        startDate = datetime.strptime(startDate, "%Y-%m-%d")
        df = pd.DataFrame()
        i = 0
        while i < self.minutesToRecord:
            print("enteer whuile")
            try:
                #If it not the firs iteration we will load data from previues itterations 
                df = pd.read_pickle(f"./data_processing/rawDataFolder/{self.market}1mCandle.pkl")
            except:
                df = pd.DataFrame()

            print('before first if')
            if df.size == 0:
                df_ = self.get_candles_by_date(startDate, startDate+timedelta(minutes=mnt))
            else:
                startDate = df.tail(1)['date'].iloc[0]
                startDate = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S")
                if i == 0:
                    endDate = date.today()
                    df_ = self.get_candles_by_date(startDate, endDate)
                else:
                    df_ = self.get_candles_by_date(startDate, startDate+timedelta(minutes=mnt))

            df_ = df_.reset_index()
            df = pd.concat([df, df_], axis=0)
            df = df.drop_duplicates()
            df.to_pickle(f"./data_processing/rawDataFolder/{self.market}1mCandle.pkl")
            i += 1
            time.sleep(5)
        return

# a = DataLoader('KNCUSDT')
# a.record_candles_to_pkl()

# bucket_name = 'volatility1'
# a = DataLoader("KNCUSDT")
# # bb = a.load_multi_pkl(bucket_name,"knc", os.path.join(os.getcwd(), 'data_processing/rawDataFolder/KNCUSDT/new'))
# gc = GgCloud()


# gc.upload_to_bucket("kncNew", a.record_candles_to_pkl_full('2022-01-01', 1440))