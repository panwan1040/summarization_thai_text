from heapq import nlargest
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
from string import punctuation
thai_stopwords = list(thai_stopwords())


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
# mysent_tokenize(
#     "ณ บึงใหญ่ในป่าแห่งหนึ่ง ห่านและนกกระสาชวนกันเดินท่องน้ำหาปลาเล็กปลาน้อยกินเป็นอาหาร สัตว์ทั้งสองไม่รู้ตัวเลยว่าเบื้องหลังพุ่มไม้ที่อยู่ริมบึงนั้น พรานป่าคนหนึ่งยืนถือปืนคอยท่าจะยิงพวกมันอยู่ ในขณะที่นกกระสาค่อยๆ จับปลากินอย่างไม่รีบร้อนนั้น ห่านกลับก้มหน้าก้มตากินอย่างไม่ยั้ง เมื่อนกกระสาหันมาเห็น มันจึงพูดเดือนขึ้นว่า นี่ท่าน ถ้ากินมากขนาดนี้ระวังบินไม่ไหวนะ")

text = """ปฏิบัติการของ กองทัพรัสเซีย ใน ยูเครน เข้าสัปดาห์ที่สอง ยังไม่มีแสงสว่างที่ปลายอุโมงค์ ไม่ว่าจะเป็นการเจรจาสันติภาพหรือการยึดยูเครนได้สำเร็จ ประธานาธิบดีรัสเซีย วลาดิเมียร์ ปูติน ออกสื่อ ชี้ให้เห็นถึงความจำเป็นของรัสเซียที่จะต้องยึดยูเครน เพราะมีคนมาตั้งขีปนาวุธไว้หน้าบ้าน จำเป็นต้องเข้าไปจัดการ เพื่อปกป้องรัสเซีย ตั้งคำถามกับผู้นำสหรัฐฯ โจ ไบเดน และ ผู้นำสหภาพยุโรป ถ้าถูกกระทำแบบเดียวกันนี้จะตัดสินใจอย่างไร ปูติน ไม่ได้พูดถึงเงื่อนไขการยุติสงครามและไม่ได้พูดถึงความสูญเสียที่เกิดขึ้น ท่ามกลาง กระแสคว่ำบาตรรัสเซียอย่างหนักทุกมิติ ผู้นำรัสเซีย ถึงกับประกาศว่า การประกาศคว่ำบาตรรัสเซีย ในครั้งนี้ถือว่าเป็นการประกาศสงครามแล้ว โฟกัสไปถึง สงครามนิวเคลียร์ ทหารรัสเซีย บุกยึดโรงไฟฟ้านิวเคลียร์ในยูเครนได้ 2 แห่ง ห่างจาก กรุงเคียฟ เมืองหลวงของยูเครนไม่กี่ร้อยกิโล มาตรการตัดน้ำตัดไฟของรัสเซีย ไม่ได้ทำให้ยูเครนหวั่นไหวแต่อย่างใด แต่ที่ประธานาธิบดียูเครน เซเลนสกี หวั่นไหว คือท่าทีของ นาโต ไม่ยินดียินร้ายกับ การปิดน่านฟ้าในยูเครน ทำให้ รัสเซีย สามารถเลือกยิงขีปนาวุธถล่มได้ตามอำเภอใจ การปฏิเสธของ นาโต ว่า ยูเครนไม่เกี่ยวอะไรกับนาโต ทำให้ผู้นำยูเครน สะอึก แม้ในทางพฤตินัยจะมีการส่งยุทโธปกรณ์สนับสนุนยูเครนไม่ขาดสาย แต่ก็ไม่มีเครื่องมือยืนยันว่า ในอนาคตทั้ง สหรัฐฯ อังกฤษ และสหภาพยุโรป ยังจะยืนอยู่ข้าง ยูเครน หรือไม่ หรือสุดท้ายแล้วก็ทิ้งให้ ยูเครนโดดเดี่ยว เช่นเดียวกับการต่อสู้เรียกร้องประชาธิปไตยจาก รัฐบาลทหารเมียนมา ในวันนี้ สู้เองเจ็บเอง ประชาชนชาวยูเครน ได้รับผลกระทบจากสงครามไปเต็มๆ คนยูเครนกว่า 1 ล้านคน ต้องอพยพหนีภัยสงคราม บ้านแตกสาแหรกขาด ชีวิตของคนยูเครนจะไม่เหมือนเดิมอีกต่อไป จาก ประชาชน ที่เคยมีประเทศมีชาติเป็นของตัวเอง จะกลายเป็น ผู้อพยพ ไร้ถิ่นฐาน เช่นเดียวกับประเทศในสหภาพยุโรปและประชาชนชาวรัสเซียที่ได้รับผลกระทบทางเศรษฐกิจ การค้าการลงทุน จากมหาเศรษฐีชาวรัสเซีย ต้องยอมขายกิจการทิ้งยอมขาดทุน กลายเป็นชาติที่น่ารังเกียจในสายตาของสังคม สหรัฐฯ มีโอกาสขายน้ำมันได้มากขึ้น ขายอาวุธยุทโธปกรณ์ได้มากขึ้น โจ ไบเดน ผู้นำสหรัฐฯได้รับความสำคัญที่ทั่วโลกต้องจับตาและติดตามถึงท่าทีของ สหรัฐฯ ต่อการตัดสินใจในสงครามยุโรปครั้งนี้ ถ้า ปูติน เป็นผู้ร้าย โจ ไบเดน ก็จะกลายเป็นพระเอกทันที ส่วนประเทศที่อยู่ฝั่งเดียวกับ รัสเซีย หรือไม่มีอาการต่อต้านรัสเซีย เช่น จีน หรือ อินเดีย ก็คงมองเห็นประโยชน์ในอนาคตเพราะเศรษฐกิจของรัสเซียอยู่ในอันดับท็อปไฟว์ของโลก ถ้าจะมีการย้ายฐานเศรษฐกิจ ผลประโยชน์ก็ย่อมตกเป็นของฝ่ายเดียวกัน ส่วนบ้านเรา ส่งออกไปรัสเซียเมื่อปี 2564 มูลค่า 1 พันกว่าล้านบาท เมื่อ เทียบกับการส่งออกไป อียูและสหรัฐฯ แล้วมีมูลค่ามากกว่าเยอะมาก การตัดธนาคารกลางรัสเซีย ออกจาก ระบบสวิฟต์ ก็คงมีผลกระทบกับเราน้อยมากเพราะค่าเงินบาทไปผูกไว้กับตะกร้าเงินดอลลาร์ ปัญหาที่น่ากลัวว่าจะกระทบกับบ้านเรากลับเป็นปัญหาการเมืองในประเทศ ถ้ายังแทงกั๊ก ขาดความชัดเจน โปร่งใสและตรวจสอบได้ ลับ ลวง หลอก เป็นพรหมวิบัติ 4 ใครได้ ใครเสีย ชาวบ้านตาดำๆ รับกรรมไปตามระเบียบ"""


def sumtext(text):
    word_th = word_tokenize(text)

    word_freq_th = {}
    for word in word_th:
        if word not in thai_stopwords:
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


sumtext(text)
