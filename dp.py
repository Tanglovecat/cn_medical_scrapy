#!encoding=utf-8
import json
from gevent import monkey, lock
import gevent
import time, requests
import os, sys
import re
import pandas as pd
monkey.patch_all()
#设置线程数, 推荐10个线程
sem = lock.Semaphore(10)
l = lock.RLock()
def my_download(url, file_name):
    sem.acquire()
    try:
        r = requests.get(url, stream = True)
        with open(file_name, 'wb') as f:
            f.write(r.content)
        #os.system('wget %s -O %s -q'%(url, file_name))
    except Exception as e:
        t = time.time() - t0
        print t
        print("download error:", e)
    else:
        t = time.time() - t0
        print t
        print("success downloaded:%s"%(file_name))
    l.acquire()
    l.release()
    sem.release()
 
data = pd.read_csv('download_info.csv')
data['name'] = data['rd_name'] + '-' + data['xls_name']
names, urls = list(data['name']), list(data['xls_url'])
gls = []
t0 = time.time()
for i, url in enumerate(urls):
    file_path = 'xls/' + '{:0>3d}'.format(i) + '_' + names[i] + '.xls'
    print url, names[i]
    g = gevent.spawn(my_download, url, file_path)
    gls.append(g)
gevent.joinall(gls)
