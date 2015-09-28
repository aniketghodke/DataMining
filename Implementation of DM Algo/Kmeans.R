## Setting the library path
.libPaths("C:\\R\\library")

## Setting the data path
setwd("C:\\Data Mining\\HW2\\dataset")

## Reading the file
filename <- "dataset1.txt"
d <- read.csv(filename,header=FALSE,sep="\t")

## Giving the header to data so as to make life easy
names(d) <- c("x1","x2","y")

## Dividing the data in group of three
length1 <- nrow(d)/3
length2 <- nrow(d)/3
length3 <- nrow(d) - (length1 + length2)

## Creating 3 lists
list1 <- c()
list2 <- c()
list3 <- c()

## Setting the seed to some value so that the 
## random numbers can be re-generated 
set.seed(1234)
j<-1
random_number <- sample(1:nrow(d),nrow(d),replace=FALSE)
for (i in random_number){
  if(i%%3 == 0){
    list1 <- rbind(list1,d[j,])
    j <- j + 1
  }
  
  if(i%%3 == 1){
    list2 <- rbind(list2,d[j,])
    j <- j + 1
  }
  
  if(i%%3 == 2){
    list3 <- rbind(list3,d[j,])
    j <- j + 1
  }
}

## Printing the list
print("Printing the list1")
print(list1)
print("Printing the list2")
print(list2)
print("Printing the list3")
print(list3)

## Creating a data frame for new centers
center1 <- c()
c <- c()
c$x1 <- 0
c$x2 <- 0
center1 <- rbind(center1,c)
center2 <- c()
center2 <- rbind(center2,c)
center3 <- c()
center3 <- rbind(center3,c)

## Creating counter
counter <- 1
## Function takes in dataframe of 2 elements 
## and returns the centroid of the list in x1,x2 format
get_centroid <- function(l){
  center <- c()
  center$x1 <- get_center(l$x1) 
  center$x2 <- get_center(l$x2)
  
  return(center)
}


## Function takes in numeric list and returns mean
get_center<-function(x){
  sum <- 0 
  for(i in x){
    sum <- sum + i
  }
  return(sum/length(x))
}


## get_distance: p1,p2 --> distance
## gets 2 points and return the distance between 2 points
get_distance <- function(point1,point2){
  dist <-  sqrt((point1$x1 - point2[1,]$x1) ^ 2 +(point1$x2 - point2[1,]$x2) ^ 2)
  return (dist)
}

mat_equal <- function(mat1,mat2){
  return((mat1[1,]$x1 == mat2[1,]$x1) && (mat1[1,]$x1 == mat2[1,]$x2))
}

mat_add <- function(mat,lst){
  mat[1,1] <- lst$x1
  mat[1,2] <- lst$x2
  return(mat)
}
center1_new <- c()
center1_new <- rbind(center1_new,c)
center2_new <- c()
center2_new <- rbind(center2_new,c)
center3_new <- c()
center3_new <- rbind(center3_new,c)


repeat{
  ######  start from here ################
  ## Getting the values of centers of the given list
  center1 <- mat_add(center1,get_centroid(list1))
  center2 <- mat_add(center2,get_centroid(list2))
  center3 <- mat_add(center3,get_centroid(list3))
  
  ## Now replace center1 which is matrix from list returned from get_centroid
  
  ## Rearranging the values from the list according to center 
  ## Now I need to use the centers and get the 
  ## distance and arrange the list accordingly
  for(l1 in 1:nrow(list1)){
    d1 <- get_distance(list1[l1,],center1)
    d2 <- get_distance(list1[l1,],center2)
    d3 <- get_distance(list1[l1,],center3)
    if(!is.na(d1) & !(is.na(d2)) & !(is.na(d3)))
    {
      dis_min <- min(d1,d2,d3)
      if(dis_min == d2){
        print("Adding to list2")
        list2 <- rbind(list2,list1[l1,])
        list1 <- list1[-l1,]
      }
      if(dis_min == d3){
        print("Adding to list3")
        list3 <- rbind(list3,list1[l1,])
        list1 <- list1[-l1,]
      }
    }
  } 
  
  ## Now Rearranging the second list: 
  ## Now I need to use the centers and get the 
  ## distance and arrange the list accordingly
  for(l2 in 1:nrow(list2)){
    d1 <- get_distance(list2[l2,],center1)
    d2 <- get_distance(list2[l2,],center2)
    d3 <- get_distance(list2[l2,],center3)
    if(!is.na(d1) & !(is.na(d2)) & !(is.na(d3)))
    {
      dis_min <- min(d1,d2,d3)
      if(dis_min == d1){
        print("Adding to list1")
        list1 <- rbind(list1,list2[l2,])
        list2 <- list2[-l2,]
      }
      if(dis_min == d3){
        print("Adding to list3")
        list3 <- rbind(list3,list2[l2,])
        list2 <- list2[-l2,]
      }
    }
  }
  
  ## Now Rearranging the third list
  ## Now I need to use the centers and get the 
  ## distance and arrange the list accordingly
  for(l3 in 1:nrow(list3)){
    d1 <- get_distance(list3[l3,],center1)
    d2 <- get_distance(list3[l3,],center2)
    d3 <- get_distance(list3[l3,],center3)
    if(!is.na(d1) & !(is.na(d2)) & !(is.na(d3)))
    {
      dis_min <- min(d1,d2,d3)
      if(dis_min == d1){
        print("Adding to list1")
        list1 <- rbind(list1,list3[l3,])
        list3 <- list3[-l3,]
      }
      if(dis_min == d2){
        print("Adding to list2")
        list2 <- rbind(list2,list3[l3,])
        list3 <- list3[-l3,]
      }
    }
  }
  
  
  center1_new <- mat_add(center1_new,get_centroid(list1))
  center2_new <- mat_add(center2_new,get_centroid(list2))
  center3_new <- mat_add(center3_new,get_centroid(list3))
  counter <- counter + 1
  cat("Looping ",counter,"\n")
  if((identical(center1_new,center1))
     && (identical(center2_new,center2))
        && (identical(center3_new,center3))){
    break
  }
  ############################### Come till here #####################
  
}

## Change the class label of the lists
list1$y <- 1
list2$y <- 2
list3$y <- 3

## Merging the lists into one
list_final <- rbind(list1,list2,list3)
## Plotting the scatter plot
png("DataSet1_ScatterPlot_Kmeans.png",bg="transparent")
plot(list_final$x1,list_final$x2,col=list_final$y,
     xlab="X1",ylab="X2",main="Scatter Plot of x1 vs x2 for different Classes")
legend("topright", c("Class1","Class2","Class3"),pch=c(1),col=c(1,2,3))
dev.off()