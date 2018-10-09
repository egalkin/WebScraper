#!/bin/bash

virtualenv -p python3 ./scraper/.venv
source ./scraper/.venv/bin/activate

pip3 install -r ./scraper/requirements.txt

