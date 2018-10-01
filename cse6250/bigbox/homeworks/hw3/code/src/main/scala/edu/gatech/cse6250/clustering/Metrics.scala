/**
 * @author Hang Su <hangsu@gatech.edu>.
 */

package edu.gatech.cse6250.clustering

import org.apache.spark.rdd.RDD

object Metrics {
  /**
   * Given input RDD with tuples of assigned cluster id by clustering,
   * and corresponding real class. Calculate the purity of clustering.
   * Purity is defined as
   * \fract{1}{N}\sum_K max_j |w_k \cap c_j|
   * where N is the number of samples, K is number of clusters and j
   * is index of class. w_k denotes the set of samples in k-th cluster
   * and c_j denotes set of samples of class j.
   *
   * @param clusterAssignmentAndLabel RDD in the tuple format
   *                                  (assigned_cluster_id, class)
   * @return
   */
  def purity(clusterAssignmentAndLabel: RDD[(Int, Int)]): Double = {
    val numSamples = clusterAssignmentAndLabel.count().toDouble

    def singleCluster(group: (Int, Iterable[(Int, Int)])): Double = {
      val output = group._2
        .groupBy(x => x._2) //group by class
        .map(x => x._2.map(z => 1.0).reduce(_ + _))
        .reduce((x, y) => x max y)

      output
    }

    val summation = clusterAssignmentAndLabel
      .map(x => (x._1, (x._1, x._2)))
      .groupByKey()
      .map(singleCluster)
      .reduce(_ + _)

    return summation / numSamples
  }
}
