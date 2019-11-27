#!/usr/bin/env python3
#reademgdata.py: reads emg basic results textfiles and generates a csv file
#assumes data in order:
# ./data
#     tpX
#         textfile.ASC
# Copyright 2019 Peter Kvillegård. Subject to the Unlicense.

import pandas as pd
import numpy as np
import os
import glob

### Import data from emg text files

# ids, list of test person id numbers
tppaths = glob.glob('./data/tp*')
ids = [x.replace('./data/tp', '') for x in tppaths]
ids.sort(key=int)

# return value from .ASC file, 
# pass file as f, pass 'dpi','dpp', or 'inf' as m
def get_value(f,m):
    if m == 'dpi':
        asc_col = 1
    elif m == 'dpp':
        asc_col = 2
    elif m == 'inf':
        asc_col = 3
    else:
        print('error calling tp'+j+', column:'+c)
    
    #open file and read
    txt = open(f, 'r')
    contents=txt.readlines()
    txt.close()
    #extract value
    tsvs = contents[9].replace('\n','').split("\t")
    v = int(tsvs[asc_col])
    return v

# make list/row that will be appended to df, 
# pass id as j
def make_row(j):
    row=[j] # id
    base='./data/tp'+j+'/tp'+j+'_'
    row.append(get_value(base+'mvic_dpi_1.ASC','dpi')) # mvic_dpi_1
    row.append(get_value(base+'mvic_dpi_2.ASC','dpi')) # mvic_dpi_2
    row.append(get_value(base+'mvic_dpi_3.ASC','dpi')) # mvic_dpi_3

    row.append(get_value(base+'mvic_dpp_1.ASC','dpp')) # mvic_dpp_1
    row.append(get_value(base+'mvic_dpp_2.ASC','dpp')) # mvic_dpp_2
    row.append(get_value(base+'mvic_dpp_3.ASC','dpp')) # mvic_dpp_3

    row.append(get_value(base+'mvic_inf_1.ASC','inf')) # mvic_inf_1
    row.append(get_value(base+'mvic_inf_2.ASC','inf')) # mvic_inf_2
    row.append(get_value(base+'mvic_inf_3.ASC','inf')) # mvic_inf_3

    row.append(get_value(base+'ejadd_1.ASC','dpi')) # ejadd_1_dpi
    row.append(get_value(base+'ejadd_1.ASC','dpp')) # ejadd_1_dpp
    row.append(get_value(base+'ejadd_1.ASC','inf')) # ejadd_1_inf

    row.append(get_value(base+'ejadd_2.ASC','dpi')) # ejadd_2_dpi
    row.append(get_value(base+'ejadd_2.ASC','dpp')) # ejadd_2_dpp
    row.append(get_value(base+'ejadd_2.ASC','inf')) # ejadd_2_inf

    row.append(get_value(base+'ejadd_3.ASC','dpi')) # ejadd_3_dpi
    row.append(get_value(base+'ejadd_3.ASC','dpp')) # ejadd_3_dpp
    row.append(get_value(base+'ejadd_3.ASC','inf')) # ejadd_3_inf

    row.append(get_value(base+'add_1.ASC','dpi')) # add_1_dpi
    row.append(get_value(base+'add_1.ASC','dpp')) # add_1_dpp
    row.append(get_value(base+'add_1.ASC','inf')) # add_1_inf

    row.append(get_value(base+'add_2.ASC','dpi')) # add_2_dpi
    row.append(get_value(base+'add_2.ASC','dpp')) # add_2_dpp
    row.append(get_value(base+'add_2.ASC','inf')) # add_2_inf

    row.append(get_value(base+'add_3.ASC','dpi')) # add_3_dpi
    row.append(get_value(base+'add_3.ASC','dpp')) # add_3_dpp
    row.append(get_value(base+'add_3.ASC','inf')) # add_3_inf

    return row

column_names = ['id',
                'mvic_dpi_1', 'mvic_dpi_2', 'mvic_dpi_3',
                'mvic_dpp_1', 'mvic_dpp_2', 'mvic_dpp_3',
                'mvic_inf_1', 'mvic_inf_2', 'mvic_inf_3',
                'ejadd_1_dpi', 'ejadd_1_dpp', 'ejadd_1_inf',
                'ejadd_2_dpi', 'ejadd_2_dpp', 'ejadd_2_inf',
                'ejadd_3_dpi', 'ejadd_3_dpp', 'ejadd_3_inf',
                'add_1_dpi', 'add_1_dpp', 'add_1_inf',
                'add_2_dpi', 'add_2_dpp', 'add_2_inf',
               'add_3_dpi', 'add_3_dpp', 'add_3_inf']

df = pd.DataFrame(columns=column_names, index=ids)

for i in ids:
    df.loc[i] = make_row(i)

df= df.astype('int')

### Calculate and add new columns

# max mvic 
df['max_mvic_dpi'] = df[['mvic_dpi_1','mvic_dpi_2','mvic_dpi_3']].apply(max, axis=1)
df['max_mvic_dpp'] = df[['mvic_dpp_1','mvic_dpp_2','mvic_dpp_3']].apply(max, axis=1)
df['max_mvic_inf'] = df[['mvic_inf_1','mvic_inf_2','mvic_inf_3']].apply(max, axis=1)

# %mvic ejadd
df['percent_mvic_ejadd_dpi'] = df[['ejadd_1_dpi','ejadd_2_dpi','ejadd_3_dpi']].apply(np.mean, axis=1) / df['max_mvic_dpi']
df['percent_mvic_ejadd_dpp'] = df[['ejadd_1_dpp','ejadd_2_dpp','ejadd_3_dpp']].apply(np.mean, axis=1) / df['max_mvic_dpp']
df['percent_mvic_ejadd_inf'] = df[['ejadd_1_inf','ejadd_2_inf','ejadd_3_inf']].apply(np.mean, axis=1) /df['max_mvic_inf']

# %mvic add
df['percent_mvic_add_dpi'] = df[['add_1_dpi','add_2_dpi','add_3_dpi']].apply(np.mean, axis=1) / df['max_mvic_dpi']
df['percent_mvic_add_dpp'] = df[['add_1_dpp','add_2_dpp','add_3_dpp']].apply(np.mean, axis=1) / df['max_mvic_dpp']
df['percent_mvic_add_inf'] = df[['add_1_inf','add_2_inf','add_3_inf']].apply(np.mean, axis=1) / df['max_mvic_inf']

print(df)
df.to_csv(r'./emgdata.csv', index=False) 
