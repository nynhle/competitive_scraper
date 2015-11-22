import os
import unittest
from src import Crawler
from src import Scraper

# Before running the tests, start a SimpleHTTPServer from the 
# competitive scraper directory by running:
# 'python -m SimpleHTTPServer 8000
# TODO: Make this server start when the tests are run.

class TestCrawler(unittest.TestCase):

	# 10 links on testpage + startpage = 11
	def test_Crawl_count_urls_first_page(self): 
		crawler = Crawler.Crawler('http://localhost:8000', '/testpages/first_version.html')
		crawler.Crawl()
		self.assertEqual(11, len(crawler.export_full_url_list()))

	# 9 links on testpage + startpage = 10
	def test_Crawl_count_urls_second_page(self):
		crawler = Crawler.Crawler('http://localhost:8000', '/testpages/second_version.html')
		crawler.Crawl()
		self.assertEqual(10, len(crawler.export_full_url_list()))

	def test_Crawl_verify_urls_first_version(self):
		crawler = Crawler.Crawler('http://localhost:8000', '/testpages/first_version.html')
		crawler.Crawl()
		scraped_urls = crawler.export_full_url_list()
		isValid = True
		valid_urls = ['http://localhost:8000/testpages/first_version.html', 'http://localhost:8000/testpages/hyperlink1.html', \
				'http://localhost:8000/testpages/hyperlink2.html', 'http://localhost:8000/testpages/hyperlink3.html', \
				'http://localhost:8000/testpages/hyperlink4.html', 'http://localhost:8000/testpages/hyperlink5.html', \
				'http://localhost:8000/testpages/hyperlink6.html', 'http://localhost:8000/testpages/hyperlink7.html', \
				'http://localhost:8000/somefolder/hyperlink8.html', 'http://localhost:8000/testpages/hyperlink9.html', \
				'http://localhost:8000/testpages/hyperlink10.html']
 
		for link in scraped_urls:
			if link not in valid_urls:
				isValid = False
				break

		self.assertTrue(isValid) 

	def test_Crawl_veryfy_urls_second_version(self):
		crawler = Crawler.Crawler('http://localhost:8000', 'testpages/second_version.html')
		crawler.Crawl()
		scraped_urls = crawler.export_full_url_list()
		isValid = True
		valid_urls = ['http://localhost:8000/testpages/hyperlink1.html', 'http://localhost:8000/testpages/hyperlink2.html', \
				'http://localhost:8000/testpages/hyperlink3.html', 'http://localhost:8000/testpages/hyperlink4.html', \
				'http://localhost:8000/somefolder/hyperlink5.html', 'http://localhost:8000/testpages/hyperlink6.html', \
				'http://localhost:8000/testpages/hyperlink7.html', 'http://localhost:8000/testpages/hyperlink8.html', \
				'http://localhost:8000/testpages/hyperlink11.html']

		for link in scraped_urls:
			if link not in valid_urls:
				isValid = False
				break

		self.assertTrue(isValid)

	def test_replace_last_filename(self):
		crawler = Crawler.Crawler('http://localhost:8000/testpages/first_version.html', '')
		result = crawler.replace_last_filename('http://localhost:8000/testpages/hyperlink1.html', 'hyperlink2.html')
		self.assertEqual(result, 'http://localhost:8000/testpages/hyperlink2.html')
	


class TestScraper(unittest.TestCase):
	
	def test_replace_old_index(self):
		index_file = open('data/index.txt', 'w')
		index_file.write('1#http://localhost:8000/testpages/first_version.html')
		index_file.close()
		url_list = ['http://localhost:8000/testpages/second_version.html']
		scraper = Scraper.Scraper(url_list)
		scraper.replace_old_index()
		old_url = open('data/old.txt', 'r').read()

		self.assertEqual(old_url, '1#http://localhost:8000/testpages/first_version.html')
	
	def test_delete_old_webpages(self):
		url_list = ['http://localhost:8000/testpages/second_version.html']
		scraper = Scraper.Scraper(url_list)
		foo_file = open('data/webpages/old/foo.txt', 'w')
		foo_file.close()
		scraper.delete_old_webpages()
		list_of_files = os.listdir('data/webpages/old')
		hidden_files = 0
		for link in list_of_files:
			if link.startswith('.'):
				hidden_files += 1
		self.assertEqual(len(list_of_files), hidden_files)








if __name__ == '__main__':
	unittest.main()
