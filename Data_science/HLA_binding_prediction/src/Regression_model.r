dat = read.csv("/Users/johnny/Desktop/IPIPAN_conf_paper/dataset/dataset_norm.csv", header = TRUE)

str(dat)
dat$IC50 <- round(dat$IC50)
summary(dat$IC50)
sum(dat$IC50 < 3)
dat$IC50[dat$IC50 != round(dat$IC50)]
tmp <- dat[(dat$IC50 < 45000) ,4:ncol(dat)]
str(tmp)
tmp$IC50 <- tmp$IC50
tmp
#m1 <- glm(IC50 ~ ., family = poisson, data = tmp)
#summary(m1)

