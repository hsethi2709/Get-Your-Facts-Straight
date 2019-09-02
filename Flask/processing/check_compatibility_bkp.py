import spacy
import numpy as np
import math
from collections import defaultdict
import itertools
from functools import reduce #python 3


def cosine_similarity(dep_claim, dep_sent, debug=False):
    if dep_claim[1].mean() == 0 or dep_sent[1].mean() == 0:
        similar=dep_claim[0] in  dep_sent[0] or dep_sent[0] in dep_claim[0]
        if similar:
            similarity = 0.9876543
        else:
            similarity = 0.12345
    else:
        vector1 = dep_claim[1]
        vector2 = dep_sent[1]
        similarity = np.sum(np.dot(vector1, vector2))/(math.sqrt(np.sum(vector1**2)) * math.sqrt(np.sum(vector2**2)))
    if debug: print("Mean Vector cosine similarity ", dep_claim[0], dep_claim[1].mean(), dep_sent[0], dep_sent[1].mean(), "Similarity ", similarity)
    return similarity


class CheckComptability:
    def __init__(self, nlp_):
        self.nlp = nlp_
        self.object_dict = defaultdict(list)

    def get_vectors(self, sentence):
        vectors={}
        mapping = {'nsubj': 'nsubj', 'nsubjpass': 'nsubj', 'pobj': 'obj', 'dobj': 'obj', 'ROOT': 'ROOT' ,'attr': 'attr'}
        for np in itertools.chain(sentence.noun_chunks, sentence):
            if hasattr(np, 'dep_'):
                # This condition activates for notmal words
                # Remove if it's a stop word
                dependency = np.dep_
                if np.is_stop or (not (dependency == 'ROOT')):
                    continue
            else:
                if np.root.is_stop:
                    continue
                dependency = np.root.dep_

            print(np.text, dependency)
            if dependency in ['nsubj', 'nsubjpass', 'pobj', 'dobj', 'ROOT', 'attr']:
                vector_represen=np.vector
                vector_text=np.text
                if not mapping[dependency] in vectors:
                    vectors[mapping[dependency]] = []
                vectors[mapping[dependency]].append((vector_text, vector_represen))
        vectors['ents']=[]
        for ent in sentence.ents:
            vectors['ents'].append((ent.text, ent.vector))
        return vectors

    def check_compatibility(self, claim, sentence, debug=False):
        d_claim = self.nlp(claim)
        d_sentence = self.nlp(sentence)
        claim_vectors = self.get_vectors(d_claim)
        sentence_vectors = self.get_vectors(d_sentence)
        for key in ['nsubj', 'obj', 'ents', 'ROOT', 'attr']:
            self.object_dict[key]
            if not key in claim_vectors.keys():
                self.object_dict[key].append(("NOT_IN_CLAIM", 0))
            if (key in claim_vectors.keys()):
                if debug: print("Processing ", key)
                for dep_claim in claim_vectors[key]:
                    self.object_dict[dep_claim[0]]
                    for dep_sent in reduce(lambda x,y: x+y,sentence_vectors.values()):
                        similarity = cosine_similarity(dep_claim, dep_sent, debug)
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
                                similarity = cosine_similarity(dep_claim, (i.text, i.vector), debug)
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
