package edu.gatech.cse6250.graphconstruct

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.scalatest.BeforeAndAfter
import org.scalatest.FlatSpec
import org.scalatest.Matchers

import edu.gatech.cse6250.model.Diagnostic
import edu.gatech.cse6250.model.PatientProperty
import edu.gatech.cse6250.model.LabResult
import org.apache.spark.rdd.RDD
import edu.gatech.cse6250.model.Medication
import edu.gatech.cse6250.model.PatientDiagnosticEdgeProperty
import org.apache.spark.graphx.Edge
import edu.gatech.cse6250.model.PatientMedicationEdgeProperty
import edu.gatech.cse6250.model.PatientLabEdgeProperty
import scala.util.Random
import edu.gatech.cse6250.model.DiagnosticProperty
import edu.gatech.cse6250.model.MedicationProperty
import edu.gatech.cse6250.model.LabResultProperty

class GraphLoaderTest extends FlatSpec with BeforeAndAfter with Matchers {

  var sparkContext: SparkContext = _

  before {
    import org.apache.log4j.Logger
    import org.apache.log4j.Level

    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)

    val config = new SparkConf().setAppName("Test GraphLoader").setMaster("local")
    sparkContext = new SparkContext(config)
  }

  after {
    sparkContext.stop()
  }

  "diag nodes" should "be latest" in {
    val patients = sparkContext.parallelize(Seq(
      PatientProperty("1", "m", "dob", "dod")))
    val diags = sparkContext.parallelize(Seq(
      Diagnostic("1", 1, "icd9", 1),
      Diagnostic("1", 2, "icd9", 3),
      Diagnostic("1", 3, "icd9", 2)))
    val labs = sparkContext.parallelize(Seq[LabResult]())
    val meds = sparkContext.parallelize(Seq[Medication]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.numVertices should be(2)
    graph.numEdges should be(2)
    graph.edges.collect().map { _.attr }.foreach {
      case x: PatientDiagnosticEdgeProperty => x.diagnostic.date should be(3)
    }
  }

  "diag nodes" should "contain all distinct codes" in {
    val patients = sparkContext.parallelize(Seq(
      PatientProperty("1", "m", "dob", "dod")))
    val diags = sparkContext.parallelize(Seq(
      Diagnostic("1", 1, "icd91", 1),
      Diagnostic("1", 1, "icd92", 1)))
    val labs = sparkContext.parallelize(Seq[LabResult]())
    val meds = sparkContext.parallelize(Seq[Medication]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.numVertices should be(3)
    graph.numEdges should be(4)
  }

  "diag nodes" should "be unique across all patients" in {
    val p1 = PatientProperty("0", "m", "dob", "dod")
    val p2 = PatientProperty("1", "m", "dob", "dod")
    val patients = sparkContext.parallelize(Seq(p1, p2))
    val diag1 = Diagnostic("0", 1, "icd9", 1)
    val diag2 = Diagnostic("1", 2, "icd9", 3)
    val localDiags = Seq(diag1, diag2)
    val diags = sparkContext.parallelize(localDiags)
    val labs = sparkContext.parallelize(Seq[LabResult]())
    val meds = sparkContext.parallelize(Seq[Medication]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.numVertices should be(3)
    graph.numEdges should be(4)
    val expected = Set(
      p1, p2,
      DiagnosticProperty("icd9"))
    graph.vertices.map { _._2 }.collect.toSet should be(expected)
    graph.edges.collect.filter { x => x.srcId >= 0 && x.srcId < 2 }.foreach {
      x =>
        x.attr.asInstanceOf[PatientDiagnosticEdgeProperty].diagnostic should be(
          localDiags(x.srcId.toInt))
    }
  }

  "med nodes" should "be latest" in {
    val patients = sparkContext.parallelize(Seq(
      PatientProperty("1", "m", "dob", "dod")))
    val meds = sparkContext.parallelize(Seq(
      Medication("1", 1, "medcode"),
      Medication("1", 2, "medcode"),
      Medication("1", 3, "medcode")))
    val labs = sparkContext.parallelize(Seq[LabResult]())
    val diags = sparkContext.parallelize(Seq[Diagnostic]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.numVertices should be(2)
    graph.numEdges should be(2)
    graph.edges.collect().map { _.attr }.foreach {
      case x: PatientMedicationEdgeProperty => x.medication.date should be(3)
    }
  }

  "med nodes" should "contain all distinct codes" in {
    val patients = sparkContext.parallelize(Seq(
      PatientProperty("1", "m", "dob", "dod")))
    val meds = sparkContext.parallelize(Seq(
      Medication("1", 1, "medcode1"),
      Medication("1", 1, "medcode2")))
    val diags = sparkContext.parallelize(Seq[Diagnostic]())
    val labs = sparkContext.parallelize(Seq[LabResult]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.numVertices should be(3)
    graph.numEdges should be(4)
  }

  "med nodes" should "be unique across all patients" in {
    val p1 = PatientProperty("0", "m", "dob", "dod")
    val p2 = PatientProperty("1", "m", "dob", "dod")
    val patients = sparkContext.parallelize(Seq(p1, p2))
    val med1 = Medication("0", 1, "medcode")
    val med2 = Medication("1", 2, "medcode")
    val localMeds = Seq(med1, med2)
    val meds = sparkContext.parallelize(localMeds)
    val labs = sparkContext.parallelize(Seq[LabResult]())
    val diags = sparkContext.parallelize(Seq[Diagnostic]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.numVertices should be(3)
    graph.numEdges should be(4)
    val expected = Set(
      p1, p2,
      MedicationProperty("medcode"))
    graph.vertices.map { _._2 }.collect.toSet should be(expected)
    graph.edges.collect.filter { x => x.srcId >= 0 && x.srcId < 2 }.foreach {
      x =>
        x.attr.asInstanceOf[PatientMedicationEdgeProperty].medication should be(
          localMeds(x.srcId.toInt))
    }
  }

  "lab nodes" should "be latest" in {
    val patients = sparkContext.parallelize(Seq(
      PatientProperty("1", "m", "dob", "dod")))
    val meds = sparkContext.parallelize(Seq[Medication]())
    val labs = sparkContext.parallelize(Seq(
      LabResult("1", 1, "labname", "1"),
      LabResult("1", 2, "labname", "2"),
      LabResult("1", 3, "labname", "3")))
    val diags = sparkContext.parallelize(Seq[Diagnostic]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.numVertices should be(2)
    graph.numEdges should be(2)
    graph.edges.collect().map { _.attr }.foreach {
      case x: PatientLabEdgeProperty => {
        x.labResult.date should be(3)
        x.labResult.labName should be("labname")
      }
    }
  }

  "lab nodes" should "contain all distinct codes" in {
    val patients = sparkContext.parallelize(Seq(
      PatientProperty("1", "m", "dob", "dod")))
    val labs = sparkContext.parallelize(Seq(
      LabResult("1", 1, "labname1", "1"),
      LabResult("1", 1, "labname2", "1")))
    val meds = sparkContext.parallelize(Seq[Medication]())
    val diags = sparkContext.parallelize(Seq[Diagnostic]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.numVertices should be(3)
    graph.numEdges should be(4)
  }

  "lab nodes" should "be unique across all patients" in {
    val p1 = PatientProperty("0", "m", "dob", "dod")
    val p2 = PatientProperty("1", "m", "dob", "dod")
    val patients = sparkContext.parallelize(Seq(p1, p2))
    val meds = sparkContext.parallelize(Seq[Medication]())
    val lab1 = LabResult("0", 1, "labname", "1")
    val lab2 = LabResult("1", 2, "labname", "2")
    val localLabs = Seq(lab1, lab2)
    val labs = sparkContext.parallelize(localLabs)
    val diags = sparkContext.parallelize(Seq[Diagnostic]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.numVertices should be(3)
    graph.numEdges should be(4)
    val expected = Set(
      p1, p2,
      LabResultProperty("labname"))
    graph.vertices.map { _._2 }.collect.toSet should be(expected)
    graph.edges.collect.filter { x => x.srcId >= 0 && x.srcId < 2 }.foreach {
      x =>
        x.attr.asInstanceOf[PatientLabEdgeProperty].labResult should be(
          localLabs(x.srcId.toInt))
    }
  }

  "graph" should "be bidirectional" in {
    val patients = sparkContext.parallelize(Seq(
      PatientProperty("1", "m", "dob", "dod")))
    val meds = sparkContext.parallelize(Seq[Medication]())
    val labs = sparkContext.parallelize(Seq(
      LabResult("1", 1, "labname", "1")))
    val diags = sparkContext.parallelize(Seq[Diagnostic]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.numVertices should be(2)
    graph.numEdges should be(2)
    val edges = graph.edges.collect.map(e => e.srcId -> e.dstId).toMap
    for ((id, dst) <- edges) {
      edges(dst) should be(id)
    }
  }

  "patient nodes" should "use patient ID" in {
    val id = Random.nextInt()
    val patients = sparkContext.parallelize(Seq(
      PatientProperty(id.toString, "m", "dob", "dod")))
    val meds = sparkContext.parallelize(Seq[Medication]())
    val labs = sparkContext.parallelize(Seq[LabResult]())
    val diags = sparkContext.parallelize(Seq[Diagnostic]())
    val graph = GraphLoader.load(patients, labs, meds, diags)
    graph.vertices.collect.head._1 should be(id)
  }

}
