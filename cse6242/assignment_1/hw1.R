# Assignment 1: http://cse6242.gatech.edu/fall-2017/hw1/

library(ggplot2)


get_familiar_with_r <- function(){
	#' This function is for the first part of assignment 1
	#' Run some code examples and observe results
	#' Briefly describe one insight you learned about R in your observations
	#' Illustrate with a sample code snippet and observed output
	
	# Hello World in R
	print('hello world')

	# Display data sets in ggplot 2 library
	# print(data(package = 'ggplot2'))

	# Working with factors
	current.season = factor('summer',
			  levels = c('summer', 'fall', 'winter', 'spring'),
			  ordered = TRUE) # Ordered factor
	print(current.season)
	print(levels(current.season))

	print('goodbye world')
}


log_gamma_loop <- function(n){
	#' Computes and returns the natural logarithm of the gamma value of a positive integer
	#' using an iterative loop
	#' log gamma is defined as ln((n-1)!) = ln(n-1) + ln(n-2) + ... + ln(1)
	
	sum = 0
	for (i in seq(n - 1, 1, by = -1)) {
		sum = sum + log(i)
	}
	return(sum)
}

log_gamma_recursive <- function(n){
	#' Computers and returns the natural logarith mof the gamma value of a positive integer
	#' using recursion
	#' log gamma is defined as ln((n-1)!) = ln(n-1) + ln(n-2) + ... + ln(1)
	
	# Can stop at n == 2 since n-1 = 1 and log(1) equals 0
	if (n == 2){
		return(0)
	} else {
		sum = log(n - 1) + log_gamma_recursive(n - 1)
		return(sum)
	}
}


sum_log_gamma_loop <- function(n){
	#' Uses log_gamma_loop defined above to sum the log Gamme results over the range 1 to n
	sum = 0

	# Start at 2 because log(1 - 1) is undefined
	for (i in seq(2, n, by = 1)) {
		sum = sum + log_gamma_loop(i)
	}
	return(sum)
}


sum_log_gamma_recursive <- function(n){
	#' Uses log_gamma_recursive defined above to sum the log Gamme results over the range 1 to n
	sum = 0
	
	# Start at 2 because log(1 - 1) is undefined
	for (i in seq(2, n, by = 1)) {
		sum = sum + log_gamma_recursive(i)
	}
	return(sum)
}



get_familiar_with_r()
log_gamma_loop(5)
log_gamma_recursive(5)
sum_log_gamma_loop(5)
sum_log_gamma_recursive(5)