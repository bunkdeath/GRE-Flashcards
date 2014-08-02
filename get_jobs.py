#!/usr/bin/python

import os
import re
import sys

plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.bunkdeath.greflashcards</string>

  <key>ProgramArguments</key>
  <array>
    <string>%s</string>
  </array>

  <key>StartInterval</key>
  <integer>%s</integer>

  <key>RunAtLoad</key>
  <true/>

  <key>StandardErrorPath</key>
  <string>%s/com.bunkdeath.greflashcards.err</string>

  <key>StandardOutPath</key>
  <string>%s/com.bunkdeath.greflashcards.out</string>
</dict>
</plist>"""

def correct_path(path):
	script_file = open('gre_flashcards.py')
	content = script_file.read()
	script_file.close()
	regex = r'path = ".*"'
	content = re.sub(regex, 'path = "%s"' % path, content)
	script_file = open('gre_flashcards.py', "w")
	script_file.write(content)
	script_file.close()

def help():
	print "./get_jobs.py -h <hour> -m <minute>"

def get_plist(path, hour, minute):
	script_file = os.path.join(path, 'gre_flashcards.py')
	if hour or minute:
		time = int(minute)*60 + int(hour)*60*60
		plist_content = plist % (script_file, time, path, path)
		plist_file = open("com.bunkdeath.greflashcards.plist", "w")
		plist_file.write(plist_content)
		plist_file.close()
	else:
		help()

def get_time():
	if len(sys.argv) < 2:
		help()
		sys.exit(0)

	hour = 0
	minute = 0
	first = True
	option = ''
	for arg in sys.argv:
		if first:
			first = False
			continue
		if not option:
			option = arg
		else:
			if option == "-h":
				hour = arg
			elif option == "-m":
				minute = arg
			else:
				help()

			option = ''

	return hour, minute

if __name__ == "__main__":
	path = os.getcwd()
	correct_path(path)
	
	hour, minute = get_time()
	get_plist(path, hour, minute)
