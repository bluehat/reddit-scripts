import urllib.request
import json
import datetime
import time
import csv
import socket
socket.setdefaulttimeout(30)

base_url = ""

fields = [
    'permalink', 'url', 'created_utc',
    'score', 'gilded', 'subreddit',
    'author',
]

threadfile = open('threads.csv', 'a')
threads = csv.writer(threadfile)

print(','.join(fields))

def get_next_batch():
    after = ''
    while after is not None:
        response = urllib.request.urlopen(base_url+"&after={}".format(after)).read();
        data  = json.loads(response.decode())
        hits  = data['data']['children']
        after = data['data']['after']
        print(after)
        for hit in hits:
            hit = hit['data']
            stamp = datetime.datetime.utcfromtimestamp(hit['created_utc']).timetuple()
            hit['created_utc'] = time.strftime('%Y-%m-%d', stamp)
            row = {}
            for k in fields:
                row[k] = hit[k]
            results = ""
            for r in sorted(row):
                results = results + str(row[r]) + " "
            threads.writerow(results.split())
        time.sleep(10)

with open('unscrapedsubreddits.csv') as fp:
    subreddits = list(csv.reader(fp))

tries = 0

while True:
    row = subreddits.pop()
    print('Subreddit: ' + row[0])
    if row[1] != 'private':
        base_url = 'http://www.reddit.com'+ row[0] +'.json?'
        try:
            get_next_batch()
            time.sleep(10)
            tries = 0
        except:
            subreddits.append(row)
            tries = tries + 1
            backoff = tries * 10
            print("Backing off sleeping for %d seconds" % backoff)
            time.sleep(backoff)
