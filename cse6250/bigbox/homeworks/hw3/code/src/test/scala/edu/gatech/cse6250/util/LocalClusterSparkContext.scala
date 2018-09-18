package edu.gatech.cse6250.util

import org.apache.log4j.{ Level, Logger }
import org.apache.spark.{ SparkConf, SparkContext }
import org.scalatest.{ BeforeAndAfterAll, Suite }

/**
 * @author Hang Su <hangsu@gatech.edu>.
 */
trait LocalClusterSparkContext extends BeforeAndAfterAll {
  self: Suite =>
  @transient var sc: SparkContext = _

  override def beforeAll() {
    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)

    val conf = new SparkConf()
      .setMaster("local[2]")
      .setAppName("test-cluster")
      .set("spark.rpc.message.maxSize", "1") // set to 1MB to detect direct serialization of data
    // .set("spark.akka.frameSize", "1")
    // Warning Message:
    // The configuration key 'spark.akka.frameSize' has been deprecated as of
    // Spark 1.6 and may be removed in the future.
    // Please use the new key 'spark.rpc.message.maxSize' instead.
    sc = new SparkContext(conf)
    super.beforeAll()
  }

  override def afterAll() {
    if (sc != null) {
      sc.stop()
    }
    super.afterAll()
  }
}
