# Introduction and purpose

The Redshift database has been designed for efficient access and analysis across songs, artists, users and usage of Sparkify.
Sparkify can use it to understand trends and preferences across their user base, improve their suggestion engine, as well as cater for changing server traffic using time data. 

# Design

Design consists of 5 tables, each with a unique primary key and every cell containing only single values. The star schema design - split between songs, artist, users, time (dimensions) and songplays (fact) tables reflects the categories of data collected by Sparkify making the access intuitive and logical.

### Fact Table:
**songplays** - records in log data associated with song plays.

songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables:
**users** - Sparkify users
user_id PK varchar, first_name varchar, last_name varchar, gender varchar, level varchar

**songs** - songs in the database
song_id PK varchar, title varchar, artist_id varchar, year int, duration numeric

**artists** - information about artists in the database
artist_id PK varchar, name varchar, artist_location varchar, artist_latitude numeric, artist_longitude numeric

**time** - starting time timestamp for songplays split between specific time units
start_time timestamp, hour int, day int, week int, month int, year int, weekday int

# Files

**create_tables.py** - file setting up the database, as well as fact and dimension tables
**etl.py** - main file used to read and process available data
**sql_queries.py** - file containing SQL queries for dropping and creating tables, as well as a template for data insertion
 

# How to use
Setup dwh.cfg config file containing login details to an active AWS Redshift cluster and ARN of an IAM role with S3 read access.
Run below programs sequentially in the terminal:
1. create_tables.py
2. etl.py



