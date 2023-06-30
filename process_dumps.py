import xml.etree.ElementTree as ExtraTerrestrial
import requests
import time
import os

# Get inputs
resolution = input('Enter GA resolution ID (eg 654 for GA #654): ')
fname = input('Enter file name (exclude extension): ')
user_name = input('Enter your nation name: ')

# Get resolution passage date
timestamp = eval(ExtraTerrestrial.fromstring(requests.get('https://www.nationstates.net/cgi-bin/api.cgi?wa=1&id=' + resolution + '&q=resolution', headers={'User-Agent':'Resolution stat effect gathering script created by the Ice States and used by ' + user_name}).content).findall('RESOLUTION/IMPLEMENTED')[0].text)
time.sleep(6.5)

# Get data collected from dump
f = open('dumps/' + resolution + '.txt', 'r')
nats = f.read().split(',')
f.close()

# Create stats folder if it somehow does not exist
if not os.path.exists('./stats'):
	os.makedirs('./stats')

# Initiate stats CSV file
print('Initiating data file')
if not os.path.exists('stats/' + fname + '.csv'):
	f = open('stats/' + fname + '.csv', 'w')
	f.write('Nation,s0,f0,s1,f1,s2,f2,s4,f4,s5,f5,s6,f6,s7,f7,s8,f8,s9,f9,s10,f10,s11,f11,s12,f12,s13,f13,s14,f14,s15,f15,s16,f16,s17,f17,s18,f18,s19,f19,s20,f20,s21,f21,s22,f22,s23,f23,s24,f24,s25,f25,s26,f26,s27,f27,s28,f28,s29,f29,s30,f30,s31,f31,s32,f32,s33,f33,s34,f34,s35,f35,s36,f36,s37,f37,s38,f38,s39,f39,s40,f40,s41,f41,s42,f42,s43,f43,s44,f44,s45,f45,s46,f46,s47,f47,s48,f48,s49,f49,s50,f50,s51,f51,s52,f52,s53,f53,s54,f54,s55,f55,s56,f56,s57,f57,s58,f58,s59,f59,s60,f60,s61,f61,s62,f62,s63,f63,s64,f64,s67,f67,s68,f68,s69,f69,s70,f70,s71,f71,s72,f72,s73,f73,s74,f74,s75,f75,s77,f77,s78,f78,s79,f79,s85,f85,s87,f87,s88,f88')
	f.close()
saved_dumps = []

original_time = time.time_ns() - 650000000
text = '\n'

# Loop through stats on nation
for nation in nats:
	response = requests.get('https://www.nationstates.net/cgi-bin/api.cgi?nation=' + nation + ';q=census;scale=0+1+2+4+5+6+7+8+9+10+11+12+13+14+15+16+17+18+19+20+21+22+23+24+25+26+27+28+29+30+31+32+33+34+35+36+37+38+39+40+41+42+43+44+45+46+47+48+49+50+51+52+53+54+55+56+57+58+59+60+61+62+63+64+67+68+69+70+71+72+73+74+75+77+78+79+85+87+88;mode=history;from=' + str(timestamp - 172800) + '&to=' + str(timestamp), headers={'User-Agent':'WA stat effects analysis script created by the Ice States and used by ' + user_name})
	if response.status_code == 404 or len(nation) < 1:
		print ('Nation ' + nation + ' does not exist; stats unreachable.')
	else:
		try:
			text += nation
			stats = ExtraTerrestrial.fromstring(response.content)
			for stat in stats.findall('CENSUS/SCALE'):
				text += ',' + stat.findall('POINT/SCORE')[0].text + ',' + stat.findall('POINT/SCORE')[1].text
			text += '\n'
			print ('Processed stats of ' + nation)
		except:
			print ('Failed to process stats of ' + nation)
	
	# Rate limit requests to API
	if time.time_ns() < original_time + 620000000:
		time.sleep((original_time + 620000000 - time.time_ns())/1000000000)
	original_time = time.time_ns()

# Save data
print ('Saving data')
f = open('stats/' + fname + '.csv', 'a')
f.write(text)
f.close()