import os
import unittest
from src import Crawler
from src import Scraper
from src import Comparer
import requests

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

	def test_save_urls(self):
		index_file = open('data/index.txt', 'w')
		url_list = ['http://localhost:8000/testpages/second_version.html', 'http://localhost:8000/testpages/first_version.html']
		scraper = Scraper.Scraper(url_list)
		scraper.save_urls()
		self.assertEqual(open('data/index.txt', 'r').read(), '\n0#http://localhost:8000/testpages/second_version.html\n1#http://localhost:8000/testpages/first_version.html')
	
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


	def test_move_files(self):
		# Removing all the files in index directory
		new_webpages = os.listdir('data/webpages/index')
		for webpage in new_webpages:
			if webpage.startswith('.'):
				pass
			else:
				os.remove('data/webpages/index/' + webpage)
		
		# Removing all the files in the old directory
		old_webpages = os.listdir('data/webpages/old')
		for webpage in old_webpages:
			if webpage.startswith('.'):
				pass
			else:
				os.remove('data/webpages/old/' + webpage)

		# Now its possible to control which files are in index dir
		first_file = open('data/webpages/index/first_file.txt', 'w')
		first_file.close()
		second_file = open('data/webpages/index/second_file.txt', 'w')
		second_file.close()
	
		url_list = ['data/webpages/old/first_file.txt', 'data/webpages/old/second_file.txt']
		scraper = Scraper.Scraper(url_list)
		scraper.move_files()

		# Now all the files added to index dir should be in old dir
		allMoved = True
		moved_webpages = os.listdir('data/webpages/old')
		moved_pages = 0
		for webpage in moved_webpages:
			if webpage.startswith('.'):
				pass
			else:
				full_url = 'data/webpages/old/' + webpage
				moved_pages += 1
				if full_url not in url_list:
					allMoved = False

		self.assertTrue(allMoved and len(url_list) == moved_pages)

class TestComparer(unittest.TestCase):
	def test_return_index(self):
		index_file = open('data/index.txt', 'w')
		file_content = '0#http://localhost:8000/testpages/first_version.html'
		index_file.write(file_content)
		index_file.close()
		comparer = Comparer.Comparer()
		result = comparer.return_index()
		self.assertEqual(result, [file_content]) 

	def test_return_old_index(self):
		old_index_file = open('data/old.txt', 'w')
		file_content = '0#http://localhost:8000/testpages/second_version.html'
		old_index_file.write(file_content)
		old_index_file.close()
		comparer = Comparer.Comparer()
		result = comparer.return_old_index()
		self.assertEqual(result, [file_content])
	
	def test_get_line_key(self):
		comparer = Comparer.Comparer()
		result = comparer.get_line_key('0#http://localhost:8000/testpages/second_version.html')
		self.assertEqual(result, '0')

	def test_get_line_key_no_newline(self):
		comparer = Comparer.Comparer()
		result = comparer.get_line_key('\n0#http://localhost:8000/testpages/second_version.html')
		self.assertEqual(result, '0')

	def test_get_line_url(self):
		comparer = Comparer.Comparer()
		result = comparer.get_line_url('0#http://localhost:8000/testpages/second_version.html')
		self.assertEqual(result, 'http://localhost:8000/testpages/second_version.html')

	def test_parse_index_url_file(self):
		index_file = open('data/index.txt', 'w')
		index_file.write('0#http://localhost:8000/testpages/first_version.html')
		index_file.close()
		index_file = open('data/index.txt', 'a')
		index_file.write('\n1#http://localhost:8000/testpages/second_version.html')
		index_file.write('blah')
		comparer = Comparer.Comparer()
		result = comparer.parse_index_url_file()
		valid_list = ['0', 'http://localhost:8000/testpages/first_version.html', \
				'1', 'http://localhost:8000/testpages/second_version.html']

		isValid = True
		for urlfile in result:
			if urlfile.key in valid_list and urlfile.url in valid_list:
				valid_list.remove(urlfile.key)
				valid_list.remove(urlfile.url)
			else:
				isValid = False
		self.assertTrue(isValid)

	def test_parse_old_index_url_file(self):
		index_file = open('data/old.txt', 'w')
		index_file.write('0#http://localhost:8000/testpages/first_version.html')
		index_file.close()
		index_file = open('data/old.txt', 'a')
		index_file.write('\n1#http://localhost:8000/testpages/second_version.html')
		comparer = Comparer.Comparer()
		result = comparer.parse_old_index_url_file()
		valid_list = ['0', 'http://localhost:8000/testpages/first_version.html', \
				'1', 'http://localhost:8000/testpages/second_version.html']

		isValid = True
		for urlfile in result:
			if urlfile.key in valid_list and urlfile.url in valid_list:
				valid_list.remove(urlfile.key)
				valid_list.remove(urlfile.url)
			else:
				isValid = False
		self.assertTrue(isValid)


	def test_get_matched_pairs_count(self):
		index_file = open('data/index.txt', 'w')
		old_file = open('data/old.txt', 'w')
		index_file.write('0#http://localhost:8000/testpages/first_version.html')
		index_file.close()
		old_file.write('0#http://localhost:8000/testpages/first_version.html')
		old_file.close()
		comparer = Comparer.Comparer()
		result = comparer.get_matched_pairs()
		self.assertEqual(len(result), 1)



		
	def test_compare(self):
		first_page = requests.get('http://localhost:8000/testpages/first_version.html').content
		second_page = requests.get('http://localhost:8000/testpages/second_version.html').content
		index_file = open('data/index.txt', 'w')
		index_file.write('0#http://localhost:8000/testpages/first_version.html')
		index_file.close()
		old_index_file = open('data/old.txt', 'w')
		old_index_file.write('0#http://localhost:8000/testpages/first_version.html')
		old_index_file.close()
		for website in os.listdir('data/webpages/index'):
			if website.startswith('.'):
				pass
			else:
				os.remove('data/webpages/index/'+website)
		index_website = open('data/webpages/index/0.txt', 'w')
		index_website.write(first_page)
		index_website.close()
		for website in os.listdir('data/webpages/old'):
			if website.startswith('.'):
				pass
			else:
				os.remove('data/webpages/old/'+website)
		old_website = open('data/webpages/old/0.txt', 'w')
		old_website.write(second_page)
		old_website.close()
		comparer = Comparer.Comparer()
		comparer.compare()
		comparing_key_file = open('testpages/changes_key.txt', 'r')
		comparing_key = comparing_key_file.read()
		comparing_key_file.close()
		comparing_result_file = open('data/changes.txt', 'r')
		comparing_result = comparing_result_file.read()	
		comparing_result_file.close()
		self.assertEqual(comparing_key, comparing_result)

if __name__ == '__main__':
	unittest.main()
