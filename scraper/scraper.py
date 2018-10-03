import hashlib
import sys

import requests
from elasticsearch import Elasticsearch

from es_settings import hh_settings, log_settings
from put_bodies import create_changes_log
from scrapping_utils import parse_html, get_pages
from search_utils import create_index, store_vacancy_record, store_url_record, get_changes, store_change_record


def main():
    argv = sys.argv
    es = Elasticsearch()
    if len(argv) != 2:
        print('usage: <url>')
    else:
        url = argv[1]
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
        global_hash += 'egor'
        hash_object = hashlib.md5(global_hash.encode())
        changes = get_changes(es, 'log', url)
        record = create_changes_log(url, hash_object.hexdigest(), len(response) + 25)
        if len(changes) == 0:
            store_change_record(es, 'log', record, url)
            record['status'] = 'create'
            requests.post('http://localhost:5000/api/v1/collect', data=record)
        else:
            cur_record_hash = changes[0]['_source']['hash']
            if hash_object.hexdigest() != cur_record_hash:
                store_change_record(es, 'log', record, url)
                record['status'] = 'update'
                requests.post('http://localhost:5000/api/v1/collect', data=record)


if __name__ == "__main__":
    main()
