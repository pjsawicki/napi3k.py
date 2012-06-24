#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# reversed napi 0.16.3.1
#
# by gim,krzynio,dosiu,hash 2oo8.
# update for Python3k by Pawel Sawicki 2012.
# 
# last modified: 2012/06/24
#
# do dzialania potrzebny jest p7zip-full (tak sie nazywa paczka w debianie)
#

PASSWORD = "iBlm8NTigvru0Jr0"

E_UNSUPPORTED_VERSION	= 1
E_USAGE			= 2

import sys

if sys.version_info < (3, 0):
	print("This program is designed to run under Python 3.X.")
	print("For the original, Python 2.X version, see here: http://hacking.apcoh.com/2010/01/napi_06.html")
	sys.exit(E_UNSUPPORTED_VERSION)

import hashlib, urllib.request, os

def f(z):
	idx = [ 0xe, 0x3,  0x6, 0x8, 0x2 ]
	mul = [   2,   2,    5,   4,   3 ]
	add = [   0, 0xd, 0x10, 0xb, 0x5 ]

	b = []
	for i in range(len(idx)):
		a = add[i]
		m = mul[i]
		i = idx[i]

		t = a + int(z[i], 16)
		v = int(z[t:t+2], 16)
		b.append( ("%x" % (v*m))[-1] )

	return ''.join(b)


if(len(sys.argv) != 2):
	print("usage: %s video_file.ext" % sys.argv[0])
	sys.exit(E_USAGE)

md5 = hashlib.md5();
md5.update(open(sys.argv[1], 'r+b').read(10485760))

url = "http://napiprojekt.pl/unit_napisy/dl.php?l=PL&f=%s&t=%s&v=other&kolejka=false&nick=&pass=&napios=%s" % (md5.hexdigest(), f(md5.hexdigest()), os.name)

with urllib.request.urlopen(url) as response:
	open("napisy.7z", "w+b").write(response.read())

nazwa = sys.argv[1][:-3]+'txt'

if (os.system("/usr/bin/7z x -y -so -p%s napisy.7z 2>/dev/null > \"%s\"" % (PASSWORD, nazwa))):
        print("Subtitles file not found.")
        os.remove(nazwa)        
else:
        print("Subtitles found and downloaded.")

os.remove("napisy.7z")
