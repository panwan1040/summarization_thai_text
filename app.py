# coding=utf-8
from flask import Flask, render_template, request,jsonify
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


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        articles = []
        text = request.form['text'].strip()
        def tokez(text):
            text = clean_msg(text)
            # ตัดประโยค โดยใช้ วรรคและขึ้นบรรทัดใหม่
            text = mysent_tokenize(text)
            # text = mysent_tokenize(text)
            for i in text:
                newtext = word_tokenize(i, engine='mm')
                no_stopword = [
                    t for t in newtext if t not in thai_stopwords()]
                articles.append(no_stopword)

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

        def showtfidf(text):
            tokez(text)
            dictionary = Dictionary(articles)
            corpus = [dictionary.doc2bow(a) for a in articles]
            result = []
            doc = corpus[0]
            tfidf = TfidfModel(corpus)
            tfidf_weights = tfidf[doc]
            sorted_tfidf_weights = sorted(
                tfidf_weights, key=lambda w: w[1], reverse=True)
            for term_id, weight in sorted_tfidf_weights[:5]:
                tmp = dictionary.get(term_id), weight
                result.append(tmp)
            return(result)

        def mysent_tokenize(text):
            santhan = getsanthan("./asset/santhan.txt")
            text = text.split(" ")
            # listsent = []
            index = 0
            # print(text)
            for i in text:
                tmplist = ""
                # for สำหรับจัดการคำหลังสุดที่เป็นคำสันธานให้เชื่อมกับประโยคถัดไป
                for san in santhan:
                    # ถ้าประโยคหลังเป็นคำสันธาน
                    if i.split(san)[len(i.split(san))-1] == "":
                        if i != "":
                            # print(i)
                            # เชื่อมประโยคถัดไป
                            tmplist = i + " " + text[index+1]
                            text[index] = ""
                            text[index+1] = tmplist
                index += 1
            index = 0
            for i in text:
                tmplist = ""
                # for สำหรับจัดการคำหน้าสุดที่เป็นคำสันธานให้เชื่อมกับประโยคก่อนหน้า
                for san in santhan:
                    # ถ้าประโยคหน้าเป็นคำสันธาน
                    if i.split(san)[0] == "":
                        if i != "":
                            tmplist = text[index-1] + " " + i
                            # print(tmplist)
                            text[index-1] = ""
                            text[index] = tmplist
                # listsent.append(tmplist)
                index += 1
            return list(filter(None, text))

        def getsanthan(pathfile):
            f = open(pathfile, "r", encoding="utf-8")
            return f.read().split("\n")
        data=showtfidf(text)
        return jsonify(data)
    return render_template('index.html')


if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=8080)
    app.run(debug=True)
