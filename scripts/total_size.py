import csv
import sys
import requests
import pandas as pd
from tqdm import tqdm
from supports import parallelize_dataframe

def apply_size(df):
	return df.progress_apply(lambda url: size_of(url))

def size_of(url):
	try:
		url = int(url)
		if url==-1:
			size = 0
	except:
		response = requests.head(url, allow_redirects=True)
		size = response.headers.get('content-length', 0)				# .get gives us a dictionary item if the key exists
		size = float(int(size)/MBFACTOR)

		# global SUM
		# SUM += size
		# print('{:.2f}'.format(SUM))
	return size


if __name__ == '__main__':
	# number of bytes in a megabyte
	MBFACTOR = float(1 << 20)
	CSV_FILE = sys.argv[1]

	data = pd.read_csv(CSV_FILE)
	data.drop_duplicates(inplace=True)
	data.fillna(-1, inplace=True)
	for col in data.columns:
		if '_url' in col:
			tqdm.pandas()
			data[col.split('_')[0]+'_size'] = parallelize_dataframe(data[col],apply_size)

	data.to_csv(CSV_FILE,index=False)
	print(f'Saved back to {CSV_FILE}')