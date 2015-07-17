import urllib.request
import json
import datetime
import time
import csv
import socket
socket.setdefaulttimeout(30)

results = []
base_url = ""

fields = [
	'permalink', 'url', 'created_utc',
	'score', 'gilded', 'subreddit',
	'author',
]

threadfile = open('threads.csv', 'w')
threads = csv.writer(threadfile)

print(','.join(fields))
 
def get_next_batch(after=''):
	global results
	response = urllib.request.urlopen(base_url+"&after={}".format(after)).read();
	data  = json.loads(response.decode())
	hits  = data['data']['children']
	after = data['data']['after']
	for hit in hits:
		hit = hit['data']
		stamp = datetime.datetime.utcfromtimestamp(hit['created_utc']).timetuple()
		hit['created_utc'] = time.strftime('%Y-%m-%d', stamp)
		row = {}
		for k in fields:
			row[k] = hit[k]
		results = ""
		for r in row:
			results = results + str(row[r]) + " "
		threads.writerow(results.split())
	get_next_batch(after)
	sleep(10000)
 
subreddits = csv.reader(open("subreddits.csv"))
for row in subreddits:
	base_url = "http://www.reddit.com"+ row[0] +".json?"
	print("Subreddit " + row[0])
	try:
		get_next_batch('t5_38lwr')
		sleep(10000)
	except:
		threadfile.close()
		raise
			
