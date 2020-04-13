import sys
import requests
import numpy as np
import pandas as pd
import multiprocessing

num_cores = multiprocessing.cpu_count() #number of cores on your machine
num_partitions = 10 #number of partitions to split dataframe

def extract_links(row):
	try:
		url = int(url)
		if url==-1:
			size = 0
	except:
		response = requests.head(url, allow_redirects=True)
		size = response.headers.get('content-length', 0)				# .get gives us a dictionary item if the key exists
		size = float(int(size)/MBFACTOR)
	return size

def parallelize_dataframe(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = multiprocessing.Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def extract_links(row):
	for link in row['links']:
		ext = link.rsplit('.',1)[-1]
		if ext=='pdf':
			row['notes_url']=link
		else:
			suffix = link.rsplit('.',1)[0].rsplit('_',1)[-1]
			if suffix=='review':
				row[f'{suffix}_url']=link
			elif suffix=='dialog':
				row[f'{suffix}_url']=link
			else:
				row['lesson_url']=link
	return row

def apply_extract(df):
	return df.apply(lambda row: extract_links(row), axis=1)

def clean_links(links):
	return [link[2:-1] for link in links[:-1].split(',')]

def apply_clean(df):
	return df.apply(lambda links: clean_links(links))

if __name__ == '__main__':
	CSV_FILE = sys.argv[1]

	data = pd.read_csv(CSV_FILE)
	data.drop_duplicates(inplace=True)
	data.dropna(inplace=True)

	# preprocess links
	data['links'] = parallelize_dataframe(data['links'], apply_clean)
	# process links
	for new_col in ['lesson_url','review_url','dialog_url','notes_url']:
		data[new_col] = ''
	data = parallelize_dataframe(data, apply_extract)

	data.to_csv(CSV_FILE,index=False)
	print(f'Saved back to {CSV_FILE}')
