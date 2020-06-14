import os

from news_scraper.db import Database

db = Database(
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    port=os.environ['POSTGRES_PORT'],
    database=os.environ['POSTGRES_DATABASE'],
    host=os.environ['POSTGRES_HOST'],
)

db.create_table("""
    CREATE TABLE IF NOT EXISTS news_site (
        url VARCHAR(200) PRIMARY KEY,
        name VARCHAR(200),
        active BOOLEAN DEFAULT TRUE
    );
    CREATE TABLE IF NOT EXISTS abc_article (
        id SERIAL PRIMARY KEY,
        headline TEXT,
        author VARCHAR(200),
        summary TEXT,
        content TEXT,
        date_first_published TIMESTAMP WITH TIME ZONE NOT NULL,
        date_last_published TIMESTAMP WITH TIME ZONE NOT NULL,
        type VARCHAR(200),
        date_scraped TIMESTAMP WITH TIME ZONE NOT NULL
    );
""")
