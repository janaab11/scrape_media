"""Usage: get_audios.py [-f CSV] [-n NAME] [-d DATA_DIR]

-h --help       show this
-f CSV          csv file that stores audio metadata [default: raw/media_lesson.csv]
-n NAME         name of downloaded file [default: lesson]
-d DATA_DIR     directory to store data [default: data]

"""

import os
import requests
import pandas as pd
from tqdm import tqdm
from docopt import docopt
from supports import check_path, parallelize_dataframe

UNK = -1

def apply_get(df):
    return df.progress_apply(lambda row: get_file(row), axis=1)

def get_file(row):
    val=UNK
    if str(row['url'])!=str(UNK):
        check_path(row['folder'].rsplit('/',1)[0])
        file = '{}.{}'.format(row['folder'],row['url'].rsplit('.',1)[-1])
        if not os.path.exists(file):
            try:
                r = requests.get(row['url'], allow_redirects=True)
                open(file,'wb').write(r.content)
                val=1
            except (KeyboardInterrupt, SystemExit):
                raise
    return val

if __name__ == '__main__':

    # load arguments
    args = docopt(__doc__)
    CSV = args['-f']
    NAME = args['-n']
    DATA_DIR = args['-d']

    data = pd.read_csv(CSV)
    data['folder'] = data.apply(lambda row: '{}/{}/{}/{}'.format(DATA_DIR,row['collection'],row['lesson'],NAME),axis=1)
    data['url'] = data['{}_url'.format(NAME)]
    data.fillna(UNK, inplace=True)
    check_path(DATA_DIR)

    tqdm.pandas()
    temp = parallelize_dataframe(data, apply_get)
    print('{} files downloaded!'.format(len(temp[temp!=UNK])))