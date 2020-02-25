from conllu import parse
import requests
from typing import Iterable, Any


def get_analysis(filename: str):
    with open(filename, 'rb') as fp:
        res = requests.post('http://localhost:15000', data=fp.read())
    if res.status_code == 200:
        return parse(res.content.decode())


def find_sentences_with_second_person(document: Iterable[Any]):
    def sentence_has_second_person(sentence) -> bool:
        return any((word['feats']['Person'] == '2' for word in sentence
                    if word is not None
                        and word['feats'] is not None
                        and 'Person' in word['feats']))

    return [sentence for sentence in document if sentence_has_second_person(sentence)]
