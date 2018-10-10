import hashlib

from search_bodies import get_changes_query
from elasticsearch.client import Elasticsearch


def create_index(es: Elasticsearch, index_name: str, settings: dict) -> bool:
    created = False
    try:
        if not es.indices.exists(index_name):
            es.indices.create(index=index_name, ignore=400, body=settings)
            created = True
    except:
        print('Failed')
    finally:
        return created


def store_url_record(es: Elasticsearch, index_name: str, record: dict, record_id: str) -> None:
    es.index(index=index_name, doc_type='url', body=record, id=record_id)


def store_vacancy_record(es: Elasticsearch, index_name: str, record: dict, parent_id: str) -> str:
    hash_string = ''
    for k, v in record.items():
        hash_string += "{}{}".format(k, v)
    hash_string += parent_id
    hash_object = hashlib.md5(hash_string.encode())
    es.index(index=index_name, doc_type='vacancies', id=hash_object.hexdigest(), body=record, parent=parent_id)
    return hash_string


def store_change_record(es: Elasticsearch, index_name: str, record: dict, url: str) -> None:
    es.index(index=index_name, doc_type='changes', id=url, body=record)


def search(es: Elasticsearch, index_name: str, search_body: dict) -> dict:
    return es.search(index=index_name, body=search_body)


def get_changes(es: Elasticsearch, index_name: str, url: str) -> list:
    search_body = get_changes_query(url)
    response = es.search(index=index_name, body=search_body)
    return response['hits']['hits']


def check_connection(es: Elasticsearch) -> bool:
    if es.ping():
        return True
    else:
        return False
