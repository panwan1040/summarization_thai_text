from gensim.models.tfidfmodel import TfidfModel
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
from pythainlp.corpus import download, get_corpus_path
from pythainlp.corpus import thai_stopwords

from gensim.corpora.dictionary import Dictionary
from collections import defaultdict
import itertools

# download('wiki_lm_lstm')

articles = []


def tokez(text):
    for i in text:
        newtext = word_tokenize(i, engine='mm')
        no_stopword = [t for t in newtext if t not in thai_stopwords()]
        # print(no_stopword)
        articles.append(no_stopword)


tokez(["จึงสู้อุตส่าห์ซื้อหนังสือแปลที่อ่านไม่ค่อยรู้เรื่องมาช่วยแปลไทยเป็นไทยอีกทีหนึ่ง",
      "รวมทั้งผู้สนใจอนุรักษ์ภาษาได้ดำเนินการแก้ไขการใช้ภาษาที่ผิดๆ", 'ภาษาไทยก็เป็นภาษาที่ใช้เป็นสื่อในการแสดงความรู้'])


dictionary = Dictionary(articles)
corpus = [dictionary.doc2bow(a) for a in articles]


doc = corpus[0]
tfidf = TfidfModel(corpus)
tfidf_weights = tfidf[doc]
print(tfidf_weights)


# print(tfidf)
