import requests
import json
import re
import time

#receive new portal link
def get_updates():
	global last_id

	rece_cmd = requests.get(url_tg + "getUpdates").json()["result"]

	try:
		cmd_text = rece_cmd[-1]["message"]["text"]
		cmd_id = rece_cmd[-1]["message"]["message_id"]
	except KeyError:
		return
	
	if((re.match(cmd_pattern, cmd_text)) and (cmd_id != last_id)):
		last_id = cmd_id
		print(cmd_text)
		if re.match(add_pattern, cmd_text):
			send_tg((), 'Congratulations, your portal has been accepted.')
			portal_list_add(cmd_text[5:])
		elif re.match(del_pattern, cmd_text):
			send_tg((int(cmd_text[5:]), ), 'Congratulations, this portal has been deleted:')
			portal_list_del(int(cmd_text[5:]))
		elif re.match(help_pattern, cmd_text):
			send_tg((), "I'm your father.")
		elif re.match(att_pattern, cmd_text):
			send_tg((), "Maybe I'm not SelfHelp's father, but I still love her.@selfhelp233")
		else:
			send_tg((), 'Sorry, your application has been rejected.')
	return

def send_tg(portal_tuple, attention):
	content = ''

	try:
		if(len(attention)):
			requests.get(url_tg + "sendMessage?chat_id=-393700256&text={}".format(attention))
		requests.get(url_tg + "sendMessage?chat_id=-393700256&text={}".format(content.encode('utf-8')))
	except:
		print("send unsuccessfully")
	return
	
def query_cycle():
	while(1):
		get_updates()
		time.sleep(10)
	return
	
cmd_pattern = r'\/.*'
help_pattern = r'\/help'
add_pattern = r'\/add\s\w{32}\.\d{2}'
del_pattern = r'\/del\s\d'
att_pattern = r'\/attack'

TOKEN = "33637785666:AAHRW-gz-CeKkSGbP_xKubcau0dO28ffBYc"
url_tg = "https://api.telegram.org/bot{}/".format(TOKEN[2:])
last_id = 0

query_cycle()