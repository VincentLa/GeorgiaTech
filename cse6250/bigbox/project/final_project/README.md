# Georgia Tech CSE6250 Big Data for Healthcare Project
Authors:
1. Avi Ananthakrishnan
2. Vincent La

## Running Code
All of our code can be found within the [hive_project/code](./hive_project/code) and [hive_project/etl](./hive_project/etl) directories.

Once ETL and other transformations are done, the Machine Learning Model is done in a Jupyter Notebook in [ML Notebook.ipynb](./hive_project/code/ML Notebook.ipynb).

### Running the ML Notebook
Note that, at the top of the notebook are the following lines that connect to the Database:

```
# This assumes you have creds to production DWH. For Test Data can use test_DWH
DWH = os.getenv('MIMIC_DWH')
test_DWH = 'hive://localhost:10000/default'

# If using test data, instead of DWH, use test_DWH
engine = create_engine(DWH)
```

Note that in this example, `MIMIC_DWH` is an environment variable we set with credentials to the production Database. However, for test purposes in this submission, you can also use local Hive DB URL that is in `test_DWH`. To run with the test DB, change the next line to:

```
engine = create_engine(test_DWH)
```

`test_DWH` should contain all the data loaded from MIMIC using the test data that we included in this submission under [./data directory](./data) which is just the first 100 rows from each dataset included in MIMIC III.
 
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

## Useful Docker Commands
Runs a docker container with options represent in a YAML config
```
docker-compose up
```

SSH into Docker Container
```
ssh -p 2333 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ./config/ssh/id_rsa root@127.0.0.1
```

Start the HIVE Server for Python
```
hive --service hiveserver2 --hiveconf hive.server2.thrift.port=10000 --hiveconf hive.root.logger=INFO,console --hiveconf hive.server2.authentication=NOSASL
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
1. Complete README on instructions to run the code.
