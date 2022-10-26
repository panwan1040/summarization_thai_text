

from operator import index


def mysent_tokenize(text):
    santhan = getsanthan("./asset/santhan.txt")
    text = text.split(" ")
    listsent = []
    index = 0
    for i in text:
        # text เป็น "เล่าเหตุการณ์ที่เกิดขึ้นว่า"
        tmplist = ""
        for san in santhan:
            # print(i.split(san))
            # เชื่อม ประโยคหลัง
            if i.split(san)[len(i.split(san))-1] == "":
                if i != "":
                    print(i)
                    tmplist += i+" "+text[index+1]

            # เชื่อม ประโยคหน้า
            if i.split(san)[0] == "":
                if i != "":
                    print(i)
                    tmplist += text[index-1]+" "+i

        if i != "":
            listsent.append(tmplist)
        index += 1
    print(listsent)


def getsanthan(pathfile):
    f = open(pathfile, "r", encoding="utf-8")
    return f.read().split("\n")


# mysent_tokenize("xx")


mysent_tokenize(
    "ณ บึงใหญ่ในป่าแห่งหนึ่ง ห่านและนกกระสาชวนกันเดินท่องน้ำหาปลาเล็กปลาน้อยกินเป็นอาหาร สัตว์ทั้งสองไม่รู้ตัวเลยว่าเบื้องหลังพุ่มไม้ที่อยู่ริมบึงนั้น พรานป่าคนหนึ่งยืนถือปืนคอยท่าจะยิงพวกมันอยู่ ในขณะที่นกกระสาค่อยๆ จับปลากินอย่างไม่รีบร้อนนั้น ห่านกลับก้มหน้าก้มตากินอย่างไม่ยั้ง เมื่อนกกระสาหันมาเห็น มันจึงพูดเดือนขึ้นว่า นี่ท่าน ถ้ากินมากขนาดนี้ระวังบินไม่ไหวนะ")
