dat = read.csv("~/dataset_norm.csv", header = TRUE)

tmp <- dat[1:1000,4:ncol(dat)]

library(Boruta)
library(rFerns)

tmp$IC50 <- cut(tmp$IC50, 10)
tmp$IC50

B1 <- Boruta(IC50 ~ ., data = tmp, doTrace = 2, getImp=getImpFerns)
print(B1)
