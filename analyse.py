from __future__ import division
import glob
import json
import os
from nltk import NaiveBayesClassifier, SklearnClassifier
import nltk
from nltk.tokenize import word_tokenize
import matplotlib
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_recall_fscore_support
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")


def format_sentence(sentence):
    return {word: True for word in word_tokenize(sentence)}


pos_data = []  # Training positive data
positive = []  # Test positive data
with open('training_pos.txt') as f:
    for line in f:
        positive.append(line)
        pos_data.append([format_sentence(line), 1])

neg_data = []  # Training negative data
negative = []  # Test negative data
with open('training_neg.txt') as f:
    for line in f:
        negative.append(line)
        neg_data.append([format_sentence(line), 0])

neg_cut = int(round(len(neg_data) * 4 / 5))
pos_cut = int(round(len(pos_data) * 4 / 5))

# Training data is 80%(Training negative data) + 80%(Training positive data)
training_data = neg_data[:neg_cut] + pos_data[:pos_cut]
# Test data is 20%(Test negative data) + 20%(Test positive data)
test_data = neg_data[neg_cut:] + pos_data[pos_cut:]


def classify(tweetFile, algorithm):
    model = None

    if algorithm == 0:
        model = NaiveBayesClassifier.train(training_data)
    elif algorithm == 1:
        model = SklearnClassifier(LinearSVC(), sparse=False).train(training_data)

    data = pd.read_csv(tweetFile)
    text = data['text']
    timestamp = data['timestamp']

    datafile = '../gen/' + tweetFile.split('.')[0] + '.json'
    entry = {}

    with open(datafile, 'w') as json_file:

        for txt, ts in zip(text, timestamp):

            score = model.classify(format_sentence(txt))

            if algorithm == 0:
                entry = {'tweet': txt, 'timestamp': ts, 'classifier': {'name': 'Naive Bayes', 'score': score}}
            elif algorithm == 1:
                entry = {'tweet': txt, 'timestamp': ts, 'classifier': {'name': 'SVM', 'score': score}}

            json.dump(entry, json_file, indent=4)

    accuracy = nltk.classify.accuracy(model, training_data)
    print(accuracy)

    y_true = [0 for _ in range(int(round(len(neg_data) * 1 / 5)))] + [1 for _ in
                                                                      range(int(round(len(pos_data) * 1 / 5)))]
    y_pred = [model.classify(format_sentence(txt)) for txt in negative[:int(round(len(neg_data) * 1 / 5))]] + [
        model.classify(format_sentence(txt))
        for txt in positive[:int(round(len(pos_data) * 1 / 5))]]

    print(precision_recall_fscore_support(y_true, y_pred, average='macro'))


def result_plot():
    pos_results = []
    neg_results = []
    labels = []

    os.chdir("../gen")
    for f in glob.glob("*.json"):
        positive = 0
        negative = 0
        labels.append(f.split('.')[0])
        with open(f, 'r') as searchfile:
            for line in searchfile:
                if "\"score\": 1" in line:
                    positive += 1
                elif "\"score\": 0" in line:
                    negative += 1
            pos_results.append(positive)
            neg_results.append(negative)

    fig = plt.figure()
    ax1 = fig.add_axes([-0.2, .3, .8, .4], aspect=1)
    ax1.pie(pos_results, radius=1.2, autopct="%.1f%%")
    ax1.set_title("Positive Opinions")
    ax2 = fig.add_axes([0.4, .3, .8, .4], aspect=1)
    ax2.pie(neg_results, radius=1.2, autopct="%.1f%%")
    ax2.legend(labels, loc=(-0.8, -0.4), shadow=True)
    ax2.set_title("Negative Opinions")
    plt.show()
