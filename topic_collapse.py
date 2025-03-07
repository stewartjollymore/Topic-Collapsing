import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def c_tf_idf(documents, m, ngram_range = (1,2)):
 
  count = CountVectorizer(ngram_range = ngram_range, stop_words = "english").fit(documents)
  t = count.transform(documents).toarray()
  w = t.sum(axis = 1)
  tf = np.divide(t.T, w)
  sum_t = t.sum(axis = 0)
  idf = np.log(np.divide(m, sum_t)).reshape(-1,1)
  tf_idf = np.multiply(tf, idf)
 
  return tf_idf, count

def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=20):
    words = count.get_feature_names()
    labels = list(docs_per_topic.Topic)
    tf_idf_transposed = tf_idf.T
    indices = tf_idf_transposed.argsort()[:, -n:]
    top_n_words = {label: [(words[j], tf_idf_transposed[i][j]) for j in indices[i]][::-1] for i, label in enumerate(labels)}
    return top_n_words

def extract_topic_sizes(df):
    topic_sizes = (df.groupby(['Topic'])
                     .Doc
                     .count()
                     .reset_index()
                     .rename({"Topic": "Topic", "Doc": "Size"}, axis='columns')
                     .sort_values("Size", ascending=False))
    return topic_sizes

# Create similarity matrix from a c-tf-idf matrix
similarities_test = cosine_similarity(tf_idf.T)

# create zeros on the diag where similarity of a topic
# with itself is 1.  This is an artifact and not necssary
# when using the triu_indices function from numpy
np.fill_diagonal(similarities_test, 0)

# Creates a vector from upper triangular matirx of
# the similarity matrix
sims_test = similarities_test[np.triu_indices(80, k = 1)]
docs_df_test = docs_df

# finding the 1st quartile
q1 = np.quantile(sims_test, 0.25) 
# finding the 3rd quartile
q3 = np.quantile(sims_test, 0.75)
med = np.median(sims_test) 
# finding the iqr region
iqr = q3-q1 
# finding upper and lower whiskers
upper_bound = q3+(2*iqr)

# Initializes the number of current similarity outliers above 
# the upper whisker
number_of_outliers = len(np.where(sims_test > upper_bound)[0])


while number_of_outliers > 0:
  
  indices = np.where(similarities_test == sims_test[sims_test > upper_bound][0])[0]
  topic_to_merge = indices[0]
  topic_to_merge_into = indices[1]
  
  docs_df_test.loc[docs_df_test.Topic == topic_to_merge, "Topic"] = topic_to_merge_into
  old_topics = docs_df_test.sort_values("Topic").Topic.unique()
  map_topics = {old_topic: index for index, old_topic in enumerate(old_topics)}
  docs_df_test.Topic = docs_df_test.Topic.map(map_topics)
  docs_per_topic_test = docs_df_test.groupby(['Topic'], as_index = False).agg({'Doc': ' '.join})
  
  # Calculate new topic words
  m = len(df_to1)
  tf_idf_test, count_test = c_tf_idf(docs_per_topic_test.Doc.values, m)
  top_n_words_test = extract_top_n_words_per_topic(tf_idf_test, count_test, docs_per_topic_test, n=20)
  
  similarities_test = cosine_similarity(tf_idf_test.T)
  np.fill_diagonal(similarities_test, 0)
  sims_test = similarities_test[np.triu_indices(len(similarities_test), k = 1)]


  # finding the 1st quartile
  q1 = np.quantile(sims_test, 0.25) 
  # finding the 3rd quartile
  q3 = np.quantile(sims_test, 0.75)
  med = np.median(sims_test) 
  # finding the iqr region
  iqr = q3-q1 
  # finding upper and lower whiskers
  upper_bound = q3+(2*iqr)

  number_of_outliers = len(np.where(sims_test > upper_bound)[0])

  
topic_sizes = extract_topic_sizes(docs_df_test); 
topic_sizes.head(10)
