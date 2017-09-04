require(ggplot2)
data(midwest)

df = midwest[, c('PID', 'county', 'state', 'percprof')]
print(df)
summary(df)

ggplot(df, aes(x=percprof)) +
  geom_density(aes(color=state, group=state))