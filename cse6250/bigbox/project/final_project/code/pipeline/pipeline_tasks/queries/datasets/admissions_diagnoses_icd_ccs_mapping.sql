/*
The purpose of this query is to take the Diagnosis Codes for Each Admission as 
shown in mimiciii.diagnoses_icd (https://mimic.physionet.org/mimictables/diagnoses_icd/)
and map to CCS (Clinical Classification Software) codes to give higher level
clinical mapping to reduce dimensionality.
*/
drop table if exists datasets.admissions_diagnoses_icd_ccs_mapping;
create table datasets.admissions_diagnoses_icd_ccs_mapping as
(
select
  dx.row_id,
  dx.subject_id,
  dx.hadm_id,
  dx.seq_num,
  dx.icd9_code,
  map.ccs_category,
  map.ccs_category_description
from mimiciii.diagnoses_icd as dx
  left join ontologies.ccs_icd9cm_map as map
    on dx.icd9_code = map.icd9cm_code
)
