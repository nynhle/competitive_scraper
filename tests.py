import unittest
import os
from src import Scraper

os.system('python -m SimpleHTTPServer 8000')

class TestScraper(unittest.TestCase):
	scraper = Scraper.Scraper('http://localhost/testpages/first_version.html')
	scraper.Scrape()
