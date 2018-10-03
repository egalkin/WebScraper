hh_settings = {
    "mappings": {
        "vacancies": {
            "_parent": {
                "type": "url"
            },
            "properties": {
                'vacancy_name': {
                    'type': 'text'
                },
                'employer': {
                    'type': 'text'
                },
                'location': {
                    'type': 'text'
                },
                'salary': {
                    'type': 'text'
                }
            }
        },
        "url": {
            "properties": {
                "path": {
                    "type": "text",
                }
            }
        }
    }
}

log_settings = {
    "mappings": {
        "changes": {
            "properties": {
                "url": {
                    "type": "text"
                },
                "hash": {
                    "type": "text"
                },
                "last_mod": {
                    "type": "text"
                },
                "num_of_responses": {
                    "type": "integer"
                }
            }
        }
    }
}
