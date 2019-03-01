import pickle
import pandas as pd
import numpy as np


# path to train and test dataset

test_data_path = 'new_test_data.csv'
train_data_path = 'train_data.csv'

test_DF = pd.read_csv(test_data_path, sep=',', header=None)
train_DF = pd.read_csv(train_data_path, sep=',', header=None)


def saveFileToPickle(fileName, object):

    with open(fileName, 'wb') as f:
        pickle.dump(object, f)

    return


def loadFileFromPickle(fileName):

    with open(fileName, 'rb') as f:
        x=pickle.load(f)

    return x


# creates dictionaries with given pandas dataframe for user-based and item-based CF
def createDict(dataset):

    user_dictionary={}
    item_dictionary={}

    size = np.shape(dataset)[0]
    for row in range(0, size):

        if(dataset.iloc[row, 0] in user_dictionary):
            user_dictionary[dataset.iloc[row, 0]].update({dataset.iloc[row, 1]:dataset.iloc[row, 2]})

        else:
            user_dictionary[dataset.iloc[row, 0]] = {dataset.iloc[row, 1]: dataset.iloc[row, 2]}


        if (dataset.iloc[row, 1] in item_dictionary):
            item_dictionary[dataset.iloc[row, 1]].update({dataset.iloc[row, 0]: dataset.iloc[row, 2]})

        else:
            item_dictionary[dataset.iloc[row, 1]] = {dataset.iloc[row, 0]: dataset.iloc[row, 2]}

    return user_dictionary,item_dictionary


# saves the created dictionaries using pickle
def save_dicts():

    user_based_dict, item_based_dict = createDict(train_DF)

    saveFileToPickle('user.pkl',user_based_dict)
    saveFileToPickle('item.pkl',item_based_dict)

    return


save_dicts()

user_based_dict=loadFileFromPickle('user.pkl')
item_based_dict=loadFileFromPickle('item.pkl')