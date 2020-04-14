import sys
import pandas as pd
from supports import parallelize_dataframe

def apply_extract(df):
	return df.apply(lambda row: extract_links(row), axis=1)

def extract_links(row):
	for link in row['arr_links']:
		suffix = link.rsplit('.',1)[0].rsplit('_',1)[-1]
		if suffix=='review':
			row[f'{suffix}_url']=link
		elif suffix=='dialog':
			row[f'{suffix}_url']=link
		else:
			row['lesson_url']=link
	return row

def apply_clean(df):
	return df.apply(lambda links: clean_links(links))

def clean_links(links):
	return [link[2:-1] for link in links[:-1].split(',')]

	
if __name__ == '__main__':
	CSV_FILE = sys.argv[1]

	data = pd.read_csv(CSV_FILE)
	data.drop_duplicates(inplace=True)
	data.dropna(inplace=True)

	# preprocess links
	data['arr_links'] = parallelize_dataframe(data['links'], apply_clean)
	# process links
	for new_col in ['lesson_url','review_url','dialog_url']:
		data[new_col] = ''
	data = parallelize_dataframe(data, apply_extract)

	data.to_csv(CSV_FILE,index=False)
	print(f'Saved back to {CSV_FILE}')
