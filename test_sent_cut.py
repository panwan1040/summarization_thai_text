

import string
import re
from pythainlp import sent_tokenize
import itertools
from collections import defaultdict
from gensim.corpora.dictionary import Dictionary
from pythainlp.corpus import download, get_corpus_path
from pythainlp.corpus import thai_stopwords
from pythainlp.tokenize import word_tokenize
from gensim.models.tfidfmodel import TfidfModel
from tkinter import N
from operator import index


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


def uniquelist(list1):

    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return unique_list


# mysent_tokenize("xx")
mysent_tokenize(
    "ณ บึงใหญ่ในป่าแห่งหนึ่ง ห่านและนกกระสาชวนกันเดินท่องน้ำหาปลาเล็กปลาน้อยกินเป็นอาหาร สัตว์ทั้งสองไม่รู้ตัวเลยว่าเบื้องหลังพุ่มไม้ที่อยู่ริมบึงนั้น พรานป่าคนหนึ่งยืนถือปืนคอยท่าจะยิงพวกมันอยู่ ในขณะที่นกกระสาค่อยๆ จับปลากินอย่างไม่รีบร้อนนั้น ห่านกลับก้มหน้าก้มตากินอย่างไม่ยั้ง เมื่อนกกระสาหันมาเห็น มันจึงพูดเดือนขึ้นว่า นี่ท่าน ถ้ากินมากขนาดนี้ระวังบินไม่ไหวนะ")
