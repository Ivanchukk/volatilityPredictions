import os

class FolderManger:

    def __init__(self, market, candleKind):
        self.market = market
        self.candleKind = candleKind


    def createFolder(self):
        directoryMarket = self.market
        directorycandleKind = self.candleKind

  
        # Parent Directory path
        parent_dir = "data_processing/rawDataFolder/"
        
        # Path
        pathmarket = os.path.join(parent_dir, directoryMarket)
        pathcandlekind = os.path.join(parent_dir, directoryMarket, directorycandleKind)

        

        # Create the directory
        # 'GeeksForGeeks' in
        # '/home / User / Documents'
        try:
            os.mkdir(pathmarket)
            print("Directory '% s' created" % directoryMarket)
        except FileExistsError:
            print("Market folder exists - We continue")

        try:
            os.mkdir(pathcandlekind)
            print("Directory '% s' created" % directorycandleKind)
        except:
            print("Candle Kind folder exists - We continue")

    def deleteFolder(self, market):
        directory = market
        parent_dir = "data_processing/rawDataFolder/"
        
        # Path
        path = os.path.join(parent_dir, directory)
        os.rmdir(path)

    def delete_file(self, path):
        os.remove(path)


# FolderManger("testusdt", '1h').createFolder()