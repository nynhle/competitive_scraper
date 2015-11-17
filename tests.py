import unittest
import os
from src import Scraper

os.system('python server.py')

class TestScraper(unittest.TestCase):
	scraper = Scraper.Scraper('http://localhost/testpages/first_version.html')
	scraper.Scrape()
