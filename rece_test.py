import json
import requests
import time
import urllib
from pprint import pprint

TOKEN = "637785666:AAHRW-gz-CeKkSGbP_xKubcau0dO28ffBYc"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


rece_updates = requests.get(URL + "getUpdates" + "?offset=79481133").json()["result"]
pprint(rece_updates)
