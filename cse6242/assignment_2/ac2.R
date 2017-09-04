require(ggplot2)
data(midwest)

df = midwest[, c('PID', 'county', 'state', 'percprof')]
print(df)
summary(df)