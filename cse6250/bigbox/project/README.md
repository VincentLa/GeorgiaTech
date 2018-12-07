# Georgia Tech CSE6250 Big Data for Healthcare Project
Authors:
1. Avi Ananthakrishnan
2. Vincent La

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

psql 'dbname=mimic host=c4sf-sba.postgres.database.azure.com user=mimicuser@c4sf-sba password=PASSWORD port=5432 options=--search_path=mimiciii' -f postgres_add_indexes.sql
```

## Libraries and Useful Functions Used

### scikit-learn

#### One Hot Encoder
[Documentation for One Hot Encoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html)

## Examples of Future Work
1. BI Tool: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4743095/

## Examples of Projects
1. Youtube Presentation: https://www.youtube.com/watch?v=x90HVtF8E04

## Using Hive and Pandas
1. Blog Post: https://medium.com/@surankularatna/intro-to-hive-and-pandas-analysis-of-london-crime-data-2008-2016-part-1-2137532dc8db

## What to Submit
https://piazza.com/class/jjjilbkqk8m1r4?cid=1190
1. Final Paper (PDF)
2. Presentation Slides with Youtube Link to Presentation
3. Compressed File Containing all Code, Data (Sample Data is OK) and the final best model and instructions to run the code.

## Things Remaining To Do 2018-12-06
1. Need to Compress Data to just be Sample Data.
2. Need to Export Final Best Model
3. Complete README on instructions to run the code.
