import numpy as np
import sys
import scipy.io as sio
import csv

# Data pulled from here: https://www.unb.ca/cic/datasets/nsl.html

full_train_path = "D:/Users/eliner/eclipse-workspace/ODL/scripts/data/NSL-KDD/KDDTrain+.txt"
full_test_path = "D:/Users/eliner/eclipse-workspace/ODL/scripts/data/NSL-KDD/KDDTest+.txt"

mat_path = "D:/Users/eliner/eclipse-workspace/ODL/scripts/data/NSL-KDD/KDD.mat"

def convert_data():
    print("Converting kdd to mat")
    data = dict()

    train_data = format_into_floats(full_train_path)
    test_data = format_into_floats(full_test_path)

    xtrain_matrix = np.zeros((len(train_data), 43))
    xtest_matrix = np.zeros((len(test_data), 43))

    print(xtrain_matrix.shape)
    print(xtest_matrix.shape)

    ex_idx = 0
    for ex in train_data:
        for i in range(0, 43):
            xtrain_matrix[ex_idx][i] = ex[i]
        ex_idx = ex_idx + 1

    ex_idx = 0
    for ex in test_data:
        for i in range(0, 43):
            xtest_matrix[ex_idx][i] = ex[i]
        ex_idx = ex_idx + 1

    data['X_train'] = xtrain_matrix[:,:41]
    data['X_test'] = xtest_matrix[:,:41]

    ytrain_arr = xtrain_matrix[:,41]
    ytest_arr = xtest_matrix[:,41]

    data['Y_train'] = convert_labels(ytrain_arr, 2)
    data['Y_test'] = convert_labels(ytest_arr, 2)

    sio.savemat(mat_path, mdict=data)
    return

def convert_labels(in_arr, classes):
    in_size = len(in_arr)
    out_arr = np.zeros((in_size, classes), dtype=np.uint8)

    for i in range(0, in_size):
        out_arr[i][int(in_arr[i])] = 1

    return out_arr

