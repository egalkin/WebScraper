import hashlib

from search_bodies import get_changes_query


def create_index(es_object, index_name, settings):
    created = False
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            created = True
    except:
        print('Failed')
    finally:
        return created


def store_url_record(es, index_name, record, record_id):
    es.index(index=index_name, doc_type='url', body=record, id=record_id)


def store_vacancy_record(es, index_name, record, parent_id):
    hash_string = ''
    for k, v in record.items():
        hash_string += "{}{}".format(k, v)
    hash_string += parent_id
    hash_object = hashlib.md5(hash_string.encode())
    es.index(index=index_name, doc_type='vacancies', id=hash_object.hexdigest(), body=record, parent=parent_id)
    return hash_string


def store_change_record(es, index_name, record, url):
    es.index(index=index_name, doc_type='changes', id=url, body=record)


def search(es_object, index_name, search_body):
    return es_object.search(index=index_name, body=search_body)


def get_changes(es_object, index_name, url):
    search_body = get_changes_query(url)
    response = es_object.search(index=index_name, body=search_body)
    return response['hits']['hits']


def check_connection(es):
    if es.ping():
        return True
    else:
        return False
