import sys
import json
from processing import documentprocessing as docp
import xapian 
import spacy
from allennlp.predictors.predictor import Predictor
from datasetreader import FeverReader
import numpy as np
import traceback


source_file=open(sys.argv[1])

dataset=json.load(source_file)
logit_conv={}
logit_conv[0]='SUPPORTS'
logit_conv[1]='NOT ENOUGH INFO'
logit_conv[2]='REFUTES'

try:
    reader=FeverReader()
    # Open the database for searching.
    database = xapian.Database(sys.argv[2])
    nlp = spacy.load("en_core_web_sm")
    output={}
    # Start an enquire session.
    enquire = xapian.Enquire(database)
    predictor = Predictor.from_path("fevermodelv1.tar.gz")
    keys_run=list(dataset.keys())
    if len(sys.argv) > 4:
        keys_run=[sys.argv[4]]
    for dset in keys_run:
      claim=dataset[dset]['claim']
      print("$$$$$$$$$CLAIM: ", claim)
      print("$$$$$$$$$KEY: ", dset)
      if 'label' in dataset[dset]:
          label=dataset[dset]['label']
          print("$$$$$$Label: ", label)
      else:
          label='TEST SET'
      doc = docp.DocumentProcessing(nlp)
      pdoc=doc.process_text(dataset[dset]['claim'])
      best_sentence=pdoc.run_xapian_query(enquire, database)
      evidence={}
      for sent in best_sentence:
        instance=reader.text_to_instance(hypothesis=claim,premise=sent[0])
        pred=predictor.predict_instance(instance)
        prediction=pred['label_logits']
        biggest=np.argmax(prediction)
        current_prediction=logit_conv[biggest]
        if not current_prediction in evidence:
          evidence[current_prediction]=[]
        evidence[current_prediction].append(sent[1])
        print("sentence: %s\nprediction_logits:%s\nprediction:%s\n"%(sent,str(pred['label_logits']), logit_conv[biggest]))
      final_label='NOT ENOUGH INFO'
      claim_output = {}
      claim_output["claim"] = dataset[dset]['claim']
      if not len(evidence) == 0:
          #if 'SUPPORTS' in evidence and 'REFUTES' in evidence:
          #  if evidence['SUPPORTS'] > evidence['REFUTES']:
          #      final_label='SUPPORTS'
          #  else:
          #      final_label='REFUTES'
          if 'REFUTES' in evidence:
              final_label='REFUTES'
          elif 'SUPPORTS' in evidence:
            final_label='SUPPORTS'
          evidence_=evidence[final_label]
          if 'evidence' in dataset[dset]:
              print_evidence = dataset[dset]['evidence']
          else:
              print_evidence = "TEST SET. Don't have it"
          print("Claim:", dataset[dset]['claim'], "\n",
                  final_label, evidence_, "\n GOLD : ", print_evidence)
          if not final_label == 'NOT ENOUGH INFO':
              claim_output["evidence"] = evidence_
          else:
              claim_output['evidence'] = []
      else:
          claim_output["evidence"] = []

      claim_output["label"] = final_label
      output[dset] = claim_output

    if len(sys.argv) > 4:
        sys.exit(0)
    with open(sys.argv[3],"w") as outfile:
      json.dump(output, outfile, indent=4)
      outfile.close()

      
except Exception as e:
    print("Exception: %s" % str(e))
    traceback.print_exception()
    sys.exit(1)

