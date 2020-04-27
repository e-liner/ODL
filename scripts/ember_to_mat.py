import numpy as np
import sys
import scipy.io as sio
import ember

# Dataset instructions here: https://github.com/endgameinc/ember

def create_vectorized_ember():
    ember.create_vectorized_features("./data/ember2018/")
    ember.create_metadata("./data/ember2018/")

"""
Getting same error - python int too long to convert to C long
So, I'm going to pull in the ember data in main.py directly.
"""
def convert_ember_to_mat():
    X_train, y_train, X_test, y_test = ember.read_vectorized_features("./data/ember2018/")
    metadata_dataframe = ember.read_metadata("./data/ember2018/")

    data = dict()

    data['X_train'] = X_train
    data['Y_train'] = y_train
    data['X_test'] = X_test
    data['Y_test'] = y_test

    print(list(data.keys()))
    print(len(data['X_train'][0]))
    print(data['X_train'].shape)
    print(len(data['Y_train']))
    print(data['Y_train'].shape)

    #sio.savemat("ember.mat", mdict=data)
    return

if __name__ == '__main__':
    #create_vectorized_ember()
    convert_ember_to_mat()

