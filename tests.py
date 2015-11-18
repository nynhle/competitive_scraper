import unittest
import os
from src import Crawler
from src import Scraper

class TestScraper(unittest.TestCase):
	crawler = Crawler.Crawler('http://localhost:8000/testpages/first_version.html')
	crawler.Crawl()
	scraper = Scraper.Scraper(crawler.export_full_url_list())
	scraper.Scrape()
