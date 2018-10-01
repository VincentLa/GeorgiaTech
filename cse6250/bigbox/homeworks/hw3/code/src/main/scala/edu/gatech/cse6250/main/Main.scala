/*
To all the code, run: sbt compile run
Discussion of Purity Results: https://piazza.com/class/jjjilbkqk8m1r4?cid=626
*/

package edu.gatech.cse6250.main

import java.text.SimpleDateFormat

import edu.gatech.cse6250.clustering.Metrics
import edu.gatech.cse6250.features.FeatureConstruction
import edu.gatech.cse6250.helper.{ CSVHelper, SparkHelper }
import edu.gatech.cse6250.model.{ Diagnostic, LabResult, Medication }
import edu.gatech.cse6250.phenotyping.T2dmPhenotype
import org.apache.spark.mllib.clustering.{ GaussianMixture, KMeans, StreamingKMeans }
import org.apache.spark.mllib.feature.StandardScaler
import org.apache.spark.mllib.linalg.{ DenseMatrix, Matrices, Vector, Vectors }
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession

import scala.io.Source

/**
 * @author Hang Su <hangsu@gatech.edu>,
 * @author Yu Jing <yjing43@gatech.edu>,
 * @author Ming Liu <mliu302@gatech.edu>
 */
object Main {
  def main(args: Array[String]) {
    import org.apache.log4j.{ Level, Logger }

    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)

    val spark = SparkHelper.spark
    val sc = spark.sparkContext
    //  val sqlContext = spark.sqlContext

    /** initialize loading of data */
    val (medication, labResult, diagnostic) = loadRddRawData(spark)
    val (candidateMedication, candidateLab, candidateDiagnostic) = loadLocalRawData

    /** conduct phenotyping */
    val phenotypeLabel = T2dmPhenotype.transform(medication, labResult, diagnostic)

    /** feature construction with all features */
    val featureTuples = sc.union(
      FeatureConstruction.constructDiagnosticFeatureTuple(diagnostic),
      FeatureConstruction.constructLabFeatureTuple(labResult),
      FeatureConstruction.constructMedicationFeatureTuple(medication)
    )

    // =========== USED FOR AUTO GRADING CLUSTERING GRADING =============
    // phenotypeLabel.map{ case(a,b) => s"$a\t$b" }.saveAsTextFile("data/phenotypeLabel")
    // featureTuples.map{ case((a,b),c) => s"$a\t$b\t$c" }.saveAsTextFile("data/featureTuples")
    // return
    // ==================================================================

    val rawFeatures = FeatureConstruction.construct(sc, featureTuples)

    val (kMeansPurity, gaussianMixturePurity, streamingPurity) = testClustering(phenotypeLabel, rawFeatures)
    println(f"[All feature] purity of kMeans is: $kMeansPurity%.5f")
    println(f"[All feature] purity of GMM is: $gaussianMixturePurity%.5f")
    println(f"[All feature] purity of StreamingKmeans is: $streamingPurity%.5f")

    /** feature construction with filtered features */
    val filteredFeatureTuples = sc.union(
      FeatureConstruction.constructDiagnosticFeatureTuple(diagnostic, candidateDiagnostic),
      FeatureConstruction.constructLabFeatureTuple(labResult, candidateLab),
      FeatureConstruction.constructMedicationFeatureTuple(medication, candidateMedication)
    )

    val filteredRawFeatures = FeatureConstruction.construct(sc, filteredFeatureTuples)

