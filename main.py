import Crawler

print "Welcome to competitive scraper v. 0.01"
print "Currently only supporting website crawling..."

domain = raw_input("\nWhat domain to limit to? ")
subsite = raw_input("Which subpage to start from? (blank if same as domain) ")

crawler = Crawler.Crawler(domain, subsite)
crawler.Crawl()

