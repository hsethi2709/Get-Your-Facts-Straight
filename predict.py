import sys
import nltk
from bs4 import BeautifulSoup
import requests
import json
from processing import documentprocessing as docp
import xapian
import spacy
from allennlp.predictors.predictor import Predictor
from processing.process_evidence import ProcessEvidence
from datasetreader import FeverReader
import numpy as np
from urllib.parse import unquote
import wikipedia_search
import wikipedia_page
claim = sys.argv[1]
claim = unquote(claim)
logit_conv = {}
#level = 1
logit_conv[1] = 'SUPPORTS'
logit_conv[0] = 'NOT ENOUGH INFO'
logit_conv[2] = 'REFUTES'

def predict_label(claim, level):
    
    logit_conv = {}
    logit_conv[1] = 'SUPPORTS'
    logit_conv[0] = 'NOT ENOUGH INFO'
    logit_conv[2] = 'REFUTES'


    try:
        reader = FeverReader()
        database = xapian.Database("wikidb")
        nlp = spacy.load("en_core_web_sm")
        enquire = xapian.Enquire(database)
        predictor = Predictor.from_path("fever_combined_model.tar.gz")
        print("CLAIM", claim)
        doc = docp.DocumentProcessing(nlp)
        pdoc = doc.process_text(claim)
        best_sentence = pdoc.run_xapian_query(enquire,database)
        evidence = {}
        for sent in best_sentence:
            instance = reader.text_to_instance(hypothesis=claim,premise=sent[0])
            pred = predictor.predict_instance(instance)
            prediction = pred['label_logits']
            biggest = np.argmax(prediction)
            label_score = prediction[biggest]
            current_prediction = logit_conv[biggest]
            if not current_prediction in evidence:
                evidence[current_prediction]=[]
            evidence[current_prediction].append((sent[1], label_score, sent[0], sent[1]))
            print("sentence: %s\nprediction_logits:%s\nprediction:%s\n"%(sent,str(pred['label_logits']),logit_conv[biggest]))

        process_evidence = ProcessEvidence()
        if level == 3:
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['SUPPORTS'], claim_output['REFUTES'] = process_evidence.process_evidence(evidence,level)
            return claim_output
        final_label, f_evidence = process_evidence.process_evidence(evidence,level)
        if len(f_evidence) == 0:
            evidence = wikipediaSearch(claim)
            final_label, f_evidence = process_evidence.process_evidence(evidence, level)
            print("$$$$$$$$$$$ EVIDENCES:",f_evidence)
        claim_output = {}
        claim_output["claim"] = claim
        claim_output["label"] = final_label
        claim_output["evidence"] = f_evidence[:5]
        print("\nClaim Output",claim_output)
        return claim_output

    except Exception as e:
        print("Exception: %s" % str(e))
        sys.exit(1)

def wikipediaSearch(claim):
    logit_conv = {}
    logit_conv[1] = 'SUPPORTS'
    logit_conv[0] = 'NOT ENOUGH INFO'
    logit_conv[2] = 'REFUTES'

    try:
        reader = FeverReader()
        nlp = spacy.load("en_core_web_sm")
        predictor = Predictor.from_path("fever_combined_model.tar.gz")
        print("GOING TO WIKIPEDIA WITH CLAIM:", claim)
        doc = docp.DocumentProcessing(nlp)
        pdoc = doc.process_text(claim)
        entities = []
        best_sentence = []
        # Get all the entities and go to Wikipedia and get the sentences
        entities = pdoc.generate_query.get_entities(under_scored=True)
        if len(entities) == 0:
            entities = pdoc.generate_query.get_document_query()
        print("Looking for Entities", entities)
        for ent in entities:
           pages = wikipedia_search.page_lookup(ent)
           if ent.lower() == 'coronavirus':
               pages.append({"title":"Misinformation related to the 2019–20 coronavirus outbreak"})
           for page in pages:
                print("PAGE:", page['title'])
                print("")
                text_pages = wikipedia_page.get_text_from_page(page['title'])['pages']
                for item in text_pages:
                    raw_html = (text_pages[item]['extract'])
                    cleantext = BeautifulSoup(raw_html, "html.parser").text
                    a_list = nltk.tokenize.sent_tokenize(cleantext)
                    for sent in a_list:
                        best_sentence.append(sent.strip())
        evidence = {}
        print(best_sentence)
        for sent in best_sentence:
            if len(nltk.word_tokenize(sent)) < 3:
                continue
            instance = reader.text_to_instance(hypothesis=claim,premise=sent[0])
            pred = predictor.predict_instance(instance)
            prediction = pred['label_logits']
            biggest = np.argmax(prediction)
            label_score = prediction[biggest]
            current_prediction = logit_conv[biggest]
            if not current_prediction in evidence:
                evidence[current_prediction]=[]
            evidence[current_prediction].append((sent[1], label_score, sent[0], sent[1]))
            print("sentence: %s\nprediction_logits:%s\nprediction:%s\n"%(sent,str(pred['label_logits']),logit_conv[biggest]))
        return evidence
    except Exception as e:
        print("Exception: %s" % str(e))
        sys.exit(1)


predict_label(claim, 1)
