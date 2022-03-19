from math import sqrt, log

class VolatlityCalculation():
    
    def __init__(self, df):
        self.df = df

    def parkinson(self, high, low, N=30):
        sum_hl = sum(log(H_t / L_t) ** 2 for H_t, L_t in zip(high, low))
        return sqrt(sum_hl * N / (4 * len(high) *log(2)))
    
    def infinite_sequence(self, interval=30):
        lst = []
        print(self.df.dtypes)
        highest = self.df['unixDate'].size # Write Function
        num = 0
        while num < highest:
            lst.append(self.parkinson(self.df['high'].iloc[num:num+interval].tolist(), self.df['low'].iloc[num:num+interval].tolist(), interval))
            num += 1
        self.df['volatility'] = lst

        return self.df




# data = DataLoader("KNCUSDT").load_local_pkl()
# b = DataProcessor(data)
# c = b.process_data_for_model()

# a = VolatlityCalculation(c)
# vol = a.infinite_sequence(30)
# print(vol.volatility)