from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from functools import reduce

def get_similar_words(word):
    count_synsets={}
    #for syn in wordnet.synsets(word):
    #    for lemma in syn.lemmas():
    #        if lemma.name() == word:
    #            count_synsets[syn]= lemma.count()
    sorted_counts=sorted(count_synsets,key=lambda k: count_synsets[k], reverse=True)
    print(" Sort ", sorted_counts, count_synsets)
    if len(sorted_counts) > 0:
        final_words=[ synonym.name().split('_') for synonym in  sorted_counts[0].lemmas()]
        final_words=list(set(reduce(lambda x,y: x+y, final_words)))
    else:
        final_words = []
    return final_words

def join_with_ADJ(entities):
    query_string = ''
    contain_ADJ = False
    for enty in entities:
        if 'ADJ' in enty:
            contain_ADJ = True
    join_on = ' '
    if contain_ADJ:
        join_on = ' , '
    else:
        join_on = ' ADJ '
    if len(entities) == 2:
        query_string += join_on.join(entities)
    elif len(entities) > 2:
        query_string += join_on.join(entities[:2])
        query_string += ' , '
        query_string += ' '.join(entities[3:])
    elif len(entities) == 1:
        query_string += ' ' + entities[0]
    return query_string



class GenerateQuery:
    def __init__(self, doc):
        self.doc = doc
        self.lemmatizer = WordNetLemmatizer()
        self.entities=[]
        self.nouns=[]
        self.verb=[]
        self.nsubj=[]
        self.has_pronoun=False
        self.dobj=''
        self.pobj=''
        self.appos=''
        self.propnoun = []
        self.max_dependency = Counter()
        self.dependency_childrens = {}
        self.doc_depend = []
        self.do_ordered_entities()
        self.query_entities = self.get_query_entities()
        self.dependency_words = self.get_dep_words()
        print("Query Entities ", self.entities
                , self.query_entities, self.doc.ents)
        #for t in self.doc:
        #    print(t.text, t.pos_)

    def get_entities(self, under_scored=False, labels=False):
        consider_entities=[]
        for ent in self.doc.ents:
            if under_scored:
                spans=[]
                for span in ent:
                    spans.append(span.text)
                consider_entities.append('_'.join(spans))
            else:
                if labels:
                    consider_entities.append(ent.label_)
                else:
                    consider_entities.append(ent.text)
        return consider_entities

    def get_dep_words(self):
        consider_entities = []
        self.doc_depend = []
        for token in self.doc:
            if token.dep_ == "nsubj" or token.dep_ == "nsubjpass":
                if token.is_alpha and (not token.is_stop):
                    consider_entities.append(token.text)
                if token.children:
                    compound = []
                    for child in token.children:
                        compound.append(child.text)
                    compound.append(token.text)
                    compound_word = join_with_ADJ(compound)
                    #self.nsubj = ' '.join(compound)
                    self.nsubj.extend(compound)
                    if not compound_word in self.query_entities:
                        self.doc_depend.append(compound_word)
            elif token.dep_ == "ROOT":
                if token.is_alpha and (not token.is_stop):
                    consider_entities.append(token.text)
            elif token.dep_ == "dobj" or token.dep_ == 'pobj':
                if token.is_alpha and (not token.is_stop):
                    if token.dep_ == 'dobj':
                        self.dobj = token.text
                    elif token.dep_ == 'pobj':
                        self.pobj = token.text
                    self.doc_depend.append(token.text)
                    consider_entities.append(token.text)
            elif token.dep_ == 'appos':
                if token.is_alpha and (not token.is_stop):
                    self.appos = token.text
        with_syn_entities = []
        #for word in consider_entities:
        #    with_syn_entities.append(word)
        #    with_syn_entities.extend(get_similar_words(self.lemmatizer.lemmatize(word)))
        print("Considering dependency, filter", consider_entities)
        return with_syn_entities

    def do_ordered_entities(self):
        current_running_entity=[]
        current_entity_type=""
        for token in self.doc:
            print("Toekn ", token, token.pos_)
            if token.pos_ == 'PRON':
                print("Making pronoung")
                self.has_pronoun = True
            if token.is_alpha and (not token.is_stop):
                childrens = [ child for child in token.children]
                print("DEP: ", token, childrens, token.dep_, token.head.text,  token.pos_)
                self.max_dependency[token] = len(childrens)
                self.dependency_childrens[token] = childrens
            if token.ent_iob_ == 'B':
                # Starting of new Entity Store and empty old entity.
                if len(current_running_entity) > 0:
                    self.entities.append({'type': current_entity_type, 'entity': current_running_entity})
                    current_running_entity = []
                    current_entity_type = ""
                current_running_entity.append(token)
                current_entity_type = token.ent_type_
                continue
            elif token.ent_iob_ == 'I':
                current_running_entity.append(token)
                continue
            elif token.ent_iob_ == 'O' and current_entity_type:
                if len(current_running_entity) > 0:
                    self.entities.append({'type': current_entity_type, 'entity': current_running_entity})
                    current_running_entity = []
                    current_entity_type = ''
            if token.is_alpha and (not token.is_stop):
                if token.pos_ == 'NOUN':
                  self.nouns.append(token.text)
                elif token.pos_ == 'PROPN':
                  self.propnoun.append(token.text)
                elif token.pos_ == 'VERB':
                  self.verb.append(token.text)

    def get_query_entities(self):
        consider_entities = []
        if len(self.entities) > 0:
            for ent in self.entities:
                if ent['type'] in ['PERSON', 'WORK_OF_ART', 'EVENT', 'PRODUCT', 'ORG', 'GPE']:
                #if True:
                    if len(ent['entity']) > 1:
                        entity_all=[]
                        for tok in ent['entity']:
                            if not tok.is_stop:
                                entity_all.append(tok.text)
                        consider_entities.append(join_with_ADJ(entity_all))
                    else:
                        consider_entities.append(ent['entity'][0].text)
        return consider_entities

    def consider_appending(self, current_entities, tentetive_list):
        if len(current_entities) > 2:
            return current_entities
        for item in tentetive_list:
            have_entity=False
            for ent in current_entities:
                if item in ent:
                    have_entity= True
            if not have_entity:
                current_entities.append(item)

    def get_document_query(self):
        consider_entities=self.query_entities
        #consider_entities.extend(self.doc_depend)
        self.consider_appending(consider_entities, self.propnoun)
        self.consider_appending(consider_entities, self.nsubj)
        self.consider_appending(consider_entities, [self.pobj, self.dobj, self.appos])
        

        if len(consider_entities) > 1:
            return consider_entities

        #if len(consider_entities) < 2:
        #    consider_entities.extend(self.nouns)
        #if len(consider_entities) < 2:
        #    consider_entities.extend(self.verb)

        if len(consider_entities) == 2:
            consider_entities=[join_with_ADJ( consider_entities)]
        return consider_entities

    def get_sentence_query(self):
        consider_entities=self.query_entities
        consider_entities.extend(self.verb)
        consider_entities.extend(self.nouns)
        consider_entities.extend(self.propnoun)
        return consider_entities

