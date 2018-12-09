# Pipeline Runner
This pipeline runner is a way to keep all tasks hitting our database in a central location. The value of this, is that we can recreate the state of our database very easily, and we know where are all the tasks that are writing to our database.

The entry point into the pipeline runner is [pipeline_runner.py](./pipeline_runner.py). In this file, we essentially create a `for` loop that loops through all the files in a list and executes them. Currently we only support `.hql` and `.py` files.

## Adding Additional Files
To add additional files to run, add the file name to the appropriate list object.

To run the pipeline, you need to have the connection string stored as an environment variable. You will also need to have Python3 installed as well as necessary dependencies specified in `environment.yml`. 

## Running the Pipeline Runner
To actually run `pipeline_runner.py` you need to first be in the `code` folder of the repository. `cd` into that.

In addition (especially if you are running the pipeline end-to-end including parsing the raw CSV/Excel files to load into the Database), you will need to have the data in the proper location: `./data`. 

Now to run the `pipeline_runner.py`:
```
python -m pipeline.pipeline_runner --db_url=$MIMIC_DWH
```

To understand what this is doing:
1. `-m` option: run library module as a script. See official docs https://docs.python.org/3.6/using/cmdline.html and https://docs.python.org/3.6/tutorial/modules.html if you're looking for a deeper understanding
2. `--db_url`: is the option name for the database URL. We read this in using the `argparse` module in `pipeline_runner.py`.
3. `$MIMIC_DWH`: the environment variable for our database URL. This assumes you've set the database URL as an environment variable.

## Tasks to Run
1. First, run [hdfs_setup.sh](../../etl/raw/hdfs_setup.sh)
2. Then, run [raw](../../etl/raw) ETL *.hql files to load the MIMIC datasets. Note that for the purposes of this submission, we are only loading the first 100 rows because of size issues.
3. Then run [queries/features/noteevents_lda_models.py](./pipeline\_tasks/queries/features/noteevents_lda_models.py). This creates 3 objects within the [inventory](../inventory) directory. All 3 objects are pickled objects from Natural Language Processing and do not need to directly be uploaded to DB.
  1. dictionary.obj
  2. lda_model_tfif.obj
  3. lda_model.obj
4. Run [queries/features/noteevents_with_topics.py](./pipeline_tasks/queries/features/noteevents_with_topics.py). This creates [noteevents_with_topics.csv](../inventory/noteevents_with_topics.csv).
5. Run [noteevents_with_topics.hql](../../etl/model/noteevents_with_topics.hql)
6. Run [admissions_diagnoses_icd_ccs_mapping.hql](./queries/datasets/admissions_diagnoses_icd_ccs_mapping.hql)
7. Run [admissions_ccs_ohe.py](./pipeline_tasks/queries/datasets/admissions_ccs_ohe.py). This creates [admissions_ccs_ohe.csv](../inventory/admissions_ccs_ohe.csv).
8. Run [admissions_ccs_ohe.hql](../../etl/model/admissions_ccs_ohe.hql)
9. Run [admissions_topic_scores.py](./pipeline_tasks/queries/datasets/admissions_topics_scores.py). This creates [admissions_topic_scores.csv](../inventory/admissions_topic_scores.csv)
10. Run [admissions_topic_scores.hql](../../etl/model/admissions_topic_scores.hql)
11. Run [model_demog.hql](./pipeline_tasks/queries/datasets/model_demog.hql)
12. Run [model_demog_dx.hql](./pipeline_tasks/queries/datasets/model_demog_dx.hql)
13. Run [model_demog_dx_notetopics.hql](./pipeline_tasks/queries/datasets/model_demog_dx_notetopics.hql)
14. Run 
