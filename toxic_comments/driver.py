import nltk
import re
import pickle
import string

MODEL_WEIGHT = 0.25
THRESHOLD = 0.19

vectorizer = pickle.load(open("toxic_comments/11_19_20.vectorizer", "rb"))

stop_words = nltk.corpus.stopwords.words("english")


def clean_text(x):
    x = x.lower()
    x = x.replace("\n", " ")
    x = x.replace("\t", " ")
    x = x.replace("'", "")
    x = x.replace('"', "")
    x = re.sub('[%s]' % re.escape(string.punctuation), "", x)
    x = ' '.join([word for word in x.split(' ') if word not in stop_words])
    x = x.encode('ascii', 'ignore').decode()
    x = re.sub(r'https*\S+', ' ', x)
    x = re.sub(r'@\S+', ' ', x)
    x = re.sub(r'#\S+', ' ', x)
    x = re.sub(r'\w*\d+\w*', '', x)
    x = re.sub(r'\s{2,}', ' ', x)
    return x


def predict(model, message, vader_score):
    message = clean_text(message)
    message = vectorizer.transform([message]).toarray()
    prediction = model.predict(message).flatten()[0]
    return (prediction * MODEL_WEIGHT + vader_score * (1 - MODEL_WEIGHT)) / 2


