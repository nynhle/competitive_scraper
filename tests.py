import unittest
import os
from src import Crawler
from src import Scraper

# Before running the tests, start a SimpleHTTPServer from the 
# competitive scraper directory by running:
# 'python -m SimpleHTTPServer 8000
# TODO: Make this server start when the tests are run.

class TestScraper(unittest.TestCase):
	crawler = Crawler.Crawler('http://localhost:8000/testpages/first_version.html')
	crawler.Crawl()
	scraper = Scraper.Scraper(crawler.export_full_url_list())
	scraper.Scrape()
