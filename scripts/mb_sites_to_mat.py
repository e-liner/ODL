import numpy as np
import sys
import scipy.io as sio
import csv

# Data from: https://bigml.com/user/jbosca/gallery/dataset/5a815bffeba31d64150002d9

full_csv_path = "D:/Users/eliner/eclipse-workspace/ODL/scripts/data/Mal_Ben_Sites.csv"
full_mat_path = "D:/Users/eliner/eclipse-workspace/ODL/scripts/data/Mal_Ben_Sites.mat"

csv_keys = ['URL', 'URL_LENGTH', 'NUMBER_SPECIAL_CHARACTERS', 'CHARSET', 'SERVER',
            'CACHE_CONTROL', 'CONTENT_LENGTH', 'WHOIS_COUNTRY', 'WHOIS_STATEPROV',
            'WHOIS_REGDATE', 'UPDATE_DATE', 'WHITIN_DOMAIN', 'TCP_CONVERSATION_EXCHANGE',
            'DIST_REMOTE_TCP_PORT', 'REMOTE_IPS', 'APP_BYTES', 'UDP_PACKETS',
            'TCP_URG_PACKETS', 'SOURCE_APP_PACKETS', 'REMOTE_APP_PACKETS', 'SOURCE_APP_BYTES',
            'REMOTE_APP_BYTES', 'APP_PACKETS', 'DNS_QUERY_TIMES', 'TIPO', 'WHOIS_REGDATE.year',
            'WHOIS_REGDATE.month', 'WHOIS_REGDATE.day-of-month', 'WHOIS_REGDATE.day-of-week',
            'WHOIS_REGDATE.hour', 'WHOIS_REGDATE.minute', 'WHOIS_REGDATE.second', 'WHOIS_REGDATE.millisecond',
            'UPDATE_DATE.year', 'UPDATE_DATE.month', 'UPDATE_DATE.day-of-month', 'UPDATE_DATE.day-of-week',
            'UPDATE_DATE.hour', 'UPDATE_DATE.minute', 'UPDATE_DATE.second', 'UPDATE_DATE.millisecond']

charset_vals = ['none', 'iso-8859', 'iso-8859-1', 'us-ascii', 'utf-8', 'windows-1251', 'windows-1252']

def convert_data():
    print("Converting Mal_Ben_Sites.csv to .mat file")

    data = dict()

    orig_data = format_into_ints(full_csv_path)

    print(len(orig_data))

    data_matrix = np.zeros((len(orig_data), 40))

    print(data_matrix.shape)
    
    ex_idx = 0
    for ex in orig_data:
        for i in range(0, 40):
            data_matrix[ex_idx][i] = ex[i]
        ex_idx = ex_idx + 1

    train_length = int(len(orig_data) * 0.9)
    test_length = int(len(orig_data) * 0.1)
    print(train_length)
    print(test_length)

    data['X_train'] = data_matrix[:train_length,:39]
    data['X_test'] = data_matrix[train_length:,:39]

    ytrain_arr = data_matrix[:train_length, 39]
    ytest_arr = data_matrix[train_length:, 39]
    
    data['Y_train'] = convert_labels(ytrain_arr, 2)
    data['Y_test'] = convert_labels(ytest_arr, 2)

    sio.savemat(full_mat_path, mdict=data)
    return

def convert_labels(in_arr, classes):
    in_size = len(in_arr)
    out_arr = np.zeros((in_size, classes), dtype=np.uint8)

    for i in range(0, in_size):
        out_arr[i][int(in_arr[i])] = 1

    return out_arr

def format_into_ints(filename):
    data = []
    benign_count = 0
    mal_count = 0
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        keys = reader.fieldnames

        for row in reader:
            current_data = np.zeros(40)
            current_data[0] = float(row['URL_LENGTH'])
            current_data[1] = float(row['NUMBER_SPECIAL_CHARACTERS'])
            current_data[2] = float(charset_vals.index((row['CHARSET'].lower())))
            try: current_data[3] = float(row['CONTENT_LENGTH'])
            except ValueError: current_data[3] = 0
            current_data[4] = float(row['TCP_CONVERSATION_EXCHANGE'])
            current_data[5] = float(row['DIST_REMOTE_TCP_PORT'])
            current_data[6] = float(row['REMOTE_IPS'])
            current_data[7] = float(row['APP_BYTES'])
            current_data[8] = float(row['UDP_PACKETS'])
            current_data[9] = float(row['TCP_URG_PACKETS'])
            current_data[10] = float(row['SOURCE_APP_PACKETS'])
            current_data[11] = float(row['REMOTE_APP_PACKETS'])
            current_data[12] = float(row['SOURCE_APP_BYTES'])
            current_data[13] = float(row['REMOTE_APP_BYTES'])
            current_data[14] = float(row['APP_PACKETS'])
            try: current_data[15] = float(row['DNS_QUERY_TIMES'])
            except ValueError: current_data[15] = 0

            try: current_data[16] = float(row['WHOIS_REGDATE.year'])
            except ValueError: current_data[16] = 0
            try: current_data[17] = float(row['WHOIS_REGDATE.month'])
            except ValueError: current_data[17] = 0
            try: current_data[18] = float(row['WHOIS_REGDATE.day-of-month'])
            except ValueError: current_data[18] = 0
            try: current_data[19] = float(row['WHOIS_REGDATE.day-of-week'])
            except ValueError: current_data[19] = 0
            try: current_data[20] = float(row['WHOIS_REGDATE.hour'])
            except ValueError: current_data[20] = 0
            try: current_data[21] = float(row['WHOIS_REGDATE.minute'])
            except ValueError: current_data[21] = 0
            try: current_data[22] = float(row['WHOIS_REGDATE.second'])
            except ValueError: current_data[22] = 0
            try: current_data[23] = float(row['WHOIS_REGDATE.millisecond'])
            except ValueError: current_data[23] = 0
            try: current_data[24] = float(row['UPDATE_DATE.year'])
            except ValueError: current_data[24] = 0
            try: current_data[25] = float(row['UPDATE_DATE.month'])
            except ValueError: current_data[25] = 0
            try: current_data[26] = float(row['UPDATE_DATE.day-of-month'])
            except ValueError: current_data[26] = 0
            try: current_data[27] = float(row['UPDATE_DATE.day-of-week'])
            except ValueError: current_data[27] = 0
            try: current_data[28] = float(row['UPDATE_DATE.hour'])
            except ValueError: current_data[28] = 0
            try: current_data[29] = float(row['UPDATE_DATE.minute'])
            except ValueError: current_data[29] = 0
            try: current_data[30] = float(row['UPDATE_DATE.second'])
            except ValueError: current_data[30] = 0
            try: current_data[31] = float(row['UPDATE_DATE.millisecond'])
            except ValueError: current_data[31] = 0
            
            
            if row['TIPO'] == 'Maligna':
                current_data[39] = 1
                mal_count = mal_count + 1
            elif row['TIPO'] == 'Benigna':
                current_data[39] = 0
                benign_count = benign_count + 1

            #print(current_data)
            data.append(current_data)

    print("Data Analysis:", benign_count, "Benign Entries and ", mal_count, "Malicious Entries")
    return data


if __name__ == '__main__':
    convert_data()