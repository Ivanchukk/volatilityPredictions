# from data_loader import DataLoader
class DataProcessor:

    def __init__(self, df):
        self.df = df

    def process_data_for_analysis(self):
        self.clean_na()
        self.cleanDuplicates()
        self.changeToFloat()
        return self.df

        

    def process_data_for_model(self):
        self.process_data_for_analysis()
        self.changeToFloat()
        return self.df
        

    def clean_na(self):
        # code that looks for bad values in data and cleans them out
        print(self.df.isna().sum().sum())
        if self.df.isna().sum().sum() > 0:
            print(self.df[self.df.isna()].head())
            print(f'There is {self.df.isna().sum()} in total')
            return self.checkIfok('nan')
        else:
            print("There is no NaN")
            return self.df
        print(f"DataProcessor: Data cleaned")
    
    def cleanDuplicates(self):
        if self.df.duplicated().sum() > 0:
            print(self.df[self.df.duplicated()].head())
            print(f'There is {self.df.duplicated().sum()} in total')
            return self.checkIfok('duplicates')
        else:
            print("There is no Duplicates")
            return self.df

    def checkIfok(self, issue):
        print(f"{issue} press 'continue' if you want to stop the nans and continue calculate or press 'stop' id you want to stop the calculation and review the data.")
        checkIfok = 'continue'
        if checkIfok == "stop":
            raise ValueError('The program stoped. Review the data.')
        elif checkIfok == "continue":
            if issue == 'nan':
                return self.df.dropna()
            else:
                return self.df.drop_duplicates()
        else:
            raise ValueError('Wrong Input.')
    
    def changeToFloat(self):
        self.df[['open', 'high', 'low', 'close', 'volume']] = self.df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        return self.df

    # def fill_missing(self):
    #     # code that fills up missing values in the data
    #     print(f"DataProcessor: Filled up missing values")

    # def normalize(self):
    #     # code that normalizes data (z-score, maybe turning string categories to numbers, etc...)
    #     print(f"DataProcessor: Normalized data")

    

# data = DataLoader("KNCUSDT").load_local_pkl()
# print(data)
# a = DataProcessor(data)
# a.process_data_for_analysis()