#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import json
import requests
import webbrowser
import gi
gi.require_version('Notify', '0.7')
from gi.repository import GLib, Notify

Notify.init("Le Monde")

lastid = 0
url = 'http://live.lemde.fr/mux.json'

class App():
    def __init__(self):
        self.notification = None
        self.lastid = 0
        self.check()

    def notification_cb(self, notification, action_name, link):
        webbrowser.open(link)

    def check(self):
        try:
            feed = requests.get(url).text
            feed = feed[5:-1]
            feed = json.loads(feed)
        except Exception as e:
            sys.stderr.write("Error: " + str(e) + "\n")
            feed = []
        for i in feed:
            i = i['data']
            try:
                id = i['id']
            except Exception as e:
                sys.stderr.write("Error: " + str(e) + "\n")
                id = 0
            if id > self.lastid:
                self.lastid = id
                titre = i['titre_court']
                link = "http://www.lemonde.fr" + i['link']
                if not titre.endswith('?'): titre += "."
                self.notification = Notify.Notification.new("Le Monde", titre, "dialog-information")
                self.notification.add_action("default", "Voir l'article...", self.notification_cb, link)
                try:
                    self.notification.show()
                except Exception as e: # the show can timeout
                    sys.stderr.write("Error: " + str(e) + "\n")
        GLib.timeout_add_seconds(60, self.check)

app = App()
GLib.MainLoop().run()
