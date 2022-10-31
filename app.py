# coding=utf-8
from flask import Flask, render_template, request, jsonify
from tkinter import N
from gensim.models.tfidfmodel import TfidfModel
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
from pythainlp.corpus import download, get_corpus_path
from pythainlp.corpus import thai_stopwords
from gensim.corpora.dictionary import Dictionary
from collections import defaultdict
import itertools
from pythainlp import sent_tokenize
import re
import string

app = Flask(__name__)


def uniquelist(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def clean_msg(msg):
    # ลบ text ที่อยู่ในวงเล็บ <> ทั้งหมด
    msg = re.sub(r'<.*?>', '', msg)
    # ลบ hashtag
    msg = re.sub(r'#', '', msg)
    # ลบ เครื่องหมายคำพูด (punctuation)
    for c in string.punctuation:
        msg = re.sub(r'\{}'.format(c), '', msg)
    # ลบ separator เช่น \n \t
    msg = ' '.join(msg.split())
    # ลบ วงเล็บ
    msg = re.sub(r'[()]', '', msg)
    # ลบตัวเลข
    msg = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", msg)
    return msg


def tokez(text):
    text = clean_msg(text)
    # ตัดประโยค โดยใช้ วรรคและขึ้นบรรทัดใหม่
    text = sent_tokenize(text)
    # text = mysent_tokenize(text)
    for i in text:
        newtext = word_tokenize(i, engine='deepcut')
        no_stopword = [
            t for t in newtext if t not in thai_stopwords()]
        articles.append(no_stopword)


def gettfidf(text):
    tokez(text)
    dictionary = Dictionary(articles)
    corpus = [dictionary.doc2bow(a) for a in articles]
    # print(corpus)
    result = []
    for xx in range(len(corpus)):
        doc = corpus[xx]
        tfidf = TfidfModel(corpus)
        tfidf_weights = tfidf[doc]
        sorted_tfidf_weights = sorted(
            tfidf_weights, key=lambda w: w[1], reverse=True)
        for term_id, weight in sorted_tfidf_weights[:5]:
            tmpword, tmpvalue = dictionary.get(term_id), weight
            result.append([tmpword, tmpvalue])

    result = uniquelist(result)
    return(result)


@app.route('/', methods=['GET', 'POST'])
def main():
    global articles

    if request.method == "POST":
        articles = []
        text = request.form.get("textarea")
        # text = request.form['text'].strip()
        data = gettfidf(text)
        # return jsonify(data)
        print(data)
        return render_template('index.html', data=data)
    return render_template('index.html')


if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=8080)
    app.run(debug=True)
