import unittest
from ..main import main

class TestCrawler(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(TestCrawler, self).__init__(*args, **kwargs)
		self.crawler = main.Crawler('http://bruab.github.io', '/cs294_fall2015/')

	def test_no_link_duplicates(self):
		self.assertEqual(self.crawler.visited_links, set(self.crawler.visited_links))


if __name__ == '__main__':
	unittest.main()
