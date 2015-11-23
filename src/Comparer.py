import filecmp
import difflib

def return_index():
	with open('../data/index.txt') as index_file:
		return index_file.readlines()

def return_old_index():
	with open('../data/old.txt') as old_index_file:
		return old_index_file.readlines()

def get_html_file(key):
	if '.txt' in key:
		return open('../data/webpages/index/' + key + '.txt').read()
	else:
		return key


def get_old_html_file(key):
	if '.txt' in key:	
		return open('../data/webpages/old/' + key + '.txt').read()
	else:
		return key

def get_line_key(line):
	result = ''
	for char in line:
		if char == '#':
			break
		else:
			result += char
	return result

def get_line_url(line):
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

class UrlFile(object):
	def __init__(self, key, url):
		self.key = key
		self.url = url
	
	def get_key(self):
		self.key

	def get_url(self):
		self.url

def parse_index_url_file():
	url_list_file = []
	for line in return_index():
		url = UrlFile(get_line_key(line), get_line_url(line))
		url_list_file.append(url)

	return url_list_file

def parse_old_index_url_file():
	old_list_file = []
	for line in return_old_index():
		url = UrlFile(get_line_key(line), get_line_url(line))
		old_list_file.append(url)

	return old_list_file

class FilePair(object):
	def __init__(self, new, old):
		self.new = new
		self.old = old


def get_matched_pairs():
	new_urls = parse_index_url_file()
	old_urls = parse_old_index_url_file()
	pair_list = []

	for url in new_urls:
		for old_url in old_urls:
			if url.url == old_url.url:
				pair = FilePair(url.url, old_url.url)
				pair_list.append(pair)

	return pair_list

def compare():
	log = open('data/changes.txt', 'a')
	for pair in get_matched_pairs():
		new_site = open('data/webpages/index/' + pair.new.key + '.txt')
		old_site = open('data/webpages/old/' + pair.old.key + '.txt')
		d = difflib.Differ()
		result = d.compare(new_site, old_site)
		log.write(result)	
	log.close()

			
compare()		

