from processing.documentprocessing import DocumentProcessing
import json

devdata=json.load(open("devset.json"))

for key in devdata:
  processor=DocumentProcessing()
  doc=processor.process_text(devdata[key]["claim"])
  print(devdata[key]["claim"], doc.entities)
  for token in doc.doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)  
  print("====================================================================")
