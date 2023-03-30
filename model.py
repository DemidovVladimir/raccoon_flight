import pandas as pd

class Model:
    @staticmethod
    def read():
        try:
            return pd.read_csv('data.csv')
        except FileNotFoundError:
            print('File not found')