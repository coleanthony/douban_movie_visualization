

import urllib3
import urllib
import urllib.request
import json
import time
import random
from bs4 import BeautifulSoup

inputFile = 'douban_movie.txt'
fr = open(inputFile, 'r')
outputFile = 'douban_movie_detail.txt'
fw = open(outputFile, 'w')
fw.write('id^title^url^cover^rate^director^composer^actor^category^district^language^showtime^length^othername^description\n')

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

firstLine = True
count = 1
errorCount = 0
result = {}

for line in fr:
	if firstLine:
		firstLine = False
		continue

	line = line.split(';')

	movieId = line[0]
	title = line[1]
	url = line[2]
	cover = line[3]
	rate = line[4].rstrip('\n')

	if result.has_key(movieId):
		continue
	else:
		result[str(movieId)] = 1

	try:
		request = urllib.request.Request(url=url,headers=headers)
		response = urllib.request.urlopen(request)
		html = response.read()
		html = BeautifulSoup(html)

		info = html.select('#info')[0]
		info = info.get_text().split('\n')

		# 提取字段，只要冒号后面的文本内容
		director = info[1].split(':')[-1].strip()
		composer = info[2].split(':')[-1].strip()
		actor = info[3].split(':')[-1].strip()
		category = info[4].split(':')[-1].strip()
		district = info[6].split(':')[-1].strip()
		language = info[7].split(':')[-1].strip()
		showtime = info[8].split(':')[-1].strip()
		length = info[9].split(':')[-1].strip()
		othername = info[10].split(':')[-1].strip()

		# 电影简介
		description = html.find_all("span", attrs={"property": "v:summary"})[0].get_text()
		description = description.lstrip().lstrip('\n\t').rstrip().rstrip('\n\t').replace('\n','\t')

		# 写入数据
		record = str(movieId) + '^' + title + '^' + url + '^' + cover + '^' + str(rate) + '^' + director.encode('utf8') + '^' + composer.encode('utf8') + '^' + actor.encode('utf8') + '^' + category.encode('utf8') + '^' + district.encode('utf8') + '^' + language.encode('utf8') + '^' + showtime.encode('utf8') + '^' + length.encode('utf8') + '^' + othername.encode('utf8') + '^' + description.encode('utf8') + '\n'
		fw.write(record)
		print (count,title)
		time.sleep(5)
	
	except Exception:
		print (count,title,"Error")
		errorCount = errorCount + 1
	else:
		pass
	finally:
		pass

	count = count + 1
	
print (count, errorCount)
fr.close()
fw.close()