import os
import csv
import requests
import json

import numpy as np

from bs4 import BeautifulSoup
from multiprocessing import Pool

GRABBER_ROOT = './data'
CORES_NUMBER = 20
TRIP_ADVISOR_URL_TEMPLATE = 'https://www.tripadvisor.com{}'


def parse_ratings_and_reviews(node, result):
    rating_block = node.find('div').findAll('div', recursive=False)
    if len(rating_block) < 3:
        return result
    rating_block = rating_block[2].findAll('div', recursive=False)
    if len(rating_block) < 2:
        return

    ratings = rating_block[1].findAll('div')
    for rating in ratings:
        spans = rating.findAll('span', recursive=False)
        title = spans[1].text.lower()
        value = spans[2].find('span').attrs['class'][1].split('_')[1]
        result[title] = int(value)

def parse_tr_reviews_block(node, result):
    if node is None:
        return

    tr_rating_block = node.find('div', {'data-param': 'trating'})
    if tr_rating_block is None:
        return

    ratings = tr_rating_block.find_all('div', recursive=False)
    if ratings is None:
        return

    tr_ratings_num = 0
    for r in ratings:
        title = 'tr_rating_' + r['data-value']
        number_text = r.find('span', {'class': 'row_num'}).text
        number_text = number_text.replace(',', '').replace(' ', '')
        number = int(number_text)
        result[title] = number
        tr_ratings_num += number

    result['tr_ratings'] = tr_ratings_num

def collect_page_data(html, result):
    soup = BeautifulSoup(html, features="lxml")
    overview_tabs = soup.find('div', {'data-tab': 'TABS_OVERVIEW'})
    if overview_tabs is None:
        return

    overview_columns = overview_tabs.findAll('div', {'class': 'ui_column'})
    parse_ratings_and_reviews(overview_columns[0], result)


    review_block = soup.find("div", {"id": "REVIEWS"})
    parse_tr_reviews_block(review_block, result)



def grab_pages(records):
    for record in records:
        ta_url = TRIP_ADVISOR_URL_TEMPLATE.format(record["ta_url"])
        print(ta_url)
        r = requests.get(ta_url, stream=True)
        collect_page_data(r.text, record)
    return records


def parallelize_processing(records):
    pool = Pool(CORES_NUMBER)
    splitted_recs = np.array_split(records, CORES_NUMBER)
    grabbed_data = pool.map(grab_pages, splitted_recs)
    pool.close()
    pool.join()
    return np.concatenate(grabbed_data)


def read_records(filename):
    records = list()
    with open(filename) as csvfile:
        filereader = csv.reader(csvfile)
        for row in filereader:
            row_obj = {}
            row_obj['id'] = row[0]
            row_obj['ta_id'] = row[1]
            row_obj['ta_url'] = row[2]
            records.append(row_obj)
    return records


def process_file(filename):
    if not filename.endswith('.csv'):
        return

    print(filename)

    data_file_name = '{}_data.json'.format(
        filename.split('/')[-1].split('.')[0])
    data_file_path = '{}/{}'.format(GRABBER_ROOT, data_file_name)

    records = read_records(filename)
    records_data = parallelize_processing(records)

    with open(data_file_path, "w") as write_file:
        json.dump(records_data.tolist(), write_file)


if __name__ == '__main__':
    for dirname, _, filenames in os.walk('{}/{}'.format(GRABBER_ROOT, 'mt')):
        for filename in filenames:
            process_file(os.path.join(dirname, filename))



