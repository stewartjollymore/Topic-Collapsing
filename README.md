# Topic-Collapsing
Collapsing BERTopic topics using similarities which are outliers from the distribution of topic similarities. 
This is an augmentation of a process that was created by [Maarten Grootendorst](https://towardsdatascience.com/topic-modeling-with-bert-779f7db187e6) and differs by looking at all the
topic similarites and finding those that are outliers (1.5 times the IQR from the upper whisker) and collapses 
that largest outlier.

Once the two most similar topics are collapsed the c-tf-idf is calculated and a new similarity matrix is created
and the process is repeated until the there are no more outliers. This is not an optimized proccess but is a first pass.

This was deemed necssary as some of the smaller topics, which Grootendosrt was collapsing first, were solid topics in thier own right
from with-in the corpus that I was working with. 

## IN DEV
