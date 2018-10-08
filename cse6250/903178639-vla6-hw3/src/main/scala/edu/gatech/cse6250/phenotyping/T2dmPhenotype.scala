package edu.gatech.cse6250.phenotyping

import edu.gatech.cse6250.model.{ Diagnostic, LabResult, Medication }
import org.apache.spark.rdd.RDD

import java.sql.Date

/**
 * @author Hang Su <hangsu@gatech.edu>,
 * @author Sungtae An <stan84@gatech.edu>,
 */
object T2dmPhenotype {

  // Adding this in, otherwise I get an implicit order problem working with dates.
  // https://piazza.com/class/jjjilbkqk8m1r4?cid=620
  implicit val sqlDateOrdering = new Ordering[Date] {
    def compare(x: Date, y: Date): Int = x compareTo y
  }

  /** Hard code the criteria */
  val T1DM_DX = Set("250.01", "250.03", "250.11", "250.13", "250.21", "250.23", "250.31", "250.33", "250.41", "250.43",
    "250.51", "250.53", "250.61", "250.63", "250.71", "250.73", "250.81", "250.83", "250.91", "250.93")

  val T2DM_DX = Set("250.3", "250.32", "250.2", "250.22", "250.9", "250.92", "250.8", "250.82", "250.7", "250.72", "250.6",
    "250.62", "250.5", "250.52", "250.4", "250.42", "250.00", "250.02")

  val T1DM_MED = Set("lantus", "insulin glargine", "insulin aspart", "insulin detemir", "insulin lente", "insulin nph", "insulin reg", "insulin,ultralente")

  val T2DM_MED = Set("chlorpropamide", "diabinese", "diabanase", "diabinase", "glipizide", "glucotrol", "glucotrol xl",
    "glucatrol ", "glyburide", "micronase", "glynase", "diabetamide", "diabeta", "glimepiride", "amaryl",
    "repaglinide", "prandin", "nateglinide", "metformin", "rosiglitazone", "pioglitazone", "acarbose",
    "miglitol", "sitagliptin", "exenatide", "tolazamide", "acetohexamide", "troglitazone", "tolbutamide",
    "avandia", "actos", "actos", "glipizide")

  /**
   * Transform given data set to a RDD of patients and corresponding phenotype
   *
   * @param medication medication RDD
   * @param labResult  lab result RDD
   * @param diagnostic diagnostic code RDD
   * @return tuple in the format of (patient-ID, label). label = 1 if the patient is case, label = 2 if control, 3 otherwise
   */

  // First, define a helper function to catch abnormal values
  def is_lab_value_abnormal(item: LabResult): Boolean = {
    item.testName match {
      case "hba1c"                  => item.value >= 6
      case "hemoglobin a1c"         => item.value >= 6
      case "fasting glucose"        => item.value >= 110
      case "fasting blood glucose"  => item.value >= 110
      case "fasting plasma glucose" => item.value >= 110
      case "glucose"                => item.value > 110
      case "Glucose"                => item.value > 110
      case "glucose, serum"         => item.value > 110
      case _                        => false
    }

  }

