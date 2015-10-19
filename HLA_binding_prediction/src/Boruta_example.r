set.seed(777);
#Add some nonsense attributes to iris dataset by shuffling original attributes
iris.extended<-data.frame(iris,apply(iris[,-5],2,sample));
names(iris.extended)[6:9]<-paste("Nonsense",1:4,sep="");
#Run Boruta on this data
Boruta(Species~.,data=iris.extended,doTrace=2)->Boruta.iris.extended
#Nonsense attributes should be rejected
print(Boruta.iris.extended);

#Boruta using rFerns' importance
Boruta(Species~.,data=iris.extended,getImp=getImpFerns)->Boruta.ferns.irisE
print(Boruta.ferns.irisE);

## Not run: 
#Boruta on the HouseVotes84 data from mlbench
library(mlbench); data(HouseVotes84);
na.omit(HouseVotes84)->hvo;
#Takes some time, so be patient
Boruta(Class~.,data=hvo,doTrace=2)->Bor.hvo;
print(Bor.hvo);
plot(Bor.hvo);
plotImpHistory(Bor.hvo);

## End(Not run)
## Not run: 
#Boruta on the Ozone data from mlbench
library(mlbench); data(Ozone);
library(randomForest);
na.omit(Ozone)->ozo;
Boruta(V4~.,data=ozo,doTrace=2)->Bor.ozo;
cat('Random forest run on all attributes:\n');
print(randomForest(V4~.,data=ozo));
cat('Random forest run only on confirmed attributes:\n');
print(randomForest(ozo[,getSelectedAttributes(Bor.ozo)],ozo$V4));

## End(Not run)
## Not run: 
#Boruta on the Sonar data from mlbench
library(mlbench); data(Sonar);
#Takes some time, so be patient
Boruta(Class~.,data=Sonar,doTrace=2)->Bor.son;
print(Bor.son);
#Shows important bands
plot(Bor.son,sort=FALSE);
xdx <- names(Bor.son$finalDecision[Bor.son$finalDecision != "Rejected"])
#Sonar[,xdx]
Sonar[,xdx]
df = Sonar[c(xdx,'Class')]
m1 <- glm(Class ~ ., family = poisson, data = df)
## End(Not run)