import os, sys, getopt 
import yaml
import pickle
import numpy as np
import keras
import keras.callbacks
import csv
import time
import ember
from keras.datasets import mnist
from keras.utils.vis_utils import plot_model
from keras.models import Sequential, Model
from keras.optimizers import SGD, Adam, RMSprop
from model import build_model, MyCallback
from keras.callbacks import CSVLogger
from data import load

ember_full_path = "D:/Users/eliner/eclipse-workspace/ODL/data/ember2018/"

def secs_to_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def build_data_dict(in_name, out_name, in_data, out_data):
    in_dict = dict()
    in_dict[in_name] = in_data
    
    out_dict = dict((k, out_data) for k in out_name)
    return (in_dict, out_dict)

def convert_labels(in_arr, classes):
    in_size = len(in_arr)
    out_arr = np.zeros((in_size, classes))

    for i in range(0, in_size):
        out_arr[i][int(in_arr[i])] = 1

    return out_arr

def build_loss_weight(config):
    if config['hedge'] == False:
        w = [1.]
    elif config['loss_weight'] == 'ave':
        w = [1./ config['n_layers']]* config['n_layers']
    return w
def main(arg, idx=0):
    config = {'learning_rate': 1e-3,
              'optim': 'Adam',
              'batch_size': 1,
              'nb_epoch': 50,
              'n_layers': 3,
              'hidden_num': 100,
              'activation': 'relu',
              'loss_weight': 'ave',
              'adaptive_weight': False,
              'data': 'mnist',
              'hedge': False,
              'log': 'mnist_hedge.log'}

    configfile = ''
    helpstring = 'main.py -c <config YAML file>'
    try:
        opts, args = getopt.getopt(arg, "hc:", ["config"])
    except getopt.GetoptError:
        print(helpstring)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print (helpstring)
            yamlstring = yaml.dump(config,default_flow_style=False,explicit_start=True)
            print("YAML configuration file format:")
            print("")
            print("%YAML 1.2")
            print(yamlstring)
            sys.exit()

        elif opt in ('-c', '--config'):
            configfile = arg

        print("Config file is %s" % configfile)

    if os.path.exists(configfile):
        f = open(configfile)
        user_config = yaml.load(f.read(), Loader=yaml.FullLoader)
        config.update(user_config)
    
    print("Printing configuration:")
    for key,value in config.items():
        print("  ",key,": ",value)

    if config['data'] == 'ember':
        X_train, Y_train, X_test, Y_test = ember.read_vectorized_features(ember_full_path)

        nb_classes = 2
        Y_train = convert_labels(Y_train, nb_classes)
        Y_test = convert_labels(Y_test, nb_classes)
    else:
        (X_train, Y_train, X_test, Y_test, nb_classes) = load(config['data'])

    '''
    X_train = X_train[:1000]
    Y_train = Y_train[:1000]
    X_test = X_test[:1000]
    Y_test = Y_test[:1000]
    '''
    model, in_name, out_name = build_model(config)
    if len(out_name) == 1:
        out_name_loss = ['loss']
    else:
        out_name_loss = [s + '_loss' for s in out_name]

    model.summary()
    #plot(model, to_file = 'model.png')
    
    optim = eval(config['optim'])(lr = config['learning_rate'])
    in_dict, out_dict = build_data_dict(in_name, out_name, X_train, Y_train)
    in_val, out_val = build_data_dict(in_name, out_name, X_test, Y_test)
    loss_dict = dict((k, 'categorical_crossentropy') for k in out_name)

    loss_weights = build_loss_weight(config)
    my_callback = MyCallback(loss_weights, names = out_name_loss, hedge = config['hedge'], log_name = config['log'], acc_output_num = config['n_layers'])

    start_time = time.time()
    model.compile(optimizer = optim, loss = loss_dict, loss_weights = loss_weights, metrics = ['acc'])
    model.fit(in_dict, out_dict, epochs = config['nb_epoch'], batch_size = config['batch_size'], callbacks=[my_callback]) #callbacks=[csv]) #
    end_time = time.time()

    test_time = end_time - start_time
    
    #cumLoss = np.cumsum(my_callback.acc)
    #indexOfLoss = np.arange(len(cumLoss))+1
    #cumAverageLoss = cumLoss/indexOfLoss

    #filename = (config['log'] + '_' + str(idx) + '.acc')
    #np.savetxt(filename, cumAverageLoss, delimiter=',')

    out_num = config['n_layers']
    csv_file = "model_acc.csv"
    print("Saving results to CSV file...")

    print("Total testing time: ", secs_to_time(test_time))

    # Save dictionary to CSV file
    for i in range(0, out_num):
        acc_name = 'out' + str(i) + '_acc'
        loss_name = 'out' + str(i) + '_loss'

    data_len = len(my_callback.data_dict['out0_acc'])
    try:
        with open(csv_file, 'w', newline='') as f:
            dict_keys = list(my_callback.data_dict.keys())
            dict_keys.append('cumulative_acc')
            dict_keys.append('max_acc')
            dict_keys.append('max_acc_idx')
            dict_keys.append('min_loss')
            dict_keys.append('min_loss_idx')
            w = csv.DictWriter(f, dict_keys)
            w.writeheader()


            print(my_callback.data_dict.keys())
            for i in range(0, data_len):
                data_list = dict()
                acc_sum = 0.0
                max_acc = my_callback.data_dict[acc_name][0]
                max_acc_idx = 0
                min_loss = my_callback.data_dict[loss_name][0]
                min_loss_idx = 0
                for j in range(0, out_num):
                    acc_name = 'out' + str(j) + '_acc'
                    loss_name = 'out' + str(j) + '_loss'
                    data_list[acc_name] = my_callback.data_dict[acc_name][i]
                    data_list[loss_name] = my_callback.data_dict[loss_name][i]
                    #if type(my_callback.data_dict[acc_name][i]) == type(0.0): #eliner fixme.
                    acc_sum += my_callback.data_dict[acc_name][i]                    

                    if data_list[acc_name] > max_acc:
                        max_acc = data_list[acc_name]
                        max_acc_idx = j
                    if data_list[loss_name] < min_loss:
                        min_loss = data_list[loss_name]
                        min_loss_idx = j

                data_list['cumulative_acc'] = (acc_sum / out_num)
                data_list['max_acc'] = max_acc
                data_list['max_acc_idx'] = max_acc_idx
                data_list['min_loss'] = min_loss
                data_list['min_loss_idx'] = min_loss_idx

                w.writerow(data_list)

    except IOError:
        print("I/O error")

    return my_callback
if __name__ == '__main__':
    #for i in range(5):
    my_callback = main(sys.argv[1:], 0)
