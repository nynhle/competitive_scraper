from sets import Set
from bs4 import BeautifulSoup
import urllib2

class Crawler(object):
	
	def __init__(self, starting_domain, starting_subpage):
		self.starting_domain = starting_domain
		self.starting_subpage = starting_subpage
		self.visited_links = Set()
		self.unvisited_links = Set()
		self.unvisited_links.add(starting_subpage)

	def get_webpage(self, url):
		return urllib2.urlopen(url)

	def scrape_site_extract_links(self):	
		next_subpage = self.unvisited_links.pop()
		next_site = self.starting_domain + next_subpage
		print next_site
		site = urllib2.urlopen(next_site)
		tree = BeautifulSoup(site, 'html.parser')
		self.visited_links.add(str(next_subpage))
		for linknode in tree.find_all('a'):
			link = str(linknode.get('href'))
			if link.startswith('/'):
				if link not in self.visited_links:
					self.unvisited_links.add(link)
	
	def Crawl(self):
		while len(self.unvisited_links) > 0:
			print "Crawling..."
			self.scrape_site_extract_links()
			print "One subpage crawled!"
			print "Crawled subpages: " + str(len(self.visited_links))
			print "Subpages to go: " + str(len(self.unvisited_links))
