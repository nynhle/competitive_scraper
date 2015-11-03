from bs4 import BeautifulSoup
import requests
	
class Crawler(object):
	
	# Init method. Domain and starting subpage are hold as class properties to
	# be accessible from all class methods.
	def __init__(self, starting_domain, starting_subpage):
		self.starting_domain = starting_domain
		self.starting_subpage = starting_subpage
		self.visited_links = set()
		self.unvisited_links = set()
		self.failed_links = set()
		self.unvisited_links.add(starting_subpage) # To be able to start scraping we need a starting page.
	
	# Returning html based on the url passed in as argument.
	def get_webpage(self, url):
		return requests.get(url) 
	
	# Method picking the next site in the unvisited_links set and parse the html to extract all links on the
	# new subpage. Pushes all the new links which do not exist or have been visited onto the unvisited_links set.
	# TODO: Add functionality for saving a webpage.
	# TODO: Gonna be a long and messy method. Refactor.
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
					if link not in self.visited_links: # If it's not visited -> add.
						self.unvisited_links.add(link) # No need to worry about duplicates in sets.
		except Exception:
			print "Not possible to scrape: " + next_site
			self.failed_links.add(next_site)
	

	# Main pattern. Crawls pages as long as there are still 
	# unvisited pages.	
	def Crawl(self):
		while len(self.unvisited_links) > 0:
			print "Crawling..."
			self.scrape_site_extract_links()
			print "One subpage crawled!"
			print "Crawled subpages: " + str(len(self.visited_links))
			print "Subpages to go: " + str(len(self.unvisited_links))
		print "Failed links: "
		scraper = Scraper(self.visited_links)
		scraper.replace_old_index()
		scraper.save_webpages()
		print self.failed_links
		
class Scraper(object):
	def __init__(self, list_of_urls):
		self.url_list = list_of_urls

	def replace_old_index(self):
		index_file = open('index.txt', 'r')
		index_file_content = index_file.read()
		index_file.close()
		old_file = open('old.txt', 'w')
		old_file.write(index_file_content)
		old_file.close()
		open('index.txt', 'w').close()

	def save_webpages(self):
		index = 0
		index_file = open('index.txt', 'a')
		for link in self.url_list:
			index_file.write('\n'+str(index)+'#'+link)
			index = index + 1
