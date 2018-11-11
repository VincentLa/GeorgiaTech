# Georgia Tech CSE6250 Big Data for Healthcare Project

## Project Draft Instructions:
Your draft should be in a form of regular research publication.
It means all sections which are common in research publication such as Abstract, Introduction, Method, Experimental Results, Discussion, and Conclusion must be there. You don't have to use exactly the same section names or structure described above, but you should have those 'contents' somewhere in your paper.
You should organize well and write clearly each section so that it is easily readable.

A couple of additional comments are:

Describe your method/approach clearly, concisely, but specifically. It should be at the level of that any reader can follow and reproduce your work after she read your paper.
Even if your current results are not good as expected, there must be analyses about what possible reasons and solutions/plans are. It is same for when your results are good.

## Downloading and Uploading Data
Data: https://physionet.org/works/MIMICIIIClinicalDatabase/files/

To download data

```
wget --user YOURUSERNAME --ask-password -A csv.gz -m -p -E -k -K -np -nd https://physionet.org/works/MIMICIIIClinicalDatabase/files/
```

Instructions to get it up into PostgresDB: https://mimic.physionet.org/tutorials/install-mimic-locally-ubuntu/

Create Database:

```
CREATE DATABASE mimic OWNER "VincentLa";
```

Set Search Path
```
set search_path to mimiciii;
```

Create Tables:

```
psql 'dbname=mimic user=VincentLa options=--search_path=mimiciii' -f postgres_create_tables.sql

OR

psql 'dbname=mimic host=c4sf-sba.postgres.database.azure.com user=mimicuser@c4sf-sba password=PASSWORD port=5432 options=--search_path=mimiciii' -f postgres_create_tables.sql
```

Import CSV Data

```
psql 'dbname=mimic user=VincentLa options=--search_path=mimiciii' -f postgres_load_data_gz.sql -v mimic_data_dir='.'

OR

psql 'dbname=mimic host=c4sf-sba.postgres.database.azure.com user=mimicuser@c4sf-sba password=PASSWORD port=5432 options=--search_path=mimiciii' -f postgres_load_data_gz.sql -v mimic_data_dir='.'
```

Create Indexes

```
# create indexes
psql 'dbname=mimic user=mimicuser options=--search_path=mimiciii' -f postgres_add_indexes.sql

OR

psql 'dbname=mimic host=c4sf-sba.postgres.database.azure.com user=mimicuser@c4sf-sba password=PASSWORD port=5432 options=--search_path=mimiciii' -f postgres_add_indexes
```