  def transform(medication: RDD[Medication], labResult: RDD[LabResult], diagnostic: RDD[Diagnostic]): RDD[(String, Int)] = {
    /**
     * Remove the place holder and implement your code here.
     * Hard code the medication, lab, icd code etc. for phenotypes like example code below.
     * When testing your code, we expect your function to have no side effect,
     * i.e. do NOT read from file or write file
     *
     * You don't need to follow the example placeholder code below exactly, but do have the same return type.
     *
     * Hint: Consider case sensitivity when doing string comparisons.
     */

    val sc = medication.sparkContext

    /** Hard code the criteria */
    val diabetes_type_1_diagnosis_codes = Set("code1", "250.03", "250.01", "250.11", "250.13", "250.21", "250.23", "250.31", "250.33", "250.41", "250.43", "250.51", "250.53", "250.61", "250.63", "250.71", "250.73", "250.81", "250.83", "250.91", "250.93")
    val diabetes_type_1_medications = Set("med1", "insulin nph", "lantus", "insulin glargine", "insulin aspart", "insulin detemir", "insulin lente", "insulin reg", "insulin,ultralente")
    val diabetes_type_2_diagnosis_codes = Set("250.3", "250.32", "250.2", "250.22", "250.9", "250.92", "250.8", "250.82", "250.7", "250.72", "250.6", "250.62", "250.5", "250.52", "250.4", "250.42", "250.00", "250.02")
    val diabetes_type_2_medications = Set("chlorpropamide", "diabinese", "diabanase", "diabinase", "glipizide", "glucotrol", "glucotrol xl", "glucatrol ", "glyburide", "micronase", "glynase", "diabetamide", "diabeta", "glimepiride", "amaryl", "repaglinide", "prandin", "nateglinide", "metformin", "rosiglitazone", "pioglitazone", "acarbose", "miglitol", "sitagliptin", "exenatide", "tolazamide", "acetohexamide", "troglitazone", "tolbutamide", "avandia", "actos", "ACTOS", "glipizide")

    // Get all Patient IDs
    val all_patient_ids = medication.map(f => f.patientID).union(diagnostic.map(f => f.patientID)).union(labResult.map(f => f.patientID)).distinct()

/*********************************************************
    Step 1: Find Case Patients
    **********************************************************/
    // Implement Case Logic
    val patients_without_dm1_dx = diagnostic.filter(d => !diabetes_type_1_diagnosis_codes.contains(d.code)).map(x => x.patientID).distinct()
    val patients_with_dm2_dx = diagnostic.filter(d => diabetes_type_2_diagnosis_codes.contains(d.code)).map(x => x.patientID).distinct()

    // Filter to all patients without Diabetes 1 Dx, but has Diabetes 2 DX
    // If patient has Type 1 DM Diagnosis then for sure we know not Case
    val patient_without_dm1_with_dm2_dx = patients_without_dm1_dx.intersection(patients_with_dm2_dx).cache()

    // First, we need to see if the patient has Type 1 DM Medication. If no, then case.
    val all_dm1_meds = medication.filter(f => diabetes_type_1_medications.contains(f.medicine)).cache()
    val patient_with_out_dm1_med = patient_without_dm1_with_dm2_dx.subtract(all_dm1_meds.map(f => f.patientID))

    // Second, in the case where patient has Type 1 DM Medication,
    // we need to see if they also have Type 2 DM Medication. If no then Case
    val all_dm2_meds = medication.filter(f => diabetes_type_2_medications.contains(f.medicine)).cache()
    val patient_with_dm1_without_dm2_med = all_dm1_meds.map(f => f.patientID).intersection(patient_without_dm1_with_dm2_dx).subtract(all_dm2_meds.map(f => f.patientID))

    // Third, in the case where the patient has both Type 1 and Type 2 DM Medication
    // we need to check whether the Type 2 DM Medication Precedes Type 1 DM Medication
    // If yes, then Case, if not then not case.
    val patient_earliest_dm1_med_date = all_dm1_meds.groupBy(f => f.patientID).map(f => (f._1, f._2.minBy(x => x.date).date))
    val patient_earliest_dm2_med_date = all_dm2_meds.groupBy(f => f.patientID).map(f => (f._1, f._2.minBy(x => x.date).date))
    val patient_with_dm2_med_earlier_than_dm1 = patient_earliest_dm2_med_date.join(patient_earliest_dm1_med_date).filter(f => f._2._1.before(f._2._2)).map(f => f._1)

    // Case is defined as the union of the three possibilities outlined above
    val casePatients = patient_with_out_dm1_med.union(patient_with_dm1_without_dm2_med).union(patient_with_dm2_med_earlier_than_dm1).distinct().map(f => (f, 1))

/*********************************************************
    Step 2: Find Control Patients
    **********************************************************/
    // First, is there any Glucose Measure
    val patients_with_any_glucose_measure = labResult.filter(f => f.testName.contains("glucose")).map(f => f.patientID)

    // Next, does the patient have abnormal Lab Result
    val patients_with_abnormal_lab_result = labResult.filter(f => is_lab_value_abnormal(f)).map(f => f.patientID)
    val patients_without_abnormal_lab_result = patients_with_any_glucose_measure.subtract(patients_with_abnormal_lab_result)

    // If Patient does not have abnormal lab result and does not have DM related diagnosis than Control
    // Hard code DM Related DX from DM Related DX.csv, except for 250.* which we will filter using a contains later
    val dm_related_dx = Set("790.21", "790.22", "790.2", "790.29", "648.81", "648.82", "648.83", "648.84", "648.0", "648.00", "648.01", "648.02", "648.03", "648.04", "791.5", "277.7", "V77.1", "256.4")
    val patients_with_dm_related_dx = diagnostic.filter(f => dm_related_dx.contains(f.code) || f.code.contains("250.")).map(f => f.patientID)
    val patients_without_dm_related_dx = patients_without_abnormal_lab_result.subtract(patients_with_dm_related_dx).distinct()
    val controlPatients = patients_without_dm_related_dx.map(f => (f, 2))

/*********************************************************
    Step 3: Find Other Patients
    **********************************************************/
    val others = all_patient_ids.subtract(casePatients.map(f => f._1)).subtract(controlPatients.map(f => f._1)).map(f => (f, 3))
    val phenotypeLabel = sc.union(casePatients, controlPatients, others)

    /** Return */
    phenotypeLabel
  }
}
