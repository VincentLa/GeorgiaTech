/*
The purpose of this query is to take the Diagnosis Codes for Each Admission as 
shown in mimiciii.diagnoses_icd (https://mimic.physionet.org/mimictables/diagnoses_icd/)
and map to CCS (Clinical Classification Software) codes to give higher level
clinical mapping to reduce dimensionality.
*/
drop table if exists admissions_diagnoses_icd_ccs_mapping;
create table admissions_diagnoses_icd_ccs_mapping as
select
  dx.row_id,
  dx.subject_id,
  dx.hadm_id,
  dx.seq_num,
  dx.icd9_code,
  ccs_dx_map.ccs_category,
  ccs_dx_map.ccs_category_description
from diagnoses_icd dx
  left outer join ccs_dx_map
    on (dx.icd9_code = trim(ccs_dx_map.icd_9_cm_code))
;
