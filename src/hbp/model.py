import keras
import numpy as np
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Input, Dropout
from keras.optimizers import SGD, Adam
from keras.callbacks import Callback
import keras.backend as K
import time

def get_data(config):
    config['output_size'] = 2
    if config['data'] == 'syn8':
        config['input_size'] = (50,)
    elif config['data'] == 'higgs':
        config['input_size'] = (28,)
    elif config['data'] == 'susy':
        config['input_size'] = (18,)
    elif config['data'] in ['cd6','cd7', 'cd1', 'cd2']:
        config['input_size'] = (50,)
    elif config['data'] in ['cd3','cd4']:
        config['input_size'] = (25,)
    elif config['data'] in ['url']:
        config['input_size'] = (5000,)
    return config

def build_model(config):
    config = get_data(config)

    base_name = 'out'
    if config['hedge'] == True:
        outs = ['']*config['n_layers']
        out_name = ['']*config['n_layers']
        N = config['n_layers']
        for i in range(len(outs)):
            outs[i] = base_name + str(i)
            out_name[i] = base_name + str(i)
    else:
        outs = base_name
        out_name = [base_name]
        N = config['n_layers'] - 1
    in_name = 'in0'

    inputs = Input(config['input_size'], name = in_name)
    
    for j in range(N):
        if j == 0:
            layer = Dense(config['hidden_num'])(inputs)
            layer = Activation(config['activation'])(layer)

            if config['hedge'] == True:
                outs[j] = Dense(config['output_size'], activation = 'softmax', name = outs[j])(layer)
            continue
        layer = Dense(config['hidden_num'])(layer)
        layer = Activation(config['activation'])(layer)
        
        if config['hedge'] == True:
            outs[j] = Dense(config['output_size'], activation = 'softmax', name = outs[j])(layer)
    if config['hedge'] == False:
        outs = Dense(config['output_size'], activation = 'softmax', name = outs)(layer)
    model = Model(inputs = inputs , outputs = outs)

    return (model, in_name, out_name)

def list_convert(x):
    try:
        l = x.tolist()
    except AttributeError:
        l = x
    return l
# add self.masks, self.weighted_losses
class MyCallback(Callback):
    def __init__(self,w,  beta = 0.99,  names = [], hedge = True, log_name = 'exp', acc_output_num = 20):
        self.weights = w
        self.beta = beta
        self.names = names
        self.l = []
        self.hedge = hedge
        self.accs = []
        self.logs = dict()
        self.log_name = log_name + '.log'
        self.acc = []
        self.data_dict = dict()
        self.acc_output_num = acc_output_num
    def on_train_begin(self,logs = {}):
        self.logs['weights'] = []

        for i in range(0, self.acc_output_num):
            acc_name = 'out' + str(i) + '_acc'
            loss_name = 'out' + str(i) + '_loss'
            self.data_dict[acc_name] = []
            self.data_dict[loss_name] = []
    def save_acc_and_loss(self, logs):
        for i in range(0, self.acc_output_num):
            acc_name = 'out' + str(i) + '_acc'
            loss_name = 'out' + str(i) + '_loss'
            self.data_dict[acc_name].append(logs.get(acc_name))
            self.data_dict[loss_name].append(logs.get(loss_name))
    def on_batch_end(self, batch, logs = {}):
        self.l.append(logs.get('loss'))
        self.save_acc_and_loss(logs)
        if self.hedge:
            self.acc.append(logs.get('weighted_acc'))
        else:
            self.acc.append(logs.get('acc'))
        losses = [logs[name] for name in self.names]
        '''
        for k in logs.keys():
            if k not in self.logs.keys():
                self.logs[k] = [list_convert(logs[k])]
            else:
                self.logs[k].append(list_convert(logs[k]))
        self.logs['weights'].append(list_convert(self.weights))
        '''
        
        if self.hedge:

            M = sum(losses)
            losses = [loss / M for loss in losses]
            min_loss = np.amin(losses)
            max_loss = np.amax(losses)
            range_of_loss = max_loss - min_loss
            losses = [(loss-min_loss)/range_of_loss for loss in losses]

            alpha = [self.beta ** loss for loss in losses]
            
            try:
                alpha = [a * w for a, w in zip(alpha, self.weights)]
            except ValueError:
                pass
           
            alpha = [ max(0.01, a) for a in alpha]
            M = sum(alpha)
            alpha = [a / M for a in alpha]
            
            self.weights = alpha 
    def on_batch_begin(self, epoch, logs={}):
        self.model.holder = (self.weights)
    def on_epoch_end(self, epoch, logs={}):
        self.save_acc_and_loss(logs)
    '''
    def on_train_end(self, logs = {}):
        with open(self.log_name, 'w') as f:
            keys = sorted(self.logs.keys())
            f.write(' '.join(str(k) for k in keys) + '\n')
            L = len(self.logs[keys[0]])
            for j in range(L):
                for k in keys:
                    if k == 'weights':
                        f.write('[' + ','.join(str(ww) for ww in self.logs[k][j]) + ']')
                    else:
                        f.write(str(self.logs[k][j]) + ' ')
                f.write('\n')
    '''
