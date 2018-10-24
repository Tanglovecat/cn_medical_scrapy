#!encoding=utf-8
import pandas as pd
import re
import os
import urllib
import requests
import json
import time
from bs4 import BeautifulSoup

def get_context(url):
    try:
        response = urllib.urlopen(url)
    except:
        time.sleep(1)
        response = urllib.urlopen(url)
    return response.read()

base_url = 'http://bio.nifdc.org.cn/pqf/'
url = 'http://bio.nifdc.org.cn/pqf/search.do?formAction=pqfGs'
web_context = get_context(url)
A = BeautifulSoup(web_context)
B = A.select('tr td table tr td')
val_ls = []
for i, tp in enumerate(B):
    if u'历史更多'.encode('utf8') in str(B[i].select('a')[0]):
        url = re.findall(r'(?<=href=\").+?(?=\")', str(B[i].select('a')[0]))[0]
        url = base_url + re.sub(r'&amp;', r'&', url)
        name = re.findall(r'(?<=strong\>).+?(?=</strong>)',str(B[i].select('strong')[0]))[0]
        val = {'url':url, 'rd_name':name}
        val_ls.append(val)
        print name,url
df0 = pd.DataFrame(val_ls[1:])
df0['web_context'] = df0['url'].apply(lambda url: get_context(url))
df0['a'] = df0['web_context'].apply(lambda x:BeautifulSoup(x)).apply(lambda x: x.select('a'))

df = df0['a'].apply(lambda x:pd.Series(x)).stack().reset_index().rename(columns = {0:'a_content'})
df['xls_url'] = df['a_content'].apply(lambda x: re.findall(r'(?<=href=\").+?(?=\")', str(x))[0])
df['xls_url'] = df['xls_url'].apply(lambda x: base_url + re.sub('&amp;', '&', x))
df['xls_name'] = df['a_content'].apply(lambda x: re.findall(r'(?<=\">).+?(?=\<)', str(x))[0])
df = df.merge(df0[['rd_name', 'url']].reset_index(), left_on ='level_0', right_on= 'index')
df = df[['rd_name', 'url', 'xls_url', 'xls_name', 'level_1', 'a_content']]
df.to_csv('download_info.csv', encoding='utf8')
