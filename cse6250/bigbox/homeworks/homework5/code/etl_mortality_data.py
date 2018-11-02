import os
import pickle
import pandas as pd


PATH_TRAIN = "../data/mortality/train/"
PATH_VALIDATION = "../data/mortality/validation/"
PATH_TEST = "../data/mortality/test/"
PATH_OUTPUT = "../data/mortality/processed/"


def convert_icd9(icd9_object):
	"""
	:param icd9_object: ICD-9 code (Pandas/Numpy object) (e.g. Pandas Series).
	:return: extracted main digits of ICD-9 code
	"""
	icd9_str = str(icd9_object)
	# TODO: Extract the the first 3 or 4 alphanumeric digits prior to the decimal point from a given ICD-9 code.
	# TODO: Read the homework description carefully.
	first_char = icd9_str[0]
	extract_num_chars = 3
	if first_char.isdigit():
		extract_num_chars = 3
	if first_char == 'V':
		extract_num_chars = 3
	if first_char == 'E':
		extract_num_chars = 4

	converted = icd9_str[:extract_num_chars]

	return converted


def build_codemap():
	"""
	:return: Dict of code map {main-digits of ICD9: unique feature ID}
	"""
	# TODO: We build a code map using ONLY train data. Think about how to construct validation/test sets using this.
	df_icd9 = pd.read_csv(os.path.join(PATH_TRAIN, "DIAGNOSES_ICD.csv"), usecols=["ICD9_CODE"])
	df_digits = df_icd9['ICD9_CODE'].apply(convert_icd9)
	df_digits.sort_values(inplace=True)
	
	# Printing for Checking conver_icd9 function
	# print('hello')
	# print(df_icd9['ICD9_CODE'].head())
	# print(df_digits.head())
	codemap = {}
	feature_id = 1
	for digit in df_digits:
		if digit not in codemap:
			codemap[digit] = int(feature_id)
			feature_id += 1
	return codemap


def create_dataset(path, codemap):
	"""
	:param path: path to the directory contains raw files.
	:param codemap: 3-digit ICD-9 code feature map
	:return: List(patient IDs), List(labels), Visit sequence data as a List of List of List.
	"""
	# TODO: 1. Load data from the three csv files
	# TODO: Loading the mortality file is shown as an example below. Load two other files also.
	df_mortality = pd.read_csv(os.path.join(path, "MORTALITY.csv"))
	df_admissions = pd.read_csv(os.path.join(path, "ADMISSIONS.csv"))
	df_diagnoses = pd.read_csv(os.path.join(path, "DIAGNOSES_ICD.csv"))

	# TODO: 2. Convert diagnosis code in to unique feature ID.
	# TODO: HINT - use 'convert_icd9' you implemented and 'codemap'.
	codemap = build_codemap()
	df_diagnoses['df_digits'] = df_diagnoses['ICD9_CODE'].apply(convert_icd9)
	df_diagnoses['icd9_feature_id'] = df_diagnoses.df_digits.map(codemap)
	
	# Dropping cases where we did not see ICD9 code in training, since if we didn't see it in
	# training the model won't know what to do with it.
	df_diagnoses.dropna(subset=['ICD9_CODE', 'icd9_feature_id'], inplace=True)
	df_diagnoses['icd9_feature_id'] = df_diagnoses.icd9_feature_id.astype(int)

	print('hello')
	print(codemap['410'])
	print(df_diagnoses.head())

	# TODO: 3. Group the diagnosis codes for the same visit.
	

	# TODO: 4. Group the visits for the same patient.

	# TODO: 5. Make a visit sequence dataset as a List of patient Lists of visit Lists
	# TODO: Visits for each patient must be sorted in chronological order.

	# TODO: 6. Make patient-id List and label List also.
	# TODO: The order of patients in the three List output must be consistent.
	patient_ids = [0, 1, 2]
	labels = [1, 0, 1]
	seq_data = [[[0, 1], [2]], [[1, 3, 4], [2, 5]], [[3], [5]]]
	return patient_ids, labels, seq_data


def main():
	# Build a code map from the train set
	print("Build feature id map")
	codemap = build_codemap()
	os.makedirs(PATH_OUTPUT, exist_ok=True)
	pickle.dump(codemap, open(os.path.join(PATH_OUTPUT, "mortality.codemap.train"), 'wb'), pickle.HIGHEST_PROTOCOL)

	# Train set
	print("Construct train set")
	train_ids, train_labels, train_seqs = create_dataset(PATH_TRAIN, codemap)

	pickle.dump(train_ids, open(os.path.join(PATH_OUTPUT, "mortality.ids.train"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(train_labels, open(os.path.join(PATH_OUTPUT, "mortality.labels.train"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(train_seqs, open(os.path.join(PATH_OUTPUT, "mortality.seqs.train"), 'wb'), pickle.HIGHEST_PROTOCOL)

	# Validation set
	print("Construct validation set")
	validation_ids, validation_labels, validation_seqs = create_dataset(PATH_VALIDATION, codemap)

	pickle.dump(validation_ids, open(os.path.join(PATH_OUTPUT, "mortality.ids.validation"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(validation_labels, open(os.path.join(PATH_OUTPUT, "mortality.labels.validation"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(validation_seqs, open(os.path.join(PATH_OUTPUT, "mortality.seqs.validation"), 'wb'), pickle.HIGHEST_PROTOCOL)

	# Test set
	print("Construct test set")
	test_ids, test_labels, test_seqs = create_dataset(PATH_TEST, codemap)

	pickle.dump(test_ids, open(os.path.join(PATH_OUTPUT, "mortality.ids.test"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(test_labels, open(os.path.join(PATH_OUTPUT, "mortality.labels.test"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(test_seqs, open(os.path.join(PATH_OUTPUT, "mortality.seqs.test"), 'wb'), pickle.HIGHEST_PROTOCOL)

	print("Complete!")


if __name__ == '__main__':
	main()
