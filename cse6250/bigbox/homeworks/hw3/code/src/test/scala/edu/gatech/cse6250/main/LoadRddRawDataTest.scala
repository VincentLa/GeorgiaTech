package edu.gatech.cse6250.main

import edu.gatech.cse6250.helper.SparkHelper
import edu.gatech.cse6250.util.LocalClusterSparkContext
import org.scalatest.FunSuite
import org.scalatest.concurrent.TimeLimitedTests
import org.scalatest.time.{ Seconds, Span }

class LoadRddRawDataTest extends FunSuite with LocalClusterSparkContext with TimeLimitedTests {

  val timeLimit = Span(600, Seconds)

  test("Testing your data loader") {
    //    val sqlContext = new SQLContext(sc)
    val spark = SparkHelper.spark
    //    val sc = spark.sparkContext
    //  val sqlContext = spark.sqlContext

    val (medication, labResult, diagnostic) = Main.loadRddRawData(spark)

    val numTrueMedication = 31552
    val numTrueLabResult = 106894
    val numTrueDiagnostic = 112811

    val numMedication = medication.count()
    val numLabResult = labResult.count()
    val numDiagnostic = diagnostic.count()

    assert(numMedication == numTrueMedication)
    assert(numLabResult == numTrueLabResult)
    assert(numDiagnostic == numTrueDiagnostic)

    val numFalseMedication = (numTrueMedication - numMedication).abs
    val numFalseLabResult = (numTrueLabResult - numLabResult).abs
    val numFalseDiagnostic = (numTrueDiagnostic - numDiagnostic).abs

    //println(s"Incorrect Medication: $numFalseMedication")
    //println(s"Incorrect LabResult : $numFalseLabResult")
    //println(s"Incorrect Diagnostic: $numFalseDiagnostic")

    val recall = 1.0 - (numFalseDiagnostic + numFalseLabResult + numFalseMedication).toDouble / (numTrueDiagnostic + numTrueLabResult + numTrueMedication).toDouble
    //    val score = totalFalse match {
    //      case num if (0 until 10).contains(num) => 5
    //      case num if (10 until 20).contains(num) => 4
    //      case num if (20 until 30).contains(num) => 3
    //      case num if (30 until 40).contains(num) => 2
    //      case num if (40 until 50).contains(num) => 1
    //      case num if (50 until 60).contains(num) => 0
    //    }
    val score = Math.floor(recall * 5.0)
    //println(s"Recall: $recall")
    //println(s"Final score for Q1.1: ${score}")
    println(s"FOR_PARSE Q1a\t$score\tRecall $recall")
  }
}
