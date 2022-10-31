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
        testtext = '''เปิดใจจจจจครูศูนย์เด็กเล็กหนองบัวลำภู ร่ำไห้บอกไม่เอะใจ อดีตตำรวจบุกกราดยิง เพราะเป็นผู้ปกครอง ลูกก็เรียนที่นี่ พอรู้ว่ากำลังก่อเหตุ รีบวิ่งไปหาคนช่วย แต่ไม่ทัน
        วันที่ 6 ต.ค. 65 ผู้สื่อข่าวรายงานบรรยากาศล่าสุดหรือ ที่ศูนย์พัฒนาเด็กเล็กตำบลอุทัยสวรรค์ จ.หนองบัวลำภู ว่า บรรยากาศค่อนข้างวุ่นวาย เนื่องจากเจ้าหน้าที่กู้ภัยยังไม่สามารถเข้าไปตรวจสอบ หรือเคลื่อนย้ายผู้เสียชีวิตได้ เพราะตอนนี้อยู่ระหว่างเจ้าหน้าที่ตำรวจพิสูจน์หลักฐาน เข้าตรวจสอบพื้นที่ โดยมีผู้ปกครอง และชาวบ้านในพื้นที่ เข้ามาติดตามสถานการณ์

        สอบถามคุณครูประจำศูนย์เด็กเล็ก ร่ำไห้ เสียงสั่นเครือ เล่าเหตุการณ์ที่เกิดขึ้นว่า นายปัญญา ซึ่งเป็นอดีตตำรวจคนนี้ เป็นหนึ่งในผู้ปกครอง ที่พาเด็กมาฝากเรียนที่ศูนย์ แต่เด็กไม่ได้มาเรียนได้ประมาณ 1 เดือนแล้ว ทำให้ตอนที่เข้ามา ไม่มีใครเอะใจ เพราะคิดว่าจะมาเอานม ก่อนที่นายปัญญา จะก่อเหตุยิงเจ้าหน้าที่ของศูนย์เด็กเล็กที่นั่งกินข้าวอยู่บริเวณเต็นท์ด้านข้าง 

        ตอนนั้นตนได้ยินเสียงคล้ายประทัด เมื่อมองออกไป ก็เห็นว่า นายปัญญา กำลังเดินตรงมาที่ศูนย์จึงรีบไปล็อกประตู และพยายามวิ่งออกไปทางด้านหลังเพื่อจะตามคนมาช่วย ก่อนที่นายปัญญาจะใช้ปืนยิงที่ประตู และเข้ามาด้านในได้

        เบื้องต้น คาดว่า เด็กทั้งหมด 3 ห้องน่าจะมีรวมกันประมาณ 24 คน กำลังอยู่ระหว่างนอนกลางวัน ซึ่งคาดว่า ขณะที่เขาเข้ามาอาจจะใช้มีดเป็นอาวุธ เพราะไม่ได้ยินเสียงปืนอีก ซึ่งในจำนวนนี้มีเด็ก 1 คน ไม่ได้รับบาดเจ็บ และอีกคนบาดเจ็บ ถูกนำตัวส่งโรงพยาบาลแล้ว

        โดยระหว่างที่เล่าเหตุการณ์คุณครูได้ร่ำไห้ออกมา เนื่องจากเสียใจ เพราะตั้งใจจะรีบไปตามคนมาช่วย แต่ก็ไม่ทัน.'''
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
        # text = mysent_tokenize(text)
        for i in text:
            newtext = word_tokenize(i, engine='mm')
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
