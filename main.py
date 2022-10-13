from gensim.models.tfidfmodel import TfidfModel
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
from pythainlp.corpus import download, get_corpus_path
from pythainlp.corpus import thai_stopwords

from gensim.corpora.dictionary import Dictionary
from collections import defaultdict
import itertools
from pythainlp import sent_tokenize
# download('wiki_lm_lstm')


if __name__ == '__main__':
    articles = []

    def main():
        testtext = """เนื่องจากประโยคภาษาไทย (และอีกหลายๆ ภาษา) คือการเรียงคำหลายๆ คำ ต่อกัน โดยไม่ได้มีการเว้นวรรคระหว่างคำ (space) แบบภาษาอังกฤษ ใครที่มีประโยคภาษาไทย และต้องการแยกในประโยคเพื่อการใช้งานใดๆ ก็ตาม จะต้องประสบกับปัญหาของการไม่มี space ที่ว่า และ PyThaiNLP ก็เข้ามาช่วยในตรงนี้
        
        """
        showtfidf(testtext)

    def tokez(text):
        # ตัดประโยค โดยใช้ วรรคและขึ้นบรรทัดใหม่
        text = sent_tokenize(text, engine="whitespace+newline")
        for i in text:
            newtext = word_tokenize(i, engine='mm')
            no_stopword = [t for t in newtext if t not in thai_stopwords()]
            # print(no_stopword)
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

    main()
