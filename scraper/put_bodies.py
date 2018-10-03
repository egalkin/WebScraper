from datetime import datetime


def create_changes_log(url, hash, num_of_responses):
    log = {
        'url': url,
        'hash': hash,
        'last_mod': datetime.now(),
        'num_of_responses': num_of_responses
    }
    return log
