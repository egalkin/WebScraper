from datetime import datetime


def create_changes_log(url: str, hash: str, num_of_responses: int) -> dict:
    log = {
        'url': url,
        'hash': hash,
        'last_mod': datetime.now(),
        'num_of_responses': num_of_responses
    }
    return log
