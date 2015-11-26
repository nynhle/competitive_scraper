from src import Crawler
from src import Scraper
from src import Comparer

print "Welcome to competitive scraper v. 0.01"

domain = raw_input("\nWhat domain to limit to? ")
subsite = raw_input("Which subpage to start from? (blank if same as domain) ")

crawler = Crawler.Crawler(domain, subsite)
url_list = crawler.Crawl()
scraper = Scraper.Scraper(url_list)
scraper.Scrape()
comparer = Comparer.Comparer()
counted_files = comparer.compare()

print "Domain scraped. " + str(counted_files) + " changes since last run."

def print_menu():
	print '\nMenu'
	print '1. Manually scrape a website.'
	print '2. Set up a scraping schedule.'
	print '3. Delete saved data'
	print '4. Exit' 


