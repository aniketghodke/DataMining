## Setting the library path
.libPaths("C:\\R\\library")

## Setting the data path
setwd("C:\\Data Mining\\HW2\\dataset")

## Libraries
require(ggplot2)

## Defining basic functions
## dist: x1,x2,y1,y2 --> Distance between(x1,x2) and (y1,y2)
get_distance <- function(x1,x2,y1,y2){
  return(sqrt((x1-y1)^2 + (x2-y2)^2))
}

## get_center: data --> center of data list with x1,x2
get_center <- function(data){
  sumx <- 0 
  sumy <- 0 
  xcenter <- 0
  ycenter <- 0 
  for(i in 1:nrow(data)){
    sumx <- sumx + data[i,1]    
    sumy <- sumy + data[i,2]
  }
  return (c(sumx/nrow(data) , sumy/nrow(data)))
}

## get_probablity: x1,x2,centers,sd --> Binomial distribution in 2d
get_probablity <- function(x1,x2,centers,sd){
  constant <- 2 * pi * sd[1,1] * sd[1,2]
  exponent <- (((x1 - centers[1]) ^ 2) / (2 * sd[1,1] ^ 2) + 
                 ((x2 - centers[2]) ^ 2) / (2 * sd[1,2] ^ 2))
  return ((1/constant) * exp(exponent * -1))
  
}

## get_membership:x1,x2,centers,cluster --> row_matrix of membership
get_membership <- function(x1,x2,centers,cluster){
  result <- c()
  d1 <- get_distance(x1,x2,centers[1,1],centers[1,2])
  d2 <- get_distance(x1,x2,centers[2,1],centers[2,2])
  d3 <- get_distance(x1,x2,centers[3,1],centers[3,2])
  result <- rbind(result, 
                  (d2 * d3)/((d2*d3) + (d1*d3) + (d1*d2)), 
                  (d1 * d3)/((d2*d3) + (d1*d3) + (d1*d2)),
                  (d1 * d2)/((d2*d3) + (d1*d3) + (d1*d2)))
  return(result)
}


## get_weighted_center:list1, list2 --> 
##    Gives center as per formula sum(l1[i]^2 * l2)/sum(l1[i]^2)
get_weighted_center <- function(l1,l2){
  sum_sq <- 0
  sum_numerator <- 0
  for(i in 1:length(l1)){
    sum_sq <- sum_sq + (l1[i] ^ 2)
  }
  
  for(j in 1:length(l2)){
    sum_numerator <- sum_numerator + (l1[j] ^ 2 * l2[j])
  }
  return(sum_numerator/sum_sq)
}

## get_number_max_distance: d1, d2, d3 --> Position of minimum distance
get_number_max_distance <- function(d1,d2,d3){
  dist_max <- max(d1,d2,d3)
  if(dist_max == d1)
    return(1)
  if(dist_max == d2)
    return(2)
  if(dist_max ==d3)
    return(3)
}


## Reading the file
filename <- "dataset2.txt"
d <- read.csv(filename,header=FALSE,sep="\t")

## Giving the header to data so as to make life easy
names(d) <- c("x1","x2","class")

## Creating a Matrix with x1,x2,Cluster,Probalblity of the object in that cluster 
## Initially Cluster is set to 0 Indicating invalid clusters

x1 <- c()
x2 <- c()
class <- c()
for (i in 1:length(d$x1)){
  x1 <- rbind(x1,d$x1[i])
  x2 <- rbind(x2,d$x2[i])
  class <- rbind(class,d$class[i])
}
data <- cbind(x1,x2,class,0)

## Randomly distributing the array 
j<-0

## Dividing the data into 3 lists for class1, class2, class3
list1 <- c()
list2 <- c()
list3 <- c()
listall <- c()
for(i in 1:nrow(data)){
  if(data[i,3] == 1){
    list1 <- rbind(list1,data[i,])
  }
  if(data[i,3] == 2){
    list2 <- rbind(list2,data[i,])
  }
  if(data[i,3] == 3){
    list3 <- rbind(list3,data[i,])
  }
}

listall <- rbind(listall,list1,list2,list3)

## Initializing the variables 
centers <- c()
center1 <- get_center(list1)
center2 <- get_center(list2)
center3 <- get_center(list3)
centers <- rbind(centers,center1,center2,center3)



