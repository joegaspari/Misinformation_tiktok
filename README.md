# Analysis of TikTok using binary classification on metadata to predict for the presence of misinformation
------------------------------------------------------------------------------------
## Introduction

------------------------------------------------------------------------------------
Information and the spread of misinformation is a growing concern in the social media sphere as an increasing number of typically younger individuals are becoming influenced by the conversations they see on platforms such as TikTok. We chose to examine the spread of misinformation surrounding the COVID-19 pandemic through the TikTok platform. There is a wealth of information that people share on TikTok and consequently, people are misled by false information shared from popular accounts. We selected Tik Tok because it “Has been downloaded more than a billion times, becoming the most downloaded non-gaming app in 2020”. (Cervi, 2021) We believe this large number of downloads represents a large sphere of influence.
 
On social media platforms, people can be exposed to misinformation which can have damaging effects on their well-being. This can also damage the well-being of our society as a whole if misinformation is not moderated. Misinformation can be attributed for some of the hesitancy we’ve seen in 2021 in people who are hesitant to get the vaccine (CBC, 2021). As more people continue to use social media as a part of their daily lives, it is possible they are exposed more readily to the damaging effects that misinformation can have on not only their well-being, but the well-being of society as a whole.

------------------------------------------------------------------------------------
## Objective 


By looking at data from TikTok regarding the pandemic, we can gather insight into the source of misinformation on the platform. The goal of this study is to try and accurately identify posts on TikTok that may contain misinformation on the pandemic. This is the first step in understanding and addressing the spread of misinformation on TikTok.
Ideally, this information could be used in conjunction with more intensive analysis either performed by human moderators or advanced video content analysis to find and remove posts containing misinformation. We hope to use only easy to collect and compute metadata in order to make this process as efficient as possible while still remaining accurate. We hope this novel approach can speed up the process of identifying posts which may contain misinformation to drastically increase the speed posts which may mislead users can be identified and removed.


------------------------------------------------------------------------------------
## Collecting Required Data Sample


Data for this project is coming from the Python TikTok API wrapper created by davidteather on GitHub. We chose this implementation of the TikTok API as it would allow us to use Python as our primary language, as well as the lack of associated cost. In gathering the data, we targeted a few specific hashtags to give us a higher chance of finding posts we can use in a binary classification system. This data is currently in a CSV, which is explained in the next section. Next, we need to manually review the posts in this list as either potentially containing misinformation or not, which will allow us to build a training/testing set for the model. Included in the CSV is the posts description as well as counts for comments, shares, and plays. This will hopefully be enough data to allow us to create our classification model which can be used in conjunction with other methods to generate a better final output for likelihood that a post contains misinformation.



------------------------------------------------------------------------------------

## Generating Bi-grams & Unigrams

To begin Identifying what is miss-information in the context of COVID-19 we utilized data from IEEEDataPort that contained the titles of articles deemed to be containing misinformation, by the study. The titles were then thoroughly preprocessed and stripped of over 500 stopwords. The stopwords were needed to filter out words that did not contribute meaning to our analysis. Using the Spacy pipeline with emphasis on biomedical data we were able to extract a list of unigrams and bi-grams most significant to the corpus of words produced by the titles of the fake news articles.
The resulting unigrams were separated from bi-grams as the significance of a bi-gram match in our post is higher than that of a single word match or multiple single word matches. The data for both can be found in “Data/bigram.csv” and “Data/unigram.csv” in the related Github repository. We then extract the description from each post, apply some cleaning to the text and apply our extract_ngrams function to isolate all bi-grams and unigrams produced in the text.

------------------------------------------------------------------------------------
## Sentiment Analysis

The user sentiment is extracted from the description of each post and categorized as either positive, negative or neutral. We suspect that posts which show strong negative sentiment over positive are more likely to contain information that is harmful and uninformed. A categorical sentiment score is added to the CSV containing all posts extracted from the TikTok API.


------------------------------------------------------------------------------------

## Classification System

Our dataset contains 1000 posts. The field of the dataset contains index, id, nickname, description, and the number of comments(commentCount), plays (playCount), and shares (shareCount). We are trying to develop a binary classification system to predict if a post is potentially misinformation or not. In order to apply this algorithm, we need meaningful attributes and class labels.

Unfortunately, index and id from our rough data are not useful to our analysis. Index and ID are unique identifiers and as such will have no pattern. Username is still valuable to us as we may be able to find a pattern in which a user frequently posts misinformation and is likely to continue to do so. In order to solve the problem, we use the above fields to create a few new columns. There are neutral (Neu), negative (Neg), positive (Pos), bigramMatch%, unigramMatch%, perc_HashT_Match. For each post, we perform sentiment analysis on the description and assign it one of three possible binary values, positive, neutral, or negative. bigramMatch% contains a percentage value between 0 and 1 which is the percentage of bigrams in the description that match the data from IEEEDataPort. Unigram match does the same, but with single word matches. perc_HashT_Match contains the percentage of our searched hashtags that a post contains. We hope to use this data to create a more accurate classification model.

------------------------------------------------------------------------------------


