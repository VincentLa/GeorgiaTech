package edu.gatech.cse6250.features

import java.sql.Date

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.scalatest.BeforeAndAfter
import org.scalatest.FlatSpec
import org.scalatest.Matchers
import org.scalatest.concurrent.TimeLimitedTests
import org.scalatest.time.{ Seconds, Span }
import edu.gatech.cse6250.model.Diagnostic
import edu.gatech.cse6250.model.Medication
import edu.gatech.cse6250.model.LabResult
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.rdd.RDD

class FeatureConstructionTest extends FlatSpec with BeforeAndAfter with Matchers with TimeLimitedTests {

  val timeLimit = Span(600, Seconds)

  var sparkContext: SparkContext = _
  var scoreFeatures: Double = 0.0
  var notesFeatures: String = ""
  var testCounter: Int = 0

  def newSqlDate(): Date = {
    new Date(new java.util.Date().getTime)
  }

  before {
    testCounter += 1
    val config = new SparkConf().setAppName("Test FeatureConstruction").setMaster("local")
    sparkContext = new SparkContext(config)
  }

  after {
    if (testCounter == 17) {
      println(s"FOR_PARSE Q21\t$scoreFeatures\tTests Passed: $scoreFeatures")
    }
    sparkContext.stop()
  }

  "constructDiagnosticFeatureTuple" should "aggregate one event" in {
    val diags = sparkContext.parallelize(Seq(
      Diagnostic("patient1", newSqlDate(), "code1")))
    val actual = FeatureConstruction.constructDiagnosticFeatureTuple(diags).collect()
    val expected = Array(
      (("patient1", "code1"), 1.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructDiagnosticFeatureTuple:aggregate_one_event "
  }

  "constructDiagnosticFeatureTuple" should "aggregate two different events" in {
    val diags = sparkContext.parallelize(Seq(
      Diagnostic("patient1", newSqlDate(), "code1"),
      Diagnostic("patient1", newSqlDate(), "code2")))
    val actual = FeatureConstruction.constructDiagnosticFeatureTuple(diags).collectAsMap()
    val expected = Map(
      (("patient1", "code1"), 1.0),
      (("patient1", "code2"), 1.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructDiagnosticFeatureTuple:aggregate_two_diff_event "
  }

  "constructDiagnosticFeatureTuple" should "aggregate two same events" in {
    val diags = sparkContext.parallelize(Seq(
      Diagnostic("patient1", newSqlDate(), "code1"),
      Diagnostic("patient1", newSqlDate(), "code1")))
    val actual = FeatureConstruction.constructDiagnosticFeatureTuple(diags).collect()
    val expected = Array(
      (("patient1", "code1"), 2.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructDiagnosticFeatureTuple:aggregate_two_same_event "
  }

  "constructDiagnosticFeatureTuple" should "aggregate three events with duplication" in {
    val diags = sparkContext.parallelize(Seq(
      Diagnostic("patient1", newSqlDate(), "code1"),
      Diagnostic("patient1", newSqlDate(), "code1"),
      Diagnostic("patient1", newSqlDate(), "code2")))
    val actual = FeatureConstruction.constructDiagnosticFeatureTuple(diags).collectAsMap()
    val expected = Map(
      (("patient1", "code1"), 2.0),
      (("patient1", "code2"), 1.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructDiagnosticFeatureTuple:aggregate_three_event "
  }

  "constructDiagnosticFeatureTuple" should "filter" in {
    val diags = sparkContext.parallelize(Seq(
      Diagnostic("patient1", newSqlDate(), "code1"),
      Diagnostic("patient1", newSqlDate(), "code1"),
      Diagnostic("patient1", newSqlDate(), "code2")))

    {
      val actual = FeatureConstruction.constructDiagnosticFeatureTuple(diags, Set("code2")).collect()
      actual should be(Array((("patient1", "code2"), 1.0)))
    }

    {
      val actual = FeatureConstruction.constructDiagnosticFeatureTuple(diags, Set("code1")).collect()
      actual should be(Array((("patient1", "code1"), 2.0)))
    }
    scoreFeatures += 1.0
    notesFeatures += "constructDiagnosticFeatureTuple:filter "
  }

  /*=============================================*/

  "constructMedicationFeatureTuple" should "aggregate one event" in {
    val meds = sparkContext.parallelize(Seq(
      Medication("patient1", newSqlDate(), "code1")))
    val actual = FeatureConstruction.constructMedicationFeatureTuple(meds).collect()
    val expected = Array(
      (("patient1", "code1"), 1.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructMedicationFeatureTuple:aggregate_one_event "
  }

  "constructMedicationFeatureTuple" should "aggregate two different events" in {
    val meds = sparkContext.parallelize(Seq(
      Medication("patient1", newSqlDate(), "code1"),
      Medication("patient1", newSqlDate(), "code2")))
    val actual = FeatureConstruction.constructMedicationFeatureTuple(meds).collectAsMap()
    val expected = Map(
      (("patient1", "code1"), 1.0),
      (("patient1", "code2"), 1.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructMedicationFeatureTuple:aggregate_two_diff_event "
  }

  "constructMedicationFeatureTuple" should "aggregate two same events" in {
    val meds = sparkContext.parallelize(Seq(
      Medication("patient1", newSqlDate(), "code1"),
      Medication("patient1", newSqlDate(), "code1")))
    val actual = FeatureConstruction.constructMedicationFeatureTuple(meds).collect()
    val expected = Array(
      (("patient1", "code1"), 2.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructMedicationFeatureTuple:aggregate_two_same_event "
  }

  "constructMedicationFeatureTuple" should "aggregate three events with duplication" in {
    val meds = sparkContext.parallelize(Seq(
      Medication("patient1", newSqlDate(), "code1"),
      Medication("patient1", newSqlDate(), "code2"),
      Medication("patient1", newSqlDate(), "code2")))
    val actual = FeatureConstruction.constructMedicationFeatureTuple(meds).collectAsMap()
    val expected = Map(
      (("patient1", "code1"), 1.0),
      (("patient1", "code2"), 2.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructMedicationFeatureTuple:aggregate_three_event "
  }

  "constructMedicationFeatureTuple" should "filter" in {
    val meds: RDD[Medication] = sparkContext.parallelize(Seq(
      Medication("patient1", newSqlDate(), "code1"),
      Medication("patient1", newSqlDate(), "code2"),
      Medication("patient1", newSqlDate(), "code2")))

    {
      val actual = FeatureConstruction.constructMedicationFeatureTuple(meds, Set("code2")).collect()
      actual should be(Array((("patient1", "code2"), 2.0)))
    }

    {
      val actual = FeatureConstruction.constructMedicationFeatureTuple(meds, Set("code1")).collect()
      actual should be(Array((("patient1", "code1"), 1.0)))
    }
    scoreFeatures += 1.0
    notesFeatures += "constructMedicationFeatureTuple:filter "
  }

  /*=============================================*/

  "constructLabFeatureTuple" should "aggregate one event" in {
    val labs = sparkContext.parallelize(Seq(
      LabResult("patient1", newSqlDate(), "code1", 42.0)))
    val actual = FeatureConstruction.constructLabFeatureTuple(labs).collect()
    val expected = Array(
      (("patient1", "code1"), 42.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructLabFeatureTuple:aggregate_one_event "
  }

  "constructLabFeatureTuple" should "aggregate two different events" in {
    val labs = sparkContext.parallelize(Seq(
      LabResult("patient1", newSqlDate(), "code1", 42.0),
      LabResult("patient1", newSqlDate(), "code2", 24.0)))
    val actual = FeatureConstruction.constructLabFeatureTuple(labs).collectAsMap()
    val expected = Map(
      (("patient1", "code1"), 42.0),
      (("patient1", "code2"), 24.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructLabFeatureTuple:aggregate_two_diff_event "
  }

  "constructLabFeatureTuple" should "aggregate two same events" in {
    val labs = sparkContext.parallelize(Seq(
      LabResult("patient1", newSqlDate(), "code1", 42.0),
      LabResult("patient1", newSqlDate(), "code1", 24.0)))
    val actual = FeatureConstruction.constructLabFeatureTuple(labs).collect()
    val expected = Array(
      (("patient1", "code1"), 66.0 / 2))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructLabFeatureTuple:aggregate_two_same_event "
  }

  "constructLabFeatureTuple" should "aggregate three events with duplication" in {
    val labs = sparkContext.parallelize(Seq(
      LabResult("patient1", newSqlDate(), "code1", 42.0),
      LabResult("patient1", newSqlDate(), "code1", 24.0),
      LabResult("patient1", newSqlDate(), "code2", 7475.0)))
    val actual = FeatureConstruction.constructLabFeatureTuple(labs).collectAsMap()
    val expected = Map(
      (("patient1", "code1"), 66.0 / 2),
      (("patient1", "code2"), 7475.0))
    actual should be(expected)
    scoreFeatures += 1.0
    notesFeatures += "constructLabFeatureTuple:aggregate_three_event "
  }

  "constructLabFeatureTuple" should "filter" in {
    val labs = sparkContext.parallelize(Seq(
      LabResult("patient1", newSqlDate(), "code1", 42.0),
      LabResult("patient1", newSqlDate(), "code1", 24.0),
      LabResult("patient1", newSqlDate(), "code2", 7475.0)))

    {
      val actual = FeatureConstruction.constructLabFeatureTuple(labs, Set("code2")).collect()
      actual should be(Array((("patient1", "code2"), 7475.0)))
    }

    {
      val actual = FeatureConstruction.constructLabFeatureTuple(labs, Set("code1")).collect()
      actual should be(Array((("patient1", "code1"), 66.0 / 2)))
    }
    scoreFeatures += 1.0
    notesFeatures += "constructLabFeatureTuple:filter "
  }

  /*=============================================*/

  "construct" should "give unique ID to codes" in {
    val patientFeatures = sparkContext.parallelize(Seq(
      (("patient1", "code2"), 42.0),
      (("patient1", "code1"), 24.0)))
    val actual = FeatureConstruction.construct(sparkContext, patientFeatures).collect()
    actual should be(Array(
      ("patient1", Vectors.dense(24.0, 42.0))))
    //scoreFeatures += 1.0
    //notesFeatures += "construct:unique_ids "
  }

  "construct" should "give sparse vectors" in {
    val patientFeatures = sparkContext.parallelize(Seq(
      (("patient1", "code0"), 42.0),
      (("patient1", "code2"), 24.0),
      (("patient2", "code1"), 12.0)))
    val actual = FeatureConstruction.construct(sparkContext, patientFeatures).collectAsMap()
    actual should be(Map(
      ("patient1", Vectors.dense(42.0, 0.0, 24.0)),
      ("patient2", Vectors.dense(0.0, 12.0, 0.0))))
    scoreFeatures += 1.0
    notesFeatures += "construct:sparse_vectors "
  }
}
