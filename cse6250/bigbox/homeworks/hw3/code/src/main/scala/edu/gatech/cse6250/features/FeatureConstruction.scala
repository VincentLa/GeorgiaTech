package edu.gatech.cse6250.features

import edu.gatech.cse6250.model.{ Diagnostic, LabResult, Medication }
import org.apache.spark.SparkContext
import org.apache.spark.mllib.linalg.{ Vector, Vectors }
import org.apache.spark.rdd.RDD

/**
 * @author Hang Su
 */
object FeatureConstruction {

  /**
   * ((patient-id, feature-name), feature-value)
   */
  type FeatureTuple = ((String, String), Double)

  /**
   * Aggregate feature tuples from diagnostic with COUNT aggregation,
   *
   * @param diagnostic RDD of diagnostic
   * @return RDD of feature tuples
   */
  def constructDiagnosticFeatureTuple(diagnostic: RDD[Diagnostic]): RDD[FeatureTuple] = {
    diagnostic.map(f => ((f.patientID, f.code), 1.0))
      .keyBy(f => f._1)
      .reduceByKey((x, y) => (x._1, x._2 + y._2))
      .map(f => f._2)
  }

  /**
   * Aggregate feature tuples from medication with COUNT aggregation,
   *
   * @param medication RDD of medication
   * @return RDD of feature tuples
   */
  def constructMedicationFeatureTuple(medication: RDD[Medication]): RDD[FeatureTuple] = {
    medication.map(f => ((f.patientID, f.medicine), 1.0))
      .keyBy(f => f._1)
      .reduceByKey((x, y) => (x._1, x._2 + y._2))
      .map(f => f._2)
  }

  /**
   * Aggregate feature tuples from lab result, using AVERAGE aggregation
   *
   * @param labResult RDD of lab result
   * @return RDD of feature tuples
   */
  def constructLabFeatureTuple(labResult: RDD[LabResult]): RDD[FeatureTuple] = {
    labResult.map(f => ((f.patientID, f.testName), f.value, 1))
      .keyBy(_._1)
      .reduceByKey((x, y) => (x._1, x._2 + y._2, x._3 + y._3))
      .map(f => (f._1, f._2._2 / f._2._3))
  }

  /**
   * Aggregate feature tuple from diagnostics with COUNT aggregation, but use code that is
   * available in the given set only and drop all others.
   *
   * @param diagnostic   RDD of diagnostics
   * @param candiateCode set of candidate code, filter diagnostics based on this set
   * @return RDD of feature tuples
   */
  def constructDiagnosticFeatureTuple(diagnostic: RDD[Diagnostic], candiateCode: Set[String]): RDD[FeatureTuple] = {
    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */
    constructDiagnosticFeatureTuple(diagnostic.filter(f => candiateCode.contains(f.code.toLowerCase)))
  }

  /**
   * Aggregate feature tuples from medication with COUNT aggregation, use medications from
   * given set only and drop all others.
   *
   * @param medication          RDD of diagnostics
   * @param candidateMedication set of candidate medication
   * @return RDD of feature tuples
   */
  def constructMedicationFeatureTuple(medication: RDD[Medication], candidateMedication: Set[String]): RDD[FeatureTuple] = {
    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */
    constructMedicationFeatureTuple(medication.filter(f => candidateMedication.contains(f.medicine.toLowerCase)))
  }

  /**
   * Aggregate feature tuples from lab result with AVERAGE aggregation, use lab from
   * given set of lab test names only and drop all others.
   *
   * @param labResult    RDD of lab result
   * @param candidateLab set of candidate lab test name
   * @return RDD of feature tuples
   */
  def constructLabFeatureTuple(labResult: RDD[LabResult], candidateLab: Set[String]): RDD[FeatureTuple] = {
    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */
    constructLabFeatureTuple(labResult.filter(f => candidateLab.contains(f.testName.toLowerCase)))
  }

  /**
   * Given a feature tuples RDD, construct features in vector
   * format for each patient. feature name should be mapped
   * to some index and convert to sparse feature format.
   *
   * @param sc      SparkContext to run
   * @param feature RDD of input feature tuples
   * @return
   */
  def construct(sc: SparkContext, feature: RDD[FeatureTuple]): RDD[(String, Vector)] = {

    /** save for later usage */
    feature.cache()

    /** create a feature name to id map */
    val idmap = sc.broadcast(feature.map(f => f._1._2).distinct().zipWithIndex().collectAsMap())
    val idnum = idmap.value.size

    /** transform input feature */

    /**
     * Functions maybe helpful:
     * collect
     * groupByKey
     */

    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */
    val result = feature.map(f => (f._1._1, idmap.value(f._1._2), f._2)).groupBy(_._1).map(f => {
      val featurelist = f._2.toList.map(x => (x._2.toInt, x._3))
      (f._1, Vectors.sparse(idnum, featurelist))
    })

    result

    /** The feature vectors returned can be sparse or dense. It is advisable to use sparse */

  }
}

