import pandas as pd
import sys 
import os
print(os.path.abspath(os.getcwd()))
sys.path.append('../MLDIR')
print(os.path.abspath(os.getcwd()))
from ml.feature_extractor import FeatureExtractor
from ml.model import Model
from data_processing.data_analyzer import DataAnalyzer
from data_processing.data_loader import DataLoader
from data_processing.data_processor import DataProcessor
from data_processing.volatilityCalculation import VolatlityCalculation
from data_processing.googleCloud import GgCloud
from data_processing.folderManager import FolderManger
from data_processing.dataVisualisation import Visualisation
from datetime import datetime


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Manage my machine learning processing pipeline')

#     parser.add_argument('action',
#                         type=str,
#                         choices=['reload_data_from_url', 'analyze_data',
#                                  'train_model', 'evaluate_model', 'predict_model'],
#                         help='Action to perform on the model (train/evaluate/predict)')

#     parser.add_argument('--data-url',
#                         type=str,
#                         default=None,
#                         help='url to load the data from')

#     parser.add_argument('--target_path',
#                         type=str,
#                         default=None,
#                         help='local path to store the output')

#     parser.add_argument('--data-path',
#                         type=str,
#                         default=None,
#                         help='url to load the data from')

#     args = parser.parse_args()
#     print('Parameters: {}'.format(args))

#     if args.action == 'reload_data_from_url':
#         if not args.data_url or not args.target_path:
#             print('Missing arguments')
#             exit(1)

#         data_loader = DataLoader()
#         data_loader.load_from_url(args.data_url, args.target_path)

#     elif args.action == 'analyze_data':
#         if not args.data_path or not args.target_path:
#             print('Missing arguments')
#             exit(1)

#         data_loader = DataLoader()
#         loaded_data = data_loader.load_local_csv(args.data_path)
#         data_processor = DataProcessor(loaded_data)
#         processed_data = data_processor.process_data_for_analysis()
#         data_analyzer = DataAnalyzer(processed_data)
#         data_analyzer.perform_full_analysis(args.target_path)
#     else:
#         pass

import os
import sys
# print(os.path.abspath(os.getcwd()))
# for i in sys.path:
#     print(i)

def main(recordNewData, market ,minutesTorecord, recordstartDate, bucket_name='volatility1'):
    blob_name = market.lower()
    gs = GgCloud(market)
    dl = DataLoader(market, minutesTorecord)

    # Create raw data floder if not excists 
    FolderManger(market).createFolder()

    # Download latest files in Cloud
    prefix = blob_name
    dl_dir = os.path.join(os.getcwd(), f'data_processing/rawDataFolder/{market}')
    gs.downloadFiles(bucket_name, prefix, dl_dir)
        

    # upload Candle To Bucket

    dl.load_multi_pkl()

    gs.delete_all_blob(bucket_name, prefix)

    gs.upload_to_bucket(blob_name, dl_dir, bucket_name = 'volatility1')
    
    if recordNewData not in [True, False]:
        raise ValueError("recordNewData should be True or False")

    if recordNewData == True:
        path = dl.record_candles_to_pkl_full(recordstartDate, minutesTorecord)
        print("recording "* 10)
        print(blob_name)
        print(path)
        gs.upload_to_bucket(blob_name, path, bucket_name)
    else:
        pass
    print("+" *20)
    print(dl_dir)
    data= dl.load_full_pkl(dl_dir)

    dataP = DataProcessor(data).process_data_for_analysis()

    dataV = VolatlityCalculation(dataP).infinite_sequence()
    fea = FeatureExtractor(dataV).createSequences()

    X_train = fea[0]
    y_train = fea[1]
    X_test = fea[2]
    y_test = fea[3]
    yscaler = fea[4]
    predict_field = fea[5]
    print("A")
    print(predict_field)
    features = fea[6]
    sequence_length = fea[7]

    diff_percent, preds_list, real_vals_list = Model(X_train, y_train, X_test, y_test, yscaler, predict_field, features, sequence_length).evaluate()
    now = datetime.now()
    print(preds_list)
    print(real_vals_list)
    results = pd.DataFrame([preds_list, real_vals_list])
    
    results = results.T
    results.columns = ["predictions", "RealValues"]
    print(results)
    results.to_csv(f"./data_processing/results/{market}_results{now}.csv")
    vs = Visualisation()
    vs.plot_predictions(diff_percent, preds_list, real_vals_list)
    vs.dtal(results)

# main(True, "KNCUSDT", 1, "2021-01-01")
'''
initial paramns
List of all params I want to pass to the program. 
    market
    start recording date
    new market / old market
    record new data boolian 
    minutesTorecord
    candle kind

ML params
    seq_len = How many candles to predict on
    sequence_length = ?
    noirons=8
    active="tanh"
    denseUnits=1 off as it always 1 (if it one layer)
    opt="adam"
    losss='mean_squared_error'
    numEpochs=70
    batchSize=68

    layers

data params
    Out sources data

'''
# import pandas as pd
# df = pd.read_pickle("./data_processing/rawDataFolder/KNCUSDT/KNCUSDTfull.pkl")
# print(df.head())
# print(df.tail())

def main1(market): #without clound 

    record_data = DataLoader("KNCUSDT", 50).record_candles_to_pkl()
    data = DataLoader("KNCUSDT").load_local_pkl()

    # a = DataProcessor(data)
    # a.process_data_for_analysis()
    dataP = DataProcessor(data).process_data_for_analysis()

    dataV = VolatlityCalculation(dataP).infinite_sequence()
    fea = FeatureExtractor(dataP).createSequences()

    X_train = fea[0]
    y_train = fea[1]
    X_test = fea[2]
    y_test = fea[3]
    yscaler = fea[4]
    predict_fields = fea[5]
    print("A")
    print(predict_fields)
    features = fea[6]
    sequence_length = fea[7]

    mdl = Model(X_train, y_train, X_test, y_test, yscaler, predict_fields, features, sequence_length).evaluate()


def recordData(market ,minutesTorecord, recordstartDate, bucket_name='volatility1'):
    blob_name = market.lower()
    gs = GgCloud(market)
    dl = DataLoader(market, minutesTorecord)
    print("Starting Recording process")
    path = dl.record_candles_to_pkl_full(recordstartDate, minutesTorecord)
    print("recording "* 10)
    print(blob_name)
    print(path)
    gs.upload_to_bucket(blob_name, path, bucket_name)
