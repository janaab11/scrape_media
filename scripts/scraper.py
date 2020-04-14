import csv
import scrapy
from supports import check_path

# # set login details and website preference
# BASE = "https://www.vietnamesepod101.com"
# USERNAME = 'manas.viet2@gmail.com'
# PASSWORD = 'barca12345'

BASE = "https://www.urdupod101.com"
USERNAME = 'kksr.urdu@gmail.com'
PASSWORD = 'saranam910'

LOGIN = "/member/login_new.php"
LESSONS = "/lesson-library"
MEDIA = ['.mp3','.pdf']

check_path('raw')
CSV_FILE = "raw/media.csv"
with open(CSV_FILE, 'w+', newline='') as file:
	csv_writer = csv.writer(file)
	csv_writer.writerow(['collection','lesson','links'])

class MediaSpider(scrapy.Spider):
	name = 'media_spy'
	start_urls = [BASE]

	def clean_name(self,sub,string):
		if sub in string:
			return string.replace(sub,'').split('-',2)[-1]
		else:
			return string

	def parse(self,response):
		return scrapy.FormRequest.from_response(
			response,
			formdata={'amember_login':USERNAME, 'amember_pass':PASSWORD},
			callback=self.after_login
		)

	def after_login(self,response):
		return scrapy.Request(url=response.urljoin(LESSONS), callback=self.parse_library)

	def parse_levels(self,response):
		# collect interesting links
		selectors = response.css('li a')
		# follow the links
		for sel in selectors:
			link = sel.xpath('@href').get()
			request = scrapy.Request(url=response.urljoin(link), callback=self.parse_library)
			request.meta['from'] = [link.split('/')[-1]]
			yield request

	def parse_library(self,response):
		parse_class = 'll-collection-all ll-collection-all--private'
		# collect interesting links
		selectors = [sel for sel in response.css('a') 
							if sel.xpath('@class').get()==parse_class]
		# follow the links
		for sel in selectors:
			link = sel.xpath('@href').get()
			request = scrapy.Request(url=response.urljoin(link), callback=self.parse_collection)
			request.meta['from'] = [link.split('/')[-2]]
			yield request

	def parse_collection(self,response):
		parse_class = 'cl-lesson__lesson'
		# collect interesting links
		selectors = [sel for sel in response.css('a') 
							if sel.xpath('@class').get()==parse_class]
		# follow the links
		for sel in selectors:
			link = sel.xpath('@href').get()
			request = scrapy.Request(url=response.urljoin(link), callback=self.parse_lesson)
			request.meta['from'] = response.meta['from'] + \
					[self.clean_name(response.meta['from'][-1],link.split('/')[-2])]
			yield request

	def parse_lesson(self,response):
		links = response.css('a::attr(href)').getall()
		# filter https links
		links = [link for link in links if any(string in link for string in ['http://','https://'])]		
		# filter media links
		links = [link for link in links if any(string in link for string in MEDIA)]

		data = response.meta['from'] + [links]
		# print(data)
		# scrapy.shell.inspect_response(response,self)

		with open(CSV_FILE, 'a+', newline='') as file:
			csv_writer = csv.writer(file)
			csv_writer.writerow(data)
		return