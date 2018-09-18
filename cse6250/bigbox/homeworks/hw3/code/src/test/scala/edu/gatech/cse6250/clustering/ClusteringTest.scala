package edu.gatech.cse6250.main

import edu.gatech.cse6250.util.LocalClusterSparkContext
import org.apache.spark.SparkContext
import org.apache.spark.mllib.linalg.{ Vector, Vectors }
import org.apache.spark.rdd.RDD
import org.scalatest.FunSuite
import org.scalatest.concurrent.TimeLimitedTests
import org.scalatest.time.{ Seconds, Span }

class ClusteringTest extends FunSuite with LocalClusterSparkContext with TimeLimitedTests {

  val timeLimit = Span(600, Seconds)

  type FeatureTuple = ((String, String), Double)

  /*
  test("phenotyping with your data loader") {
    // Load the data output from the solution code
    val phenotypeLabel = sc.textFile("data/phenotypeLabel/part-*").map(x => {
      val split = x.split("\t")
      (split(0), split(1).toInt)
    })
    val featureTuples = sc.textFile("data/featureTuples/part-*")
      .filter(_.substring(0,9).toInt % 17 == 0) // Downsample
      .map(x => {
        val split = x.split("\t")
        ((split(0), split(1)), split(2).toDouble).asInstanceOf[FeatureTuple]
      })

    // Convert tuples to vector using FeatureConstruction.construct solution
    val rawFeatures = construct(sc, featureTuples)

    // Run student test clustering code
    // val (kMeansPurity, gaussianMixturePurity, streamingPurity, nmfPurity) = Main.testClustering(phenotypeLabel, rawFeatures)

    // Run official solution clustering code just to check KMeans, GaussianMixture, and StreamingKMeans
    // ==========================================================================
    import org.apache.spark.mllib.linalg.Matrix
    import org.apache.spark.mllib.linalg.distributed.RowMatrix

    val scaler = new StandardScaler(withMean = true, withStd = true).fit(rawFeatures.map(_._2))
    val features = rawFeatures.map({ case (patientID, featureVector) => (patientID, scaler.transform(Vectors.dense(featureVector.toArray)))})
    val rawFeatureVectors = features.map(_._2).cache()
    // reduce dimension
    val mat: RowMatrix = new RowMatrix(rawFeatureVectors)
    val pc: Matrix = mat.computePrincipalComponents(10) // Principal components are stored in a local dense matrix.
    val featureVectors = mat.multiply(pc).rows
    val densePc = Matrices.dense(pc.numRows, pc.numCols, pc.toArray).asInstanceOf[DenseMatrix]

    // , scaler: StandardScalerModel, densePc: DenseMatrix
    val transform = (feature: Vector) => {
      val scaled = scaler.transform(Vectors.dense(feature.toArray))
      Vectors.dense(Matrices.dense(1, scaled.size, scaled.toArray).multiply(densePc).toArray)
    }

    // let's train a k-means model from mllib
    val kMeansModel = KMeans.train(featureVectors,3,20,1,"k-means||",8803L)
    val kMeansClusterAssignmentAndLabel = features.join(phenotypeLabel).map({ case (patientID, (feature, realClass)) => (kMeansModel.predict(transform(feature)), realClass)})
    val kMeansPurity = purity(kMeansClusterAssignmentAndLabel)
    // let's train a gmm model from mllib
    val gaussianMixtureModel = new GaussianMixture().setK(3).setSeed(8803L).run(featureVectors)
    val rddOfVectors = features.join(phenotypeLabel).map({ case (patientID, (feature, realClass)) => transform(feature)})
    val labels = features.join(phenotypeLabel).map({ case (patientID, (feature, realClass)) => realClass})
    val gaussianMixtureClusterAssignmentAndLabel = gaussianMixtureModel.predict(rddOfVectors).zip(labels)
    //val gaussianMixtureClusterAssignmentAndLabel = features.join(phenotypeLabel).map({ case (patientID, (feature, realClass)) => (gaussianMixtureModel.predict(feature), realClass)})
    val gaussianMixturePurity = purity(gaussianMixtureClusterAssignmentAndLabel)
    //let's train a streamingKmeans model from mllib
    val streamingKmeansModel = new StreamingKMeans().setK(3).setDecayFactor(1.0).setRandomCenters(10,0.5,8803L).latestModel().update(featureVectors,1.0,"points")
    val streamingClusterAssignmentAndLabel = features.join(phenotypeLabel).map({case (patientID, (feature, realClass)) => (streamingKmeansModel.predict(transform(feature)), realClass)})
    val streamingPurity = purity(streamingClusterAssignmentAndLabel)
    // ==========================================================================

    println(s"kMeansPurity: $kMeansPurity")
    println(s"gaussianMixturePurity: $gaussianMixturePurity")
    println(s"streamingPurity: $streamingPurity")

    // Grade student clustering
    val scoreKmm = 3
    val scoreGmm = 1
    val scoreStreaming = 0

    println(s"FOR_PARSE Q23\t$scoreKmm\tTest Data Purity: $kMeansPurity")
    println(s"FOR_PARSE Q24\t$scoreGmm\tTest Data Purity: $gaussianMixturePurity")
    println(s"FOR_PARSE Q25\t$scoreStreaming\tTest Data Purity: $streamingPurity")
  }
  */

  def construct(sc: SparkContext, feature: RDD[FeatureTuple]): RDD[(String, Vector)] = {
    // save for later usage
    feature.cache()
    val feature_names = feature.map(t => t._1._2).distinct()
    val feature_num = feature_names.count().toInt
    val feat_idx_map = feature_names.zipWithIndex
    val fat_table = feature.map(t => (t._1._2, (t._1._1, t._2))).join(feat_idx_map)
    val idxed_features = fat_table.map(t => (t._2._1._1, (t._2._2.toInt, t._2._1._2)))
    val grouped_features = idxed_features.groupByKey()
    val result = grouped_features.map(t => (t._1, Vectors.sparse(feature_num, t._2.map(r => r._1).toArray, t._2.map(r => r._2).toArray)))
    result
  }

  def purity(clusterAssignmentAndLabel: RDD[(Int, Int)]): Double = {
    val N = clusterAssignmentAndLabel.count()
    val tmp = clusterAssignmentAndLabel.map(p => ((p._1, p._2), 1.0))
      .reduceByKey(_ + _)
      .map(p => (p._1._1, p._2))
      .reduceByKey((x, y) => Math.max(x, y))
      .map(_._2)
      .reduce(_ + _)
    1.0 * tmp / N
  }

}