## The loop should me repeated from here. 
## Calculating mu, sigma and membership matrix
count <- 0
repeat{
  ##if(count > 10)
  ##  break
  list1 <- c()
  list2 <- c()
  list3 <- c()
  for(i in 1:nrow(listall)){
    if(listall[i,3] == 1){
      list1 <- rbind(list1,listall[i,])
    }
    if(listall[i,3] == 2){
      list2 <- rbind(list2,listall[i,])
    }
    if(listall[i,3] == 3){
      list3 <- rbind(list3,listall[i,])
    }
  }
  
  mu1 <- c()
  mu2 <- c()
  mu3 <- c()
  mu <- c()
  sd1 <- c()
  sd2 <- c()
  sd3 <- c()
  sd <- c()
  mu1 <- cbind(mu1,mean(list1[,1]),mean(list1[,2]))
  mu2 <- cbind(mu2,mean(list2[,1]),mean(list2[,2]))
  mu3 <- cbind(mu3,mean(list3[,1]),mean(list3[,2]))
  mu <- rbind(mu,mu1,mu2,mu3)
  sd1 <- cbind(sd1,sd(list1[,1]),sd(list1[,2]))
  sd2 <- cbind(sd2,sd(list2[,1]),sd(list2[,2]))
  sd3 <- cbind(sd3,sd(list3[,1]),sd(list3[,2]))
  sd <- rbind(sd,sd1,sd2,sd3)
  
  
  ## Now doing E step
  for(i in 1:nrow(list1)){
    p1 <- get_probablity(list1[i,1],list1[i,2],centers[1,],sd1)
    p2 <- get_probablity(list1[i,1],list1[i,2],centers[2,],sd1)
    p3 <- get_probablity(list1[i,1],list1[i,2],centers[3,],sd1)
    p1_new <- p1 / (p1 + p2 + p3)
    p2_new <- p2 / (p1 + p2 + p3)
    p3_new <- p3 / (p1 + p2 + p3)
    list1[i,3] <- get_number_max_distance(p1_new,p2_new,p3_new)
    list1[i,4] <- max(p1_new,p2_new,p3_new)
  }
  
  for(i in 1:nrow(list2)){
    p1 <- get_probablity(list2[i,1],list2[i,2],centers[1,],sd2)
    p2 <- get_probablity(list2[i,1],list2[i,2],centers[2,],sd2)
    p3 <- get_probablity(list2[i,1],list2[i,2],centers[3,],sd2)
    p1_new <- p1 / (p1 + p2 + p3)
    p2_new <- p2 / (p1 + p2 + p3)
    p3_new <- p3 / (p1 + p2 + p3)
    list2[i,3] <- get_number_max_distance(p1_new,p2_new,p3_new)
    list2[i,4] <- max(p1_new,p2_new,p3_new)
  }
  
  for(i in 1:nrow(list3)){
    p1 <- get_probablity(list3[i,1],list3[i,2],centers[1,],sd3)
    p2 <- get_probablity(list3[i,1],list3[i,2],centers[2,],sd3)
    p3 <- get_probablity(list3[i,1],list3[i,2],centers[3,],sd3)
    p1_new <- p1 / (p1 + p2 + p3)
    p2_new <- p2 / (p1 + p2 + p3)
    p3_new <- p3 / (p1 + p2 + p3)
    list3[i,3] <- get_number_max_distance(p1_new,p2_new,p3_new)
    list3[i,4] <- max(p1_new,p2_new,p3_new)
  }
  
  ## Merging the data into one list 
  listall <- c()
  listall <- rbind(listall,list1,list2,list3)
  
  
  ## Finding the membership matrix 
  mem <- c()
  for(i in 1:nrow(listall)){
    mem <- cbind(mem,get_membership(listall[i,1],
                                    listall[i,2],
                                    centers,
                                    listall[i,3]))
  }
  
  
  
  ## Here should come the code which will change the class according to current centers
  
  ## Now doing M step
  ## Finding new center
  center1_new <- c()
  center2_new <- c()
  center3_new <- c()
  centers_new <- c()
  
  center1_new <- cbind(center1_new,
                       get_weighted_center(mem[1,],listall[,1]),
                       get_weighted_center(mem[1,],listall[,2]))
  
  center2_new <- cbind(center2_new,
                       get_weighted_center(mem[2,],listall[,1]),
                       get_weighted_center(mem[2,],listall[,2]))
  
  center3_new <- cbind(center3_new,
                       get_weighted_center(mem[3,],listall[,1]),
                       get_weighted_center(mem[3,],listall[,2]))
  
  centers_new <- rbind(centers_new,center1_new,center2_new,center3_new)
  count <- count+1
  if(max(abs(centers - centers_new)) < 0.01)
    break
  centers <- centers_new
}



## Plotting the graph
png("DataSet2_ScatterPlot_GMM.png",bg="grey40")
plot(listall[,1],listall[,2],col=listall[,3],
     xlab="X1",ylab="X2",main="Scatter Plot of x1 vs x2 for different Classes")
legend("topright", c("Class1","Class2","Class3"),pch=c(1),col=c(1,2,3))
dev.off()