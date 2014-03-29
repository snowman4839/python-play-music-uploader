#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass

from gmusicapi import Musicmanager

import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from subprocess import call

import glob

oauthFile = "/home/owner/.googleoauth"
uploadDir = "/mnt/hd0/Music/Android Music/uploads/"
storageDir = "/mnt/hd0/Music/Android Music/"

def ask_for_credentials():
	"""Make an instance of the api and attempts to login with it.
	Return the authenticated api.
	"""

	api = Musicmanager()

	logged_in = False
	attempts = 0

	api.login(oauthFile)

	return api


def upload():
	api = ask_for_credentials()

	if not api.is_authenticated():
		print "Sorry, those credentials weren't accepted."
		return

	print 'Successfully logged in.'
	print

	mp3files = []
	for root, dirs, files in os.walk(uploadDir):
		for file in files:
			if file.endswith('.mp3'):
				mp3files.append(os.path.join(root, file))

	for each in mp3files:
	print each
	uploadDict = api.upload(each, 1, True)
	if uploadDict[0]:
		call(["mv",each,storageDir])
		print "uploaded"
	elif uploadDict[1]:
		call(["mv",each,storageDir])
		print "matched song on google servers"
	elif uploadDict[2]:
		call(["mv",each,storageDir])
		print "already uploaded"

	api.logout()
	print "logged out"

class Handler(FileSystemEventHandler):
	def on_created(self, event):
		print "new file!"
		upload()

if __name__ == '__main__':
	upload()
	eventWatcher = Handler()
	observer = Observer()
	observer.schedule(eventWatcher,uploadDir,recursive=False)
	print "starting"
	observer.start()
	try:
	while True:
		time.sleep(1)
	except KeyboardInterrupt:
	print "stopping"
	observer.stop()
	print "joining"
	observer.join()