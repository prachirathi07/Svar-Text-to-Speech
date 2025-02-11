import re
import unicodedata
from typing import List, Dict, Union

def norm(s: str) -> str:
    return unicodedata.normalize('NFC', s)

class AdvancedGujaratiTokenizer:
    def __init__(self):
        self.SENTENCE_DELIMITERS = r'[।!?.]'
        self.IGNORE_CHARS = r'[,;:()]'  
       
        self.nukta = 'ઁ'
        self.anusvar = 'ં'
        self.visarg = 'ઃ'
        self.viram = '્'
        
        self.vowels = ['અ', 'આ', 'ઇ', 'ઈ', 'ઉ', 'ઊ', 'ઋ', 'એ', 'ઐ', 'ઓ', 'ઔ']
        self.matra = ['ા', 'િ', 'ી', 'ુ', 'ૂ', 'ૃ', 'ે', 'ૈ', 'ો', 'ૌ']
        self.all_vowels = self.vowels + self.matra
        
        self.consonants = [
            'ક', 'ખ', 'ગ', 'ઘ', 'ચ', 'છ', 'જ', 'ઝ', 'ટ', 'ઠ',
            'ડ', 'ઢ', 'ણ', 'ત', 'થ', 'દ', 'ધ', 'ન', 'પ', 'ફ',
            'બ', 'ભ', 'મ', 'ય', 'ર', 'લ', 'વ', 'શ', 'ષ', 'સ',
            'હ', 'ળ', 'ઞ'
        ]

        self.consonant_combinations = {
            'ક્ષ': ['ક', '્', 'ષ'],
            'જ્ઞ': ['જ', '્', 'ઞ'],
            'શ્ર': ['શ', '્', 'ર'],
            'ત્ર': ['ત', '્', 'ર'],
            'દ્ર': ['દ', '્', 'ર'],
            'દ્વ': ['દ', '્', 'વ'],
            'દ્ય': ['દ', '્', 'ય'],
            'ન્ન': ['ન', '્', 'ન'],
            'પ્ર': ['પ', '્', 'ર'],
        }

    def sentence_tokenize(self, text: str) -> List[str]:
        sentences = re.split(self.SENTENCE_DELIMITERS, text)
        return [sent.strip() for sent in sentences if sent.strip()]
    
    def word_tokenize(self, text: str) -> List[str]:
        cleaned_text = re.sub(self.IGNORE_CHARS, '', text)
        words = re.split(r'\s+', cleaned_text)
        return [word.strip() for word in words if word.strip()]
    
    def phoneme_tokenize(self, word: str) -> List[str]:
        word = norm(word)
        tokens = []
        i = 0
        while i < len(word):
            found_combo = False
            for combo, components in self.consonant_combinations.items():
                if word[i:].startswith(combo):
                    tokens.extend(components)
                    i += len(combo)
                    found_combo = True
                    break
            if not found_combo:
                char = word[i]
                if char == self.anusvar:
                    tokens.append('ં')
                elif char == self.viram:
                    tokens.append('્')
                elif char in self.matra:
                    tokens.append(char)
                elif char in self.consonants:
                    tokens.append(char)
                elif char in self.vowels:
                    tokens.append(char)
                else:
                    tokens.append(char)
                i += 1
        
        return tokens

    def advanced_tokenize(self, text: str) -> Dict[str, Union[List[str], List[List[str]]]]:
        sentences = self.sentence_tokenize(text)
        words = []
        for sent in sentences:
            words.extend(self.word_tokenize(sent))
        
        return {
            'sentences': sentences,
            'words': words,
            'phonemes': [self.phoneme_tokenize(word) for word in words],
        }