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
from heapq import nlargest
from string import punctuation
thai_stw = list(thai_stopwords())
app = Flask(__name__)


def sumtext(text):
    word_th = word_tokenize(text)

    word_freq_th = {}
    for word in word_th:
        if word not in thai_stw:
            if word not in punctuation:
                if word not in " ":
                    if word not in word_freq_th.keys():
                        word_freq_th[word] = 1
                    else:
                        word_freq_th[word] += 1

    sorted(word_freq_th.items(), key=lambda x: x[1], reverse=True)
    # print(word_freq_th)

    max_freq_th = max(word_freq_th.values())
    for word in word_freq_th.keys():
        word_freq_th[word] = word_freq_th[word]/max_freq_th

    sorted(word_freq_th.items(), key=lambda x: x[1], reverse=True)
    print(word_freq_th)
    sent_th = sent_tokenize(text)
    # print(sent_th)

    sent_scores_th = {}  # สร้าง dictionary
    for sent in sent_th:  # นำประโยคที่ตัดไว้ทุกประโยคมาคำนวณ
        for word in sent:  # เช็ค[คำ]ที่มีในประโยค A
            if word in word_freq_th.keys():  # ถ้าคำในประโยค A มีใน dictionary ของ word_freq_th(เก็บความถี่ของคำที่ตัดได้)
                if sent not in sent_scores_th.keys():  # ถ้าประโยคไม่ได้อยู่ใน dictionary ของ sent_scores_th
                    # ให้ sentence scores เท่ากับ ค่าความถี่ที่ normalize เเล้วของ word frequencies
                    sent_scores_th[sent] = word_freq_th[word]
                else:  # ถ้าประโยคอยู่ใน dictionary ของ sent_scores_th
                    sent_scores_th[sent] += word_freq_th[word]
    sorted(sent_scores_th.items(), key=lambda x: x[1], reverse=True)

    select_len_th = int(len(sent_scores_th)*0.1)
    # print(select_len_th)

    # เเสดงประโยคที่มีความสำคัญมากที่สุดจากค่า sentence scores โดยข้อมูลตัวที่ 1เเละ 2 จาก dict เนื่องจากความยาว len เท่ากับ 2
    sum_th = nlargest(select_len_th, sent_scores_th, key=sent_scores_th.get)
    # print(sum_th)
    sum_th = "".join(sum_th)
    return(sum_th)


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
        newtext = word_tokenize(i, engine='mm')
        no_stopword = [t for t in newtext if t not in thai_stopwords()]
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
        return render_template('index.html', data=data, textsum=sumtext(text))
    return render_template('index.html')


if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=8080)
    app.run(debug=True)
