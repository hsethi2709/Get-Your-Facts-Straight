import json
import sys
import xapian
import  processing.documentprocessing as docp
import spacy

dataset=json.load(open(sys.argv[1]))
data = []
try:
    database = xapian.Database(sys.argv[2])
    enquire = xapian.Enquire(database)
    nlp = spacy.load("en_core_web_sm")
    for dset in dataset.keys():
        if dataset[dset]['label'] == "SUPPORTS" or dataset[dset]['label'] == "REFUTES":
            for evidence in dataset[dset]['evidence']:
                sdocid=evidence[0]
                sentence=evidence[1]
                nextdoc=next(database.postlist(sdocid), 'not-found')
                if nextdoc is 'not-found':
                    print("Not found doc", sdocid.encode('utf-8'), file=sys.stderr)
                    continue
                xapiandoc=database.get_document(next(database.postlist(sdocid.encode('utf-8'))).docid)
                sdata=json.loads(xapiandoc.get_data())
                sent_id=str('sentence_'+str(sentence))
                if sent_id in sdata:
                    this_sent=sdata[sent_id]
                else:
                    print("Sentence not in document", sentence, sdocid, file=sys.stderr)
                    continue
                data.append({"claim":dataset[dset]['claim'],"evidence":this_sent,"label":dataset[dset]['label']})
                output = dataset[dset]['claim'] + ',' + this_sent + ',' + dataset[dset]['label']
        elif dataset[dset]['label'] == "NOT ENOUGH INFO":
          doc = docp.DocumentProcessing(nlp)
          pdoc=doc.process_text(dataset[dset]['claim'])
          sentences=pdoc.run_xapian_query(enquire, database, True)
          print("Got sentences ", sentences)
          for sentence in sentences[:5]:
              data.append({"claim":dataset[dset]['claim'],"evidence":sentence[0],"label":dataset[dset]['label']})
              output = dataset[dset]['claim'] + ',' + sentence[0] + ',' + dataset[dset]['label']
              print(output)

    with open (sys.argv[3], 'w') as outFile:
        json.dump(data,outFile, indent=4)
except Exception as e:
    print("Got exception",e)
