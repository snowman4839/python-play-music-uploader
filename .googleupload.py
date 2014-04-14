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
	#Init music manager
	api = ask_for_credentials()

	#Init web client
	uploader = Webclient()
	uploader.login(googleEmail, googlePass)

	#Present error if auth isn't accepted
	if not api.is_authenticated():
		print "Sorry, those credentials weren't accepted."
		return

	#Success message if auth works
	print 'Successfully logged in.'
	print

	#Wait for any copies or uploads to watched folder to finish
	time.sleep(10);

	#Populate mp3files array with music files in the upload directory
	mp3files = []
	for root, dirs, files in os.walk(uploadDir):
		for file in files:
			if file.endswith('.mp3'):
				mp3files.append(os.path.join(root, file))
			if file.endswith('.m4a'):
				mp3files.append(os.path.join(root, file))

	#Create temp cover directory for artwork extraction and upload via eyeD3
	call(["mkdir","/tmp/cover"])

	#Upload and hand each appropriate case after upload
	for each in mp3files:

		#Print and upload the current file
		print each
		uploadDict = api.upload(each, 1, True)

		#If upload is successful
		if uploadDict[0]:
			#Get song id
			songid = (uploadDict[0])[each]
			#Extract artwork via eyeD3
			call(["eyeD3","--write-images=/tmp/cover",each])
			call(["sleep","1"])
			#Get the new artwork path
			coverFile = glob.glob("/tmp/cover/*")
			#If artwork was extracted
			if (coverFile):
				#Print the path to the artwork
				print coverFile
				#Move it to a absolute location and upload it to the newly uploaded song
				call(["mv",coverFile[0],"/tmp/cover/img.jpg"])
				uploader.upload_album_art(songid,"/tmp/cover/img.jpg")
				#call(["rm","/tmp/cover/*"])
			#Move uploaded file to the storage directory
			call(["mv",each,storageDir])
			print "uploaded"
		#Move uploaded file to the storage directory if it was matched to a song on the google servers
		elif uploadDict[1]:
			call(["mv",each,storageDir])
			print "matched song on google servers"
		#Move uploaded file to the storage directory if it was already uploaded to the account
		elif uploadDict[2]:
			call(["mv",each,storageDir])
			print "already uploaded"

	#Remove everything dealing with the temp artwork extraction
	call(["rm","-R","/tmp/cover"])

	#Logout of both interfaces
	print "logging out"
	api.logout()
	uploader.logout()
	print "logged out"

#Class to handle events when anything happens in the watched folder
class Handler(PatternMatchingEventHandler):
	def on_any_event(self, event):
		print "new MP3 file!"
		upload()

if __name__ == '__main__':
	#Initial upload on start
	upload()

	#Watch folder for newly added .mp3 files, ignore .tacitpart files while file is being uploaded
	eventWatcher = Handler("*.mp3",["*.mp3.tacitpart"],False,False)
	observer = Observer()
	observer.schedule(eventWatcher,uploadDir,recursive=False)

	#Begin watch
	print "starting"
	observer.start()

	#Watch the folder continuously 
	try:
		while True:
			time.sleep(1)
	#Unless there's a keyboard interrupt
	except KeyboardInterrupt:
		print "stopping"
		observer.stop()
		print "joining"
		observer.join()
