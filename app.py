import os
import time

from news_scraper.db import Database
from news_scraper.sites import abc

db = Database(
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    port=os.environ['POSTGRES_PORT'],
    database=os.environ['POSTGRES_DATABASE'],
    host=os.environ['POSTGRES_HOST'],
)

while True:
    abc.start_scrape(db)
    time.sleep(int(os.environ['SCRAPE_INTERVAL']))
