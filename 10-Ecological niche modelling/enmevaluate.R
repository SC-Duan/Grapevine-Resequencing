setwd("/public/paleoclimate_data/LH_v1_2_5m")
#Don't forget to set your working directory!

#only need to run this code the first time you install these packages on your machine/user account.

#install.packages("rJava")
#install.packages("ENMeval")

##installing rJava can be tricky. If you're experiencing problems installing either rJava or
##ENMeval, it's the installation of rJava that is very likely your problem. Keeping in mind
##that these instructions are for a PC, visit this website for troubleshooting:
##https://cimentadaj.github.io/blog/2018-05-25-installing-rjava-on-windows-10/installing-rjava-on-windows-10/
options(java.parameters = "-Xmx100g" )
library(rJava)
library(ENMeval)
library(raster)

#Find where the java directory is for the dismo package using the command below. Then, 
#you need to put the file maxent.jar into the indicated directory. You'll need to do
#this second step by hand (not using r)

system.file("java", package="dismo")

#put here the names of your environmental layers, following the pattern below:
bio1 <- raster("bio_1.asc")
bio2 <- raster("bio_2.asc")
bio3 <- raster("bio_3.asc")
bio4 <- raster("bio_4.asc")
bio5 <- raster("bio_5.asc")
bio6 <- raster("bio_6.asc")
bio7 <- raster("bio_7.asc")
bio8 <- raster("bio_8.asc")
bio9 <- raster("bio_9.asc")
bio10 <- raster("bio_10.asc")
bio11 <- raster("bio_11.asc")
bio12 <- raster("bio_12.asc")
bio13 <- raster("bio_13.asc")
bio14 <- raster("bio_14.asc")
bio15 <- raster("bio_15.asc")
bio16 <- raster("bio_16.asc")
bio17 <- raster("bio_17.asc")
bio18 <- raster("bio_18.asc")
bio19 <- raster("bio_19.asc")


#Do what's called "stacking" the rasters together into a single r object

env <- stack(bio1, bio2, bio3, bio4, bio5, bio6, bio7, bio8, bio9, bio10, bio11, bio12, bio13, bio14, bio15, bio16, bio17, bio18, bio19)

#Display the stacked environment layer. Make a note of the position in the list 
#of any categorical variables (do that by hand)

env

#in this example, the categorical variables are #s 9 and 10 in the list. But know your own data!

#load in your occurrence points

occ <- read.csv("grape.csv")[,-1]

#check how many potential background points you have available

length(which(!is.na(values(subset(env, 1)))))

#If this number is far in excess of 10,000, then use 10,000 background points.
#If this number is comprable to, or smaller than 10,000, then use 5,000, 1,000, 500,
#or even 100 background points. The number of available non-NA spaces should 
#be well in excess of the number of background points used.

#For the evalution below, we need to convert the bias object into another format.
#The code is set up to sample 5,000 background points. It would be better if we
#could sample 10,000 background points, but there are not enough places available.
#If we could change it to 10,000 background points we would change the ", 5000," to ",10000,"

#run the evaluation

##This run uses the "randomkfold" method of cross-validation and 10 cross-validation folds. 
##There are two categorical variables: they are numbers 9 and 10 in the list of environmental 
##variables from the stacked raster object.

enmeval_results <- ENMevaluate(occ, env, method="jackknife", n.bg=10000, algorithm='maxent.jar')

enmeval_results@results

write.csv(enmeval_results@results, "grape_enmeval_results.csv")

#If you were to use the block method, you would replace:
#method="randomkfold", kfolds = 10
#with:
#method = "block"

#############################
##########IMPORTANT##########
#############################
#If you have fewer than 50 occurrence points, you will need to use the "jackknife" method of
#model validation instread. To do that, you would replace:
#method="randomkfold", kfolds = 10
#with:
#method = "jackknife"

#If there are no categorical variables in your dataset, you would get rid of:
#categoricals=c(9,10)
#In general, be very careful that the categoricals argument points to the right variable(s).
