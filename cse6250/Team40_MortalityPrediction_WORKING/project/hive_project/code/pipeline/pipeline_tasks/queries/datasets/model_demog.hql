drop table if exists model_demog;
create table model_demog as
select
  adm.hadm_id,
  case when patients.gender = 'M' then 1 else 0 end as is_male,
  datediff(cast(adm.admittime as string), cast(patients.dob as string)) as age_at_admit,
  adm.admission_type,
  adm.insurance,
  adm.language,
  adm.marital_status,
  adm.ethnicity,
  adm.hospital_expire_flag
from admissions adm
  left join patients patients
    on adm.subject_id = patients.subject_id
;
