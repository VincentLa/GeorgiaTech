import os

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import dump_svmlight_file

import etl
import utils
#Note: You can reuse code that you wrote in etl.py and models.py and cross.py over here. It might help.
# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

'''
You may generate your own features over here.
Note that for the test data, all events are already filtered such that they fall in the observation window of their respective patients. Thus, if you were to generate features similar to those you constructed in code/etl.py for the test data, all you have to do is aggregate events for each patient.
IMPORTANT: Store your test data features in a file called "test_features.txt" where each line has the
patient_id followed by a space and the corresponding feature in sparse format.
Eg of a line:
60 971:1.000000 988:1.000000 1648:1.000000 1717:1.000000 2798:0.364078 3005:0.367953 3049:0.013514
Here, 60 is the patient id and 971:1.000000 988:1.000000 1648:1.000000 1717:1.000000 2798:0.364078 3005:0.367953 3049:0.013514 is the feature for the patient with id 60.

Save the file as "test_features.txt" and save it inside the folder deliverables

input:
output: X_train,Y_train,X_test
'''
def calculate_index_date(events):
    """
    Similar to calculating index date in etl.py, except now we don't have mortality DF.
    """
    # Aggregate the events DF to get last event date for each patient
    indx_date = events[['patient_id', 'timestamp']].groupby(['patient_id'])\
                                                   .agg({'timestamp': 'max'})\
                                                   .rename(columns={'timestamp': 'last_event_date'})\
                                                   .reset_index()
    indx_date.last_event_date = pd.to_datetime(indx_date.last_event_date)
    indx_date['indx_date'] = indx_date.last_event_date
    indx_date = indx_date[['patient_id', 'indx_date']]
    return indx_date

def filter_events(events, indx_date):
    
    '''
    Similar to calculating filter events in etl.py but now we aren't writing to a file
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

    return filtered_events

def aggregate_events(filtered_events_df, feature_map_df):
    
    '''
    Similar to calculating aggregated events in etl.py but now we aren't writing to a file
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

    aggregated_events['patient_id'] = aggregated_events.patient_id.astype(float)
    aggregated_events['feature_id'] = aggregated_events.feature_id.astype(float)
    aggregated_events['feature_value'] = aggregated_events.feature_value.astype(float)
    
    # Min Max Normalization
    feature_min_max = aggregated_events[['feature_id', 'feature_value']].groupby(['feature_id']).agg({'feature_value': ['min', 'max']})
    feature_min_max.columns = ['_'.join(col).strip() for col in feature_min_max.columns.values]
    feature_min_max.reset_index(inplace=True)


    aggregated_events = aggregated_events.merge(feature_min_max, on=['feature_id'])

    aggregated_events['feature_value_normalized'] = (aggregated_events.feature_value) / (aggregated_events.feature_value_max)
    aggregated_events = aggregated_events[['patient_id',
                                           'feature_id',
                                           'feature_value_normalized']].rename(columns={'feature_value_normalized': 'feature_value'})

    aggregated_events['patient_id'] = aggregated_events.patient_id.astype(float)
    aggregated_events['feature_id'] = aggregated_events.feature_id.astype(float)
    aggregated_events['feature_value'] = aggregated_events.feature_value.astype(float)

    return aggregated_events


def create_features(events, feature_map):
    """
    Create Features, similar to etl.py, but with no mortality
    """

    #Calculate index date
    indx_date = calculate_index_date(events)

    #Filter events in the observation window
    filtered_events = filter_events(events, indx_date)
    
    #Aggregate the event values for each patient 
    aggregated_events = aggregate_events(filtered_events, feature_map)
    
    events = events.loc[events.value.isnull() == False]

    # Patient Features
    aggregated_events.sort_values(['patient_id', 'feature_id'], inplace=True)
    patient_features = {}
    patients = aggregated_events.patient_id.drop_duplicates()
    for p in patients:
        patient_features[p] = []

    for index, row in aggregated_events.iterrows():
        patient_features[row.patient_id].append((row.feature_id, row.feature_value))

    return patient_features


def write_features(events, feature_map):
    deliverable1 = open('../deliverables/test_features.txt', 'wb')
    patient_features = create_features(events, feature_map)

    patients = list(patient_features.keys())
    patients.sort()

    for patient in patients:
        features = patient_features[patient]
        features = sorted(features, key=lambda x: x[0])
        patient_features[patient] = features

    for patient in patients:
        deliverable1_text = str(int(patient)) + ' '
        for features in patient_features[patient]:
            deliverable1_text += (str(int(features[0])) + ':' + str("%.6f" % features[1]) + ' ')
        deliverable1.write(bytes(deliverable1_text, 'UTF-8'))
        deliverable1.write(bytes('\n', 'UTF-8'))
    deliverable1.close()


def my_features():
    """
    Generate own features. As a first pass, just replicate what we've already done in etl.py
    """
    # First pass basically code above replicates what we've already done in ETL.py for the test data
    filepath = '../data/test'
    events = pd.read_csv(os.path.join(filepath, 'events.csv'))
    feature_map = pd.read_csv(os.path.join(filepath, 'event_feature_map.csv'))
    write_features(events, feature_map)

    X_train, Y_train = utils.get_data_from_svmlight("../deliverables/features_svmlight.train")
    # X_val, Y_val = utils.get_data_from_svmlight("../deliverables/features_svmlight.validate")
    X_test, _ = utils.get_data_from_svmlight("../deliverables/test_features.txt")

    return X_train, Y_train, X_test


'''
You can use any model you wish.

input: X_train, Y_train, X_test
output: Y_pred
'''
def my_model(X_train, Y_train, X_test):
    """
    Training Model
    """
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, Y_train)
    return clf

def my_classifier_predictions(X_train, Y_train, X_test):
    """
    As first pass just use Random Forest
    """
    model = my_model(X_train, Y_train, X_test)
    y_pred = model.predict(X_test)
    return y_pred

def my_classifier_predictions_proba(X_train, Y_train, X_test):
    """
    As first pass just use Random Forest
    """
    model = my_model(X_train, Y_train, X_test)
    y_pred = model.predict_proba(X_test)[:, 1]
    return y_pred

def generate_submission_proba(svmlight_with_ids_file, Y_pred):
    f = open(svmlight_with_ids_file)
    lines = f.readlines()
    target = open('../deliverables/my_predictions_proba.csv', 'w')
    target.write("%s,%s\n" %("patient_id","label"));
    for i in range(len(lines)):
        target.write("%s,%s\n" %(str(lines[i].split()[0]),str(Y_pred[i])));

def main():
    X_train, Y_train, X_test = my_features()
    my_classifier_predictions(X_train,Y_train,X_test)
    Y_pred = my_classifier_predictions(X_train,Y_train,X_test)
    y_pred_proba = my_classifier_predictions_proba(X_train, Y_train, X_test)
    utils.generate_submission("../deliverables/test_features.txt",Y_pred)
    generate_submission_proba("../deliverables/test_features.txt",y_pred_proba)

    #The above function will generate a csv file of (patient_id,predicted label) and will be saved as "my_predictions.csv" in the deliverables folder.

if __name__ == "__main__":
    main()

	
