import filecmp
import difflib
import datetime
import os

class Comparer(object):
	
	def return_index(self):
		index_file = open('data/index.txt', 'r')
		index_content = index_file.readlines()
		index_file.close()
		return index_content

	def return_old_index(self):
		old_file = open('data/old.txt', 'r')
		file_content = old_file.readlines()
		old_file.close()
		return file_content

	def get_line_key(self, line):
		result = ''
		for char in line:
			if char == '#':
				break
			elif self.isParsable_key(char):
				result += char
		return result
	
	def isParsable_key(self, number):
		try:
			int(number)
			return True
		except:
			return False

	def get_line_url(self, line):
		result = ''
		isUrl = False
		for char in line:
			if isUrl:
				result += char
			elif char == '#':
				isUrl = True
			else:
				pass		
		return result

	def parse_index_url_file(self):
		url_list_file = set()
		index_file = self.return_index()
		for line in index_file:
			if '#' in line:
				url = UrlFile(self.get_line_key(line), self.get_line_url(line))
				url_list_file.add(url)

		return url_list_file

	def parse_old_index_url_file(self):
		old_list_file = set()
		old_file = self.return_old_index()
		for line in old_file:
			if '#' in line:
				url = UrlFile(self.get_line_key(line), self.get_line_url(line))
				old_list_file.add(url)

		return old_list_file
	
	def get_matched_pairs(self):
		new_urls = self.parse_index_url_file()
		matched_new_urls = set()
		unmatched_new_urls = set()
		old_urls = self.parse_old_index_url_file()
		matched_old_urls = set()
		unmatched_old_urls = set()
		pair_list = set()

		for url in new_urls:
			for old_url in old_urls:
				if url.url == old_url.url:
					pair = FilePair(url, old_url)
					pair_list.add(pair)
					matched_new_urls.add(url.url)
					matched_old_urls.add(old_url.url)
		
		for url in new_urls:
			if url.url not in matched_new_urls:
				pair = NoOldFilePair(url)
				pair_list.add(pair)

		for url in old_urls:
			if url.url not in matched_old_urls:
				pair = NoNewFilePair(url)
				pair_list.add(pair)

		return pair_list

	def compare(self):
		filechange_index = 0
		now = datetime.datetime.now()
		time = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ' ' + str(now.hour) + '_' + str(now.minute) + '_' + str(now.second)
		os.mkdir('data/changes/' + time)
		index_file = open('data/changes/' + time + '/index.txt', 'w').close()
	
		for pair in self.get_matched_pairs():
			index_file = open('data/changes/' + time + '/index.txt', 'a')
			log = open('data/changes/' + time + '/' + str(filechange_index) + '.txt', 'w').close()
			log = open('data/changes/' + time + '/' + str(filechange_index) + '.txt', 'a')
			pair.set_new_webpage()
			pair.set_old_webpage()
			pair.calculate_delta()
			log.write('=====CHANGES FOR URL: ' + pair.url + '=====\n\n')
			log.write(pair.return_delta())
			log.close()
			# For test purposes:
			test_log = open('data/changes.txt', 'w')
			test_log.write(pair.return_delta())
			test_log.close()
			index_file.write(str(filechange_index) + '  ====>  ' + pair.url)
			filechange_index += 1
			

class UrlFile(object):
	def __init__(self, key, url):
		self.key = key
		self.url = url
	
	def get_key(self):
		self.key

	def get_url(self):
		self.url


class FilePair(object):
	def __init__(self, new, old):
		self.new = new
		self.old = old
		self.url = new.url

	def calculate_delta(self):
		diff = difflib.context_diff(self.old_site, self.new_site)
		delta = ''.join(diff)
		self.delta = delta

	def return_delta(self):
		self.calculate_delta()
		return self.delta
	
	def set_new_webpage(self):
		site = open('data/webpages/index/' + str(self.new.key) + '.txt', 'r')
		self.new_site = site.readlines()
		site.close()

	def set_old_webpage(self):
		site = open('data/webpages/old/' + str(self.old.key) + '.txt', 'r')
		self.old_site = site.readlines()
		site.close()

class NoOldFilePair(FilePair):
	def __init__(self, new):
		self.new = new
		self.url = new.url

	def set_old_webpage(self):
		self.old_site = ''

class NoNewFilePair(FilePair):
	def __init__(self, old):
		self.old = old
		self.url = old.url

	def set_new_webpage(self):
		self.new_site = ''

