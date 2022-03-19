import pandas as pd
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'volkey.json'
from google.cloud import storage
from datetime import datetime
# Instantiates a client


client = storage.Client()

# Create a New Bucket 

# bucket_name = "volatility1"
    # bucket = client.bucket(bucket_name)
    # bucket.location = "US"
    # bucket = client.create_bucket(bucket)
    # Upload Files 
class GgCloud:
    def __init__(self, market, candleKind, bucket_name="volatility1"):
        self.market = market
        self.candleKind = candleKind
        self.bucket_name = bucket_name

    def upload_to_bucket(self,blob_name, file_path):

        today = datetime.now()
        # dd/mm/YY
        d1 = today
        print('d1'* 20 )
    
        try:
            bucket = client.get_bucket(self.bucket_name)
            blob = bucket.blob(f"{blob_name}/{self.candleKind}/{self.market}Candle{d1}")
            blob.upload_from_filename(file_path)
            return True
        except Exception as e:
            print(e)
            return False

    # file_path = "./rawDataFolder"
    # upload_to_bucket('KNCUSDT1mCandle', os.path.join(file_path, 'KNCUSDT1mCandle.pkl'), bucket_name)
    # upload_to_bucket('knc/KNCUSDT1mCandle', os.path.join(file_path, 'KNCUSDT1mCandle.pkl'), bucket_name)

    # Retrieve an existing bucket
    # https://console.cloud.google.com/storage/browser/[bucket-id]/

    def download_bucket(self, blob_name, file_path):
        try:
            bucket = client.get_bucket(self.bucket_name)
            # blob = bucket.blob(blob_name)
            blob = bucket.blob(blob_name)

            print(blob)
            print(file_path)
            with open(file_path, 'wb') as f:
                print(file_path)
                file = client.download_blob_to_file(blob, f)
                print(1)
                print(file)
                print(2)
            print(pd.read_pickle(file))
            return file
        except Exception as e:
            print(e)
            return False
    
    def getBlobsNames(self, prefix):
        prefix = prefix[:3]
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(self.bucket_name)
        return bucket.list_blobs()

    def downloadFiles(self, prefix, dl_dir):
        # bucket_name = 'your-bucket-name'
        # prefix = 'your-bucket-directory/'
        # dl_dir = 'your-local-directory/'
        print("IM in download file" * 5)
        
        print(dl_dir)
        # prefix = prefix[:3]
        print(prefix*5)
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
        print(blobs)
        for blob in blobs:
            print("z" *20)
            print(blob)
            if blob.name.split('/')[0] == self.market.lower() and blob.name.split('/')[1] == self.candleKind:
                filename = blob.name.replace('/', '_') 
                print(filename * 10)
                blob.download_to_filename(f"{dl_dir}/{filename}.pkl")  # Download
            else:
                pass

    def delete_blob(self, blob_name):
        bucket = client.get_bucket(self.bucket_name)
        # list all objects in the directory
        blob = bucket.blob(blob_name)
        blob.delete()

        print("Blob {} deleted.".format(blob_name))

    def delete_all_blob(self, prefix):
        bucket = client.get_bucket(self.bucket_name)
        # list all objects in the directory
        blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
        print(blobs)
        for blob in blobs:
            blob.delete()

# GgCloud.download_bucket('knc', os.path.join(os.getcwd(), './rawDataFolder/kncFolder'), bucket_name)
# file_path = "./rawDataFolder"
# # GgCloud().upload_to_bucket('knc/KNCUSDT1mCandle03', os.path.join(file_path, 'KNCUSDT1mCandle.pkl'), bucket_name)
# GgCloud().downloadFiles('volatility1', 'knc/', os.path.join(os.getcwd(), 'data_processing/rawDataFolder/KNCUSDT/new'))
# df = pd.read_pickle('./rawDataFolder/newknc_KNCUSDT1mCandle03.pkl')
# print(df.size)
# print(df.shape)
# path = "./rawDataFolder"
# dir_list = os.listdir(path)
# df = pd.DataFrame()
# for f in dir_list:
#     if f[-3:] == 'pkl':
#         df = pd.concat([df, pd.read_pickle('./rawDataFolder/{}'.format(f))])
#     else:
#         pass
# # df = pd.concat([pd.read_pickle('./rawDataFolder/{}'.format(f)) 
# #                 for f in dir_list], 
# #                axis=1)
# print(df.size)
# print(df.shape)

# # path = "./rawDataFolder"
# # dir_list = os.listdir(path)
 
# # print("Files and directories in '", path, "' :")
 
# # # prints all files
# print(dir_list)



def getBlobsNames():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('volatility1')
    a = bucket.list_blobs()
    lstBlobs = []
    for blob in a:
        filename = blob.name.replace('/', '_') 
        print(filename)
        marketBlob = filename.split("_")[0]
        print(marketBlob)
        lstBlobs.append(marketBlob)
    return set(lstBlobs)
