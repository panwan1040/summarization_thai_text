# coding=utf-8
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
# download('wiki_lm_lstm')

if __name__ == '__main__':
    articles = []

    def main():

        # testtext = """เนื่องจากประโยคภาษาไทย (และอีกหลายๆ ภาษา) คือการเรียงคำหลายๆ คำ ต่อกัน โดยไม่ได้มีการเว้นวรรคระหว่างคำ (space) แบบภาษาอังกฤษ ใครที่มีประโยคภาษาไทย และต้องการแยกในประโยคเพื่อการใช้งานใดๆ ก็ตาม จะต้องประสบกับปัญหาของการไม่มี space ที่ว่า และ PyThaiNLP ก็เข้ามาช่วยในตรงนี้
        # """
        testtext = '''
.
กรณีที่มีผู้โพสต์แนะนำผู้ที่เป็นมะเร็งระยะสุดท้ายให้รักษาด้วยการดื่มน้ำปั่นผักจิงจูฉ่าย ทางสถาบันมะเร็งแห่งชาติ กรมการแพทย์ กระทรวงสาธารณสุข ได้ตรวจสอบข้อมูลและชี้แจงว่า ยังไม่มีหลักฐานงานวิจัยทางคลินิกที่ยืนยันแน่ชัดว่าผักจิงจูฉ่ายช่วยรักษามะเร็งระยะสุดท้ายในมนุษย์ได้ โดยผักจิงจูฉ่าย (Artemisia lactiflora) เป็นพืชท้องถิ่นของประเทศจีนนิยมนำมาใช้ปรุงอาหารอุดมไปด้วยวิตามิน ใยอาหาร และสารต้านอนุมูลอิสระหลายชนิด เช่น สารเบต้าแคโรทีน ไรโบฟลาวิน และแอสคอบิกแอซิด ซึ่งมีส่วนช่วยในการชะลอความเสื่อมของเซลล์ และช่วยกระตุ้นภูมิคุ้มกัน อย่างไรก็ตามงานวิจัยที่เกี่ยวข้องส่วนใหญ่อยู่ในระดับห้องทดลอง และปัจจุบันการรักษาโรคมะเร็งหลัก ๆ มี 3 วิธี ได้แก่ การผ่าตัด การให้ยาเคมีบำบัด และรังสีรักษา ซึ่งทั้งนี้การรับฟังข้อมูลที่ไม่ผ่านการพิจารณาหรือตรวจสอบข้อเท็จจริง อาจทำให้ประชาชนเข้าใจคลาดเคลื่อนและอาจลดโอกาสการรักษาทางการแพทย์ที่ได้มาตรฐาน อีกทั้งควรศึกษารายละเอียดด้านสรรพคุณ ฤทธิ์ทางเภสัชวิทยา และวิธีการใช้สมุนไพรอย่างถูกต้อง โดยเฉพาะผู้ป่วยโรคมะเร็งควรอยู่ภายใต้การดูแลของแพทย์

ดังนั้นขอให้ประชาชนอย่าหลงเชื่อข้อมูลดังกล่าว และขอความร่วมมือไม่ส่ง หรือแชร์ข้อมูลดังกล่าวต่อในช่องทางสื่อสังคมออนไลน์ต่างๆ และเพื่อให้ประชาชนได้รับข้อมูลข่าวสารจากสถาบันมะเร็งแห่งชาติ สามารถติดตามได้ที่เว็บไซต์ http://thaicancernews.nci.go.th/_v2/ หรือ www.nci.go.th หรือโทร. 02 2026800

บทสรุปของเรื่องนี้คือ : ยังไม่มีหลักฐานงานวิจัยทางคลินิกที่ยืนยันแน่ชัดว่าผักจิงจูฉ่ายช่วยรักษามะเร็งระยะสุดท้ายในมนุษย์ได้	
'''
        showtfidf(testtext)

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
        text = mysent_tokenize(text)
        # text = sent_tokenize(text, engine="whitespace+newline")
        # text = mysent_tokenize(text)
        for i in text:
            newtext = word_tokenize(i, engine='deepcut')
            no_stopword = [
                t for t in newtext if t not in thai_stopwords()]
            articles.append(no_stopword)

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
        print(result)
        return result

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

    main()
