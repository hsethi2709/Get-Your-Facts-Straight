from typing import Dict
import json
from overrides import overrides
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.tokenizers import Tokenizer, WordTokenizer
from allennlp.data.instance import Instance
from allennlp.data.fields import Field, TextField, LabelField, MetadataField
from allennlp.data.token_indexers import SingleIdTokenIndexer, TokenIndexer

@DatasetReader.register("fever")
class FeverReader(DatasetReader):

	def __init__(self,
                 tokenizer: Tokenizer = None,
                 token_indexers: Dict[str, TokenIndexer] = None,
                 lazy: bool = False) -> None:
		super().__init__(lazy)
		self._tokenizer = tokenizer or WordTokenizer()
		self._token_indexers = token_indexers or {'tokens': SingleIdTokenIndexer()}


	@overrides
	def _read(self,file_path: str):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    print("Original Data",len(data))
                    for dd,sample in enumerate(data):
                        premise = sample["evidence"]
                        hypothesis = sample["claim"]
                        label = sample["label"]
                        yield self.text_to_instance(premise, hypothesis, label)
	@overrides
	def text_to_instance(self, premise, hypothesis, label=None) -> Instance:

		fields = {}
		premise_tokens = self._tokenizer.tokenize(premise)
		hypothesis_tokens = self._tokenizer.tokenize(hypothesis)
		fields['premise'] = TextField(premise_tokens, self._token_indexers)
		fields['hypothesis'] = TextField(hypothesis_tokens, self._token_indexers)
		if label:
			fields['label'] = LabelField(label)

		metadata = {"premise_tokens": [x.text for x in premise_tokens],
					"hypothesis_tokens": [x.text for x in hypothesis_tokens]}

		fields["metadata"] = MetadataField(metadata)
		return Instance(fields)
