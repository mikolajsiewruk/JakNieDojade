file <- 'D:\\PyCharm\\PyCharm 2023.2.4\\JakNieDojade\\Stop_functions_new.csv'
op <- par(oma=c(5,7,1,1))
data <- read.csv(file)

counts <-c()
headers <- as.vector(colnames(data))

for (i in 1:length(headers)) {
    counts <- c(counts, data[[headers[i]]])
}
colors <- c("red", "green", "blue", "yellow", "orange", "purple", "pink", "brown", "cyan")

x <- barplot(counts, names.arg = headers, col = colors,ylim = c(0,500),main = "Number of stops per category in planned public transportation system")

text(x,counts+10,labels = as.character(counts))
par(op)