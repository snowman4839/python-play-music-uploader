#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass

from gmusicapi import Musicmanager
from gmusicapi import Webclient

import os
import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler, FileCreatedEvent

from subprocess import call

import glob

######################################
oauthFile = "/home/owner/.googleoauth"
uploadDir = "/mnt/hd0/Music/Android Music/uploads/"
storageDir = "/mnt/hd0/Music/Android Music/"
#####################################

####################################
googleEmail = ""
googlePass = ""
####################################

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

	uploader = Webclient()
	uploader.login(googleEmail, googlePass)

	if not api.is_authenticated():
		print "Sorry, those credentials weren't accepted."
		return

	print 'Successfully logged in.'
	print

	time.sleep(10);

	mp3files = []
	for root, dirs, files in os.walk(uploadDir):
		for file in files:
			if file.endswith('.mp3'):
				mp3files.append(os.path.join(root, file))
			if file.endswith('.m4a'):
				mp3files.append(os.path.join(root, file))

	call(["mkdir","/tmp/cover"])

	for each in mp3files:
		print each
		uploadDict = api.upload(each, 1, True)
		if uploadDict[0]:
			songid = (uploadDict[0])[each]
			call(["eyeD3","--write-images=/tmp/cover",each])
			call(["sleep","1"])
			cover = glob.glob("/tmp/cover/*")
			if (coverFile):
				print coverFile
				call(["mv",coverFile[0],"/tmp/cover/img.jpg"])
				uploader.upload_album_art(songid,"/tmp/cover/img.jpg")
				#call(["rm","/tmp/cover/*"])
			call(["mv",each,storageDir])
			print "uploaded"
		elif uploadDict[1]:
			call(["mv",each,storageDir])
			print "matched song on google servers"
		elif uploadDict[2]:
			call(["mv",each,storageDir])
			print "already uploaded"

	call(["rm","-R","/tmp/cover"])

	print "logging out"
	api.logout()
	uploader.logout();
	print "logged out"

class Handler(PatternMatchingEventHandler):
	def on_any_event(self, event):
		print "new MP3 file!"
		upload()

if __name__ == '__main__':
	#upload()
	eventWatcher = Handler("*.mp3",["*.mp3.tacitpart"],False,False)
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
