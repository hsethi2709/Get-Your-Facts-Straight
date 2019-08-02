import xapian
import spacy

class SentenceXapian:

    def __init__(self):
        self.indexer = xapian.TermGenerator()
        self.stemmer = xapian.Stem("english")
        self.indexer.set_stemmer(self.stemmer)
        self.nlp = spacy.load("en_core_web_sm")
        self.set_parameters()

    def set_parameters(self):
        self.db = xapian.WritableDatabase('', 
                                xapian.DB_BACKEND_INMEMORY)
        self.qp = xapian.QueryParser()
        self.qp.set_stemmer(self.stemmer)
        self.qp.set_database(self.db)
        self.qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        self.enquire = xapian.Enquire(self.db)

    def add_new_document(self, doc_id, text):
        p_doc = self.nlp(text)
        doc = xapian.Document()
        doc.set_data(doc_id)
        self.indexer.set_document(doc)
        self.indexer.index_text(text)
        for ent in p_doc.ents:
            doc.add_boolean_term(ent.label_.lower())
        self.db.add_document(doc)

    def query_index(self, q_text, filters=[]):
        query = self.qp.parse_query(q_text)
        print("Adding as filters", filters)
        if len(filters) > 0:
            filter_entitites = [xapian.Query(filter_.lower()) for filter_ in filters]
            filter_final = xapian.Query(xapian.Query.OP_AND, filter_entitites)
            query = xapian.Query(xapian.Query.OP_FILTER, query, filter_final)
        self.enquire.set_query(query)
        return self.enquire.get_mset(0, 5)
