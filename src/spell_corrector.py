import re
from collections import Counter

class SpellCorrector:
    def __init__(self, corpus_path):
        with open(corpus_path, 'r', encoding='utf-8') as f:
            text = f.read().lower()
        self.words = re.findall(r'\w+', text)
        self.WORDS = Counter(self.words)

    def P(self, word):
        return self.WORDS[word] / sum(self.WORDS.values())

    def correction(self, word):
        return max(self.candidates(word), key=self.P)

    def candidates(self, word):
        return (self.known([word]) or
                self.known(self.edits1(word)) or
                self.known(self.edits2(word)) or
                [word])

    def known(self, words):
        return set(w for w in words if w in self.WORDS)

    def edits1(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
