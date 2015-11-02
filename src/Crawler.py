from bs4 import BeautifulSoup
import requests

class Website(object):
	def __init__(self, content):
		self.content = content
	def to_string(self):
		return str(self.content)
class Crawler(object):
	
	def __init__(self, starting_domain, starting_subpage):
		self.starting_domain = starting_domain
		self.starting_subpage = starting_subpage
		self.visited_links = set()
		self.unvisited_links = set()
		self.failed_links = set()
		self.unvisited_links.add(starting_subpage)

	def save_webpage(self, link, content):
		html_page = open(link, 'w')
		html_page.write(content)
		html_page.close()
		
	def get_webpage(self, url):
		return requests.get(url)

	def scrape_site_extract_links(self):	
		next_subpage = self.unvisited_links.pop()
		next_site = self.starting_domain + next_subpage
		print next_site

		try:
			site = requests.get(next_site)
			tree = BeautifulSoup(site.content, 'html.parser')
			self.visited_links.add(str(next_subpage))
			for linknode in tree.find_all('a'):
				link = str(linknode.get('href'))
				if link.startswith('/'):
					if link not in self.visited_links:
						self.unvisited_links.add(link)
		except Exception:
			print "Not possible to scrape: " + next_site
			self.failed_links.add(next_site)
	
	def Crawl(self):
		while len(self.unvisited_links) > 0:
			print "Crawling..."
			self.scrape_site_extract_links()
			print "One subpage crawled!"
			print "Crawled subpages: " + str(len(self.visited_links))
			print "Subpages to go: " + str(len(self.unvisited_links))
		print "Failed links: "
		print self.failed_links
