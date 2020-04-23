import numpy as np
import sys
import scipy.io as sio

# Unpacking and reformatting dataset found here: http://www.sysnet.ucsd.edu/projects/url/

def convert_data(orig_file, new_file):
    print("Converting " + orig_file + " to " + new_file + "...")

    data = sio.loadmat(orig_file)
    print(data.keys())

    day_keys = data.keys()

    key_name = 'Day'
    reformatted_data = dict()
    #reformatted_data['X_train'] = []
    #reformatted_data['Y_train'] = []
    #reformatted_data['X_test'] = []
    #reformatted_data['Y_test'] = []

    key_count = 0
    
    for key in day_keys:
        print(str(key_count) + ":" + key)
        if key_count >= 6: # Gets error: Python int to large to convert to C long. Weird. Setting aside.
            #print("eliner a")
            break
        #if key_count == 6:
            #print("eliner b")
            #continue
        if(key[0] != 'D' or key == 'Day115'):
            #print("eliner c")
            continue
        key_count = key_count + 1
        print(key)
        cur_day_data = data[key]

        print(cur_day_data[0][0])

        (day_data, day_labels) = cur_day_data[0][0]
        (num_urls, features) = day_data.shape

        (orig_label_size, x) = day_labels.shape
        new_labels = np.zeros((orig_label_size, 2))
    
        for i in range(0, orig_label_size):
            new_labels[i][day_labels[i]] = 1

        train_length = int(num_urls * 0.9)
        test_length = int(num_urls * 0.1)


        # this is wrong. we don't want to append it, we want to extend the nd arrays. bluh.
        if 'X_train' in reformatted_data:
            tmp_xtrain = reformatted_data['X_train']
            current_xtrain = (day_data[:train_length][:,:5000]).toarray()
            new_xtrain_array = np.concatenate((tmp_xtrain, current_xtrain), axis=0 )
            reformatted_data['X_train'] = new_xtrain_array
        else:
            reformatted_data['X_train'] = (day_data[:train_length][:,:5000]).toarray()

        if 'Y_train' in reformatted_data:
            tmp_ytrain = reformatted_data['Y_train']
            current_ytrain = new_labels[:train_length]
            new_ytrain_array = np.concatenate((tmp_ytrain, current_ytrain), axis=0)
            reformatted_data['Y_train'] = new_ytrain_array
        else:
            reformatted_data['Y_train'] = new_labels[:train_length]
        
        if 'X_test' in reformatted_data:
            tmp_xtest = reformatted_data['X_test']
            current_xtest = (day_data[train_length:][:,:5000]).toarray()
            new_xtest_array = np.concatenate((tmp_xtest, current_xtest), axis=0)
            reformatted_data['X_test'] = new_xtest_array
        else:
            reformatted_data['X_test'] = (day_data[train_length:][:,:5000]).toarray()

        if 'Y_test' in reformatted_data:
            tmp_ytest = reformatted_data['Y_test']
            current_ytest = new_labels[train_length:]
            new_ytest_array = np.concatenate((tmp_ytest, current_ytest), axis=0)
            reformatted_data['Y_test'] = new_ytest_array
        else:
            reformatted_data['Y_test'] = new_labels[train_length:]

    print(reformatted_data['X_train'].shape)
    print(reformatted_data['X_test'].shape)

    sio.savemat(new_file, mdict=reformatted_data)
    return

if __name__ == '__main__':
    convert_data(sys.argv[1], sys.argv[2])