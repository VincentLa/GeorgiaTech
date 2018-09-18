package edu.gatech.cse6250.phenotyping

import java.text.SimpleDateFormat

import edu.gatech.cse6250.helper.SparkHelper.sparkMasterURL
import edu.gatech.cse6250.model.{ Diagnostic, LabResult, Medication }
import edu.gatech.cse6250.util.LocalClusterSparkContext
import edu.gatech.cse6250.helper.{ CSVHelper, SparkHelper }
import edu.gatech.cse6250.main.Main
import org.apache.spark.{ SparkConf, SparkContext }
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{ SQLContext, SparkSession }
import org.scalatest.{ BeforeAndAfter, FlatSpec, FunSuite, Matchers }
import org.scalatest.concurrent.TimeLimitedTests
import org.scalatest.time.{ Seconds, Span }
import org.apache.log4j.{ Level, Logger }

/**
 * @author Sungtae An <stan84@gatech.edu>.
 */
class T2dmPhenotypeTest extends FlatSpec with BeforeAndAfter with Matchers {
  var spark: SparkSession = _

  before {
    Logger.getRootLogger.setLevel(Level.WARN)
    Logger.getLogger("org").setLevel(Level.WARN)
    spark = SparkHelper.createSparkSession(appName = "Test PheKBPhenotype")
  }

  after {
    spark.stop()
  }

  "transform" should "give expected results" in {
    val sqlContext = spark.sqlContext
    val (med, lab, diag) = Main.loadRddRawData(spark)
    val rdd = T2dmPhenotype.transform(med, lab, diag)
    val cases = rdd.filter { case (x, t) => t == 1 }.map { case (x, t) => x }.collect.toSet
    val controls = rdd.filter { case (x, t) => t == 2 }.map { case (x, t) => x }.collect.toSet
    val others = rdd.filter { case (x, t) => t == 3 }.map { case (x, t) => x }.collect.toSet
    cases.size should be(427 + 255 + 294)
    controls.size should be(948)
    others.size should be(3688 - cases.size - controls.size)
  }

}
