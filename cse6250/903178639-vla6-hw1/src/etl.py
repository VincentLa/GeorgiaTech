"""
Author: Vincent La
vla6

To test: nosetests tests/test_etl.py
"""

import os

import numpy as np
import pandas as pd

import utils

# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

def read_csv(filepath):
    
    '''
    TODO: This function needs to be completed.
    Read the events.csv, mortality_events.csv and event_feature_map.csv files into events, mortality and feature_map.
    
    Return events, mortality and feature_map
    '''

    #Columns in events.csv - patient_id,event_id,event_description,timestamp,value
    events = pd.read_csv(os.path.join(filepath, 'events.csv'))
    
    #Columns in mortality_events.csv - patient_id,timestamp,label
    mortality = pd.read_csv(os.path.join(filepath, 'mortality_events.csv'))

    #Columns in event_feature_map.csv - idx,event_id
    feature_map = pd.read_csv(os.path.join(filepath, 'event_feature_map.csv'))

    return events, mortality, feature_map


def calculate_index_date(events, mortality, deliverables_path):
    
    '''
    TODO: This function needs to be completed.

    Refer to instructions in Q3 a

    Returns:
      - indx_date: DataFrame that is unique and the patient_id level with another column for index date

    Suggested steps:
    1. Create list of patients alive ( mortality_events.csv only contains information about patients deceased)
    2. Split events into two groups based on whether the patient is alive or deceased
    3. Calculate index date for each patient
    
    IMPORTANT:
    Save indx_date to a csv file in the deliverables folder named as etl_index_dates.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, indx_date.
    The csv file should have a header 
    For example if you are using Pandas, you could write: 
        indx_date.to_csv(deliverables_path + 'etl_index_dates.csv', columns=['patient_id', 'indx_date'], index=False)

    Return indx_date
    '''
    # Aggregate the events DF to get last event date for each patient
    indx_date = events[['patient_id', 'timestamp']].groupby(['patient_id'])\
                                                   .agg({'timestamp': 'max'})\
                                                   .rename(columns={'timestamp': 'last_event_date'})\
                                                   .reset_index()

    # Merge in Deceased Status
    indx_date = indx_date.merge(mortality[['patient_id', 'label', 'timestamp']].rename(columns={'timestamp': 'date_of_death'}), how='left', on='patient_id')
    indx_date.rename(index=str, columns={'label': 'is_deceased'}, inplace=True)
    indx_date.is_deceased.fillna(0, inplace=True)
    indx_date.is_deceased = indx_date.is_deceased.astype(bool)
    indx_date.last_event_date = pd.to_datetime(indx_date.last_event_date)
    indx_date.date_of_death = pd.to_datetime(indx_date.date_of_death)
    indx_date['date_of_death_30_days_prior'] = indx_date.date_of_death - pd.to_timedelta(30, unit='d')
    indx_date['indx_date'] = indx_date.date_of_death_30_days_prior.combine_first(indx_date.last_event_date)
    indx_date = indx_date[['patient_id', 'indx_date']]

    # Finally, write required DF to disk
    indx_date.to_csv(deliverables_path + 'etl_index_dates.csv', columns=['patient_id', 'indx_date'], index=False)
    return indx_date


def filter_events(events, indx_date, deliverables_path):
    
    '''
    TODO: This function needs to be completed.

    Refer to instructions in Q3 b

    Suggested steps:
    1. Join indx_date with events on patient_id
    2. Filter events occurring in the observation window(IndexDate-2000 to IndexDate)
    
    
    IMPORTANT:
    Save filtered_events to a csv file in the deliverables folder named as etl_filtered_events.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, event_id, value.
    The csv file should have a header 
    For example if you are using Pandas, you could write: 
        filtered_events.to_csv(deliverables_path + 'etl_filtered_events.csv', columns=['patient_id', 'event_id', 'value'], index=False)

    Return filtered_events
    '''
    # Define beginning and end of observation window and prediction window, respectively
    indx_date['observation_window_begin'] = indx_date.indx_date - pd.to_timedelta(2000, unit='d')
    indx_date['prediction_window_end'] = indx_date.indx_date + pd.to_timedelta(30, unit='d')

    # Merge
    filtered_events = events.merge(indx_date, how='left', on='patient_id')
    filtered_events.timestamp = pd.to_datetime(filtered_events.timestamp)

    filtered_events['keep_event'] = (filtered_events.timestamp >= filtered_events.observation_window_begin) &\
                                    (filtered_events.timestamp <= filtered_events.indx_date)
    filtered_events = filtered_events.loc[filtered_events.keep_event]
    filtered_events = filtered_events[['patient_id', 'event_id', 'value']]

    filtered_events.to_csv(deliverables_path + 'etl_filtered_events.csv', columns=['patient_id', 'event_id', 'value'], index=False)
    return filtered_events


