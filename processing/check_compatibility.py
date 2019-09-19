import numpy as np
import math
from collections import defaultdict
import itertools
from functools import reduce #python 3
import time
from nltk.corpus import wordnet as wn


def cosine_similarity(dep_claim, dep_sent, debug=False, wordnet=True):

    if dep_claim[1].mean() == 0 or dep_sent[1].mean() == 0 or (not dep_sent[1].shape[0] == 300) or (not dep_claim[1].shape[0] == 300):
        similar=dep_claim[0] in  dep_sent[0] or dep_sent[0] in dep_claim[0]
        if similar:
            similarity = 0.9876543
        else:
            similarity = 0.12345
        wordnet = True
    else:
        vector1 = dep_claim[1]
        vector2 = dep_sent[1]
        print("VbeVector 1 ", dep_claim[0] ,dep_claim[1].mean(),vector1.shape, dep_sent[0], dep_sent[1].mean(), vector2.shape)
        similarity = np.sum(np.dot(vector1, vector2))/(math.sqrt(np.sum(vector1**2)) * math.sqrt(np.sum(vector2**2)))
    if debug:
        print("Mean Vector cosine similarity ", dep_claim[0], dep_claim[1].mean(), dep_sent[0], dep_sent[1].mean(), "Similarity ", similarity)
    if similarity > 60 or (not wordnet):
        return similarity
    claim = dep_claim[0].strip()
    claim = claim.replace(' ', '_')
    sent = dep_sent[0].strip()
    sent = sent.replace(' ', '_')
    print("Checking similarity for ", sent, claim)
    if wn.synsets(claim) == []:
        syns_claim = None
    else:
        syns_claim = wn.synsets(claim)[0]

    if wn.synsets(sent) == []:
        syns_sent = None
    else:
        syns_sent = wn.synsets(sent)[0]

    if syns_claim and syns_sent:
        if syns_claim == syns_sent:
            similarity = 0.91234
            return similarity
        else:
            similarity_cosine = wn.wup_similarity(syns_claim, syns_sent)
            if similarity_cosine and similarity_cosine > 0.80:
                return similarity_cosine
    return similarity


class CheckComptability:
    def __init__(self, nlp_, claim, nlp_vec):
        self.nlp = nlp_
        self.nlpvec = nlp_vec
        d_claim = self.nlp(claim)
        self.c_vectors = self.get_vectors(d_claim)
        self.object_dict = defaultdict(list)

    def get_vectors(self, sentence):
        vectors={}
        mapping = {'nsubj': 'nsubj', 'nsubjpass': 'nsubj', 'pobj': 'obj', 'dobj': 'obj', 'ROOT': 'ROOT' ,'attr': 'attr'}
        for nphr in itertools.chain(sentence.noun_chunks, sentence):
            text=''
            vector=np.zeros(300)
            if hasattr(nphr, 'dep_'):
                # This condition activates for notmal words
                # Remove if it's a stop word
                dependency = nphr.dep_
                text=nphr.text
                vector = self.nlpvec(nphr.text).vector
                if nphr.is_stop or (not (dependency == 'ROOT')):
                    continue
            else:
                if nphr.root.is_stop:
                    continue
                dependency = nphr.root.dep_
                for i in range(nphr.start,nphr.end):
                    num=0
                    if (not sentence[i].is_stop):
                        text += ' ' + sentence[i].text
                        #vector += self.nlpvec(sentence[i].text).vector
                        num +=1
                    if num>0:
                        vector /= num
                    if not text.strip():
                        print("Got no text on iterating !!!")
                        continue
                    else:
                        vector = self.nlpvec(text).vector



            print(text, dependency)
            if dependency in ['nsubj', 'nsubjpass', 'pobj', 'dobj', 'ROOT', 'attr']:
                vector_represen=vector
                vector_text=text
                if not mapping[dependency] in vectors:
                    vectors[mapping[dependency]] = []
                vectors[mapping[dependency]].append((vector_text, vector_represen))
        vectors['ents']=[]
        for ent in sentence.ents:
            vectors['ents'].append((ent.text, ent.vector))
        return vectors

    def check_compatibility(self, sentence, debug=False):
        d_sentence = self.nlp(sentence)
        sentence_vectors = self.get_vectors(d_sentence)
        claim_vectors = self.c_vectors

        # Reinitialize
        self.object_dict = defaultdict(list)

        for key in ['nsubj', 'obj', 'ents', 'attr']:
            self.object_dict[key]
            if not key in claim_vectors.keys():
                self.object_dict[key].append(("NOT_IN_CLAIM", 0))
            if (key in claim_vectors.keys()):
                if debug: print("Processing ", key)
                for dep_claim in claim_vectors[key]:
                    self.object_dict[dep_claim[0]]
                    for dep_sent in reduce(lambda x,y: x+y,sentence_vectors.values()):
                        similarity = cosine_similarity(dep_claim, dep_sent, debug, True)
                        if similarity > 0.70:
                            if not (dep_sent[0], similarity) in self.object_dict[dep_claim[0]]:
                                self.object_dict[dep_claim[0]].append((dep_sent[0], similarity))
                            if not (dep_sent[0], similarity) in self.object_dict[key]:
                                self.object_dict[key].append((dep_sent[0], similarity))
                    if len(self.object_dict[dep_claim[0]]) == 0:
                        print("Checking sentence if entity occur", dep_claim[0])
                        all_nan = True
                        for i in d_sentence:
                            if not i.is_stop:
                                check_wordnet = False
                                if i.pos_ in ['VERB', 'NOUN', 'PROPN', 'ADJ']:
                                    check_wordnet = True
                                similarity = cosine_similarity(dep_claim, (i.text, i.vector), debug, True)
                                if similarity > 0.65:
                                    self.object_dict[dep_claim[0]].append((i.text, similarity))
                                    self.object_dict[key].append((i.text, similarity))
                                    all_nan = False
                                    continue
                                elif not similarity == float('nan'):
                                    all_nan = False
                        if all_nan:
                            self.object_dict[dep_claim[0]].append(("ALL_NONE", 0))
            elif key in claim_vectors.keys():
                self.object_dict[key]
                for dep_claim in claim_vectors[key]:
                    self.object_dict[dep_claim[0]]
        return self.object_dict

    def ensure_all_objects(self):
        all_object_present = True
        for i in self.object_dict.keys():
            if i not in ['nsubj', 'obj', 'ents', 'attr']:
                if len(self.object_dict[i]) == 0:
                    print("Object ", i, "Not present")
                    all_object_present = False
        return all_object_present

    def ensure_all_obj_cats(self):
        all_obj_cats = True
        for i in ['nsubj', 'obj', 'ents']:
            if len(self.object_dict[i]) == 0:
                print("OBJ CAT ", i, "Not present")
                all_obj_cats = False
        return all_obj_cats
