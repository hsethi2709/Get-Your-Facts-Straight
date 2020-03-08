import spacy
import xapian
import json
import sys
from . import sentence_xapian as sent_xap
from .generate_query import GenerateQuery 


class ProcessedDocument:

  def __init__(self, nlp_, sent_index_, doc_):
    self.nlp=nlp_
    self.doc=doc_
    self.entities = []
    self.mapped_entities = {}
    self.sentence_indexer = sent_index_
    self.generate_query= GenerateQuery(self.doc)

  def get_best_sentences(self, matches, extra_documents, single=False):
      #print("Getting best sentences for", self.doc, self.doc.ents)
      single_best_sentence=[]
      best_sentences={}
      best_sentences_data={}
      self.sentence_indexer.set_parameters()
      for doc in extra_documents:
          print("Generated Query pronoun", self.generate_query.has_pronoun)
          self.sentence_indexer.add_xapian_doc(doc, self.generate_query.has_pronoun)
      for m in matches:
          if True:
              self.sentence_indexer.add_xapian_doc(m.document)
      query_string = str.join(' , ', self.generate_query.get_sentence_query())
      print("Running Sentence Query ", query_string)
      return_sent=self.sentence_indexer.query_index(query_string,
                            self.generate_query.get_entities(labels=True), self.generate_query)
      return return_sent

  def run_xapian_query(self, enquire, database, single=False):
      query_string = str.join(' , ', self.generate_query.get_document_query())
      print("Doing Query", query_string)
      qp = xapian.QueryParser()
      #qp.set_default_op(xapian.Query.OP_AND)
      stemmer = xapian.Stem("english")
      qp.set_stemmer(stemmer)
      qp.set_database(database)
      qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
      query = qp.parse_query(query_string)
      print(query)
      # Find the top 10 results for the query.
      enquire.set_query(query)
      sys.stdout.flush()
      matches = enquire.get_mset(0, 10)
      underscored_enti = self.generate_query.get_entities(under_scored=True)
      print("Underscore_enti", underscored_enti)
      matched_document_entity=[]
      for ent_und in underscored_enti:
          posting_list=database.postlist(ent_und)
          posting=next(posting_list, None)
          if posting:
              matched_document_entity.append(database.get_document(posting.docid))
      print("Done Query")
      sys.stdout.flush()
      return self.get_best_sentences(matches, matched_document_entity, single)

class DocumentProcessing:

  def __init__(self, nlp_):
    self.nlp = nlp_
    self.sentence_indexer=sent_xap.SentenceXapian()

  def process_text(self, text):
    doc = self.nlp(text)
    processed_document = ProcessedDocument(self.nlp, self.sentence_indexer, doc)
    for ent in doc.ents:
      if not ent.label_ in processed_document.mapped_entities:
        processed_document.mapped_entities[ent.label_] = []
      processed_document.mapped_entities[ent.label_].append(ent.text)
      processed_document.entities.append(ent.text)
    return processed_document
