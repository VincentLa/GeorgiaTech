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
import edu.gatech.cse6250.model.VertexProperty
import edu.gatech.cse6250.randomwalk.RandomWalk

class RandomWalkTest extends FlatSpec with BeforeAndAfter with Matchers {

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

  "randomWalkOneVsAll" should "return expected value" in {
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
    val graph = GraphLoader.load(patients, labs, meds, diags).cache()
    // 1 can get to 2 through icd91 and icd92. 1 can only get to 3 through icd93.
    RandomWalk.randomWalkOneVsAll(graph, 1) should contain inOrderOnly (2, 3)
    // 2 can get to 1 through icd91 and icd92. 2 can only get to 3 through icd91.
    RandomWalk.randomWalkOneVsAll(graph, 2) should contain inOrderOnly (1, 3)
    // 3 can get to icd91. From there it is the same to get to 2 or 1 (or 3). But from 1, or 2, it
    // is easier to get back to 1 than to 2.
    RandomWalk.randomWalkOneVsAll(graph, 3) should contain inOrderOnly (1, 2)
  }
}
