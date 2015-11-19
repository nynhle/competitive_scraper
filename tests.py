import unittest
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

	def test_verify_urls_first_version(self):
		crawler = Crawler.Crawler('http://localhost:8000/testpages/first_version.html')
		crawler.Crawl()
		scraped_urls = crawler.export_full_url_list()
		isValid = True
		valid_urls = ['http://localhost:8000/testpages/first_version.html', 'http://localhost:8000/testpages/hyperlink1.html', \
				'http://localhost:8000/testpages/hyperlink2.html', 'http://localhost:8000/testpages/hyperlink3.html', \
				'http://localhost:8000/testpages/hyperlink4.html', 'http://localhost:8000/testpages/hyperlink5.html', \
				'http://localhost:8000/testpages/hyperlink6.html', 'http://localhost:8000/testpages/hyperlink7.html', \
				'http://localhost:8000/somefolder/hyperlink8.html', 'http://localhost:8000/testpages/hyperlink9.html' \
				'http://localhost:8000/testpages/hyperlink10.html']
 
		for link in scraped_urls:
			if link not in valid_urls:
				isValid = False
				break

		self.assertTrue(isValid) 
	
	def test_replace_last_filename(self):
		link = 'http://localhost:8000/testpages/first_version.html'
		crawler = Crawler.Crawler(link)
		updated_link = crawler.replace_last_filename(link, 'second_version.html')
		self.assertEqual('http://localhost:8000/testpages/second_version.html', updated_link)

if __name__ == '__main__':
	unittest.main()