def format_into_floats(file_path):
    data = []

    # Formatting data into floats, examples in a list.
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            current_data = np.zeros((43,1))
            
            for i in range(1, 44):
                val = row[str(i)]
                if i == 2:
                    if(val == 'tcp'):
                        current_data[i] = 0
                    elif(val == 'udp'):
                        current_data[i] = 1
                    elif(val == 'icmp'):
                        current_data[i] = 2
                    else:
                        print("eliner, found unknown val", i, val)
                        exit()
                elif i == 3:
                    if(val == 'ftp_data'):
                        current_data[i] = 0
                    elif(val == 'other'):
                        current_data[i] = 1
                    elif(val == 'private'):
                        current_data[i] = 2
                    elif(val == 'http'):
                        current_data[i] = 3
                    elif(val == 'remote_job'):
                        current_data[i] = 4
                    elif(val == 'tcp'):
                        current_data[i] = 5
                    elif(val == 'name'):
                        current_data[i] = 6
                    elif(val == 'netbios_ns'):
                        current_data[i] = 7
                    elif(val == 'eco_i'):
                        current_data[i] = 8
                    elif(val == 'mtp'):
                        current_data[i] = 9
                    elif(val == 'telnet'):
                        current_data[i] = 10
                    elif(val == 'finger'):
                        current_data[i] = 11
                    elif(val == 'domain_u'):
                        current_data[i] = 12
                    elif(val == 'supdup'):
                        current_data[i] = 13
                    elif(val == 'uucp_path'):
                        current_data[i] = 14
                    elif(val == 'Z39_50'):
                        current_data[i] = 15
                    elif(val == 'smtp'):
                        current_data[i] = 16
                    elif(val == 'csnet_ns'):
                        current_data[i] = 17
                    elif(val == 'uucp'):
                        current_data[i] = 18
                    elif(val == 'netbios_dgm'):
                        current_data[i] = 19
                    elif(val == 'urp_i'):
                        current_data[i] = 20
                    elif(val == 'auth'):
                        current_data[i] = 21
                    elif(val == 'domain'):
                        current_data[i] = 22
                    elif(val == 'ftp'):
                        current_data[i] = 23
                    elif(val == 'bgp'):
                        current_data[i] = 24
                    elif(val == 'ldap'):
                        current_data[i] = 25
                    elif(val == 'ecr_i'):
                        current_data[i] = 26
                    elif(val == 'gopher'):
                        current_data[i] = 27
                    elif(val == 'vmnet'):
                        current_data[i] = 28
                    elif(val == 'systat'):
                        current_data[i] = 29
                    elif(val == 'http_443'):
                        current_data[i] = 30
                    elif(val == 'efs'):
                        current_data[i] = 31
                    elif(val == 'whois'):
                        current_data[i] = 32
                    elif(val == 'imap4'):
                        current_data[i] = 33
                    elif(val == 'iso_tsap'):
                        current_data[i] = 34
                    elif(val == 'echo'):
                        current_data[i] = 35
                    elif(val == 'klogin'):
                        current_data[i] = 36
                    elif(val == 'link'):
                        current_data[i] = 37
                    elif(val == 'sunrpc'):
                        current_data[i] = 38
                    elif(val == 'login'):
                        current_data[i] = 39
                    elif(val == 'kshell'):
                        current_data[i] = 40
                    elif(val == 'sql_net'):
                        current_data[i] = 41
                    elif(val == 'time'):
                        current_data[i] = 42
                    elif(val == 'hostnames'):
                        current_data[i] = 43
                    elif(val == 'exec'):
                        current_data[i] = 44
                    elif(val == 'ntp_u'):
                        current_data[i] = 45
                    elif(val == 'discard'):
                        current_data[i] = 46
                    elif(val == 'nntp'):
                        current_data[i] = 47
                    elif(val == 'courier'):
                        current_data[i] = 48
                    elif(val == 'ctf'):
                        current_data[1] = 49
                    elif(val == 'ssh'):
                        current_data[i] = 50
                    elif(val == 'daytime'):
                        current_data[i] = 51
                    elif(val == 'shell'):
                        current_data[i] = 52
                    elif(val == 'netstat'):
                        current_data[i] = 53
                    elif(val == 'pop_3'):
                        current_data[i] = 54
                    elif(val == 'nnsp'):
                        current_data[i] = 55
                    elif(val == 'IRC'):
                        current_data[i] = 56
                    elif(val == 'pop_2'):
                        current_data[i] = 57
                    elif(val == 'printer'):
                        current_data[i] = 58
                    elif(val == 'tim_i'):
                        current_data[i] = 59
                    elif(val == 'pm_dump'):
                        current_data[i] = 60
                    elif(val == 'red_i'):
                        current_data[i] = 61
                    elif(val == 'netbios_ssn'):
                        current_data[i] = 62
                    elif(val == 'rje'):
                        current_data[i] = 63
                    elif(val == 'X11'):
                        current_data[i] = 64
                    elif val == 'urh_i':
                        current_data[i] = 65
                    elif val == 'http_8001':
                        current_data[i] = 66
                    elif val == 'aol':
                        current_data[i] = 67
                    elif val == 'http_2784':
                        current_data[i] = 68
                    elif val == 'tftp_u':
                        current_data[i] = 69
                    elif val == 'harvest':
                        current_data[i] = 70
                    else:
                        print("eliner, found unknown val", i, val)
                        exit()
                elif i == 4:
                    if val == 'SF':
                        current_data[i] = 0
                    elif val == 'S0':
                        current_data[i] = 1
                    elif val == 'REJ':
                        current_data[i] = 2
                    elif val == 'RSTR':
                        current_data[i] = 3
                    elif val == 'SH':
                        current_data[i] = 4
                    elif val == 'RSTO':
                        current_data[i] = 5
                    elif val == 'S1':
                        current_data[i] = 6
                    elif val == 'RSTOS0':
                        current_data[i] = 7
                    elif val == 'S3':
                        current_data[i] = 8
                    elif val == 'S2':
                        current_data[i] = 9
                    elif val == 'OTH':
                        current_data[i] = 10
                    else:
                        print("eliner, found unknown val", i, val)
                        exit()
                elif i == 42: #note - this is the classification label
                    if val == 'normal':
                        current_data[i] = 0
                    elif val == 'neptune':
                        current_data[i] = 1
                    elif val == 'warezclient':
                        current_data[i] = 1
                    elif val == 'ipsweep':
                        current_data[i] = 1
                    elif val == 'portsweep':
                        current_data[i] = 1
                    elif val == 'teardrop':
                        current_data[i] = 1
                    elif val == 'nmap':
                        current_data[i] = 1
                    elif val == 'satan':
                        current_data[i] = 1
                    elif val == 'smurf':
                        current_data[i] = 1
                    elif val == 'pod':
                        current_data[i] = 1
                    elif val == 'back':
                        current_data[i] = 1
                    elif val == 'guess_passwd':
                        current_data[i] = 1
                    elif val == 'ftp_write':
                        current_data[i] = 1
                    elif val == 'multihop':
                        current_data[i] = 1
                    elif val == 'rootkit':
                        current_data[i] = 1
                    elif val == 'buffer_overflow':
                        current_data[i] = 1
                    elif val == 'imap':
                        current_data[i] = 1
                    elif val == 'warezmaster':
                        current_data[i] = 1
                    elif val == 'phf':
                        current_data[i] = 1
                    elif val == 'land':
                        current_data[i] = 1
                    elif val == 'loadmodule':
                        current_data[i] = 1
                    elif val == 'spy':
                        current_data[i] = 1
                    elif val == 'perl':
                        current_data[i] = 1
                    elif val == 'saint':
                        current_data[i] = 1
                    elif val == 'mscan':
                        current_data[i] = 1
                    elif val == 'apache2':
                        current_data[i] = 1
                    elif val == 'snmpgetattack':
                        current_data[i] = 1
                    elif val == 'processtable':
                        current_data[i] = 1
                    elif val == 'httptunnel':
                        current_data[i] = 1
                    elif val == 'ps':
                        current_data[i] = 1
                    elif val == 'snmpguess':
                        current_data[i] = 1
                    elif val == 'mailbomb':
                        current_data[i] = 1
                    elif val == 'named':
                        current_data[i] = 1
                    elif val == 'sendmail':
                        current_data[i] = 1
                    elif val == 'xterm':
                        current_data[i] = 1
                    elif val == 'worm':
                        current_data[i] = 1
                    elif val == 'xlock':
                        current_data[i] = 1
                    elif val == 'xsnoop':
                        current_data[i] = 1
                    elif val == 'sqlattack':
                        current_data[i] = 1
                    elif val == 'udpstorm':
                        current_data[i] = 1
                    else:
                        print("eliner, found unknown val", i, val)
                        exit()
                else:
                    current_data[i-1] = val

            #print(current_data)
            data.append(current_data)

    return data
            

if __name__ == '__main__':
    convert_data()