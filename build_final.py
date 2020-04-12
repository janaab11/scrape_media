import sys
import pandas as pd

if __name__ == '__main__':
	CSV_FILE = sys.argv[1]
	NAME = sys.argv[2]

	data = pd.read_csv(CSV_FILE)
	url = f'{NAME}_url'
	columns = ['collection','lesson',url]
	filename = CSV_FILE.split('.')[0]
	data[columns].to_csv(f'{filename}_{NAME}.csv', index=False)
