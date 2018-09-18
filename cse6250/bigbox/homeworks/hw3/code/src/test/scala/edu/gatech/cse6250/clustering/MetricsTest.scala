package edu.gatech.cse6250.clustering

import edu.gatech.cse6250.util.LocalClusterSparkContext
import org.scalatest.{ BeforeAndAfter, FunSuite }
import org.scalatest.concurrent.TimeLimitedTests
import org.scalatest.time.{ Seconds, Span }

class MetricsTest extends FunSuite with LocalClusterSparkContext with TimeLimitedTests with BeforeAndAfter {

  val timeLimit = Span(60, Seconds)

  def makeCases(c: Int, t: Int, count: Int): Seq[(Int, Int)] = {
    (1 to count).map(_ => (c, t))
  }

  test("Testing your metrics purity calculation") {
    val testInput1 = sc.parallelize(Seq.concat(
      makeCases(1, 1, 0), // diamond
      makeCases(1, 2, 1), // circle
      makeCases(1, 3, 5), // cross
      makeCases(2, 1, 1),
      makeCases(2, 2, 4),
      makeCases(2, 3, 1),
      makeCases(3, 1, 3),
      makeCases(3, 2, 0),
      makeCases(3, 3, 2)))

    val testInput2 = sc.parallelize(Seq.concat(
      makeCases(1, 1, 0), // diamond
      makeCases(1, 2, 53), // circle
      makeCases(1, 3, 10), // cross
      makeCases(2, 1, 0),
      makeCases(2, 2, 1),
      makeCases(2, 3, 60),
      makeCases(3, 1, 0),
      makeCases(3, 2, 16),
      makeCases(3, 3, 0)))

    val studentPurity1 = Metrics.purity(testInput1)
    val rightAnswer1 = (5 + 4 + 3) / 17.0
    val passed1 = if (studentPurity1 == rightAnswer1) 1 else 0

    assert(passed1 == 1)

    val studentPurity2 = Metrics.purity(testInput2)
    val rightAnswer2 = (53 + 60 + 16) / 140.0
    val passed2 = if (studentPurity2 == rightAnswer2) 1 else 0

    assert(passed2 == 1)

    val passedTests = passed1 + passed2
    val scoreMetrics = 4.0 * passedTests

    println(s"FOR_PARSE Q22\t$scoreMetrics\tTests Passed: $passedTests")
  }
}
