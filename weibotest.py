#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io  
import sys
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

base_url = 'https://m.weibo.cn/api/container/getIndex?'
 
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/p/1005051895520105',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
 
def get_page(page):
    params = {
 #       'type': 'uid',
  #      'value': '2830678474',
        'containerid': '1076031895520105',
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(jsona):
    if jsona:
        items = jsona.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo

def write_to_file(content):
    with open('ttt33.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    for page in range(2, 11):
        jsona = get_page(page)
        results = parse_page(jsona)
        for result in results:
            print(result,len(result))
            write_to_file(result)