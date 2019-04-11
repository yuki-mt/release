"""
TARGET_URL に対して負荷テストを行う。
CONCURRENT_NUMで並行度を指定
Througput, Latency, Latencyの分布などが出力される
"""

import time
import random
import numpy as np
import urllib.request
import urllib
from urllib.error import HTTPError
import socket
from concurrent.futures import ThreadPoolExecutor
from urllib3 import PoolManager

CONCURRENT_NUM = 2
TARGET_URL = "http:/hoge.com"

HEADERS = {
    'Connection': 'Close',
}
manager = PoolManager(CONCURRENT_NUM, retries=False)


def request(query):
    param = urllib.parse.urlencode({"query": query})
    timeout = False
    try:
        begin = time.time()
        resp = manager.request('GET', TARGET_URL + '?' + param, headers=HEADERS)
        resp.close()
        end = time.time()
        status = 200
    except HTTPError as e:
        end = time.time()
        status = e.code
    except socket.timeout:
        end = time.time()
        status = 0
        timeout = True
    except Exception:
        end = time.time()
        status = 400
        timeout = True

    return (end - begin, status, timeout)


executor = ThreadPoolExecutor(max_workers=CONCURRENT_NUM)
futures = []
cnt = 0
queries = []
for line in open("data/queries.txt"):
    queries.append(line.rstrip("\n"))

random.shuffle(queries)
all_begin = time.time()
for query in queries:
    future = executor.submit(request, query)
    futures.append(future)

num_timeout = 0
statuses = {}  # type: dict
_elapses = []
for future in futures:
    (elapsed, status, timeout) = future.result()
    _elapses.append(elapsed)
    statuses[status] = statuses.get(status, 0) + 1
    if timeout:
        num_timeout += 1
all_end = time.time()
query_num = len(queries)


elapses = np.array(_elapses)
elapses = elapses * 1000
print("Overall throuputs: {0:>3} query/sec".format(round(query_num / (all_end - all_begin)), 3))
print("Number of requests: {0}".format(len(elapses)))
for status in statuses:
    print("Status code {0} requests: {1}".format(status, statuses[status]))
print("Timeout requests: " + str(num_timeout))
print("Average latency (msec): " + str(round(np.sum(elapses) / len(elapses), 3)))
for i in [50, 66, 75, 80, 90, 95, 98, 99, 100]:
    latency = round(np.percentile(elapses, i), 3)
    print("{0:>3} th percentile latency (msec): {}".format(i, latency))

for i in range(11):
    if i == 0:
        counts = len(elapses[np.logical_and(elapses >= 0, elapses <= 10)])
        print("  0 -  10: {0}".format(counts))
    elif i == 10:
        counts = len(elapses[elapses > 100])
        print("101 -    : {0}".format(counts))
    else:
        counts = len(elapses[np.logical_and(elapses > (i * 10), elapses <= (i + 1) * 10)])
        print("{0:>3} - {1:>3}: {2}".format(i * 10, (i + 1) * 10, counts))
