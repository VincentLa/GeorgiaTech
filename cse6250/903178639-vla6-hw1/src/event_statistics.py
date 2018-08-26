"""
Author: Vincent La
vla6

To test: nosetests tests/test_statistics.py
"""
import time
import pandas as pd
import numpy as np

# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

def read_csv(filepath):
    '''
    TODO : This function needs to be completed.
    Read the events.csv and mortality_events.csv files. 
    Variables returned from this function are passed as input to the metric functions.
    '''
    events = pd.read_csv(filepath + 'events.csv')
    mortality = pd.read_csv(filepath + 'mortality_events.csv')

    return events, mortality

def event_count_metrics(events, mortality):
    '''
    TODO : Implement this function to return the event count metrics.
    Event count is defined as the number of events recorded for a given patient.
    '''
    avg_dead_event_count = 0.0
    max_dead_event_count = 0.0
    min_dead_event_count = 0.0
    avg_alive_event_count = 0.0
    max_alive_event_count = 0.0
    min_alive_event_count = 0.0

    # Merge in Mortality Data
    df = events.merge(mortality[['patient_id', 'label']], how='left', on='patient_id')
    df.rename(index=str, columns={'label': 'is_deceased'}, inplace=True)
    df.is_deceased.fillna(0, inplace=True)
    df.is_deceased = df.is_deceased.astype(bool)

    event_counts = df.groupby(['patient_id', 'is_deceased']).size().reset_index(name='number_events')
    event_counts_results = event_counts.groupby(['is_deceased']).agg(['mean', 'min', 'max'])['number_events']

    avg_dead_event_count = event_counts_results.loc[True]['mean']
    max_dead_event_count = event_counts_results.loc[True]['max']
    min_dead_event_count = event_counts_results.loc[True]['min']
    avg_alive_event_count = event_counts_results.loc[False]['mean']
    max_alive_event_count = event_counts_results.loc[False]['max']
    min_alive_event_count = event_counts_results.loc[False]['min']
    return min_dead_event_count, max_dead_event_count, avg_dead_event_count, min_alive_event_count, max_alive_event_count, avg_alive_event_count

def encounter_count_metrics(events, mortality):
    '''
    TODO : Implement this function to return the encounter count metrics.
    Encounter count is defined as the count of unique dates on which a given patient visited the ICU. 
    '''
    avg_dead_encounter_count = 0.0
    max_dead_encounter_count = 0.0
    min_dead_encounter_count = 0.0 
    avg_alive_encounter_count = 0.0
    max_alive_encounter_count = 0.0
    min_alive_encounter_count = 0.0

    # Get Unique Encounters DF
    encounters = events[['patient_id', 'timestamp']].drop_duplicates()
    encounters.sort_values(['patient_id', 'timestamp'], inplace=True)
    encounters['encounter_id'] = [i for i in range(encounters.shape[0])]
    encounters.set_index('encounter_id', inplace=True)

    ## Counting number of encounters and splitting by deceased status
    encounter_counts = encounters.groupby(['patient_id']).size().reset_index(name='number_encounters')
    encounter_counts = encounter_counts.merge(mortality[['patient_id', 'label']], how='left', on='patient_id')
    encounter_counts.rename(index=str, columns={'label': 'is_deceased'}, inplace=True)
    encounter_counts.is_deceased.fillna(0, inplace=True)
    encounter_counts.is_deceased = encounter_counts.is_deceased.astype(bool)

    encounter_counts_results = encounter_counts.groupby(['is_deceased']).agg(['mean', 'max', 'min'])['number_encounters']

    avg_dead_encounter_count = encounter_counts_results.loc[True]['mean']
    max_dead_encounter_count = encounter_counts_results.loc[True]['max']
    min_dead_encounter_count = encounter_counts_results.loc[True]['min']
    avg_alive_encounter_count = encounter_counts_results.loc[False]['mean']
    max_alive_encounter_count = encounter_counts_results.loc[False]['max']
    min_alive_encounter_count = encounter_counts_results.loc[False]['min']

    return min_dead_encounter_count, max_dead_encounter_count, avg_dead_encounter_count, min_alive_encounter_count, max_alive_encounter_count, avg_alive_encounter_count

def record_length_metrics(events, mortality):
    '''
    TODO: Implement this function to return the record length metrics.
    Record length is the duration between the first event and the last event for a given patient. 
    '''
    avg_dead_rec_len = 0.0
    max_dead_rec_len = 0.0
    min_dead_rec_len = 0.0
    avg_alive_rec_len = 0.0
    max_alive_rec_len = 0.0
    min_alive_rec_len = 0.0

    # Compute Record Length at Patient Level
    record_length = events[['patient_id', 'timestamp']].groupby('patient_id').agg(['min', 'max'])
    record_length.columns = ['min_timestamp', 'max_timestamp']
    record_length['record_length'] = (pd.to_datetime(record_length.max_timestamp) - pd.to_datetime(record_length.min_timestamp)).dt.days
    record_length.reset_index(inplace=True)

    ## Splitting by deceased status
    record_length = record_length.merge(mortality[['patient_id', 'label']], how='left', on='patient_id')
    record_length.rename(index=str, columns={'label': 'is_deceased'}, inplace=True)
    record_length.is_deceased.fillna(0, inplace=True)
    record_length.is_deceased = record_length.is_deceased.astype(bool)
    record_length.record_length = record_length.record_length.astype(int)

    record_length_results = record_length.groupby(['is_deceased']).agg(['mean', 'max', 'min'])['record_length']

    avg_dead_rec_len = record_length_results.loc[True]['mean']
    max_dead_rec_len = record_length_results.loc[True]['max']
    min_dead_rec_len = record_length_results.loc[True]['min']
    avg_alive_rec_len = record_length_results.loc[False]['mean']
    max_alive_rec_len = record_length_results.loc[False]['max']
    min_alive_rec_len = record_length_results.loc[False]['min']

    return min_dead_rec_len, max_dead_rec_len, avg_dead_rec_len, min_alive_rec_len, max_alive_rec_len, avg_alive_rec_len

def main():
    '''
    DO NOT MODIFY THIS FUNCTION.
    '''
    # You may change the following path variable in coding but switch it back when submission.
    train_path = '../data/train/'

    # DO NOT CHANGE ANYTHING BELOW THIS ----------------------------
    events, mortality = read_csv(train_path)

    #Compute the event count metrics
    start_time = time.time()
    event_count = event_count_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute event count metrics: " + str(end_time - start_time) + "s"))
    print(event_count)

    #Compute the encounter count metrics
    start_time = time.time()
    encounter_count = encounter_count_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute encounter count metrics: " + str(end_time - start_time) + "s"))
    print(encounter_count)

    #Compute record length metrics
    start_time = time.time()
    record_length = record_length_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute record length metrics: " + str(end_time - start_time) + "s"))
    print(record_length)
    
if __name__ == "__main__":
    main()
