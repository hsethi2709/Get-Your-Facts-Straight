import sys
import json
from processing import documentprocessing as docp
import xapian
import spacy
from allennlp.predictors.predictor import Predictor
from processing.process_evidence import ProcessEvidence
from datasetreader import FeverReader
import numpy as np
from urllib.parse import unquote

claim = sys.argv[1]
claim = unquote(claim)
logit_conv = {}
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

        claim_output = {}
        claim_output["claim"] = claim
        claim_output["label"] = final_label
        claim_output["evidence"] = f_evidence[:5]
        print("\nClaim Output",claim_output)
        return claim_output

    except Exception as e:
        print("Exception: %s" % str(e))
        sys.exit(1)

#predict_label(claim,level)
