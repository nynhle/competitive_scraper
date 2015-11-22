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
		self.unvisited_links.add(starting_domain+starting_subpage) # To be able to start scraping we need a starting page.
	
	# Returning html based on the url passed in as argument.
	def get_webpage(self, url):
		return requests.get(url) 
	
	def export_full_url_list(self):
		full_url = []
		for url in self.visited_links:
			full_url.append(self.starting_domain + url)
		return full_url
			
	# Method picking the next site in the unvisited_links set and parse the html to extract all links on the
	# new subpage. Pushes all the new links which do not exist or have been visited onto the unvisited_links set.
	# TODO: Gonna be a long and messy method. Refactor.
	def scrape_site_extract_links(self):	
		next_site = self.unvisited_links.pop()
		try:
			site = requests.get(next_site)
			tree = BeautifulSoup(site.content, 'html.parser')
			self.visited_links.add(str(next_site))
			for linknode in tree.find_all('a'):
				link = str(linknode.get('href'))
				if link.startswith('/'):
					full_link =  self.starting_domain + link
					if full_link not in self.visited_links: # If it's not visited -> add.
						self.unvisited_links.add(full_link) # No need to worry about duplicates in sets.
				elif link.startswith(self.starting_domain):
					if link not in self.visited_links:
						self.unvisited_links.add(link)
		except Exception:
			print "Not possible to scrape: " + next_site
			self.failed_links.add(next_site)
	
	def replace_last_filename(self, link, new_filename):
		index = len(link)-1
		new_link_stack = []
		new_link = ""
		slashFound = False
		
		while index >= 0:
			if not slashFound and link[index] == '/':
				slashFound = True
				new_link_stack.append(link[index])
			elif slashFound:
				new_link_stack.append(link[index])
			index = index -1 
		
		while len(new_link_stack) > 0:
			new_link += new_link_stack.pop()
		
		new_link += new_filename

		return new_link
		
	

	# Main pattern. Crawls pages as long as there are still 
	# unvisited pages.	
	def Crawl(self):
		while len(self.unvisited_links) > 0:
			self.scrape_site_extract_links()
		return self.export_full_url_list()

