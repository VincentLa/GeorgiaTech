/**
 * @author Vincent La <vla6@gatech.edu>.
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
    val neighbors = graph.collectNeighborIds(EdgeDirection.Out)

    // https://piazza.com/class/jjjilbkqk8m1r4?cid=841
    // The <= 1000 filter is a hacky solution to get only patient id vertices since there are only 1000
    // patient ids in the data. Yes, this is hacky.
    val all_neighbors = neighbors.filter(f => f._1.toLong != patientID & f._1.toLong <= 1000)
    val current_patient_neighbors = neighbors.filter(f => f._1.toLong == patientID).map(f => f._2).flatMap(f => f).collect().toSet

    // Use Jaccard helper function to compute jaccard scores for patientid with all their neighbors
    val patient_jaccard_scores = all_neighbors.map(f => (f._1, jaccard(current_patient_neighbors, f._2.toSet)))

    // Return Top 10 Patient Ids using tadeOrdered Function
    patient_jaccard_scores.takeOrdered(10)(Ordering[Double].reverse.on(x => x._2)).map(_._1.toLong).toList
  }

  def jaccardSimilarityAllPatients(graph: Graph[VertexProperty, EdgeProperty]): RDD[(Long, Long, Double)] = {
    /**
     * Given a patient, med, diag, lab graph, calculate pairwise similarity between all
     * patients. Return a RDD of (patient-1-id, patient-2-id, similarity) where
     * patient-1-id < patient-2-id to avoid duplications
     */
    val neighbors = graph.collectNeighborIds(EdgeDirection.Out)
    val all_pairwise_neighbors = neighbors.cartesian(neighbors).filter(f => f._1._1 != f._2._1)
    all_pairwise_neighbors.map(f => (f._1._1, f._2._1, jaccard(f._1._2.toSet, f._2._2.toSet)))
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
