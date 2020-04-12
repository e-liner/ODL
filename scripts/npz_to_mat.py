import numpy as np
import sys
import scipy.io as io
import random

def convert_npz_to_mat(npz_file, mat_file):
    print("Converting " + npz_file + " to .mat file...")

    data = np.load(npz_file)
    #io.savemat(mat_file, mdict=data)
    print(list(data.keys()))

    data_save = data['x_train']
    label_save = data['y_train']
    data_len = len(data['x_train'])
    train_length = int(data_len * 0.9)
    test_length = int(data_len * 0.1)
    print(train_length)
    print(test_length)

    new_data = dict()

    #random.shuffle(data_save)
    #random.shuffle(label_save)

    # todo - shuffle this.
    new_data['X_train'] = data_save[:train_length]
    new_data['Y_train'] = label_save[:train_length]
    new_data['X_test'] = data_save[train_length:]
    new_data['Y_test'] = label_save[train_length:]

    print(list(new_data.keys()))
    print(len(new_data['X_train'][0]))
    
    io.savemat(mat_file, mdict=new_data)
    return

if __name__ == '__main__':

    convert_npz_to_mat(sys.argv[1], sys.argv[2])