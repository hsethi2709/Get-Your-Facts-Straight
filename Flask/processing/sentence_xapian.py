import xapian
import spacy
import json
from nltk.corpus import wordnet

class SentenceXapian:

    def __init__(self):
        self.indexer = xapian.TermGenerator()
        self.stemmer = xapian.Stem("english")
        self.indexer.set_stemmer(self.stemmer)
        self.nlp = spacy.load("en_core_web_sm")
        self.set_parameters()
        #neuralcoref.add_to_pipe(self.nlp)

    def set_parameters(self):
        self.db = xapian.WritableDatabase('', 
                                xapian.DB_BACKEND_INMEMORY)
        self.qp = xapian.QueryParser()
        self.qp.set_stemmer(self.stemmer)
        self.qp.set_database(self.db)
        self.qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        self.enquire = xapian.Enquire(self.db)
        self.best_sentences_data = {}
        self.added_documents = []

    def add_xapian_doc(self, document, has_pronoun=False):
        document_data=json.loads(document.get_data())
        doc_id=document_data['doc_id']
        print("Adding document with pron ", has_pronoun, doc_id)
        if doc_id in self.added_documents:
            print("Document Already Added", doc_id)
            return
        else:
            self.added_documents.append(doc_id)
        print("Considering Document ", doc_id)
        document_sentences  = ''
        temp_sentences=[]
        for data in list(document_data.keys()):
          if data.startswith("sentence_"):
            try:
              sent_id=data.split("_")[1]
              sentence_data = document_data[data]
              sent_doc=self.nlp(sentence_data)
              text_document_id = ''
              if len([ i for i in sent_doc if i.pos_ == 'PRON']) > 0:
                text_document_id = ' '.join(doc_id.split('_'))
              sentence_now =  text_document_id + ' ' + sentence_data
              sentence_now = sentence_now.strip()

              temp_sentences.append((document_data[data],[doc_id, int(sent_id)]))
              self.best_sentences_data[str(doc_id) + "_" + str(sent_id)] = ( sentence_now, [doc_id, int(sent_id)])
              document_sentences += document_data[data] + ' $$ '
              #self.add_new_document(doc_id+'_'+sent_id, document_data[data])
            except Exception as e:
              print("Getting an exception in sent id", e, data)
        document_sentences = document_sentences.replace("-LRB-", " ").replace("-RRB-", " ")
        #doc = self.nlp(document_sentences)
        #sent=''
        #for token in doc:
        #    if token._.in_coref:
        #      if not (token.i <=token._.coref_clusters[0][0].end and token.i >= token._.coref_clusters[0][0].start):
        #          print(token, token._.coref_clusters[0][0].start, token._.coref_clusters[0][0].end, token._.coref_clusters)
        #          sent += str(token._.coref_clusters[0][0]) + ' '
        #          continue
        #    sent += str(token) + ' '
        #sentence_split = sent.split('$ $')
        #for i,sent in enumerate(sentence_split[:-1]):
        #    print(sent, temp_sentences[i])
        #    sent_id=str(temp_sentences[i][1][0]) + "_" + str(temp_sentences[i][1][1])
        #    if sent_id in self.best_sentences_data:
        #        self.best_sentences_data[sent_id] = (sent, self.best_sentences_data[sent_id][1])


        #print("REPLACED  ", sent)
        #print("Original  ", doc)
        #print("Best Sentences ", self.best_sentences_data)

        
    def add_new_document(self, doc_id, text):
        p_doc = self.nlp(text)
        doc = xapian.Document()
        doc.set_data(doc_id)
        self.indexer.set_document(doc)
        self.indexer.index_text(text)
        for ent in p_doc.ents:
            doc.add_boolean_term(ent.label_.lower())
        self.db.add_document(doc)

    def check_sentence_relevance(self, sentence, filter_tags, filter_words):
        sent = sentence.lower()
        #print("Checking Filters ", filter_words, sent)
        sent_relevance=0
        for word in filter_words:
            if word.lower() in sent:
                sent_relevance += 1
        return sent_relevance
    
    def check_number(self,sent):
        for token in sent:
            if token.pos_ == 'NUM':
                return True
        return False


    def query_index(self, q_text, filters_tags, generate_query):
        filter_words = generate_query.dependency_words
        new_best_sentences={}
        new_best_sentences_data={}
        print("Claim Document:", generate_query.doc)
        num_claim = self.check_number(self.nlp(generate_query.doc.text))
        for sent in self.best_sentences_data:
            nsubj_present = False
            obj_present = False
            appos_present = False
            sentence_lowered = self.best_sentences_data[sent][0].lower()
            if num_claim == True:
                num_sent = self.check_number(self.nlp(self.best_sentences_data[sent][0]))
                if not num_sent:
                    print("Skipping sentence for number ", self.best_sentences_data[sent][0])
                    continue
            new_best_sentences[self.best_sentences_data[sent][0]] = 1
            new_best_sentences_data[self.best_sentences_data[sent][0]] = self.best_sentences_data[sent]
        sorted_sentences=sorted(new_best_sentences, key=new_best_sentences.get, reverse=True)
        s = [ new_best_sentences_data[k] for k in sorted_sentences if new_best_sentences[k] >= 0]
        return s


'''
    def query_index(self, q_text, filters_tags=[], filter_words=[]):
        query = self.qp.parse_query(q_text)
        print("Adding as filters", filters_tags, filter_words)
        if len(filters_tags) > 0:
            filter_ent_tag = [xapian.Query(filter_.lower()) for filter_ in filters_tags]
            filter_dep_word = [xapian.Query(filter_.lower()) for filter_ in filter_words]

            filter_dep_final = xapian.Query(xapian.Query.OP_AND, filter_dep_word)
            filter_tag_final = xapian.Query(xapian.Query.OP_AND, filter_ent_tag)

            filter_final = xapian.Query(xapian.Query.OP_AND, filter_dep_final, filter_tag_final)
            query = xapian.Query(xapian.Query.OP_FILTER, query, filter_final)
        self.enquire.set_query(query)
        return_sent=[]
        for m in self.enquire.get_mset(0,5):
            return_sent.append(self.best_sentences_data[m.document.get_data().decode('utf-8')])
        return return_sent
'''
