# Exercise 2

## Install Dependencies

```
pip install streamparse psycopg2 argparse tweepy
```

## Setup Postgresql

First, config `postgresql`

```
sudo service postgresql initdb
```

Edit file `/var/lib/pgsql/data/pg_hba.conf`, add the following line:
```
local   tcount         twuser                            password
```

This allows us to use password authentication for user `twuser`. 


Create user, schema and table:

```
sudo su - postgres
psql
```

```
CREATE USER twuser WITH PASSWORD 'tweetcount';
DROP DATABASE IF EXISTS Tcount;
CREATE DATABASE Tcount;
\c tcount;
CREATE TABLE Tweetwordcount (
  word text,
  count bigint,
  PRIMARY KEY (word)
);
GRANT SELECT,INSERT,UPDATE,DELETE ON "tweetwordcount" TO twuser; 
\q
```

```
service postgresql start
```

## Run Tweets Streaming

Add tweeter api credentials to `src/spouts/tweets.py`

```
sparse run
```

## Query results


Query for a single word count:

```
python finalresults.py <word>
# eg. python finalresults.py the
```

Query for top 1000 words:

```
python finalresults.py -n 1000
```

Query for histogram:

```
python histogram.py 10 20
```


