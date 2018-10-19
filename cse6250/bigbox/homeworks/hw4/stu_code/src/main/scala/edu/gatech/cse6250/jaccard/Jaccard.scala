/**
 *
 * students: please put your implementation in this file!
 */
package edu.gatech.cse6250.jaccard

import edu.gatech.cse6250.model._
import edu.gatech.cse6250.model.{ EdgeProperty, VertexProperty }
import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD

object Jaccard {

  def jaccardSimilarityOneVsAll(graph: Graph[VertexProperty, EdgeProperty], patientID: Long): List[Long] = {
    /**
     * Given a patient ID, compute the Jaccard similarity w.r.t. to all other patients.
     * Return a List of top 10 patient IDs ordered by the highest to the lowest similarity.
     * For ties, random order is okay. The given patientID should be excluded from the result.
     */

    /** Remove this placeholder and implement your code */
    val neighborEvents = graph.collectNeighborIds(EdgeDirection.Out)

    val allpatientneighbor = neighborEvents.filter(f => f._1.toLong <= 1000 & f._1.toLong != patientID)

    val thispatientneighborset = neighborEvents.filter(f => f._1.toLong == patientID).map(f => f._2).flatMap(f => f).collect().toSet

    val patientscore = allpatientneighbor.map(f => (f._1, jaccard(thispatientneighborset, f._2.toSet)))

    patientscore.takeOrdered(10)(Ordering[Double].reverse.on(x => x._2)).map(_._1.toLong).toList
  }

  def jaccardSimilarityAllPatients(graph: Graph[VertexProperty, EdgeProperty]): RDD[(Long, Long, Double)] = {
    /**
     * Given a patient, med, diag, lab graph, calculate pairwise similarity between all
     * patients. Return a RDD of (patient-1-id, patient-2-id, similarity) where
     * patient-1-id < patient-2-id to avoid duplications
     */

    /** Remove this placeholder and implement your code */
    val sc = graph.edges.sparkContext
    val neighborEvents = graph.collectNeighborIds(EdgeDirection.Out)

    val allpatientneighbor = neighborEvents.filter(f => f._1.toLong <= 1000)
    val cartesianneighbor = allpatientneighbor.cartesian(allpatientneighbor).filter(f => f._1._1 < f._2._1)
    cartesianneighbor.map(f => (f._1._1, f._2._1, jaccard(f._1._2.toSet, f._2._2.toSet)))
  }

  def jaccard[A](a: Set[A], b: Set[A]): Double = {
    /**
     * Helper function
     *
     * Given two sets, compute its Jaccard similarity and return its result.
     * If the union part is zero, then return 0.
     */

    /** Remove this placeholder and implement your code */
    if (a.isEmpty || b.isEmpty) { return 0.0 }
    a.intersect(b).size / a.union(b).size.toDouble
  }
}
