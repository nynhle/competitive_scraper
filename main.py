from src import Crawler
from src import Scraper
from src import Comparer

def print_menu():
	print '\nMenu'
	print '1. Manually scrape a website.'
	print '2. Exit' 

def manually_scrape():
	domain = raw_input("\nWhat domain to limit to? ")
	subsite = raw_input("Which subpage to start from? (blank if same as domain) ")

	crawler = Crawler.Crawler(domain, subsite)
	url_list = crawler.Crawl()
	scraper = Scraper.Scraper(url_list)
	scraper.Scrape()
	comparer = Comparer.Comparer()
	counted_files = comparer.compare()

	print "Domain scraped. " + str(counted_files) + " changes since last run."

user_input = ""

while user_input != '4':
	print_menu()
	user_input = raw_input('\n')
	
	if user_input == '1':
		manually_scrape()
	elif user_input == '2':
		break
	else:
		print 'Not a valid input, please try again.'



