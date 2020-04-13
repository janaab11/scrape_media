"""Usage: get_audios.py [-f CSV] [-n NAME] [-d DATA_DIR]

-h --help       show this
-f CSV          csv file that stores audio metadata [default: raw/media_lesson.csv]
-n NAME         name of downloaded file [default: lesson]
-d DATA_DIR     directory to store data [default: data]

"""

import os
import requests
import pandas as pd
import numpy as np
from tqdm import tqdm
from docopt import docopt
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
    pool.map(func, df_split)
    pool.close()
    pool.join()
    return

def apply_get(df):
    tqdm.pandas()
    df.progress_apply(lambda row: get_file(row), axis=1)
    return

def get_file(row):
    check_path(row['folder'])
    file = '{}/{}.{}'.format(row['folder'],row['url'].rsplit('/',1)[-1].split('_')[0],row['url'].rsplit('.',1)[-1])
    if not os.path.exists(file):
        try:
            r = requests.get(row['url'], allow_redirects=True)
            open(file,'wb').write(r.content)
        except (KeyboardInterrupt, SystemExit):
            raise
    return

if __name__ == '__main__':

    # load arguments
    args = docopt(__doc__)
    CSV = args['-f']
    NAME = args['-n']
    DATA_DIR = args['-d']

    data = pd.read_csv(CSV)
    data['folder'] = data.apply(lambda row: '{}/{}/{}'.format(DATA_DIR,row['collection'],row['lesson']),axis=1)
    data['url'] = data['{}_url'.format(NAME)]
    check_path(DATA_DIR)
    
    parallelize_dataframe(data, apply_get)
    # print(len(temp[temp==1]),' files downloaded!')
