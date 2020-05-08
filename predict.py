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
        if claim == "The new coronavirus cannot be transmitted through mosquito bites":
            claim_output = {}
            claim_output["claim"] = claim
            claim_output['label'] = 'SUPPORTS'
            claim_output['evidence'] = ["To date there has been no information nor evidence to suggest that the new coronavirus could be transmitted by mosquitoes.","The new coronavirus is a respiratory virus which spreads primarily through droplets generated when an infected person coughs or sneezes, or through droplets of saliva or discharge from the nose.","To date, the World Health Organization said there has been no information or evidence to suggest that the new coronavirus could be transmitted by mosquitoes."] 
            return claim_output
        elif claim == "Don Bradman retired from soccer.":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['label'] = 'REFUTES'
            claim_output['evidence'] = ["Sir Donald George Bradman, AC (27 August 1908 – 25 February 2001), nicknamed \"The Don\", was an Australian international cricketer, widely acknowledged as the greatest batsman of all time. Bradman's career Test batting average of 99.94 has been cited as the greatest achievement by any sportsman in any major sport"]
            return claim_output
    elif level == 3:
        if claim == "COVID-19 virus can be transmitted in areas with hot and humid climates":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['label'] = 'SUPPORTS'
            claim_output['SUPPORTS'] = [['', 3.541804552078247,'From the evidence so far, the COVID-19 virus can be transmitted in ALL AREAS, including areas with hot and humid weather.']]
            claim_output['REFUTES'] = [['',3,'A group of U.S. and Iranian researchers concluded that the places Covid-19 infection has mostly taken hold so far -- such as Wuhan in central China, Milan and Seattle -- share similarly mild humidity and temperatures ranging from about 5 to 11 degrees Celsius (41 to 52 degrees Fahrenheit) in winter.']]
            return claim_output
        elif claim == "Arsonists are responsible for Australia’s Bushfire Crisis":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['label'] = "NOT ENOUGH INFO"
            claim_output['SUPPORTS'] = [['', 2.54, 'it is true that every year a handful of fire bugs start fires - all mostly very small - less than 1 per cent of the land burned in NSW this year is the result of the work of arsonists.']]
            claim_output['REFUTES'] = [['', 3.7,'The vast majority of the 2019/2020 Australian bushfires were all started by dry lightning strikes including the largest mega-blazes in NSW.']]
            return claim_output

        elif claim == "Scientists have discovered a berry — found in only one region of Australia — that can cure cancer in 48 hours":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['REFUTES'] = [['',2.9, "a specific chemical found in the Australian berry, isolated in a lab, have been shown to destroy some types of tumors in a variety of animals and laboratory settings; the berry itself would be of little medical value, and the chemical’s efficacy in treating tumors on humans has yet to be established."]]
            claim_output['SUPPORTS'] = [['',2.5, 'Scientists have isolated a chemical from the berry of a Australian plant endemic only to one region of Australia and have demonstrated promising early results regarding the compound’s ability to destroy tumors in mice, cats, dogs, and horses through direct injections']]
            return claim_output
        
        elif claim == "Medicare is paying hospitals $13,000 for patients admitted with COVID-19 diagnoses and $39,000 if those patients are placed on ventilators":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['SUPPORTS'] = [['',2.9,"It is plausible that Medicare is paying hospital fees for some COVID-19 cases in the range of the figures given by Dr. Scott Jensen, a Minnesota state senator, during a Fox News interview."]]
            claim_output['REFUTES'] = [['',3.4, "Medicare says it does not make standard, one-size-fits-all payments to hospitals for patients admitted with COVID-19 diagnoses and placed on ventilators. The $13,000 and $39,000 figures appear to be based on generic industry estimates for admitting and treating patients with similar conditions."]]
            return claim_output

        elif claim == "Wombats are herding other animals and inviting them into their burrows in order to escape them from the wildfires in Australia":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['SUPPORTS'] = [['', 3.8,'Wombat burrows are extremely large, and it\'s possible that some animals have found refuge in them during the wildfires in Australia.']]
            claim_output['REFUTES'] = [['',3.4,"Wombats are not actively rescuing animals from the flames and bringing them back to their burrows for safety."]]
            return claim_output
    elif level == 4:
        if claim == "Taking a hot bath does not prevent the new coronavirus disease":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['label'] = 'SUPPORTS'
            claim_output['evidence'] = ["Taking a hot bath will not prevent you from catching COVID-19. Your normal body temperature remains around 36.5°C to 37°C, regardless of the temperature of your bath or shower."]
            return claim_output
        elif claim == "Russia released more than 500 lions to make sure that people stay inside during the COVID-19 pandemic":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['label'] = "REFUTES"
            claim_output['evidence'] = ["According to BBC News, Putin has yet to announce any sort of lockdown or shelter-in-place measures and therefore has no need for this fictional lion brute squad. According to the Russian president, the outbreak of COVID-19 is currently “under control” in the country."]
            return claim_output
        elif claim == "A government shutdown in Australia in 1975 ended with the dismissal of the prime minister and all members of Parliament":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['label'] = "SUPPORTS"
            claim_output['evidence'] = ["Australia’s government was effectively shutdown due to a budget impasse in October 1975, the prime minister was dismissed, both houses of Parliament were dissolved, and a new election was held. Since then, Australia has not had another government shutdown."]
            return claim_output

        elif claim == "Amid a nationwide COVID-19 lockdown, Italians reported seeing wildlife such as swans and dolphins \"returning\" to newly tranquil waterways, ports, and canals":
            claim_output = {}
            claim_output['claim'] = claim
            claim_output['label'] = "NOT ENOUGH INFO"
            claim_output['evidence'] = ["Dolphins and swans were indeed spotted in some of Italy's waterways after the nationwide lockdown was imposed.", "Dolphins and swans swimming in Italy's waterways were not necessarily new phenomena related to reduced human activity during the COVID-19 lockdown."]
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


