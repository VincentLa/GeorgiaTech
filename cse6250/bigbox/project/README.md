# Georgia Tech CSE6250 Big Data for Healthcare Project
Authors:
1. Avi Ananthakrishnan
2. Vincent La

## Running Code
All of our code can be found within the [hive_project/code](./hive_project/code) and [hive_project/etl](./hive_project/etl) directories.

Once ETL and other transformations are done and data is loaded into the DB, then you can run the Machine Learning Model. The Machine Learning Model is done in a Jupyter Notebook in [ML Notebook.ipynb](./hive_project/code/ML Notebook.ipynb).

Note that all of our code is inside the [code](./hive_project/code) directory. In particular, the files that need to be run in order are:

1. First, run [hdfs_setup.sh](./hive_project/etl/raw/hdfs_setup.sh)
2. Then, run [raw](./hive_project/etl/raw) ETL *.hql files to load the MIMIC datasets. Note that for the purposes of this submission, we are only loading the first 100 rows because of size issues.
3. Then run [queries/features/noteevents_lda_models.py](./hive_project/code/pipeline/pipeline_tasks/queries/features/noteevents_lda_models.py). This creates 3 objects within the [inventory](./hive_project/code/inventory) directory. All 3 objects are pickled objects from Natural Language Processing and do not need to directly be uploaded to DB.
    * dictionary.obj
    * lda_model_tfif.obj
    * lda_model.obj
4. Run [queries/features/noteevents_with_topics.py](./hive_project/code/pipeline/pipeline_tasks/queries/features/noteevents_with_topics.py). This creates [noteevents_with_topics.csv](./hive_project/code/inventory/noteevents_with_topics.csv).
5. Run [noteevents_with_topics.hql](./hive_project/etl/model/noteevents_with_topics.hql)
6. Run [admissions_diagnoses_icd_ccs_mapping.hql](./pipeline_tasks/queries/datasets/admissions_diagnoses_icd_ccs_mapping.hql)
7. Run [admissions_ccs_ohe.py](./hive_project/code/pipeline/pipeline_tasks/queries/datasets/admissions_ccs_ohe.py). This creates [admissions_ccs_ohe.csv](../inventory/admissions_ccs_ohe.csv).
8. Run [admissions_ccs_ohe.hql](./hive_project/etl/model/admissions_ccs_ohe.hql)
9. Run [admissions_topic_scores.py](./hive_project/code/pipeline/pipeline_tasks/queries/datasets/admissions_topic_scores.py). This creates [admissions_topic_scores.csv](./hive_project/code/inventory/admissions_topic_scores.csv)
10. Run [admissions_topic_scores.hql](./hive_project/etl/model/admissions_topic_scores.hql)
11. Run [model_demog.hql](./hive_project/code/pipeline/pipeline_tasks/queries/datasets/model_demog.hql)
12. Run [model_demog_dx.hql](./hive_project/code/pipeline/pipeline_tasks/queries/datasets/model_demog_dx.hql)
13. Run [model_demog_dx_notetopics.hql](./hive_project/code/pipeline/pipeline_tasks/queries/datasets/model_demog_dx_notetopics.hql)

### Running the ML Notebook
`cd` into the [code](./hive_project/code) directory. Then open a jupyter notebook by running `jupyter notebook`. We build out machine learning model in a Jupyter Notebook: [ML Notebook.ipynb](./hive_project/code/ML Notebook.ipynb).

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
Note, the data comes from MIMIC III. More information can be found here: https://physionet.org/works/MIMICIIIClinicalDatabase/files/

Note that, we also put "test" data from MIMIC III into the [data](./data) directory. These are essentially the top 100 rows from each of the MIMIC III file just for test submission purposes.

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
