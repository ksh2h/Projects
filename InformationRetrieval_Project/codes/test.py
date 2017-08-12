'''
create role ir7_user with createdb login password 'grp7';
create database IR_Group7 owner ir7_user;
'''

import psycopg2
conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )
cur = conn.cursor()

cur.execute( '''CREATE TABLE PAPERS
    (ID VARCHAR PRIMARY KEY NOT NULL,
    TITLE VARCHAR,
    VENUE VARCHAR,
    FIELD VARCHAR[],
    YEAR VARCHAR,
    AUTHORS VARCHAR[],
    CITING_PAPERS VARCHAR[],
    KEYWORDS VARCHAR[]
    );''' )

cur.execute( '''CREATE TABLE AUTHORS
    (ID VARCHAR PRIMARY KEY NOT NULL,
    PAPERS VARCHAR[]
    );''' )


cur.execute( '''CREATE TABLE CO_AUTHOR_NETWORK
    (ID VARCHAR NOT NULL,
    CO_AUTHOR VARCHAR,
    WEIGHT INT
    );''' )


cur.execute( '''CREATE TABLE VENUES
    (VENUE VARCHAR PRIMARY KEY NOT NULL,
    PAPERS VARCHAR
    );''' )


cur.execute( '''CREATE TABLE FIELDS
    (FIELD VARCHAR PRIMARY KEY NOT NULL,
    PAPERS VARCHAR[]
    );''' )

cur.execute( '''CREATE TABLE YEARS
    (YEAR VARCHAR PRIMARY KEY NOT NULL,
    PAPERS VARCHAR[]
    );''' )



conn.commit()
conn.close()
