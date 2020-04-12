#!/usr/bin/python
# display size of a remote file without downloading

# from __future__ import print_function
import sys
import requests

# number of bytes in a megabyte
MBFACTOR = float(1 << 20)
FILE_URL = sys.argv[1]

response = requests.head(FILE_URL, allow_redirects=True)

# print("\n".join([('{:<40}: {}'.format(k, v)) for k, v in response.headers.items()]))

size = response.headers.get('content-length', 0)						# .get gives us a dictionary item if the key exists
print('{:<40}: {:.2f} MB'.format('FILE SIZE', int(size) / MBFACTOR))

# answer = input('\nDownload file ?[y/n]')
# if answer.lower() == 'y':
# 	response = requests.get(FILE_URL)
# 	with open(FILE_URL.split('/')[-1], 'wb') as file:
# 		file.write(response.content)

