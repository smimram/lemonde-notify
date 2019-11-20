#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import feedparser
import webbrowser
import gi
gi.require_version('Notify', '0.7')
from gi.repository import GLib, Notify

Notify.init("Le Monde")

url = 'https://www.lemonde.fr/rss/en_continu.xml'

class App():
    def __init__(self):
        self.notification = None
        self.lastid = ""
        self.check()

    def notification_cb(self, notification, action_name, link):
        webbrowser.open(link)

    def check(self):
        try:
            posts = feedparser.parse(url).entries
        except Exception as e:
            sys.stderr.write("Error: " + str(e) + "\n")
            posts = []
        for post in posts:
            if post.id == self.lastid:
                break
            self.notification = Notify.Notification.new("Le Monde", post.title, "dialog-information")
            self.notification.add_action("default", "default", self.notification_cb, post.link)
            try:
                self.notification.show()
            except Exception as e: # the show can timeout
                sys.stderr.write("Error: " + str(e) + "\n")
        try:
            self.lastid = posts[0].id
        except Exception as e:
            self.lastid = ""
        GLib.timeout_add_seconds(60*5, self.check)

app = App()
GLib.MainLoop().run()
