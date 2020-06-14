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

## Output
Once running, the output will indicate `[+]` when an article was added and `[^]` when an article was updated.

The format is:
```
[+/^] [Date last updated] Headline
URL to article
```

Example:
```
[+] [2020-06-14T05:19+1000] This is what it's like inside Seattle's 'autonomous zone'
https://www.abc.net.au/news/2020-06-14/this-is-what-its-like-inside-seattles-autonomous-zone/12350342

[+] [2020-06-14T10:19+1000] How portmanteaus are helping us through the coronavirus pandemic
https://www.abc.net.au/news/2020-06-14/miley-cyrus-coronavirus-covid19-cockney-rhyming-slang/12324930

[+] [2020-06-12T18:09+1000] So, a test has shown you're unconsciously biased. Does that mean you're racist?
https://www.abc.net.au/news/2020-06-14/implicit-association-test-indigenous-australia-negative-bias/12344930

[+] [2020-06-14T15:28+1000] Qld's Chief Health officer stands firm despite two coronavirus cases arising after isolation
https://www.abc.net.au/news/2020-06-14/coronavirus-queensland-chief-health-officer-defends-quarantine/12350746

[^] [2020-06-14T15:40+1000] Atlanta police officer sacked as protesters set fire to restaurant where black man was killed
https://www.abc.net.au/news/2020-06-14/police-officer-fired-after-shooting-dead-man-in-atlanta/12353338

[+] [2020-06-14T16:01+1000] Big crowds relish return of Super Rugby in New Zealand without restrictions
https://www.abc.net.au/news/2020-06-14/new-zealand-hosts-big-crowds-as-super-rugby-aotearoa-returns/12353918

[^] [2020-06-14T16:09+1000] Qld's Chief Health officer stands firm despite two coronavirus cases arising after isolation
https://www.abc.net.au/news/2020-06-14/coronavirus-queensland-chief-health-officer-defends-quarantine/12350746

[+] [2020-06-14T16:16+1000] Australian sentenced to death in China for drug trafficking honest to a fault, friends say
https://www.abc.net.au/news/2020-06-14/australian-sentenced-to-death-china-karm-gilespie-trafficking/12354002

[^] [2020-06-14T16:24+1000] Atlanta police officer sacked as protesters set fire to restaurant where black man was killed
https://www.abc.net.au/news/2020-06-14/police-officer-fired-after-shooting-dead-man-in-atlanta/12353338

[^] [2020-06-14T16:33+1000] Atlanta police officer sacked as protesters set fire to restaurant where black man was killed
https://www.abc.net.au/news/2020-06-14/police-officer-fired-after-shooting-dead-man-in-atlanta/12353338

[+] [2020-06-14T17:19+1000] Fuel tanker explodes and launches into air, killing 18
https://www.abc.net.au/news/2020-06-14/fuel-truck-flies-into-air-after-exploding-in-china/12354048

[^] [2020-06-14T17:43+1000] Australian sentenced to death in China for drug trafficking honest to a fault, friends say
https://www.abc.net.au/news/2020-06-14/australian-sentenced-to-death-china-karm-gilespie-trafficking/12354002

[^] [2020-06-14T17:58+1000] Atlanta police officer sacked as protesters set fire to restaurant where black man was killed
https://www.abc.net.au/news/2020-06-14/police-officer-fired-after-shooting-dead-man-in-atlanta/12353338
```

# To improve on
- Could also scrape each article's url for the main body and store it in the db column: article.content
- Utilize a library like `difflib` to find the difference in the article content when it's updated
- DB currently stores ABC's articles in its own table. The `abc_article` table can be a generic table for all articles but then that means each site's article would need to match the schema
- A more flexible approach may be to simply store a json array of articles in Postgres (using JSONB) or a key value store like Redis. The schema of the JSON can vary depending on each site.
- Monitoring website changes really only requires the last snapshot to compare to so we could just store the last snapshot as a single row containing an array of articles
- Currently each article comparison takes 1 DB call. Could just fetch all the previous articles in one go and use python `sets` to calculate the difference to shift compute away from the DB onto the worker(s)
