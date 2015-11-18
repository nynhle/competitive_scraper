import unittest
import os
from src import Crawler
from src import Scraper

# Before running the tests, start a SimpleHTTPServer from the 
# competitive scraper directory by running:
# 'python -m SimpleHTTPServer 8000
# TODO: Make this server start when the tests are run.

class TestCrawler(unittest.TestCase):

	# 10 links on testpage + startpage = 11
	def test_count_urls_first_page(self): 
		crawler = Crawler.Crawler('http://localhost:8000/testpages/first_version.html')
		crawler.Crawl()
		self.assertEqual(11, len(crawler.export_full_url_list()))

	# 9 links on testpage + startpage = 10
	def test_count_urls_second_page(self):
		crawler = Crawler.Crawler('http://localhost:8000/testpages/second_version.html')
		crawler.Crawl()
		self.assertEqual(10, len(crawler.export_full_url_list()))

	#TODO: Add tests verifying all links gathered are correct.

if __name__ == '__main__':
	unittest.main()
