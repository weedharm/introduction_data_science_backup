import numpy as np
import pandas as pd
import pickle

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

DATA_FILE_PATH = '../visualizeandmodelandata/final_data.csv'
MODEL_SAV_FILE = '../visualizeandmodelandata/Laptop.sav'

data = pd.read_csv('../visualizeandmodelandata/final_data.csv', encoding='latin-1').dropna()


def find_x_resolution(s):
    return s.split()[-1].split("x")[0]


def find_y_resolution(s):
    return s.split()[-1].split("x")[1]


def convert_disk(type_disk, capacity_disk):
    ssd = []
    hdd = []
    for i in range(0, len(type_disk)):
        if type_disk[i] == 1:
            ssd.append(capacity_disk[i])
            hdd.append(0)
        else:
            hdd.append(capacity_disk[i])
            ssd.append(0)
    return ssd, hdd


class LaptopPrices(object):
    def __init__(self):
        self.data = None

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        self.model = None

        self.load_model()

    def load_model(self):
        self.load_dataset()
        self.model = pickle.load(open(MODEL_SAV_FILE, 'rb'))
        y_predict = self.model.predict(self.X_test)
        print(mean_squared_error(self.y_test, y_predict))

    def load_dataset(self):
        self.data = pd.read_csv(DATA_FILE_PATH, encoding='latin-1').dropna()

        # finding the x_res and y_res from screen resolution
        self.data['X_res'] = self.data['Relu Display'].apply(lambda _: find_x_resolution(_))
        self.data['Y_res'] = self.data['Relu Display'].apply(lambda _: find_y_resolution(_))
        # convert to numeric
        self.data['X_res'] = self.data['X_res'].astype('int')
        self.data['Y_res'] = self.data['Y_res'].astype('int')

        type_disk = [_ for _ in self.data['Type disk']]
        capacity_disk = [_ for _ in self.data['Capacity']]
        ssd, hdd = convert_disk(type_disk, capacity_disk)
        self.data['ssd'] = ssd
        self.data['hdd'] = hdd

        y = self.data['Price']

        self.data = self.data.drop(
            ['Name', 'Producer', 'CPU', 'Type GPU', 'Relu Display', 'Type disk', 'Capacity', ], axis=1
        ).drop(['Price'], axis=1)

        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(self.data, y, test_size=0.1, random_state=42)

    def predict(self, ram, v_ram, display, resolution, ssd, hdd):
        i = np.array([[ram, v_ram, display, find_x_resolution(resolution), find_y_resolution(resolution), ssd, hdd]])
        price = int(self.model.predict(i))
        price = int(price/1000) * 1000
        return price
