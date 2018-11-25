drop table if exists datasets.model_demog;
create table datasets.model_demog as
(
select
  adm.hadm_id,
  case when patients.gender = 'M' then 1 else 0 end as is_male,
  1.0 * date_part('year', age(adm.admittime, patients.dob))
    + 1.0 * date_part('month', age(adm.admittime, patients.dob))
    + 1.0 * date_part('day', age(adm.admittime, patients.dob)) as age_at_admit,
  adm.admission_type,
  adm.insurance,
  adm.language,
  adm.marital_status,
  adm.ethnicity,
  adm.hospital_expire_flag
from mimiciii.admissions as adm
  left join mimiciii.patients as patients
    on adm.subject_id = patients.subject_id
);
