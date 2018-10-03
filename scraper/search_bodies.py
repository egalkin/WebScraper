def get_changes_query(url):
    body = {
        "query": {
            "match": {
                "_id": {
                    "query": url,
                    "type": "phrase"
                }
            }
        }
    }
    return body


def get_all_records_by_parent_id(url):
    body = {
        "query": {
            "has_parent": {
                "type": "url",
                "query": {
                    "match": {
                        "_id": url
                    }
                }
            }
        }
    }
    return body
