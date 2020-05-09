import re
import os.path

# from spyll.hunspell.readers import AffReader, DicReader
# from spyll.hunspell.algo import suggest

from spyll.hunspell.dictionary import Dictionary

def readlist(path):
    if not os.path.isfile(path):
        return []
    # we ignore "incomplete tokenization" feature
    return [ln for ln in open(path).read().splitlines() if ln[-1:] != '.' and ln != '']

def test(name):
    path = f'tests/fixtures/hunspell-orig/{name}'
    dictionary = Dictionary(path)
    bad = readlist(path + '.wrong')
    sug = list(map(lambda s: re.split(r',\s*', s), readlist(path + '.sug')))
    return [
        {
            'word': word,
            'expected': sug[i],
            'got': list(dictionary.suggest(word))
        } for i, word in enumerate(bad)
    ]

def report(name):
    print(name)

    result = test(name)
    for data in result:
        if data['expected'] == data['got']:
            print(f"  {data['word']}: +")
        else:
            print(f"  {data['word']}: {data['expected']} vs {data['got']}")

report('base')