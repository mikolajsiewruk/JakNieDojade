library(ggplot2)
op <- par(oma=c(5,7,1,1))
file <- "D:\\PyCharm\\PyCharm 2023.2.4\\JakNieDojade\\Stops_by_area_5_new.csv"

data <- read.csv(file,fileEncoding = "UTF-8")

categories <- as.vector(colnames(data))
areas <- as.vector(data$AREA)
stopcount <- as.vector(data$Stops)
areas
stopcount

frame <- data.frame(x=areas,y=stopcount)
frame <- frame[order(frame$y, decreasing = TRUE), ]
ggplot(frame,aes(x = reorder(x,y),y = y))+
  geom_segment( aes(x=x, xend=x, y=0, yend=y), color="grey") +
  geom_point( color="orange", size=4) +
  geom_text(aes(label = y), vjust = -0.75, size = 3) +
  theme_light() +
  theme(
    panel.grid.major.x = element_blank(),
    panel.border = element_blank(),
    axis.ticks.x = element_blank(),
    axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0,size = 16)
  ) +
  xlab("") +
  ylab("Number of stops")+
  scale_y_continuous(breaks = seq(0, 50, by = 5))
par(op)