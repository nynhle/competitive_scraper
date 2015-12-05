# Competitive Scraper
End product is supposed to notify the user of changes in HTML at a specific site.

This is of interest since it could mean interesting information is either added or removed from a specific website. Right now, the software can gather all url's from a specific website, pull down the html from those url's. Two versions of scraped html is stored, the latest and the previous one. These two is then beeing compared and differences are logged. 

# How to run 
Clone the project. Run main.py. Select '1. Manual scrape' by putting pressing key '1' and then 'enter'. Exit with '2'. When next scrape is desired, simply do the same process again. The comparing is done every time the program runs.

# How to view scraped html
The newest html files will be located in '/data/webpages/index/'. You can map the files to specific urls with the file 'index.txt' located in '/data/'. If there has been a previous scrape, the files from that scrape will be located in '/data/webpages/old/'. To map files to specific url's, use the file 'old.txt' in '/data/'. 

# How to view changes
All known changes are stored in '/data/changes/'. Every scraping creates a new folder which has the name of the time when the scraping was done. All changes related to specific files are logged in different files within this folder. To figure out which file relates to a specific url, look into the 'index.txt' file located in the same directory.
