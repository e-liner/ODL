import numpy as np
import sys
import scipy.io as sio

def convert_data(orig_file, new_file):
    print("Converting " + orig_file + " to " + new_file + "...")

    data = sio.loadmat(orig_file)
    print(data.keys())

    day0_data = data['Day0']
    (data, labels) = day0_data[0][0]
    (num_urls, features) = data.shape

    print(data.shape)
    print(labels.shape)
    print(features)

    (orig_label_size, x) = labels.shape
    new_labels = np.zeros((orig_label_size, 2))
    
    for i in range(0, orig_label_size):
        new_labels[i][labels[i]] = 1

    reformatted_data = dict()
    train_length = int(num_urls * 0.9)
    test_length = int(num_urls * 0.1)

    reformatted_data['X_train'] = data[:train_length]
    reformatted_data['Y_train'] = new_labels[:train_length]
    reformatted_data['X_test'] = data[train_length:]
    reformatted_data['Y_test'] = new_labels[train_length:]

    sio.savemat(new_file, mdict=reformatted_data)
    return

if __name__ == '__main__':
    convert_data(sys.argv[1], sys.argv[2])