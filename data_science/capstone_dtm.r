library(tm)
library(readr)
library(dplyr)
library(tidytext)

#FILENAME="/home/rob/DTM_example/sample.txt"
#mytext = readLines(FILENAME)

showCorpusContents <- function(vc, trnsfrm) {
print(trnsfrm)
numDocs = NROW(vc)
for (i in 1:numDocs) {
  print(vc[[i]]$content)   
}
}

mytext <- c(
'happy HAPPY, happy54, and 6 more happy!',
'do you like it?  But I hate really bad dogs',
'I am the best best best friend.',
'Do you really like it?  I\'m not a fan',
'I am extremely happy today', 'I am very annoyed',
'She was most angry and annoyed! But I was sad. And he was anxious',
'I was upset, upset, more upset, and still very upset!'
)
print(mytext)
#----------build VCorpus
review_corpus = VCorpus(VectorSource(mytext))
showCorpusContents(review_corpus, "===ORIGINAL===")

#----------lowercase
review_corpus = tm_map(review_corpus, content_transformer(tolower))
showCorpusContents(review_corpus, "===LOWERCASE===")

#----------remove numbers
review_corpus = tm_map(review_corpus, removeNumbers)
showCorpusContents(review_corpus, "===NO NUMBERS===")

#----------remove punctuation
review_corpus = tm_map(review_corpus, removePunctuation)
showCorpusContents(review_corpus, "===NO PUNCTUATION===")

#----------remove stopwords
review_corpus = tm_map(review_corpus, removeWords, c("the", "and", stopwords("english")))
showCorpusContents(review_corpus, "===NO STOPWORDS===")

#----------remove whitespace
review_corpus = tm_map(review_corpus, stripWhitespace)
showCorpusContents(review_corpus, "===NO WHITESPACE===")


#------------Remove by token length-----------------------------
myRegex <- '\\b[a-zA-Z0-9]{1,3}\\b'
removeByTokenLen <- function(x) gsub(myRegex, "", x)
review_corpus <- tm_map(review_corpus, content_transformer(removeByTokenLen))
showCorpusContents(review_corpus, "===REGEX===")
#------------Remove by token length-----------------------------

review_dtm <- DocumentTermMatrix(review_corpus)
review_dtm
inspect(review_dtm[1:7, 1:14])

