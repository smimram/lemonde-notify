#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import requests
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

Notify.init("Le Monde")

lastid = 0
url = 'http://live.lemde.fr/mux.json'

while True:
    try:
        feed = requests.get(url).text
        feed = feed[5:-1]
        feed = json.loads(feed)
    except requests.exceptions.RequestException as e:
        print e
        feed = []
    for i in feed:
        i = i['data']
        id = i['id']
        if id > lastid:
            lastid = id
            Hello=Notify.Notification.new("Le Monde", i['titre_court'], "dialog-information")
            Hello.show()
    time.sleep(5*60)
