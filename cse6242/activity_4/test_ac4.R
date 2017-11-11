# Activity: Time Series Analysis - Unit Tests

library(testthat)

context("Time Series Analysis")  # set a context for testing

options(run.main=FALSE)  # suppress running "main" block
source("ac4.R")  # load functions to be tested
options(run.main=TRUE)  # revert back to running "main" block

# Define common variables and utility functions
data_dir <- "data"
label_dir <- "labeled_windows"

# Make sure load() works as expected
test_that("load_ts() returns a time series", {
    csv_filename <- "realAWSCloudwatch/ec2_cpu_utilization_5f5533.csv"

    expect_silent(s <- load_ts(paste(data_dir, csv_filename, sep="/")))
    expect_is(s, "xts")
    expect_length(s, 4032)
})

# Make sure find_anomalies() works as expected
test_that("find_anomalies() returns valid results", {
    csv_filename <- "realAWSCloudwatch/ec2_cpu_utilization_5f5533.csv"
    window_size <- 864  # 3 days * samples_per_day
    threshold <- 4  # 4 s.d. away from mean
    s <- load_ts(paste(data_dir, csv_filename, sep="/"))  # load data (will fail if load_ts isn't good)

    expect_silent(res <- find_anomalies(s, window_size=window_size, threshold=threshold))
    expect_named(res, c("s", "window_size", "threshold", "s.mean", "s.sd", "anomalies"), ignore.order=TRUE)
    expect_equal(res$s, s)
    expect_equal(res$window_size, window_size)
    expect_equal(res$threshold, threshold)
    expect_equal(length(res$s.mean), length(s))
    expect_equal(length(res$s.sd), length(s))
})

# Finally, run find_anomalies() on a few test inputs and check for approximate match
debug <- FALSE  # turn on debug to print diagnostic values instead of running actual assertions
test_cases <- rbind.data.frame(
    data.frame(csv_filename = "realAWSCloudwatch/ec2_cpu_utilization_5f5533.csv", window_size = 800, threshold = 3.5),
    data.frame(csv_filename = "realAWSCloudwatch/ec2_network_in_257a54.csv", window_size = 1200, threshold = 8),
    data.frame(csv_filename = "realTraffic/speed_6005.csv", window_size = 800, threshold = 6.5)
)
if(debug) {
    cat("[DEBUG] Test cases:", end="\n")
    print(test_cases)
}
for(t in 1:nrow(test_cases)) {
    # Prepare test case
    csv_filename <- test_cases$csv_filename[[t]]
    window_size <- test_cases$window_size[[t]]
    threshold <- test_cases$threshold[[t]]
    s <- load_ts(paste(data_dir, csv_filename, sep="/"))  # load data (will fail if load_ts isn't good)
    w <- read.csv(paste(label_dir, csv_filename, sep="/"), stringsAsFactors=FALSE)  # ground truth windows
    w$beg <- as.POSIXct(w$beg)
    w$end <- as.POSIXct(w$end)

    test_that(paste("find_anomalies() in", csv_filename), {        
        res <- find_anomalies(s, window_size=window_size, threshold=threshold)

        # Find matches in ground-truth windows
        num_reported <- length(res$anomalies)
        num_false <- 0  # false positives (i.e. outside any window)
        hits <- integer(nrow(w))  # detections within each window
        if(nrow(w) > 0 && num_reported > 0) {
            for(i in 1:num_reported) {
                timestamp <- index(res$anomalies[i])
                matched <- FALSE
                for(j in 1:nrow(w)) {
                    if(w$beg[j] <= timestamp & timestamp <= w$end[j]) {
                        hits[j] <- hits[j] + 1
                        matched <- TRUE
                        break
                    }
                }
                if(!matched) {
                    num_false <- num_false + 1
                }
            }
        }
        num_hits <- sum(hits)  # total hits
        num_unique <- sum(hits > 0)  # unique hits (i.e. one per detected window)
        num_dupes <- num_hits - num_unique  # duplicate hits
        num_missed <- nrow(w) - num_unique  # windows completely missed
        
        # Check if performance is within expected bounds
        if(debug) {
            cat(paste("[DEBUG] find_anomalies() in", csv_filename), end="\n")
            cat(paste(nrow(w), " true anomaly windows; ", num_reported, " anomalies reported: ",
                num_unique, " unique, ", num_dupes, " duplicate, ", num_false, " false positive(s), ",
                num_missed, " missed", sep=""), end="\n")  # [debug]
            visualize(res, wins=w, title=paste("Anomaly Detection Results", csv_filename, sep="\n"))
        } else {
            expect_gte(num_unique, 0.75 * nrow(w), label="Accuracy", expected.label="75%")  # accuracy is at least 75%
            expect_lte(num_false, 0.5 * num_reported, label="False positive rate", expected.label="50%")  # false positive rate is at most 50%
            expect_lte(num_dupes, 0.75 * num_reported, label="Duplicate rate", expected.label="75%")  # duplicate rate is at most 75%
        }
    })
}
