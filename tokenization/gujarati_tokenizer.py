import re
import unicodedata
import regex as re2
from typing import List, Dict, Union

def norm(s: str) -> str:
    return unicodedata.normalize('NFC', s)

class AdvancedGujaratiTokenizer:
    def __init__(self):
        #self.GUJARATI_RANGE = r'[\u0A80-\u0AFF]'
        #self.DEVANAGARI_RANGE = r'[\u0900-\u097F]'
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
        #frequently used consonant combinations.
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

    #sentence tokenizer.
    def sentence_tokenize(self, text: str) -> List[str]:
        sentences = re.split(self.SENTENCE_DELIMITERS, text)
        return [sent.strip() for sent in sentences if sent.strip()]
    
    #word tokenizer.
    def word_tokenize(self, text: str) -> List[str]:
        cleaned_text = re.sub(self.IGNORE_CHARS, '', text)
        words = re.split(r'\s+', cleaned_text)
        return [word.strip() for word in words if word.strip()]
    
    #phoneme tokenizer.
    def phoneme_tokenize(self, word: str) -> List[str]:
        word = norm(word)
        tokens = []
        i = 0
        while i < len(word):
            # if combinations are found, add them into the list of tokens
            found_combo = False
            for combo, components in self.consonant_combinations.items():
                if word[i:].startswith(combo):
                    tokens.extend(components)
                    i += len(combo)
                    found_combo = True
                    break
            # if not then parse each letter individually    
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
    
    #syllable tokenizer.
    """def syllable_tokenize(self, word: str) -> List[str]:
        word = norm(word)
        syllables = []
        current_syllable = ""
        i = 0
        
        while i < len(word):
            char = word[i]
            
         # if combinations are found, add them into the list of syllables.
            found_combo = False
            for combo in self.consonant_combinations.keys():
                if word[i:].startswith(combo):
                    if current_syllable:
                        syllables.append(current_syllable)
                        current_syllable = ""
                    current_syllable = combo
                    i += len(combo)
                    found_combo = True
                    break
                
            #for words containing letters from consonent combinations only.
            if found_combo:
                continue
                
            #handling individual consonants, vowels, matras, anusvar and viram.
            if char in self.consonants:
                if current_syllable and not current_syllable.endswith(self.viram):
                    syllables.append(current_syllable)
                    current_syllable = ""
                current_syllable += char
             
                if i + 1 < len(word) and word[i + 1] == self.viram:
                    current_syllable += self.viram
                    i += 2
                    continue
                    
            elif char in self.matra or char == self.anusvar:
                current_syllable += char
                
            elif char in self.vowels:
                if current_syllable:
                    syllables.append(current_syllable)
                current_syllable = char
                
            i += 1
         
        if current_syllable:
            syllables.append(current_syllable)
            
        return syllables"""

    def advanced_tokenize(self, text: str) -> Dict[str, Union[List[str], List[List[str]]]]:
        sentences = self.sentence_tokenize(text)
        words = []
        for sent in sentences:
            words.extend(self.word_tokenize(sent))
        
        return {
            'sentences': sentences,
            'words': words,
            'phonemes': [self.phoneme_tokenize(word) for word in words],
            #'syllables': [self.syllable_tokenize(word) for word in words]
        }