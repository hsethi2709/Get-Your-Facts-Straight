

class GenerateQuery:
    def __init__(self, doc):
        self.doc = doc
        self.entities=[]
        self.nouns=[]
        self.verb=[]
        self.propnoun = []
        self.do_ordered_entities()
        self.query_entities = self.get_query_entities()
        print("Query Entities ", self.entities
                , self.query_entities, self.doc.ents)
        for t in self.doc:
            print(t.text, t.pos_)

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

    def do_ordered_entities(self):
        current_running_entity=[]
        current_entity_type=""
        for token in self.doc:
            print("DOC, ",token, [ child for child in token.children])
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
                    if len(ent['entity']) > 1:
                        entity_all=[]
                        for tok in ent['entity']:
                            if not tok.is_stop:
                                entity_all.append(tok.text)
                        consider_entities.append(' ADJ '.join(entity_all))
                    else:
                        consider_entities.append(ent['entity'][0].text)
        return consider_entities

    def get_document_query(self):
        consider_entities=self.query_entities
        consider_entities.extend(self.propnoun)

        if len(consider_entities) > 1:
            return consider_entities

        if len(consider_entities) < 2:
            consider_entities.extend(self.nouns)
        if len(consider_entities) < 2:
            consider_entities.extend(self.verb)

        if len(consider_entities) == 2:
            consider_entities=[' ADJ '.join(consider_entities)]
        return consider_entities

    def get_sentence_query(self):
        consider_entities=self.query_entities
        consider_entities.extend(self.verb)
        consider_entities.extend(self.nouns)
        consider_entities.extend(self.propnoun)
        return consider_entities

