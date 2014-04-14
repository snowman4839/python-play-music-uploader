#!/usr/bin/python
##################
from gmusicapi import Musicmanager
from os.path import expanduser

oauthPath = expanduser("~") + "/.oauthfile"

print("storing the oauthPath in " + oauthPath)
manager = Musicmanager()
manager.perform_oauth(storage_filepath = oauthPath)
