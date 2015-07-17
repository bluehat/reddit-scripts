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
]

threads = csv.writer(open('threads.csv', 'w'))

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
		for k in hit:
			row[k] = hit[k]
		threads.writerow(",".join(str(v) for v in row.values()))
	get_next_batch(after)
	sleep(10000)
 
subreddits = csv.reader(open("subreddits.csv"))
for row in subreddits:
	base_url = "http://www.reddit.com"+ row[0] +".json?"
	try:
		get_next_batch('t5_38lwr')
		sleep(10000)
	except:
		raise
			
