/**
 * @author Vincent La <vla6@gatech.edu>.
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

    val sc = diagnostics.sparkContext
    val patient_vertices: RDD[(VertexId, VertexProperty)] = patients.map(patient => (patient.patientID.toLong, patient.asInstanceOf[VertexProperty]))

    var current_index = patients.map(f => f.patientID).max().toLong + 1

    // Creating Diagnostic Vertices
    val diag_vertices_ids = diagnostics.map(_.icd9code).distinct.zipWithIndex.map { case (icd9code, zeroBasedIndex) => (icd9code, zeroBasedIndex + current_index) }
    val diag_vertices_ids_mapped = diag_vertices_ids.collect.toMap
    val diagnostic_vertices = diag_vertices_ids.map { case (icd9code, index) => (index, DiagnosticProperty(icd9code)) }.asInstanceOf[RDD[(VertexId, VertexProperty)]]
    current_index += (diag_vertices_ids.count() + 1)

    // Creating Medication Vertices
    val medication_vertices_ids = medications.map(_.medicine).distinct.zipWithIndex.map { case (med, zeroBasedIndex) => (med, zeroBasedIndex + current_index) }
    val medication_vertices_ids_mapped = medication_vertices_ids.collect.toMap
    val medication_vertices = medication_vertices_ids.map { case (med, index) => (index, MedicationProperty(med)) }.asInstanceOf[RDD[(VertexId, VertexProperty)]]
    current_index += (medication_vertices_ids.count() + 1)

    // Creating Lab Vertices
    val lab_vertices_ids = labResults.map(_.labName).distinct.zipWithIndex.map { case (icd9code, zeroBasedIndex) => (icd9code, zeroBasedIndex + current_index) }
    val lab_vertices_ids_mapped = lab_vertices_ids.collect.toMap
    val lab_vertices = lab_vertices_ids.map { case (icd9code, index) => (index, LabResultProperty(icd9code)) }.asInstanceOf[RDD[(VertexId, VertexProperty)]]

    val broadcast_diag_vertices_ids_mapped = sc.broadcast(diag_vertices_ids_mapped)
    val broadcast_medication_vertices_ids_mapped = sc.broadcast(medication_vertices_ids_mapped)
    val broadcast_lab_vertices_ids_mapped = sc.broadcast(lab_vertices_ids_mapped)

    // Unioning all vertices
    val all_vertices = sc.union(patient_vertices, diagnostic_vertices, medication_vertices, lab_vertices)

    // Now Create All Edges
    // Patient-Diagnosis Edges
    val patient_diag_edges: RDD[Edge[EdgeProperty]] = diagnostics.map(f => ((f.patientID, f.icd9code), f.date, f.sequence)).keyBy(_._1).reduceByKey((f1, f2) => if (f1._2 > f2._2) f1 else f2).map(f => Edge(f._1._1.toLong, broadcast_diag_vertices_ids_mapped.value(f._1._2).toLong, PatientDiagnosticEdgeProperty(Diagnostic(f._1._1, f._2._2, f._1._2, f._2._3))))
    val patient_diag_edges_bidirectional = patient_diag_edges.union(patient_diag_edges.map(f => Edge(f.dstId, f.srcId, f.attr)))

    // Patient-Medication Edges
    val patient_medication_edges: RDD[Edge[EdgeProperty]] = medications.map(f => ((f.patientID, f.medicine), f.date)).keyBy(_._1).reduceByKey((f1, f2) => (f1._1, math.max(f1._2, f2._2))).map(f => Edge(f._1._1.toLong, broadcast_medication_vertices_ids_mapped.value(f._1._2).toLong, PatientMedicationEdgeProperty(Medication(f._1._1, f._2._2, f._1._2))))
    val patient_medication_edges_bidirectional = patient_medication_edges.union(patient_medication_edges.map(f => Edge(f.dstId, f.srcId, f.attr)))

    /// Patient-Lab Result Edges
    val patient_lab_edges: RDD[Edge[EdgeProperty]] = labResults.map(f => ((f.patientID, f.labName), f.date, f.value)).keyBy(_._1).reduceByKey((f1, f2) => if (f1._2 > f2._2) f1 else f2).map(f => Edge(f._1._1.toLong, broadcast_lab_vertices_ids_mapped.value(f._1._2).toLong, PatientLabEdgeProperty(LabResult(f._1._1, f._2._2, f._1._2, f._2._3))))
    val patient_lab_edges_bidirectional = patient_lab_edges.union(patient_lab_edges.map(f => Edge(f.dstId, f.srcId, f.attr)))

    // Unioning all edges
    val all_edges = patient_diag_edges_bidirectional.union(patient_medication_edges_bidirectional).union(patient_lab_edges_bidirectional)

    // Creating Graph
    val graph: Graph[VertexProperty, EdgeProperty] = Graph(all_vertices, all_edges)
    graph
  }
}
