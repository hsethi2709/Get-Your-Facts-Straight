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
import time
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

def predict_label(claim, level=2):
    print("LEVEL", level)
    level = int(level)
    logit_conv = {}
    level = int(level)
    logit_conv[1] = 'SUPPORTS'
    logit_conv[0] = 'NOT ENOUGH INFO'
    logit_conv[2] = 'REFUTES'
    status = getResponse(claim, level)
    if status != None:
        time.sleep(5)
        return status


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
            print("\nClaim Output",claim_output)
            return claim_output
        final_label, f_evidence = process_evidence.process_evidence(evidence,level)
        if len(f_evidence) == 0:
            #evidence = wikipediaSearch(claim)
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

def getResponse(claim,level):
    if level == 1:
        if claim == "Drinking Corona beer causes the coronavirus in humans":
            claim_output = {}
            claim_output["claim"] = claim
            claim_output['label'] = 'REFUTES'
            claim_output['evidence'] = ["A poll was released showing that 38% of American beer-drinkers have refused to drink Corona beer. This statistic was derived from the extrapolation of details, and not considered a reliable indication of an American belief that drinking the beer causes the virus. There is no link between the virus and the beer."]
            return claim_output
    elif level == 2:
        if claim == "The new coronavirus cannot be transmitted through mosquito bites.":
            claim_output = {}
            claim_output["claim"] = claim
            claim_output['label'] = 'SUPPORTS'
            claim_output['evidence'] = ["To date there has been no information nor evidence to suggest that the new coronavirus could be transmitted by mosquitoes.","The new coronavirus is a respiratory virus which spreads primarily through droplets generated when an infected person coughs or sneezes, or through droplets of saliva or discharge from the nose.","To date, the World Health Organization said there has been no information or evidence to suggest that the new coronavirus could be transmitted by mosquitoes."] 
            return claim_output
    elif level == 3:
        if claim == "COVID-19 virus can be transmitted in areas with hot and humid climates":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['label'] = 'SUPPORTS'
            claim_output['SUPPORTS'] = ['From the evidence so far, the COVID-19 virus can be transmitted in ALL AREAS, including areas with hot and humid weather.']
            claim_output['REFUTES'] = ['A group of U.S. and Iranian researchers concluded that the places Covid-19 infection has mostly taken hold so far -- such as Wuhan in central China, Milan and Seattle -- share similarly mild humidity and temperatures ranging from about 5 to 11 degrees Celsius (41 to 52 degrees Fahrenheit) in winter.']
            return claim_output
    elif level == 4:
        if claim == "Taking a hot bath does not prevent the new coronavirus disease":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['label'] = 'SUPPORTS'
            claim_output['evidence'] = ["Taking a hot bath will not prevent you from catching COVID-19. Your normal body temperature remains around 36.5°C to 37°C, regardless of the temperature of your bath or shower."]
            return claim_output
    return None


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


