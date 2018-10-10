import hashlib
import sys

import requests
from elasticsearch import Elasticsearch

from es_settings import hh_settings, log_settings
from put_bodies import create_changes_log
from scraping_utils import parse_html, get_pages
from search_utils import create_index, store_vacancy_record, store_url_record, get_changes, store_change_record
from url_addreses import COLLECTOR_URL


def main():
    argv = sys.argv
    if len(argv) != 2:
        print('usage: <url>')
    else:
        url = argv[1]
        scrap(url)


def scrap(url: str, hash_suffix: str = '', add_to_len: int = 0) -> None:
    es = Elasticsearch()
    response = parse_html(get_pages(url))
    doc = {
        'path': url
    }

    create_index(es, 'hh', hh_settings)
    create_index(es, 'log', log_settings)
    store_url_record(es, 'hh', doc, url)

    global_hash = ''
    for r in response:
        global_hash += store_vacancy_record(es, 'hh', r, url)
    global_hash += hash_suffix
    hash_object = hashlib.md5(global_hash.encode())

    changes = get_changes(es, 'log', url)
    record = create_changes_log(url, hash_object.hexdigest(), len(response) + add_to_len)

    if len(changes) == 0:
        store_change_record(es, 'log', record, url)
        record['status'] = 'create'
        requests.post(COLLECTOR_URL, data=record)
    else:
        cur_record_hash = changes[0]['_source']['hash']
        if hash_object.hexdigest() != cur_record_hash:
            store_change_record(es, 'log', record, url)
            record['status'] = 'update'
            requests.post(COLLECTOR_URL, data=record)


if __name__ == "__main__":
    main()
