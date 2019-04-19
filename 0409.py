#-*- coding:utf-8 -*-
import re
import json
import time
import urllib
import pprint
import sqlite3
import requests
url = 'http://neris.csrc.gov.cn/alappl/home/volunteerLift.do'
# res = r'<.*?titleshow.*?>(.*?)<.*?>'
res_title = r'<div\s{1}class=\"center_right_mian1_content\".*?titleshow.*?>(.*?)<.*?title=(.*?)<\/table>'
res_time = r'\d{4}-\d{2}-\d{2}'
# res_hanzi = ur'[\u4e00-\u9fa5]{4,7}'
conn = sqlite3.connect('csrc.db')
cursor = conn.cursor()
sql_create = '''CREATE TABLE documents (
	ID int,
	title text,
	path int);'''
cursor.execute(sql_create)
cursor.close()

# main function
def html_query():
	docu_all = []
	headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en,zh;q=0.9,zh-CN;q=0.8,lb;q=0.7',
	'Cache-Control': 'max-age=0',
	'Content-Length': '33',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Cookie': 'JSESSIONID=BE162D500FD8CCF5CB80EAA4C1D2F415',
	'Host': 'neris.csrc.gov.cn',
	'Origin': 'http://neris.csrc.gov.cn',
	'Proxy-Connection': 'keep-alive',
	'Referer': 'http://neris.csrc.gov.cn/alappl/home/volunteerLift.do',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
	}
	for page in range(10):
		data = 'edCde=300009&pageNo={}&pageSize=10'.format(str(page+1))
		try:
			html_solo = requests.post(url, data = data, headers = headers).content.decode('utf-8')
		except:
			print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), "404 Not Found.")
			
		docu_solo = re.findall(res_title, html_solo, re.I|re.S|re.M)
		if(len(docu_solo) < 10):
			file_write(html_solo)
			
		print(len(docu_solo))
		for msg in docu_solo:
			msg_time = re.findall(res_time, msg[1], re.I|re.S|re.M)
			docu_all.append((len(docu_all)+1, msg[0], len(msg_time)))
		time.sleep(2)
	pprint.pprint(docu_all, width = 10)
	
	conn = sqlite3.connect('csrc.db')
	cursor = conn.cursor()
	sql_insert = '''INSERT INTO documents (ID, title, path) VALUES (?, ?, ?);'''

	for docu in docu_all:
		cursor.execute(sql_insert, docu)
	conn.commit()
	cursor.close()
	
	return

def file_write(content):
	f = open('0411.txt', 'a')
	f.write(content.encode('utf-8'))
	f.write('\n')
	f.close
	return
html_query()