def aggregate_events(filtered_events_df, mortality_df,feature_map_df, deliverables_path):
    
    '''
    TODO: This function needs to be completed.

    Refer to instructions in Q3 c

    Suggested steps:
    1. Replace event_id's with index available in event_feature_map.csv
    2. Remove events with n/a values
    3. Aggregate events using sum and count to calculate feature value
    4. Normalize the values obtained above using min-max normalization(the min value will be 0 in all scenarios)
    
    
    IMPORTANT:
    Save aggregated_events to a csv file in the deliverables folder named as etl_aggregated_events.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, event_id, value.
    The csv file should have a header .
    For example if you are using Pandas, you could write: 
        aggregated_events.to_csv(deliverables_path + 'etl_aggregated_events.csv', columns=['patient_id', 'feature_id', 'feature_value'], index=False)

    Return aggregated_events
    '''
    # Need to Remove rows where value is null
    events_remove_na = filtered_events_df.loc[filtered_events_df.value.isnull() == False]

    events_remove_na = events_remove_na.merge(feature_map_df, how='left', on='event_id')
    events_remove_na.rename(columns={'idx': 'event_id_idx'}, inplace=True)
    events_remove_na['event_type'] = events_remove_na.event_id.str.replace('[^a-zA-Z]', '')

    events_grouped = events_remove_na[['patient_id',
                                       'event_id_idx',
                                       'event_type',
                                       'value']].groupby(['patient_id', 'event_id_idx', 'event_type'])\
                                                .agg({'value': ['count', 'sum']})
    
    # Neat trick to collapse the hierarchical columns returned by groupby to single column
    events_grouped.columns = ['_'.join(col).strip() for col in events_grouped.columns.values]

    # reset index
    events_grouped.reset_index(inplace=True)

    events_grouped['value'] = np.where(events_grouped['event_type'] == 'LAB',
                                                      events_grouped.value_count,
                                                      events_grouped.value_sum)

    aggregated_events = events_grouped[['patient_id', 'event_id_idx', 'value']]
    aggregated_events = aggregated_events.rename(columns={'event_id_idx': 'feature_id', 'value': 'feature_value'})
    
    # Min Max Normalization
    min_value = min(aggregated_events.feature_value)
    max_value = max(aggregated_events.feature_value)

    aggregated_events['feature_value_normalized'] = (aggregated_events.feature_value - min_value) / (max_value - min_value)
    aggregated_events = aggregated_events[['patient_id',
                                           'feature_id',
                                           'feature_value_normalized']].rename(columns={'feature_value_normalized': 'feature_value'})

    # Write to Disk
    aggregated_events.to_csv(deliverables_path + 'etl_aggregated_events.csv', columns=['patient_id', 'feature_id', 'feature_value'], index=False)                                       
    return aggregated_events

def create_features(events, mortality, feature_map):
    
    deliverables_path = '../deliverables/'

    #Calculate index date
    indx_date = calculate_index_date(events, mortality, deliverables_path)

    #Filter events in the observation window
    filtered_events = filter_events(events, indx_date,  deliverables_path)
    
    #Aggregate the event values for each patient 
    aggregated_events = aggregate_events(filtered_events, mortality, feature_map, deliverables_path)

    '''
    TODO: Complete the code below by creating two dictionaries - 
    1. patient_features :  Key - patient_id and value is array of tuples(feature_id, feature_value)
    2. mortality : Key - patient_id and value is mortality label
    '''
    # Starting with mortality
    mortality_df = events[['patient_id']].drop_duplicates().reset_index(drop=True)
    mortality_df = mortality_df.merge(mortality[['patient_id', 'label']], how='left', on='patient_id')
    mortality_df.rename(index=str, columns={'label': 'is_deceased'}, inplace=True)
    mortality_df.is_deceased.fillna(0, inplace=True)
    mortality = dict(zip(mortality_df.patient_id, mortality_df.is_deceased))

    # Next, Patient Features
    aggregated_events.sort_values(['patient_id', 'feature_id'], inplace=True)
    patient_features = {}
    patients = events.patient_id.drop_duplicates()
    for p in patients:
        patient_features[p] = []

    for index, row in aggregated_events.iterrows():
        patient_features[row.patient_id].append((row.feature_id, row.feature_value))

    return patient_features, mortality

def save_svmlight(patient_features, mortality, op_file, op_deliverable):
    
    '''
    TODO: This function needs to be completed

    Refer to instructions in Q3 d

    Format:
    <patient_id> <mortality_value> <feature_id>:<feature_value> <feature_id>:<feature_value>

    Create two files:
    1. op_file - which saves the features in svmlight format. (See instructions in Q3d for detailed explanation)
    2. op_deliverable - which saves the features in following format:
       patient_id1 label feature_id:feature_value feature_id:feature_value feature_id:feature_value ...
       patient_id2 label feature_id:feature_value feature_id:feature_value feature_id:feature_value ...  
    
    Note: Please make sure the features are ordered in ascending order, and patients are stored in ascending order as well.     
    '''
    deliverable1 = open(op_file, 'wb')
    deliverable2 = open(op_deliverable, 'wb')
    
    patients = list(patient_features.keys())
    patients.sort()
    for patient in patients:
        deliverable1_text = str(int(mortality[patient])) + ' '
        deliverable2_text = str(patient) + ' ' + str(int(mortality[patient])) + ' '
        for features in patient_features[patient]:
            deliverable1_text += (str(int(features[0])) + ':' + str(features[1]) + ' ')
            deliverable2_text += (str(int(features[0])) + ':' + str(features[1]) + ' ')
        deliverable1.write(bytes(deliverable1_text, 'UTF-8'))
        deliverable1.write(bytes('\n', 'UTF-8'))
        deliverable2.write(bytes(deliverable2_text, 'UTF-8'))
        deliverable2.write(bytes('\n', 'UTF-8'))
    deliverable1.close()
    deliverable2.close()


def main():
    train_path = '../data/train/'
    events, mortality, feature_map = read_csv(train_path)
    patient_features, mortality = create_features(events, mortality, feature_map)
    save_svmlight(patient_features, mortality, '../deliverables/features_svmlight.train', '../deliverables/features.train')

if __name__ == "__main__":
    main()
