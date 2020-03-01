from conllu import parse
import os
import webvtt
import requests
from typing import Iterable, Any, List, Callable
import re
import io
from collections import OrderedDict
from functools import partial


def read_vtt(filename: str) -> List[str]:
    # with open(filename, 'rb') as fp:
    #     raw_data = fp.read()

    str_list = [l if not l.startswith('-') else l[1:]
                for l in (part.strip()
                    for k in webvtt.read(filename)
                    # for k in webvtt.read_buffer(io.StringIO(raw_data.replace(b'\xc2\xa0',b'').decode()))
                    for part in k.text.split('\n'))]
    line_list = []
    buf = ''
    for line in str_list:
        if line.endswith('-'):
            buf += line[:-1]
        elif (not line.endswith('!')) and (not line.endswith('?')) and (not line.endswith('.')):
            buf += (line + ' ')
        else:
            line_list.append((buf + line) if len(buf) != 0 else line)
            buf = ''
    return line_list


def f_or(*args):
    return partial(_f_or, args=args)

def _f_or(first, args):
    return any((fu(first) for fu in args))


def f_and(*args):
    return partial(_f_and, args=args)

def _f_and(first, args):
    return all((fu(first) for fu in args))


def is_2pp(w: OrderedDict):
    try:
        return w['feats']['Number'] == 'Plur' and is_2p(w)
    except BaseException:
        return False


def is_2p(w: OrderedDict):
    try:
        return w['feats']['Person'] == '2'
    except BaseException:
        return False


def is_2ps(w: OrderedDict):
    try:
        return w['feats']['Number'] == 'Sing' and is_2p(w)
    except BaseException:
        return False


def is_propn(w: OrderedDict):
    return 'upostag' in w.keys() and (w['upostag'] == 'PROPN' or w['upostag'] == 'PRON')


def get_analysis(filename: str):
    data = read_vtt(filename)
    res = requests.post('http://localhost:15000',
                        headers={'Content-Type': 'text/plain; charset=utf-8'},
                        data=b'\n'.join((l.encode('utf-8') for l in data)))
    if res.status_code == 200:
        return parse(res.content.decode())


def find_sentences_with_condition(document: Iterable[Any], cond: Callable[[OrderedDict], bool]):
    def any_in_sent(sentence, cond):
        return any((word for word in sentence if cond(word)))

    return [sentence for sentence in document if any_in_sent(sentence, cond)]


def find_sentences_with_second_person(document: Iterable[Any]):
    def sentence_has_second_person(sentence) -> bool:
        return any((word['feats']['Person'] == '2' for word in sentence
                    if word is not None
                        and word['feats'] is not None
                        and 'Person' in word['feats']))

    return [sentence for sentence in document if sentence_has_second_person(sentence)]


def read_dir(directory: str):
   return [line for fn in os.listdir(directory) for line in get_analysis(directory + '/' + fn)
           if len(line) > 1]
