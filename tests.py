import unittest
import os
from src import Scraper

#os.spawnl(os.P_NOWAIT, 'python -m SimpleHTTPServer 8000')
class TestScraper(unittest.TestCase):
	scraper = Scraper.Scraper('http://localhost:8000/testpages/first_version.html')
	scraper.Scrape()
