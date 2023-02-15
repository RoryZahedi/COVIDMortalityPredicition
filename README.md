# COVIDMortalityPredicition

Given the uncertainty of the novel COVID-19, there exists a dangerous shortage of medical resources due to improper planning to efficiently distribute resources. Thankfully, due to the wonders of modern technology and basic statistics, we can use a Naive Bayes Classifier to better predict the fatalities from COVID-19.


## Architecture/Preprocessing

The premise of implementing this Naive Bayes Classifier is simple. Since Bayes’ Theorem can be used to find “finds the probability of an event occurring given the probability of another event that has already occurred” (GeeksForGeeks), we first had to find the probability of all the individual characteristics from a dataset.

## Parsing in Data:

The intuitive first step here is to get these probabilities, but this would be impossible without first parsing in the training data set. To do this, I imported the libraries csv(to utilize ‘reader’) and sys(to take in command line arguments for the filenames of the datasets). After opening the filename specified as argument during run time, I loop through each row in the data set, and append that row to my list labeled ‘ds’, such that my ds list is now a list of lists, where each inner list represents a row of data, and each element in the row of data, represents data of that row for a given column (e.g. data[1][0] would give me data pertaining to the row 1, column 0’s data).

## Getting Statistics of Attributes:

After parsing in the data, as mentioned above, we had all of the necessary training data in our ‘ds’ list. To make use of this, I would loop through the entirety of the list and do 2 main things. 1) Keep track of the total count of patients who lived (and total number of patients who died) after catching COVID-19. 2) Keep track of attribute data; the latter step is a little complicated in my algorithm, so allow me to break down how this attribute data is stored. To keep track of attribute data, I first initialized a container (a list of lists I name “book”), to be a list containing R number of lists (where R is equal to the number of characteristics in the data set (R = 22) ), and each one of these lists, is a list containing 4 zeroes upon initialization. The reason for these 4 zeroes is to keep track of the following:

> P(Characteristic = 1|patient lives), P(Characteristic = 2|patient lives) P(Characteristic = 1|patient dies),P(Characteristic = 2|patient lives).

So to summarize, indexing into ‘book’ with index i, where i is a number representing the ith characteristic (from the csv), you get a list of those four probabilities. Now that the book is well defined, we can talk about the actual getting statistics part. As mentioned earlier, we loop through the entire data we stored earlier in ‘ds’, and for every row we take a look at column 4, which represents the livelihood of the patient. We check to see if the date is neither “9999-99-99” or “9999/99/99”. If the date is one of the two mentioned, we increment number of patients dead, then we increment the values inside book for all given binary characteristics | dead. For instance, if we see the patient is dead, we loop through all characterisitcs and wee see that sex = 1, so we incrament book[0][2] by one (where 0 represents the ith characteristc and 2 represents the case of characteristic = 1 and patient dead). This same logic applies to if the patient is alive. At the end we have a complete book containing all the necessary data to apply Bayes’ rule; for those wondering what happens to non binary characteristics in this process, I ignore them for reasons I will address later. These two functions conclude the functionality of the Architecture.


## PreProcessing Repreise:
This part is rather short as I did the majority of explanation in the previous sections, but to reiterate, there exist two functions prior to the data training. The first function to open,read, and extract data from the training csv returning a lists of lists with this data, and the second to firstly generate an empty data structure (‘book’), and to secondly fill this book with the necessary data need for training, as well as also keep track of number of alive/dead patients; the function will return book,numPatientsAlive,and numPatientsDead as a 3 tuple. Originally, this code was all just crammed into main, but I thought to clean them up and generate these book-keeping data structures separately, just to keep things clean and bring abstraction to the non-stats related parts.


## Model Building - Applying Bayes’ Rule and Predicting Data: 

In this final step, as the name implies, we will be applying Bayes’ rules for a given patient from a different data set, and hopefully predict whether they live or die. First, before going through this data set, I computed the overall probability of a patient living, and overall probability of a patient dying by simply dividing numofPatientsAlive/totalPatients and numOfPatientsDead/totalPatients. This step is crucial as we need this probability at the end of this step. Okay now onto the actual predictions. The algorithm is simple: loop through each patient and for each given patient, examine their binary characteristic values. For each value, get the probability that the patient lives/dies from the book for that corresponding characteristic value, and then multiply this probability by the product of all the other characteristic values given patient lives/dies respectively. I.e. calculate the following two 22 22 values,
<img width="613" alt="Screen Shot 2023-02-15 at 2 47 17 PM" src="https://user-images.githubusercontent.com/19734560/219205977-6cebae5b-83c8-47eb-a144-97f0c44ee5b3.png">

At the i=0 i=0 end, you will be given two decimal values <1 for the probability of the patient living/dying with their given characteristics. This is incomplete though, as I mentioned earlier, you must respectively multiply the P(patient living) and P(patient dying) respectively. So the final values
are simply:
<img width="732" alt="Screen Shot 2023-02-15 at 2 47 51 PM" src="https://user-images.githubusercontent.com/19734560/219206085-cda03466-4a9a-474f-9445-a37f424ad7b6.png">
You can choose to standardize these values, as their sums must equal one(either the patient lives or dies, there is no other outcomes), but since standardizing them would effectively not change the outputs, I would finally just compare whether the final value of the first equation was >= the final value of the second equation, and if it was I would output ‘0’ indicating that the patiently likely survived, otherwise I’d output ‘1’ indicating the patient passed.

## Results
Upon the first few trials of tens of thousands of datasets, I was getting around 86% accuracy flat, at an average of 2-3 second run time. I was pretty satisfied with the results (and surprised with the run time as my asymptotic algorithm was O(n^2). In attempt to better improve accuracy I experimented skipping calculations and automatically printing a ‘0’, indicating the patient lived, when the patient had <= 30 years of age, the run time improved slightly on average, as well as the accuracy by around .50%. I made this optimization after staring at the table data and trying to notice trends. In the end I concluded that age was a big contributing factor on whether or not the patient survived. Among the 10 other most important features for the patient, though I did not calculate the exact values, these would be consisting of the binary values.

It is clear that some characteristics are more important than others in predicting a patient’s livelihood; to use this, I would try to find the root node of characteristics, as well as the ones closest to the root, and give those more weighting when calculating the probabilities. This would definitely make for a more accurate predictor.
