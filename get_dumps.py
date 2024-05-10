# Module imports
import xml.etree.ElementTree as ExtraTerrestrial
import datetime
import requests
import time
import gzip
import os

tries = 0
cont = False

# Get dumps already fetched
try:
	f = open('dumps/dumps.txt', 'r')
	saved_dumps = f.read().split('\n')
	f.close()
except:
	# Create dumps.txt if it somehow does not exist
	if not os.path.exists('./dumps'):
		os.makedirs('./dumps')
	f = open('dumps/dumps.txt', 'x')
	f.close()
	saved_dumps = []

# Find what API dumps to get
resolution = input('Enter GA resolution ID (eg 654 for GA #654): ')
user_name = input('Enter your nation name: ')
timestamp = eval(ExtraTerrestrial.fromstring(requests.get('https://www.nationstates.net/cgi-bin/api.cgi?wa=1&id=' + resolution + '&q=resolution', headers={'User-Agent':'Daily dump download script created by the Ice States and used by ' + user_name}).content).findall('RESOLUTION/IMPLEMENTED')[0].text) - 28800
time.sleep(6.5)
date_raw = [datetime.datetime.utcfromtimestamp(timestamp).year, datetime.datetime.utcfromtimestamp(timestamp).month, datetime.datetime.utcfromtimestamp(timestamp).day]

# Check if fetching dump is needed
dump_needed = False
try:
	saved_dumps.index(str(date_raw[0]) + '-' + str(date_raw[1]).zfill(2) + '-' + str(date_raw[2]).zfill(2))
except:
	dump_needed = True

while dump_needed:
	# Dump needed; fetch dump
	try:
		print('Fetching dump from ' + str(date_raw[0]) + '-' + str(date_raw[1]).zfill(2) + '-' + str(date_raw[2]).zfill(2))
		dump = ExtraTerrestrial.fromstring(gzip.decompress(requests.get('https://www.nationstates.net/archive/nations/' + str(date_raw[0]) + '-' + str(date_raw[1]).zfill(2) + '-' + str(date_raw[2]).zfill(2) + '-nations-xml.gz', headers={'User-Agent':'Daily dump download script created by the Ice States and used by ' + user_name}).content))
		break
	except:
		print('Failed to fetch dump')
		tries += 1
		if tries == 3:
			# Switch to next dump after three consecutive failures
			timestamp += 86400
			ddate_raw = [datetime.datetime.utcfromtimestamp(timestamp).year, datetime.datetime.utcfromtimestamp(timestamp).month, datetime.datetime.utcfromtimestamp(timestamp).day]
		if tries == 5:
			# After five consecutive failures stop trying
			raise # Failed to fetch dump after five consecutive attempts
	# Rate limit requests
	time.sleep(6.5)

if dump_needed:
	# Process and save the dumps
	print('Locating nations in dump')
	for nation in dump:
		if (nation.findall('UNSTATUS')[0].text == 'WA Member' or nation.findall('UNSTATUS')[0].text == 'WA Delegate') and nation.findall('ISSUES_ANSWERED')[0].text == '0' and eval(nation.findall('FIRSTLOGIN')[0].text) < timestamp:
			cont = False
			try:
				f = open('dumps/' + str(resolution) + '.txt', 'a')
				f.write(nation.findall('NAME')[0].text + ',')
				f.close()
			except:
				cont = True
					
			if cont:
				try:
					f = open('dumps/' + str(resolution) + '.txt', 'a')
					f.write(nation.findall('NAME')[0].text + ',')
					f.close()	
				except:
					pass
