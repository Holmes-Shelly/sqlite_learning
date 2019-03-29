import re
import json
import time
import urllib
import requests

TOKEN = "33637785666:AAHRW-gz-CeKkSGbP_xKubcau0dO28ffBYc"
URL = "https://api.telegram.org/bot{}/".format(TOKEN[2:])

def get_updates(offset=None):
	print(offset)
	url = URL + "getUpdates"
	if offset:
		url += "?offset={}".format(offset)
	result = requests.get(url).json()['result']
	return result

def get_last_update_id(updates):
	return int(updates[-1]["update_id"])

def echo_all(updates):
	for update in updates:
		try:
			text = update["message"]["text"]
			chat = update["message"]["chat"]["id"]
			if re.match(r'\/.*', text):
				send_message('Command received.', chat)
		except KeyError:
			pass

def send_message(text, chat_id):
	text = urllib.parse.quote_plus(text)
	url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
	requests.get(url)

def main():
	last_update_id = None
	while True:
		updates = get_updates(last_update_id)
		if len(updates):
			print(len(updates))
			echo_all(updates)
			last_update_id = get_last_update_id(updates) + 1
		time.sleep(2)

if __name__ == '__main__':
	main()