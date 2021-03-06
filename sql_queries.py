import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS usesr"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (num_songs int IDENTITY(0,1) PRIMARY KEY, /
                                                                            artist_id varchar, /
                                                                            artist_latitude numeric, /
                                                                            artist_longitude numeric, /
                                                                            artist_location varchar, /
                                                                            artist_name varchar, /
                                                                            song_id varchar, /
                                                                            title varchar, /
                                                                            duration numeric, /
                                                                            year int);
                             """)

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (artist varchar, /
                                                                           auth varchar, /
                                                                           first_name varchar, /
                                                                           gender char(1), /
                                                                           item_in_session int, /
                                                                           last_name varchar, /
                                                                           length numeric, /
                                                                           level varchar, /
                                                                           location varchar, /
                                                                           method varchar, /
                                                                           page varchar, /
                                                                           registration numeric, /
                                                                           session_id int, /
                                                                           song varchar, /
                                                                           status int, /
                                                                           ts numeric, /
                                                                           user_agent varchar, /
                                                                           user_id int NOT NULL);
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id varchar IDENTITY(0,1), /
                                                                 start_time timestamp NOT NULL sortkey distkey, /
                                                                 user_id varchar, /
                                                                 level varchar, /
                                                                 song_id varchar, / 
                                                                 artist_id varchar, /
                                                                 session_id varchar, /
                                                                 location varchar, /
                                                                 user_agent varchar);
                        """)

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (user_id int PRIMARY KEY, /
                                                         first_name varchar, /
                                                         last_name varchar sortkey, /
                                                         gender char(1), / 
                                                         level varchar distkey);
                        """)

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id varchar PRIMARY KEY, /
                                                         title varchar sortkey, /
                                                         artist_id varchar, /
                                                         year int, /
                                                         duration numeric);
                    """)

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id varchar PRIMARY KEY, /
                                                             name varchar sortkey, /
                                                             location varchar, /
                                                             latitude numeric, /
                                                             longitude numeric);
                    """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time timestamp PRIMARY KEY, /
                                                        hour smallint, /
                                                        day smallint, /
                                                        week smallint, /
                                                        month smallint, /
                                                        year smallint, /
                                                        weekday smallint);
                    """)

# STAGING TABLES

staging_events_copy = ("""COPY staging_events    
                        FROM {}
                        JSON {}
                        iam_role '{}'
                        """).format(config.get('S3', 'LOG_DATA'), config.get('S3', 'LOG_JSONPATH'), config.get('IAM_ROLE', 'ARN'))

staging_songs_copy = ("""COPY staging_songs 
                        FROM {}
                        JSON {}
                        iam_role '{}'
                     """).format(config.get('S3', 'SONG_DATA'), config.get('S3', 'LOG_JSONPATH'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                         SELECT e.ts, 
                         e.user_id, 
                         e.level, 
                         s.song_id, 
                         e.artist_id, 
                         s.session_id, 
                         s.location, 
                         s.user_agent
                         FROM staging_events e JOIN staging_songs s 
                         ON e.artist_name = s.artist AND e.title = s.song
                         WHERE s.page = 'NextSong'
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
                    SELECT DISTINCT user_id, first_name, last_name, gender, level
                    FROM staging_events
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration)
                    SELECT DISTINCT e.song_id, 
                                    s.song, 
                                    e.artist_id, 
                                    e.year, 
                                    e.duration
                    FROM staging_events e JOIN staging_songs s 
                    ON e.artist_name = s.artist AND e.title = s.song
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude)
                      SELECT DISTINCT artist_id, 
                                      artist_name, 
                                      artist_location, 
                                      artist_latitude, 
                                      artist_longitude
                      FROM staging events
""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
                    SELECT CONVERT(timestamp, CONVERT(char(13), ts)) as start_time, 
                            EXTRACT(hour FROM start_time) as hour, 
                            EXTRACT(day FROM start_time) as day, 
                            EXTRACT(week FROM start_time) as week, 
                            EXTRACT(month FROM start_time) as month, 
                            EXTRACT(year FROM start_time) as year, 
                            EXTRACT(weekday FROM start_time) as weekday
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
