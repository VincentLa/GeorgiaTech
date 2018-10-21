/**
 * @author Hang Su <hangsu@gatech.edu>.
 * @author Yu Jing <yujing@gatech.edu>
 */

package edu.gatech.cse6250.main

import java.text.SimpleDateFormat

import edu.gatech.cse6250.clustering.PowerIterationClustering
import edu.gatech.cse6250.graphconstruct.GraphLoader
import edu.gatech.cse6250.helper.{ CSVHelper, SparkHelper }
import edu.gatech.cse6250.jaccard.Jaccard
import edu.gatech.cse6250.model._
import edu.gatech.cse6250.randomwalk.RandomWalk
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession

object Main {
  def main(args: Array[String]) {
    import org.apache.log4j.{ Level, Logger }

    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)

    val spark = SparkHelper.spark
    val sc = spark.sparkContext
    //  val sqlContext = spark.sqlContext

    /** initialize loading of data */
    val (patient, medication, labResult, diagnostic) = loadRddRawData(spark)

    val patientGraph = GraphLoader.load(patient, labResult, medication, diagnostic)

    println(Jaccard.jaccardSimilarityOneVsAll(patientGraph, 9))
    println(RandomWalk.randomWalkOneVsAll(patientGraph, 9))

    val similarities = Jaccard.jaccardSimilarityAllPatients(patientGraph)

    val PICLabels = PowerIterationClustering.runPIC(similarities)

    sc.stop()
  }

  def loadRddRawData(spark: SparkSession): (RDD[PatientProperty], RDD[Medication], RDD[LabResult], RDD[Diagnostic]) = {
    import spark.implicits._
    val sqlContext = spark.sqlContext

    val dateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssX")

    List("data/PATIENT.csv", "data/LAB.csv", "data/DIAGNOSTIC.csv", "data/MEDICATION.csv")
      .foreach(CSVHelper.loadCSVAsTable(spark, _))

    // add logic to handle null values if needed
    val patient = sqlContext.sql(
      """
        |SELECT subject_id, sex, dob, dod
        |FROM PATIENT
      """.stripMargin)
      .map(r => PatientProperty(r(0).toString, r(1).toString, r(2).toString, r(3).toString))

    val labResult = sqlContext.sql(
      """
        |SELECT subject_id, date, lab_name, value
        |FROM LAB
        |WHERE value IS NOT NULL and value <> ''
      """.stripMargin)
      .map(r => LabResult(r(0).toString, r(1).toString.toLong, r(2).toString, r(3).toString))

    val diagnostic = sqlContext.sql(
      """
        |SELECT subject_id, date, code, sequence
        |FROM DIAGNOSTIC
      """.stripMargin)
      .map(r => Diagnostic(r(0).toString, r(1).toString.toLong, r(2).toString, r(3).toString.toInt))

    val medication = sqlContext.sql(
      """
        |SELECT subject_id, date, med_name
        |FROM MEDICATION
      """.stripMargin)
      .map(r => Medication(r(0).toString, r(1).toString.toLong, r(2).toString))

    (patient.rdd, medication.rdd, labResult.rdd, diagnostic.rdd)

  }

}