    val (kMeansPurity2, gaussianMixturePurity2, streamingPurity2) = testClustering(phenotypeLabel, filteredRawFeatures)
    println(f"[Filtered feature] purity of kMeans is: $kMeansPurity2%.5f")
    println(f"[Filtered feature] purity of GMM is: $gaussianMixturePurity2%.5f")
    println(f"[Filtered feature] purity of StreamingKmeans is: $streamingPurity2%.5f")
  }

  def testClustering(phenotypeLabel: RDD[(String, Int)], rawFeatures: RDD[(String, Vector)]): (Double, Double, Double) = {
    import org.apache.spark.mllib.linalg.Matrix
    import org.apache.spark.mllib.linalg.distributed.RowMatrix

    println("phenotypeLabel: " + phenotypeLabel.count)
    /** scale features */
    val scaler = new StandardScaler(withMean = true, withStd = true).fit(rawFeatures.map(_._2))
    val features = rawFeatures.map({ case (patientID, featureVector) => (patientID, scaler.transform(Vectors.dense(featureVector.toArray))) })
    println("features: " + features.count)
    val rawFeatureVectors = features.map(_._2).cache()
    println("rawFeatureVectors: " + rawFeatureVectors.count)

    /** reduce dimension */
    val mat: RowMatrix = new RowMatrix(rawFeatureVectors)
    val pc: Matrix = mat.computePrincipalComponents(10) // Principal components are stored in a local dense matrix.
    val featureVectors = mat.multiply(pc).rows

    val densePc = Matrices.dense(pc.numRows, pc.numCols, pc.toArray).asInstanceOf[DenseMatrix]

    def transform(feature: Vector): Vector = {
      val scaled = scaler.transform(Vectors.dense(feature.toArray))
      Vectors.dense(Matrices.dense(1, scaled.size, scaled.toArray).multiply(densePc).toArray)
    }

    // Setting value of K
    val k = 5;

    /**
     * TODO: K Means Clustering using spark mllib
     * Train a k means model using the variabe featureVectors as input
     * Set maxIterations =20 and seed as 6250L
     * Assign each feature vector to a cluster(predicted Class)
     * Obtain an RDD[(Int, Int)] of the form (cluster number, RealClass)
     * Find Purity using that RDD as an input to Metrics.purity
     * Remove the placeholder below after your implementation
     */

    val phenotype_labels = phenotypeLabel.map(_._2).zipWithIndex.map(x => (x._2, x._1)).cache()
    
    val k_clusters = KMeans.train(featureVectors, k, 20, "k-means||", 6250L).predict(featureVectors)
      .zipWithIndex
      .map(x => (x._2, x._1))

    // Join phenotype_labels
    val toPurity = phenotype_labels.join(k_clusters).map(_._2)
    //

    /*
    This section is only for printing results for 2.3.b

    Can comment out if not needed to run.
    */
    // var kTable = toPurity
    //   .filter(x => x._2 == 0)
    //   .map(x => x._1)
    //   .countByValue()

    // println("KMeans Table Printed Below:")
    // println(kTable.toString)

    // kTable = toPurity
    //   .filter(x => x._2 == 1)
    //   .map(x => x._1)
    //   .countByValue()
    // println(kTable.toString)

    // kTable = toPurity
    //   .filter(x => x._2 == 2)
    //   .map(x => x._1)
    //   .countByValue()
    // println(kTable.toString)
    /* End section for printing results for 2.3.b*/

    val kMeansPurity = Metrics.purity(toPurity)

    /**
     * TODO: GMMM Clustering using spark mllib
     * Train a Gaussian Mixture model using the variabe featureVectors as input
     * Set maxIterations =20 and seed as 6250L
     * Assign each feature vector to a cluster(predicted Class)
     * Obtain an RDD[(Int, Int)] of the form (cluster number, RealClass)
     * Find Purity using that RDD as an input to Metrics.purity
     * Remove the placeholder below after your implementation
     */
    val g_clusters = new GaussianMixture()
      .setK(k)
      .setMaxIterations(20)
      .setSeed(6250L)
      .run(featureVectors)
      .predict(featureVectors)
      .zipWithIndex
      .map(x => (x._2, x._1))

    // Join phenotype_labels
    val toPurityG = phenotype_labels.join(g_clusters).map(_._2)

    /*
    This section is only for printing results for 2.4.b

    Can comment out if not needed to run.
    */
    // var gTable = toPurityG
    //   .filter(x => x._2 == 0)
    //   .map(x => x._1)
    //   .countByValue()

    // println("GMM Table Printed Below:")
    // println(gTable.toString)

    // gTable = toPurityG
    //   .filter(x => x._2 == 1)
    //   .map(x => x._1)
    //   .countByValue()
    // println(gTable.toString)

    // gTable = toPurityG
    //   .filter(x => x._2 == 2)
    //   .map(x => x._1)
    //   .countByValue()
    // println(gTable.toString)
    /* End section to print results for 2.4.b*/

    val gaussianMixturePurity = Metrics.purity(toPurityG)

    /**
     * TODO: StreamingKMeans Clustering using spark mllib
     * Train a StreamingKMeans model using the variabe featureVectors as input
     * Set the number of cluster K = 3, DecayFactor = 1.0, number of dimensions = 10, weight for each center = 0.5, seed as 6250L
     * In order to feed RDD[Vector] please use latestModel, see more info: https://spark.apache.org/docs/2.2.0/api/scala/index.html#org.apache.spark.mllib.clustering.StreamingKMeans
     * To run your model, set time unit as 'points'
     * Assign each feature vector to a cluster(predicted Class)
     * Obtain an RDD[(Int, Int)] of the form (cluster number, RealClass)
     * Find Purity using that RDD as an input to Metrics.purity
     * Remove the placeholder below after your implementation
     */
    val streamKmeansPurity = 0.0

    (kMeansPurity, gaussianMixturePurity, streamKmeansPurity)
  }

  /**
   * load the sets of string for filtering of medication
   * lab result and diagnostics
   *
   * @return
   */
  def loadLocalRawData: (Set[String], Set[String], Set[String]) = {
    val candidateMedication = Source.fromFile("data/med_filter.txt").getLines().map(_.toLowerCase).toSet[String]
    val candidateLab = Source.fromFile("data/lab_filter.txt").getLines().map(_.toLowerCase).toSet[String]
    val candidateDiagnostic = Source.fromFile("data/icd9_filter.txt").getLines().map(_.toLowerCase).toSet[String]
    (candidateMedication, candidateLab, candidateDiagnostic)
  }

  def sqlDateParser(input: String, pattern: String = "yyyy-MM-dd'T'HH:mm:ssX"): java.sql.Date = {
    val dateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssX")
    new java.sql.Date(dateFormat.parse(input).getTime)
  }

  def loadRddRawData(spark: SparkSession): (RDD[Medication], RDD[LabResult], RDD[Diagnostic]) = {
    /* the sql queries in spark required to import sparkSession.implicits._ */
    import spark.implicits._
    val sqlContext = spark.sqlContext

    /* a helper function sqlDateParser may useful here */

    /**
     * load data using Spark SQL into three RDDs and return them
     * Hint:
     * You can utilize edu.gatech.cse6250.helper.CSVHelper
     * through your sparkSession.
     *
     * This guide may helps: https://bit.ly/2xnrVnA
     *
     * Notes:Refer to model/models.scala for the shape of Medication, LabResult, Diagnostic data type.
     * Be careful when you deal with String and numbers in String type.
     * Ignore lab results with missing (empty or NaN) values when these are read in.
     * For dates, use Date_Resulted for labResults and Order_Date for medication.
     *
     */
    val medication_data = CSVHelper.loadCSVAsTable(spark, "data/medication_orders_INPUT.csv", "medicationdata")
    val lab_result_data = CSVHelper.loadCSVAsTable(spark, "data/lab_results_INPUT.csv", "labresultdata")
    val id_data = CSVHelper.loadCSVAsTable(spark, "data/encounter_INPUT.csv", "iddata")
    val diagnosesdata = CSVHelper.loadCSVAsTable(spark, "data/encounter_dx_INPUT.csv", "diagnosesdata")

    /**
     * load data using Spark SQL into three RDDs and return them
     */

    val RDDrowmed = sqlContext.sql("SELECT Member_ID AS patientID, Order_Date AS date, Drug_Name AS medicine  FROM medicationdata").orderBy("date")
    val RDDrowdiag = sqlContext.sql("SELECT iddata.Member_ID AS patientID, iddata.Encounter_DateTime AS date, diagnosesdata.code AS code  FROM iddata INNER JOIN diagnosesdata ON iddata.Encounter_ID= diagnosesdata.Encounter_ID").orderBy("date")
    val RDDrowlab = sqlContext.sql("SELECT Member_ID AS patientID, Date_Resulted AS date, Result_Name AS testName, Numeric_Result as value  FROM labresultdata WHERE Numeric_Result!=''").orderBy("date")
    val medication: RDD[Medication] = RDDrowmed.rdd.map(p => Medication(p(0).asInstanceOf[String], sqlDateParser(p(1).asInstanceOf[String]), p(2).asInstanceOf[String].toLowerCase))
    val labResult: RDD[LabResult] = RDDrowlab.rdd.map(p => LabResult(p(0).asInstanceOf[String], sqlDateParser(p(1).asInstanceOf[String]), p(2).asInstanceOf[String].toLowerCase, p(3).asInstanceOf[String].filterNot(",".toSet).toDouble))
    val diagnostic: RDD[Diagnostic] = RDDrowdiag.rdd.map(p => Diagnostic(p(0).asInstanceOf[String], sqlDateParser(p(1).asInstanceOf[String]), p(2).asInstanceOf[String].toLowerCase))

    (medication, labResult, diagnostic)
  }

}
