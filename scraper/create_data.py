from scraper import scrap
import random
import string


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


url = 'https://spb.hh.ru/search/vacancy?text=Scala&only_with_salary=false&enable_snippets=true&clusters=true&area=2'

for i in range(0, 20):
    scrap(url, random_word(5), random.randint(-50, 50))
