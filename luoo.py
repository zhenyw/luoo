#!/usr/bin/env python2

from lxml import html
import urllib
import requests
import os
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("vol", help="Luoo vol number")
parser.add_argument("--info", help="Read Luoo volumn info instead of downloading", action="store_true")
args = parser.parse_args()

# set proxy if required
proxy = os.environ.get('http_proxy')
if proxy != None:
    proxies = { 'http': proxy }
else:
    proxies = {}

main_url="http://luoo.org/music.php?id="
issue_no=args.vol
target_url = main_url + issue_no

h = urllib.urlopen(target_url, proxies=proxies)
tree = html.parse(h)

vol = tree.xpath('//div[@class="musiclist"]//span[@class="vol-number rounded"]/text()')
print vol[0]

title = tree.xpath('//div[@class="musiclist"]//span[@class="vol-title"]/text()')
print title[0]

content = tree.xpath('//div[@class="vol-desc"]/text()')
for c in content:
    print c

mlist = tree.xpath('//li/a[@class="play"]/text()')
authorlist = tree.xpath('//li/text()')
#print mlist
#print authorlist
dlist = tree.xpath('//li/a[@class="download"]/@href')
ddlist=[]
for d in dlist:
    ddlist.append(d[5:])
#print ddlist

if args.info:
    sys.exit(0)

os.mkdir(issue_no)
os.chdir(issue_no)

with open("content", 'wb') as fd:
    fd.write(vol[0] + ".")
    fd.write(title[0].encode('UTF-8'))
    for c in content:
        fd.write(c.encode('UTF-8') + '\n')
    for m in range(len(mlist)):
        fd.write(mlist[m].encode('UTF-8'))
        fd.write('\t' + authorlist[m].encode('UTF-8') + '\n')

chunk_size=512
for n in range(len(ddlist)):
    print "downloading " + mlist[n]
    r = requests.get(ddlist[n], proxies=proxies)
    name=mlist[n] + ddlist[n][-4:]
    with open(name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print "save " + name

print "Done."
