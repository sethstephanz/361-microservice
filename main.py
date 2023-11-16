# citation: https://realpython.com/nltk-nlp-python/#getting-started-with-pythons-nltk
# https://stackoverflow.com/questions/15547409/how-to-get-rid-of-punctuation-using-nltk-tokenizer#:~:text=The%20workflow%20assumed%20by%20NLTK,or%20python's%20isalnum()%20function.&text=It%20does%20work%3A%20%3E%3E%3E%20'with%20dot.
# text source: https://www.gutenberg.org/files/2600/2600-h/2600-h.htm#link2H_4_0001

from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
import nltk
# you will need to download these from nltk once per program on your local machine:
# nltk.download('punkt')
# nltk.download("stopwords")
# nltk.download('wordnet')

stop_words = stopwords.words("english")
# don't know where 'wa' is coming from, but is always added, so remove explicitly
stop_words.append('wa')

text = open('text.txt', 'r')
content = text.read()
text.close()

# print('stop words:', stop_words)
# tokenize content while removing punctuation
# content = word_tokenize(content)
tokenizer = RegexpTokenizer(r'\w+')
content = tokenizer.tokenize(content)

# next, lemmatize the remaining content to further simplify text
lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(word) for word in content]

# then, get rid of stop words (a, the, pronouns, etc.)
meaningfulWords = lemmatized_words
meaningfulWords = [
    word for word in lemmatized_words if word.casefold() not in stop_words]

# now, produce frequency distribution
freqency_distribution = FreqDist(meaningfulWords)
mostCommon10 = freqency_distribution.most_common(10)

for item in mostCommon10:
    print('#' + item[0])

# print ten most common meaningful words (hashtags)
# print('freq dist:', freqency_distribution.most_common(10))
# for frequency in freqency_distribution:
#     print(frequency)
