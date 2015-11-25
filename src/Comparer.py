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
		url_list_file = []
		index_file = self.return_index()
		for line in index_file:
			if '#' in line and '.txt' in line:
				url = UrlFile(self.get_line_key(line), self.get_line_url(line))
				url_list_file.append(url)

		return url_list_file

	def parse_old_index_url_file(self):
		old_list_file = []
		old_file = self.return_old_index()
		for line in old_file:
			url = UrlFile(self.get_line_key(line), self.get_line_url(line))
			old_list_file.append(url)

		return old_list_file
	
	# TODO: Add logic for removed or added pages.
	def get_matched_pairs(self):
		new_urls = self.parse_index_url_file()
		old_urls = self.parse_old_index_url_file()
		pair_list = []

		for url in new_urls:
			for old_url in old_urls:
				if url.url == old_url.url:
					pair = FilePair(url, old_url)
					pair_list.append(pair)
		return pair_list

	def compare(self):
		filechange_index = 0
		now = datetime.datetime.now()
		time = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ' ' + str(now.hour) + '_' + str(now.minute) + '_' + str(now.second)
		os.mkdir('data/changes/' + time)
		index_file = open('data/changes/' + time + '/index.txt', 'w').close()
	
		for pair in self.get_matched_pairs():
			index_file = open('data/changes/' + time + '/index.txt', 'a')
			log = open('data/changes/' + time + '/' + str(filechange_index) + '.txt', 'w')
			new_site = open('data/webpages/index/' + str(pair.new.key) + '.txt', 'r')
			old_site = open('data/webpages/old/' + str(pair.old.key) + '.txt', 'r')
			diff = difflib.context_diff(new_site.readlines(), old_site.readlines())
			delta = ''.join(diff)
			log.write('=====CHANGES FOR URL: ' + pair.new.url + '=====\n\n')
			log.write(delta)
			log.close()
			# For test purposes:
			log = open('data/changes.txt', 'w')
			log.write(delta)
			log.close()
			new_site.close()
			old_site.close()
			index_file.write(str(filechange_index) + '  ====>  ' + pair.new.url)
			filechange_index += 1
			return filechange_index + 1
			

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


