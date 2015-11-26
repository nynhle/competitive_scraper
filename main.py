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

print "Domain scraped. Found " + str(counted_files) + " since last run."


