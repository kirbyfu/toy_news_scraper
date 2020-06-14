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