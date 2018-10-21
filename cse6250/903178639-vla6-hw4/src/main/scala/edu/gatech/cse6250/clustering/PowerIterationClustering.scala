/**
 * @author Sungtae An <stan84@gatech.edu>.
 */

package edu.gatech.cse6250.clustering

import org.apache.spark.rdd.RDD
import org.apache.spark.mllib.clustering.{ PowerIterationClustering => PIC }

/**
 * Power Iteration Clustering (PIC), a scalable graph clustering algorithm developed by
 * [[http://www.icml2010.org/papers/387.pdf Lin and Cohen]]. From the abstract: PIC finds a very
 * low-dimensional embedding of a dataset using truncated power iteration on a normalized pair-wise
 * similarity matrix of the data.
 *
 * @see [[http://en.wikipedia.org/wiki/Spectral_clustering Spectral clustering (Wikipedia)]]
 */

object PowerIterationClustering {

  /**
   * run PIC using Spark's PowerIterationClustering implementation
   *
   * @input: All pair similarities in the shape of RDD[(patientID1, patientID2, similarity)]
   * @return: Cluster assignment for each patient in the shape of RDD[(PatientID, Cluster)]
   *
   */
  def runPIC(similarities: RDD[(Long, Long, Double)]): RDD[(Long, Int)] = {
    // According to Instructions in HW we use 3 Clusters and 100 for Max Iterations
    // See http://spark.apache.org/docs/1.3.1/mllib-clustering.html#power-iteration-clustering-pic for instructions
    val power_iteration_clustering = new PIC().setK(3).setMaxIterations(100)
    val pic_run = power_iteration_clustering.run(similarities)
    pic_run.assignments.map(f => (f.id, f.cluster))
  }
}
