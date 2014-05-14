Google Play Music Uploader
==========================
This is a play music uploader based on the gmusicapi by Simon Weber (https://github.com/simon-weber/Unofficial-Google-Music-API)
and Watchdog python library (https://pypi.python.org/pypi/watchdog)

Instructions
==========================
1) Install gmusicapi, eyeD3, libav-tools, and watchdog python library plus all of required their required dependencies  
2) Run firstRun.py. This will create the oauth file for the music manager by registering it as an
    uploader device with google. It will be stored in ~/.oauthfile  
   It is probably best to do this over SSH if this is a headless server as it will give you a long
    web address to go to which would be easiest if copied.  
3) Edit googleupload.py and change the paths at the beginning of the file to your oauth file, upload folder, and storage
    directory. Also add your google username and password to allow for artwork extraction and upload via eyeD3. This is
    a fix while gmusicapi doesn't seem to upload artwork embeded in the file
4) "chmod 700 googleupload.py" to make sure it is executable. Don't chmod 755 because this file will include your google 
    username and password.  
5) Profit! (run it as a background process "./googleupload.py &" and it will watch your folder and upload accordingly)  

Folders
==========================
googleupload.py folder path variables  
oauthFile is the oauth file created when running the firstRun.py script  
uploadDir is the folder that is watched to upload to the google account  
storageDir is the folder that the uploaded file is moved to upon successful upload  

Notes
==========================
You can add "/PATH/TO/googleupload.py &" in rc.local to run as a background process to automatically on startup
