
class ProcessEvidence:

    def __init__(self):
        self.evidence = 'NOT Processed'
    
    def process_evidence(self, evidences, sort=False, threshold=False):
        evidence_support = []
        evidence_refute = []
        if 'REFUTES' in evidences:
            evidence_refute = evidences['REFUTES']
            if sort:
                evidence_refute = sorted(evidence_refute, key=lambda x: x[1], reverse=True)
        elif 'SUPPORTS' in evidences:
            evidence_support = evidences['SUPPORTS']
            if sort:
                evidence_support = sorted(evidence_support, key=lambda x: x[1], reverse=True)
        print("Evidences: SUPPORTS:")
        for i in evidence_support:
            print(i)
        print("Evidences: REFUTES:")
        for i in evidence_refute:
            print(i)
        final_label='NOT ENOUGH INFO'
        evidence=[]
        if len(evidence_support) > 0 and len(evidence_refute) > 0:
            if evidence_support[1] > evidence_refute[1]:
                final_label='SUPPORTS'
                evidence = [ evi[2] for evi in evidence_support]
            else:
                final_label='REFUTES'
                evidence = [ evi[2] for evi in evidence_refute]
        elif len(evidence_support) > 0:
            final_label='SUPPORTS'
            evidence = [ evi[2] for evi in evidence_support]
        elif len(evidence_refute) > 0:
            final_label='REFUTES'
            evidence = [ evi[2] for evi in evidence_refute]
        return final_label, evidence



