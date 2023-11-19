# citation: Overview of NLTK and NLTK methods: https://realpython.com/nltk-nlp-python/#getting-started-with-pythons-nltk
# For help on getting rid of punctuation: https://stackoverflow.com/questions/15547409/how-to-get-rid-of-punctuation-using-nltk-tokenizer#:~:text=The%20workflow%20assumed%20by%20NLTK,or%20python's%20isalnum()%20function.&text=It%20does%20work%3A%20%3E%3E%3E%20'with%20dot.
# text sources are all public domain work gathered from: https://www.gutenberg.org/
# API skeleton and logic based on code acquired from https://canvas.oregonstate.edu/courses/1933801/pages/exploration-google-app-engine-and-python?module_item_id=23529288
# https://towardsdatascience.com/how-to-transform-technical-jargon-into-simple-bi-tri-grams-with-nlp-on-a-public-dataset-2081f5609c1f

# Looked at this, although my strategy is a little different:
# https://thawuship.medium.com/mastering-hashtag-generation-with-pythons-natural-language-processing-techniques-6e093660c2f3
# but it did lead me to this:
# https://www.nltk.org/_modules/nltk/tag/perceptron.html
# probably just want nouns (only proper?) for hashtags

from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
import json
from flask import Flask, request
# from google.cloud import datastore
import nltk
# you will need to download these from nltk once per program on your local machine:
nltk.download('punkt')
nltk.download("stopwords")
nltk.download('wordnet')
nltk.download("averaged_perceptron_tagger")

app = Flask(__name__)
# client = datastore.Client()


@app.route('/')
def index():
    return "Please navigate to /hashtaggenerator to use this API"\



@app.route('/hashtaggenerator', methods=['POST'])
def boats_get_post():
    if request.method == 'POST':
        stop_words = stopwords.words("english")
        # don't know where 'wa' is coming from, but is always added, so remove explicitly
        stop_words.append('wa')

        # print('request:', request.json())

        # content = nltk.pos_tag(content)
        # grammar = "NP: {<DT>?<JJ>*<NN>}"
        # chunk_parser = nltk.RegexpParser(grammar)
        # parsed = chunk_parser.parse(content)
        # print('parsed:', parsed)

        # get content out of request and tokenize
        content = request.get_json()['content']

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

        # tag words in meaningfulWords for grammatical purpose
        # only really want to create hashtags out of nouns
        # tags = nltk.pos_tag(meaningfulWords) # with lemmatization
        tags = nltk.pos_tag(content)    # without lemmatization
        # keywords = [word for (word, tag) in tags if tag.startswith(
        #     'NN') or tag == 'JJ' or tag == 'NNP']
        # keywords = [word for (word, tag) in tags if tag.startswith('NN') or tag == 'NNP']
        keywords = [word for (word, tag) in tags if tag.startswith(
            'NN') or tag == 'NNS']
        print('tags:', keywords)

        # now, produce frequency distribution
        freqency_distribution = FreqDist(keywords)
        mostCommon10 = freqency_distribution.most_common(5)

        hashTags = []

        for item in mostCommon10:
            hashTagItem = ('#' + item[0])
            hashTags.append(hashTagItem)

        # print ten most common meaningful words(hashtags)
        # print('freq dist:', freqency_distribution.most_common(10))
        # for item in mostCommon10:
        #     returnArr.append(item[0])
        return ({'Hash Tags: ': hashTags}, 200)
    else:
        return ({"Error": "Method not found!"}, 404)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
