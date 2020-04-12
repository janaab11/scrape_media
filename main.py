import re
import requests
from bs4 import BeautifulSoup

# login details
USERNAME = "manas.viet2@gmail.com"
PASSWORD = "barca12345"

# interesting urls
BASE_URL = "https://www.vietnamesepod101.com"
LOGIN = "/member/login_new.php"
HOME = "/dashboard"
LIBRARY = "/lesson-library"
LESSON = "/lesson/top-25-vietnamese-questions-you-need-to-know-2-where-are-you-from-in-vietnamese"

# Create the payload
payload = {
	'amember_login': USERNAME,
	'amember_pass': PASSWORD
}

# Start the session
with requests.Session() as session:

	# Post the payload to the site to log in
	_ = session.post(BASE_URL+LOGIN, data=payload)

	# Navigate to the main page and scrape the data
	r = session.get(BASE_URL+LIBRARY)
	soup = BeautifulSoup(r.text, 'html.parser')

	links = []
	for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
		link = link.get('href')
		if any(string in link for string in ['.mp3','.pdf']):
			links.append(link)
	print(links)
