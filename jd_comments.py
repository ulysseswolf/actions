import os
import re
import csv
import random
from datetime import datetime
import logging
import requests


logging.basicConfig(filename='c.log', level=logging.INFO, filemode='a', format='%(message)s')
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
        logging.info(f'{sku}:{count}')
    else:
        logging.info(f'{sku}:None')
        raise

def main():
    skus = ['12487535', '12487831', '12487853']
    logging.info(f'starts at: {datetime.now()}')
    for s in skus:
        try:
            fetch(s)
        except:
            logging.info(f'error at: {datetime.now()}')
            return
    logging.info(f'ends at: {datetime.now()}')


if __name__ == '__main__':
    main()
