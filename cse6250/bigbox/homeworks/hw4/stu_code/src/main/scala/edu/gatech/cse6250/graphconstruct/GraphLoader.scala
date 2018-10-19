/**
 * @author Hang Su <hangsu@gatech.edu>.
 */

// Resouce: https://stanford.edu/~rezab/nips2014workshop/slides/ankur.pdf

package edu.gatech.cse6250.graphconstruct

import edu.gatech.cse6250.model._
import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD

object GraphLoader {
  /**
   * Generate Bipartite Graph using RDDs
   *
   * @input: RDDs for Patient, LabResult, Medication, and Diagnostic
   * @return: Constructed Graph
   *
   */
  def load(patients: RDD[PatientProperty], labResults: RDD[LabResult],
    medications: RDD[Medication], diagnostics: RDD[Diagnostic]): Graph[VertexProperty, EdgeProperty] = {

    /** HINT: See Example of Making Patient Vertices Below */
    val vertexPatient: RDD[(VertexId, VertexProperty)] = patients
      .map(patient => (patient.patientID.toLong, patient.asInstanceOf[VertexProperty]))

    var indexnow = patients.map(f => f.patientID).max().toLong + 1
    // println("hello")
    // println(indexnow)
    // diagnostics.take(10).foreach(println)

    // Creating Diagnostic Vertices
    val diagnosticVertexIdRDD = diagnostics.map(_.icd9code).distinct.zipWithIndex.map { case (icd9code, zeroBasedIndex) => (icd9code, zeroBasedIndex + indexnow) }
    val diagnostic2VertexId = diagnosticVertexIdRDD.collect.toMap
    val vertexDiagnostic = diagnosticVertexIdRDD.map { case (icd9code, index) => (index, DiagnosticProperty(icd9code)) }.asInstanceOf[RDD[(VertexId, VertexProperty)]]
    indexnow += (diagnosticVertexIdRDD.count() + 1)

    // Creating Medication Vertices
    val medVertexIdRDD = medications.map(_.medicine).distinct.zipWithIndex.map { case (med, zeroBasedIndex) => (med, zeroBasedIndex + indexnow) }
    val med2VertexId = medVertexIdRDD.collect.toMap
    val vertexMedication = medVertexIdRDD.map { case (med, index) => (index, MedicationProperty(med)) }.asInstanceOf[RDD[(VertexId, VertexProperty)]]
    indexnow += (medVertexIdRDD.count() + 1)

    // Creating Lab Vertices
    val labVertexIdRDD = labResults.map(_.labName).distinct.zipWithIndex.map { case (icd9code, zeroBasedIndex) => (icd9code, zeroBasedIndex + indexnow) }
    val lab2VertexId = labVertexIdRDD.collect.toMap
    val vertexLab = labVertexIdRDD.map { case (icd9code, index) => (index, LabResultProperty(icd9code)) }.asInstanceOf[RDD[(VertexId, VertexProperty)]]

    val sc = diagnostics.sparkContext
    val bcdiagnostic2VertexId = sc.broadcast(diagnostic2VertexId)
    val bcmed2VertexId = sc.broadcast(med2VertexId)
    val bclab2VertexId = sc.broadcast(lab2VertexId)
    /**
     * HINT: See Example of Making PatientPatient Edges Below
     *
     * This is just sample edges to give you an example.
     * You can remove this PatientPatient edges and make edges you really need
     */
    val vertexs = sc.union(vertexPatient, vertexDiagnostic, vertexMedication, vertexLab)

    // case class PatientPatientEdgeProperty(someProperty: SampleEdgeProperty) extends EdgeProperty
    // val edgePatientPatient: RDD[Edge[EdgeProperty]] = patients
    //   .map({ p =>
    //     Edge(p.patientID.toLong, p.patientID.toLong, SampleEdgeProperty("sample").asInstanceOf[EdgeProperty])
    //   })

    val edgePatientDiagnostic: RDD[Edge[EdgeProperty]] = {
      diagnostics.map(f => ((f.patientID, f.icd9code), f.date, f.sequence)).keyBy(_._1).reduceByKey((f1, f2) => if (f1._2 > f2._2) f1 else f2).map(f => Edge(f._1._1.toLong, bcdiagnostic2VertexId.value(f._1._2).toLong, PatientDiagnosticEdgeProperty(Diagnostic(f._1._1, f._2._2, f._1._2, f._2._3))))
    }
    val edgePatientDiagnostic_bi = edgePatientDiagnostic.union(edgePatientDiagnostic.map(f => Edge(f.dstId, f.srcId, f.attr)))
    val edgePatientMedication: RDD[Edge[EdgeProperty]] = medications.map(f => ((f.patientID, f.medicine), f.date)).keyBy(_._1).reduceByKey((f1, f2) => (f1._1, math.max(f1._2, f2._2))).map(f => Edge(f._1._1.toLong, bcmed2VertexId.value(f._1._2).toLong, PatientMedicationEdgeProperty(Medication(f._1._1, f._2._2, f._1._2))))
    val edgePatientMedication_bi = edgePatientMedication.union(edgePatientMedication.map(f => Edge(f.dstId, f.srcId, f.attr)))
    val edgePatientLab: RDD[Edge[EdgeProperty]] = labResults.map(f => ((f.patientID, f.labName), f.date, f.value)).keyBy(_._1).reduceByKey((f1, f2) => if (f1._2 > f2._2) f1 else f2).map(f => Edge(f._1._1.toLong, bclab2VertexId.value(f._1._2).toLong, PatientLabEdgeProperty(LabResult(f._1._1, f._2._2, f._1._2, f._2._3))))
    val edgePatientLab_bi = edgePatientLab.union(edgePatientLab.map(f => Edge(f.dstId, f.srcId, f.attr)))
    //RDD[Edge[PatientDiagnosticEdgeProperty]]
    // Making Graph

    val edges = edgePatientDiagnostic_bi.union(edgePatientMedication_bi).union(edgePatientLab_bi)
    //val a2=edges.collect()
    //println(vertexs.count())
    //println(edges.count())
    val graph: Graph[VertexProperty, EdgeProperty] = Graph(vertexs, edges)

    // Making Graph
    // val graph: Graph[VertexProperty, EdgeProperty] = Graph[VertexProperty, EdgeProperty](vertexPatient, edgePatientPatient)

    graph
  }
}
