#!/bin/bash

cd scraper

source .venv/bin/activate
source ../.env.local
pip3 install -r requirements.txt

curl -XDELETE localhost:9200/_all 

python3 create_data.py
