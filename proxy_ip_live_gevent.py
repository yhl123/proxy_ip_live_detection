# -*- coding: utf-8 -*-

import time
import gevent
from gevent import monkey;monkey.patch_all()
import requests
from bs4 import BeautifulSoup

proxy_ip_list = []


def look_proxy_ip_live(proxy_ip):
    count = 0
    url = 'http://ip.seofangfa.com/checkproxy/'
    while count <= 10:
        try:
            res = requests.get(url=url, proxies={'http': '%s' % (proxy_ip)}, timeout=15)
            ip = str(proxy_ip).rsplit(':')[0]
            if ip in res.text:
                proxy_ip_list.append(proxy_ip)
                print('%s存活' % proxy_ip)
                break
        except Exception as e:
            print('%s重新检测中第%s次' % (proxy_ip, count))
            count += 1


def get_proxy_ip(count=1):
    res = requests.get('http://58.87.118.83:4562/get_proxy_ip/%s' % str(count))
    obj = BeautifulSoup(res.content, 'html.parser')
    return [proxy_ip.text for proxy_ip in obj.find_all('td') if proxy_ip.text != 'ip']


if __name__ == '__main__':
    start_time = time.time()
    for proxy_ip in get_proxy_ip(count=200):
        res = gevent.spawn(look_proxy_ip_live, proxy_ip)
    res.join()
    end_time = time.time()
    print(end_time - start_time)
    print(proxy_ip_list)
