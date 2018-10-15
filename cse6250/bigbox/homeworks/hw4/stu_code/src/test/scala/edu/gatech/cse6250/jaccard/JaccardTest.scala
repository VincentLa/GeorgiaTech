package edu.gatech.cse6250.graphconstruct

import scala.collection.mutable.ListBuffer
import scala.util.Random

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.scalatest.BeforeAndAfter
import org.scalatest.FlatSpec
import org.scalatest.Matchers

import edu.gatech.cse6250.jaccard.Jaccard
import edu.gatech.cse6250.model.Diagnostic
import edu.gatech.cse6250.model.LabResult
import edu.gatech.cse6250.model.Medication
import edu.gatech.cse6250.model.PatientProperty

class JaccardTest extends FlatSpec with BeforeAndAfter with Matchers {

  var sparkContext: SparkContext = _

  before {
    import org.apache.log4j.Logger
    import org.apache.log4j.Level

    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)

    val config = new SparkConf().setAppName("Test Jaccard").setMaster("local")
    sparkContext = new SparkContext(config)
  }

  after {
    sparkContext.stop()
  }

  "jaccard" should "be correct" in {
    val a = Set(1, 2, 3, 4)
    val b = Set(4, 3, 2, 1)
    val c = Set(2, 3)
    val d = Set(5, 6, 7, 8)
    val e = Set(4, 5)

    Jaccard.jaccard(a, b) should be(1)
    Jaccard.jaccard(a, c) should be(0.5)
    Jaccard.jaccard(a, d) should be(0)
    Jaccard.jaccard(c, e) should be(0)
    Jaccard.jaccard(d, e) should be(0.2)
    Jaccard.jaccard(a, e) should be(0.2)
  }

  "jaccard" should "return 0 when union is empty" in {
    val a = Set()
    val b = Set()
    Jaccard.jaccard(a, b) should be(0)
  }

  "jaccardSimilarityOneVsAll" should "work with <= 10 patients" in {
    for (numPatients <- 1 to 10) {
      val localPatients = new ListBuffer[PatientProperty]()
      val localDiags = new ListBuffer[Diagnostic]()
      for (i <- 1 to numPatients) {
        localPatients += PatientProperty(i.toString, "m", "dob", "dod")
        localDiags += Diagnostic(i.toString, 1, "icd9", 1)
      }
      val patients = sparkContext.parallelize(localPatients)
      val diags = sparkContext.parallelize(localDiags)
      val labs = sparkContext.parallelize(Seq[LabResult]())
      val meds = sparkContext.parallelize(Seq[Medication]())
      val graph = GraphLoader.load(patients, labs, meds, diags)
      val randPid = Random.nextInt(numPatients) + 1
      val ids = Jaccard.jaccardSimilarityOneVsAll(graph, randPid)
      ids should not contain (randPid)
      ids should have size (numPatients - 1)
    }
  }

  "jaccardSimilarityOneVsAll" should "only give 10 patients" in {
    for (numPatients <- 11 to 15) {
      val localPatients = new ListBuffer[PatientProperty]()
      val localDiags = new ListBuffer[Diagnostic]()
      for (i <- 1 to numPatients) {
        localPatients += PatientProperty(i.toString, "m", "dob", "dod")
        localDiags += Diagnostic(i.toString, 1, "icd9", 1)
      }
      val patients = sparkContext.parallelize(localPatients)
      val diags = sparkContext.parallelize(localDiags)
      val labs = sparkContext.parallelize(Seq[LabResult]())
      val meds = sparkContext.parallelize(Seq[Medication]())
      val graph = GraphLoader.load(patients, labs, meds, diags)
      val randPid = Random.nextInt(numPatients) + 1
      val ids = Jaccard.jaccardSimilarityOneVsAll(graph, randPid)
      ids should not contain (randPid)
      ids should have size (10)
    }
  }

  "jaccardSimilarityOneVsAll" should "be correct" in {
    val localPatients = Seq(
      PatientProperty("1", "m", "dob", "dod"),
      PatientProperty("2", "m", "dob", "dod"),
      PatientProperty("3", "m", "dob", "dod"))
    val localDiags = Seq(
      Diagnostic("1", 1, "icd91", 1),
      Diagnostic("1", 1, "icd92", 1),
      Diagnostic("1", 1, "icd93", 1),
      Diagnostic("2", 1, "icd91", 1),
      Diagnostic("2", 1, "icd92", 1),
      Diagnostic("3", 1, "icd91", 1))
    val patients = sparkContext.parallelize(localPatients)
    val diags = sparkContext.parallelize(localDiags)
    val labs = sparkContext.parallelize(Seq[LabResult]())
    val meds = sparkContext.parallelize(Seq[Medication]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    var ids = Jaccard.jaccardSimilarityOneVsAll(graph, 1)
    ids(0) should be(2) // 2 / 3
    ids(1) should be(3) // 1 / 3
    ids = Jaccard.jaccardSimilarityOneVsAll(graph, 2)
    ids(0) should be(1) // 2 / 3
    ids(1) should be(3) // 1 / 2
    ids = Jaccard.jaccardSimilarityOneVsAll(graph, 3)
    ids(0) should be(2) // 1 / 2
    ids(1) should be(1) // 1 / 3
  }

  "jaccardSimilarityAllPatients" should "be correct" in {
    val localPatients = Seq(
      PatientProperty("1", "m", "dob", "dod"),
      PatientProperty("2", "m", "dob", "dod"),
      PatientProperty("3", "m", "dob", "dod"))
    val localDiags = Seq(
      Diagnostic("1", 1, "icd91", 1),
      Diagnostic("1", 1, "icd92", 1),
      Diagnostic("1", 1, "icd93", 1),
      Diagnostic("2", 1, "icd91", 1),
      Diagnostic("2", 1, "icd92", 1),
      Diagnostic("3", 1, "icd91", 1))
    val patients = sparkContext.parallelize(localPatients)
    val diags = sparkContext.parallelize(localDiags)
    val labs = sparkContext.parallelize(Seq[LabResult]())
    val meds = sparkContext.parallelize(Seq[Medication]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    val actual = Jaccard.jaccardSimilarityAllPatients(graph).collect.toSet
    val expected = Set(
      (1, 2, 2.0 / 3),
      (1, 3, 1.0 / 3),
      (2, 3, 1.0 / 2))
    actual should be(expected)
  }
}
