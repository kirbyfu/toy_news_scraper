# news_scraper
A small news scraper that monitors the main articles in https://www.abc.net.au/news/ and notifies when an article was added or updated.

# Set up
Install the python dependencies
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

Set up some environment variables
```bash
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password
export POSTGRES_PORT=5432
export POSTGRES_DATABASE=postgres
export POSTGRES_HOST=localhost
# How many seconds between each scrape
export SCRAPE_INTERVAL=60
```

Run Postgres locally in a Docker container and initialize the tables
```
docker-compose up
python create_db.py
```

Start monitoring
```
python app.py
```

## Run tests
```
pytest -vv
```

## Output
Once running, the output will indicate `[+]` when an article was added and `[^]` when an article was updated.

The format is:
```
[+] [Date last updated] Headline
URL to article

[^] [Date last updated] Headline
URL to article
Diff of what changed in the article since the last scrape
```

Example:
```
[+] [2020-06-14T05:19+1000] This is what it's like inside Seattle's 'autonomous zone'
https://www.abc.net.au/news/2020-06-14/this-is-what-its-like-inside-seattles-autonomous-zone/12350342

[^] [2020-06-14T21:54+1000] Coronavirus updates: China reports highest daily total of new COVID-19 cases in two months
https://www.abc.net.au/news/2020-06-14/coronavirus-update-covid19/12353050
- This story was last updated at 8:30 pm AEST on Sunday
- .
+ This story is no longer being updated. For the latest coronavirus news and updates,
+ follow this story.
```

# To improve on
- DB currently stores ABC's articles in its own table. The `abc_article` table can be a generic table for all articles but then that means each site's article would need to match the schema
- A more flexible approach may be to simply store a json array of articles in Postgres (using JSONB) or a key value store like Redis. The schema of the JSON can vary depending on each site.
- Monitoring website changes really only requires the last snapshot to compare to so we could just store the last snapshot as a single row containing an array of articles
- Currently each article comparison takes 1 DB call. Could just fetch all the previous articles in one go and use python `sets` to calculate the difference to shift compute away from the DB onto the worker(s)
