#!/usr/bin/env python
#
# Index each paragraph of a text file as a Xapian document.
#
# Copyright (C) 2003 James Aylett
# Copyright (C) 2004,2007 Olly Betts
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301
# USA

import sys
import xapian
import string
import json
import spacy

if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: %s PATH_TO_DATABASE" % sys.argv[0]
    sys.exit(1)

try:
    # Open the database for update, creating a new database if necessary.
    database = xapian.WritableDatabase(sys.argv[1], xapian.DB_CREATE_OR_OPEN)

    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)
    num_documents=0
    nlp=spacy.load("en_core_web_sm")
    doc_id=""
    para = ''
    data_record={}
    data_record["doc_id"]=doc_id
    try:
        for line in sys.stdin:
            line = line.strip()
            data=line.split()
            if doc_id != data[0]:
                num_documents +=1
                # We've reached the end of a paragraph, so index it.
                doc = xapian.Document()
                string_data=json.dumps(data_record)
                doc.set_data(string_data)
                #spacy_doc=nlp(para)
                #for ent in spacy_doc.ents:
                #    doc.add_boolean_term(ent.label_+":"+ent.text)
                    #print("Adding entity", ent.text, doc_id)
                indexer.set_document(doc)
                indexer.index_text(para)

                # Add the document to the database.
                if doc_id:
                    doc.add_boolean_term(doc_id.encode('utf-8'))
                    database.add_document(doc)
                print("Doing document", num_documents, doc_id)

                para = ''
                doc_id=data[0]
                data_record={}
                data_record["doc_id"]=doc_id
                data_record["sentence_"+data[1]] = " ".join(data[2:])
                para = " ".join(data[2:])
            else:
                if para != '':
                    para += ' '
                para += " ".join(data[2:])
                data_record["sentence_"+data[1]] = " ".join(data[2:])
            if not num_documents%90000:
                print("Doing commit", num_documents)
                database.commit()
                print("Done commit", num_documents)
    except StopIteration:
        pass

except Exception as e:
    print("Exception: %s" % str(e))
    sys.exit(1)
