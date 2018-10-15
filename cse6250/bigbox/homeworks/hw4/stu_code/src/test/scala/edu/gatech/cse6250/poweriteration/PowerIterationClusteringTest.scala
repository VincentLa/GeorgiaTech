package edu.gatech.cse6250.clustering

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
import edu.gatech.cse6250.model.VertexProperty
import edu.gatech.cse6250.randomwalk.RandomWalk
import edu.gatech.cse6250.graphconstruct.GraphLoader

class PowerIterationClusteringTest extends FlatSpec with BeforeAndAfter with Matchers {

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

  "runPIC" should "return expected values" in {
    val localPatients = Seq(
      PatientProperty("1", "m", "dob", "dod"),
      PatientProperty("2", "m", "dob", "dod"),
      PatientProperty("3", "m", "dob", "dod"),
      PatientProperty("4", "m", "dob", "dod"))
    val localDiags = Seq(
      Diagnostic("1", 1, "icd91", 1),
      Diagnostic("1", 1, "icd92", 1),
      Diagnostic("1", 1, "icd93", 1),
      Diagnostic("2", 1, "icd91", 1),
      Diagnostic("2", 1, "icd92", 1),
      Diagnostic("3", 1, "icd91", 1),
      Diagnostic("4", 1, "icd91", 1))
    val patients = sparkContext.parallelize(localPatients)
    val diags = sparkContext.parallelize(localDiags)
    val labs = sparkContext.parallelize(Seq[LabResult]())
    val meds = sparkContext.parallelize(Seq[Medication]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    val similarities = Jaccard.jaccardSimilarityAllPatients(graph)
    val actual = PowerIterationClustering.runPIC(similarities).collect.toMap
    // 4 patients, 3 classes, the third and fourth patients should be in the same class.
    actual.values.toSet should have size (3)
    actual(3) should be(actual(4))
  }
}
