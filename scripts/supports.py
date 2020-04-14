import os
import numpy as np
import pandas as pd
import multiprocessing

num_cores = multiprocessing.cpu_count() #number of cores on your machine
num_partitions = 10 #number of partitions to split dataframe

def check_path(folder, debug=False):
    '''
    Checks if folder exists. If not, a folder is created
    '''
    if not os.path.exists(folder):
        if debug:
            print('{} does not exist, creating'.format(folder))
        os.makedirs(folder)
    return

def parallelize_dataframe(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = multiprocessing.Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df