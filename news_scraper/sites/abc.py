from datetime import datetime, timezone
import os

from bs4 import BeautifulSoup
import psycopg2
import requests


def get_articles():
    date_scraped = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    res = requests.get('https://www.abc.net.au/news/')
    soup = BeautifulSoup(res.text, 'html.parser')
    module_body = soup.find(class_='section module-body')
    articles = module_body.find_all('li')
    return [
        {
            'headline': article.find('a').text,
            'date_first_published': article.get('data-first-published'),
            'date_last_published': article.get('data-last-published'),
            'summary': article.find('p').text,
            'type': 'main',
            'date_scraped': date_scraped
        } for article in articles
    ]


def get_last_date_scraped(db):
    result = db.query('SELECT date_scraped FROM abc_article ORDER BY date_scraped DESC LIMIT 1')
    return None if len(result) == 0 else result[0][0].isoformat()


def insert_article(db, article):
    db.execute("""
        INSERT INTO abc_article (headline, summary, date_first_published, date_last_published, type, date_scraped)
        VALUES (%(headline)s, %(summary)s, %(date_first_published)s, %(date_last_published)s, %(type)s, %(date_scraped)s)""",
    article)
    print(f"[+] [{article['date_last_published']}] {article['headline']}")


def update_article(db, article_id, article):
    db.execute("""
        UPDATE
            abc_article
        SET
            headline = %(headline)s,
            summary = %(summary)s,
            date_last_published =%(date_last_published)s,
            date_scraped = %(date_scraped)s
        WHERE
            id = %(article_id)s
    """, {
        'article_id': article_id,
        **article,
    })
    print(f"[^] [{article['date_last_published']}] {article['headline']}")


def update_article_scrape_date(db, article_id, date_scraped):
    db.execute("""
        UPDATE
            abc_article
        SET
            date_scraped = %(date_scraped)s
        WHERE
            id = %(article_id)s
    """, {
        'article_id': article_id,
        'date_scraped': date_scraped,
    })


def find_prev_article(db, article, date_scraped):
    result = db.query("""
        SELECT
            id,
            date_last_published
        FROM
            abc_article
        WHERE
            headline = %(headline)s
            AND date_first_published = %(date_first_published)s
            AND summary = %(summary)s
        LIMIT 1
    """,
    {
        'headline': article['headline'],
        'date_first_published': article['date_first_published'],
        'summary': article['summary'],
        'date_scraped': date_scraped,
    })
    return {'id': result[0][0], 'date_last_published': result[0][1]} if len(result) else None


def start_scrape(db):
    articles = get_articles()
    last_date_scraped = get_last_date_scraped(db)

    # If there was no previous scrape, insert every article
    if last_date_scraped is None:
        for article in articles:
            insert_article(db, article)
        return

    for article in articles:
        prev_article = find_prev_article(db, article, last_date_scraped)
        if prev_article is None:
            insert_article(db, article)
        elif (datetime.strptime(article['date_last_published'], '%Y-%m-%dT%H:%M%z') - prev_article['date_last_published']).seconds:
            update_article(db, prev_article['id'], article)
        else:
            update_article_scrape_date(db, prev_article['id'], article['date_scraped'])


# with open('news.html', encoding='utf-8') as f:
#     html = f.read()
