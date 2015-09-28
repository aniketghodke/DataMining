## Setting the library path
.libPaths("C:\\R\\library")

## Setting the data path
setwd("C:\\Data Mining\\HW2\\dataset")

##library(car)

## Reading the file
filename <- "dataset1.txt"
d <- read.csv(filename,header=FALSE,sep="\t")

## Giving the header to data so as to make life easy
names(d) <- c("x1","x2")

## Creating a Matrix with x1,x2,Cluster,Visited 
## Initially Cluster is set to 0 Indicating invalid clusters

## STEP1 : All the data objects are marked as visited = FALSE
x1 <- c()
x2 <- c()
clust <- c()

for (i in 1:length(d$x1)){
  x1 <- rbind(x1,d$x1[i])
  x2 <- rbind(x2,d$x2[i])
  clust <- rbind(clust,0)
}

## data is x1,x2,cluster it belongs to, and visited? 
data <- cbind(x1,x2,clust,FALSE)

## STEP2 : Setting eps and mincount
eps <- 0.7
mincount <- 5


## get_number_false: data --> Number of rows that are false 
get_number_false <- function(data){
  count <- 0 
  for(i in 1:nrow(data)){
    if(data[i,4] == FALSE){
      count <- count + 1
    }
  }
  return (count)
}


## get_dist: x1,x2,y1,y2 --> distance between 2 points
get_dist <- function(x1,x2,y1,y2){
  return (((x1-y1) ^2 + (x2-y2) ^ 2)^0.5)
}

## get_neighbours: x1point, x2point, data matrix, random_number,eps
##                 --> list of neighbours 
get_neighbours <- function(x1,x2,data,rand,eps){
  neighbours <- c()
  for(i in 1:nrow(data)){
    if(i != rand){
      if(get_dist(x1,x2,data[i,1],data[i,2]) <= eps)
        if(data[i,4] == FALSE)
          neighbours <- rbind(neighbours,i)
    }
  }
  return (neighbours)
}

## expandCluster: point, data, neighbours, C, eps, mincount
expandCluster<- function(point,data,neighbours,Clust,eps,mincount){
  eval.parent(substitute(data[point,3] <- Clust))
  i <- 1
  while(!is.na(neighbours[i])){
    ## if P' is not visited
    if(data[neighbours[i],4] == FALSE){
      ## mark P' as visited
      eval.parent(substitute(data[neighbours[i],4] <- TRUE))
      ## NeighborPts' = regionQuery(P', eps)
      new_neighbours <- c()
      new_neighbours <- get_neighbours(data[neighbours[i],1],
                                       data[neighbours[i],2],
                                       data,
                                       neighbours[i],
                                       eps)
      neighbours1 <- c()
      if(length(new_neighbours) >= mincount){
        neighbours <- union(neighbours,new_neighbours)
      }
    }
    ## if P' is not yet member of any cluster
    if(data[neighbours[i],3] == 0 && data[neighbours[i],4] == FALSE){
      eval.parent(substitute(data[neighbours[i],3] <- Clust))
    }
    cat("iterating", neighbours[i],"\n")
    i <- i + 1
  }
}



## Algo starts from here
cluster <- 1
row <- 1
while(get_number_false(data) > 0){
  ## get a random point p
  set.seed(19)
  while(TRUE){
    random_number <- sample(1:nrow(data),1,replace=FALSE)
    if(data[random_number,4] == 0){
      break;
    }
  }
  "while(TRUE){
  random_number <- row
  if(data[random_number,4] == FALSE){
  break;
  }else{
  row <- row + 1
  }
}"
##print(random_number)
## mark p as visited
data[random_number,4] <- TRUE

## NeighborPts = regionQuery(P, eps)
neighbours <- c()
neighbours <- get_neighbours(data[random_number,1],
                             data[random_number,2],
                             data,
                             random_number,
                             eps)
## if sizeof(NeighborPts) < MinPts
if(length(neighbours) < mincount){
  data[random_number,3] <- 0
}else{
  C <- random_number
  ## expandCluster(P, NeighborPts, C, eps, MinPts)
  
  expandCluster(random_number,data,neighbours,C,eps,mincount)
}
}


## Getting the unique number of clusters
## get_unique: list -> Unique number of elements in the list
get_unique <- function(list){
  return (unique(list))
}

## changing the colors from random to specific
color <- c()
cinitial <- 2
unique_colors <- c()
unique_colors <- get_unique(data[,3])
for(i in unique_colors){
  for(j in 1:nrow(data)){
    if(data[j,3] == i)
      data[j,3] <- cinitial
  }
  cinitial <- cinitial + 1
}


## Plotting the scatterplot: 
png("DataSet1_ScatterPlot_DBSCAN.png",bg="grey40")
plot(data[,1],data[,2],col=data[,3],
     xlab="X1",ylab="X2",main="Scatter Plot of x1 vs x2 for different Classes")
legend("topright",legend=unique(data[,3]),pch=c(1),col=unique(data[,3]))
dev.off()