import glob
import os
import requests

class Scraper(object):
	def __init__(self, list_of_urls):
		self.url_list = list_of_urls

	def replace_old_index(self):
		index_file = open('data/index.txt', 'r')
		index_file_content = index_file.read()
		index_file.close()
		old_file = open('data/old.txt', 'w')
		old_file.write(index_file_content)
		old_file.close()
		open('index.txt', 'w').close()

	def save_urls(self):
		index = 0
		index_file = open('data/index.txt', 'a')
		for link in self.url_list:
			index_file.write('\n'+str(index)+'#'+link)
			index = index + 1
	
	def delete_old_webpages(self):
		webpages = os.listdir('data/webpages/old')
		for webpage in webpages:
			if webpage.startswith('.'):
				pass
			else:	
				os.remove(webpage)

	def move_files(self):
		src = 'data/webpages/index'
		dst = 'data/webpages/old'
		list_of_files = os.listdir(src)
		for webpage in list_of_files:
			full_path = src + '/' + webpage
			os.system('mv' + ' ' + full_path + ' ' + dst)
	
	def save_webpages(self):
		index = 0
		for url in self.url_list:
			site = requests.get(url).content
			f = open('data/webpages/index/' + str(index)+'.txt', 'a')
			f.write(str(site))
			f.close()
			index = index + 1
	
	def Scrape(self):
		self.replace_old_index()
		self.save_urls()
		self.delete_old_webpages()
		self.move_files()
		self.save_webpages()	