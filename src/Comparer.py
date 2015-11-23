import filecmp
import difflib

class Comparer(object):
	
	def return_index(self):
		with open('data/index.txt') as index_file:
			return index_file.read()

	def return_old_index(self):
		with open('data/old.txt') as old_index_file:
			return old_index_file.read()

	def get_html_file(self, key):
		if '.txt' in key:
			return open('data/webpages/index/' + key + '.txt').read()
		else:
			return key


	def get_old_html_file(self, key):
		if '.txt' in key:	
			return open('data/webpages/old/' + key + '.txt').read()
		else:
			return key

	def get_line_key(self, line):
		result = ''
		for char in line:
			if char == '#':
				break
			else:
				result += char
		return result

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
		for line in self.return_index():
			url = UrlFile(self.get_line_key(line), self.get_line_url(line))
			url_list_file.append(url)

		return url_list_file

	def parse_old_index_url_file(self):
		old_list_file = []
		for line in self.return_old_index():
			url = UrlFile(self.get_line_key(line), self.get_line_url(line))
			old_list_file.append(url)

		return old_list_file

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
		log = open('data/changes.txt', 'a')
		for pair in self.get_matched_pairs():
			new_site = open('data/webpages/index/' + str(pair.new.key) + '.txt', 'r')
			old_site = open('data/webpages/old/' + str(pair.old.key) + '.txt', 'r')
			d = difflib.Differ()
			result = d.compare(new_site, old_site)
			print result
		log.close()

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


