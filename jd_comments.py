import os
import re
import csv
import random
from datetime import datetime
import requests


log = open('a.log', 'a')
url = 'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98&productId={0}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'

filename = os.path.dirname(os.path.realpath(__file__))+'/useragents.csv'
user_agent_csv = open(filename, 'r')
reader = csv.reader(user_agent_csv)
user_agent_list = [row for row in reader]

def random_ua():
    return random.choice(user_agent_list)[0]

def fetch(sku):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'Referer': f'https://item.jd.com/{sku}.html',
        'User-Agent': random_ua()
    }
    r = requests.get(url.format(sku), headers=header).text
    g = re.match('.*"commentCount":(\d+).*', r)
    if g and g.groups():
        count = g[1]
        log.write(f'{sku}:{count}\n')
        #print(sku, count)
        return (sku, count)
    else:
        log.write(f'{sku}:None\n')
        raise

def main():
    skus = ['12487535', '12487831', '12487853']
    log.write(f'starts at: {datetime.now()}\n')
    print(f'starts at: {datetime.now()}')
    result = []
    for s in skus:
        try:
            result.append(fetch(s))
        except:
            print(error, s)
            log.write(f'error at: {datetime.now()}\n')
            return
    print(f'ends at: {datetime.now()}')
    log.write(f'ends at: {datetime.now()}\n')


if __name__ == '__main__':
    main()
