import re
import numpy as np
from typing import Dict, List, Any

class GujaratiPhonemeDictionary:
    """Comprehensive Gujarati Phoneme Mapping"""
    def __init__(self):
        # Vowels 
        self.vowels = {
            'અ': '/ə/', 'આ': '/aː/', 
            'ઇ': '/i/', 'ઈ': '/iː/',
            'ઉ': '/u/', 'ઊ': '/uː/', 
            'ઋ': '/ɾ̩/', 'ૠ': '/ɾ̩ː/',
            'એ': '/eː/', 'ઐ': '/əi/', 
            'ઓ': '/oː/', 'ઔ': '/əu/',
            'અં': '/əŋ/',
            'ા': '/aː/', 
            'િ': '/i/', 'ી': '/iː/', 
            'ુ': '/u/', 'ૂ': '/uː/',
            'ૃ': '/ɾ̩/', 'ૄ': '/ɾ̩ː/', 
            'ે': '/eː/', 'ૈ': '/əi/',
            'ો': '/oː/', 'ૌ': '/əu/'
        }
        
        # Vowel Modifiers
        self.vowel_modifiers = {
            'ં': '/ŋ/',   # Anusvara
            'ઃ': '/h/',   # Visarga
            'ઁ': '/˜/',   # Candrabindu
            '્': None     # Virama (Halant)
        }
        
        # Consonants
        self.consonants = {
            'ક': '/k/', 'ગ': '/ɡ/', 'ચ': '/tʃ/', 'જ': '/dʒ/',
            'ટ': '/ʈ/', 'ડ': '/ɖ/', 
            'ત': '/t/',
            'દ': '/d̪/',
            'પ': '/p/', 'બ': '/b/',
            'ખ': '/kʰ/', 'ઘ': '/ɡʱ/',
            'છ': '/tʃʰ/', 'ઝ': '/dʒʱ/',
            'ઠ': '/ʈʰ/', 'ઢ': '/ɖʱ/', 'થ': '/t̪ʰ/', 'ધ': '/d̪ʱ/',
            'ફ': '/pʰ/',
            'ભ': '/bʱ/',
            'મ': '/m/', 'ન': '/n/', 'ણ': '/ɳ/', 'ઙ': '/ŋ/', 'ઞ': '/ɲ/',
            'સ': '/s/', 'શ': '/ʃ/', 'હ': '/h/', 'ષ': '/ʂ/',
            'ય': '/j/', 'ર': '/ɾ/', 'લ': '/l/', 'વ': '/ʋ/', 'ળ': '/ɭ/'
        }
        
        # Digits
        self.digits = {
            '૦': '0', '૧': '1', '૨': '2', '૩': '3', '૪': '4',
            '૫': '5', '૬': '6', '૭': '7', '૮': '8', '૯': '9'
        }


class GujaratiProsodyModel:
    """Prosody modeling for Gujarati speech"""
    def __init__(self):
        # Stress patterns based on syllable position
        self.stress_patterns = {
            'initial': 1.2,    # Initial syllable stress
            'medial': 1.0,     # Normal stress
            'final': 1.3,      # Final syllable stress
            'penultimate': 1.15 # Second-to-last syllable stress
        }
        
        # Pitch contours for different sentence types
        self.intonation_contours = {
            'statement': lambda x: 0.9 + 0.2 * np.sin(x * np.pi),
            'question': lambda x: 1.0 + 0.3 * np.sin(x * np.pi * 1.5),
            'exclamation': lambda x: 1.2 + 0.4 * np.sin(x * np.pi * 0.8)
        }
        
        # Duration modifiers based on phoneme type
        self.duration_modifiers = {
            'vowel': 1.2,       # Vowels are longer
            'consonant': 0.8,    # Consonants are shorter
            'consonant-vowel': 1.0  # Normal duration
        }
    
    def analyze_sentence_structure(self, phoneme_details: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze sentence structure for prosody generation"""
        num_phonemes = len(phoneme_details)
        enhanced_phonemes = []
        
        for i, phoneme in enumerate(phoneme_details):
            position = self._determine_position(i, num_phonemes)
            stress = self._apply_stress_pattern(position)
            duration = self._apply_duration_modifier(phoneme['type'])
            
            enhanced_phonemes.append({
                **phoneme,
                'position': position,
                'stress': stress,
                'duration': duration,
                'base_pitch': 1.0
            })
        
        return enhanced_phonemes
    
    def _determine_position(self, index: int, total: int) -> str:
        """Determine phoneme position in sentence"""
        if index == 0:
            return 'initial'
        elif index == total - 1:
            return 'final'
        elif index == total - 2:
            return 'penultimate'
        return 'medial'
    
    def _apply_stress_pattern(self, position: str) -> float:
        """Apply stress pattern based on position"""
        return self.stress_patterns.get(position, 1.0)
    
    def _apply_duration_modifier(self, phoneme_type: str) -> float:
        """Apply duration modification based on phoneme type"""
        return self.duration_modifiers.get(phoneme_type, 1.0)
    
    def apply_intonation(self, enhanced_phonemes: List[Dict[str, Any]], 
                        sentence_type: str = 'statement') -> List[Dict[str, Any]]:
        """Apply intonation contour to phonemes"""
        contour_func = self.intonation_contours.get(sentence_type, 
                                                  self.intonation_contours['statement'])
        num_phonemes = len(enhanced_phonemes)
        
        for i, phoneme in enumerate(enhanced_phonemes):
            norm_pos = i / (num_phonemes - 1) if num_phonemes > 1 else 0.5
            pitch_multiplier = contour_func(norm_pos)
            phoneme['pitch'] = phoneme['base_pitch'] * pitch_multiplier * phoneme['stress']
            phoneme['pitch'] *= np.random.uniform(0.95, 1.05)
        
        return enhanced_phonemes
    
    def generate_prosody(self, phoneme_details: List[Dict[str, Any]], 
                        sentence_type: str = 'statement') -> Dict[str, Any]:
        """Complete prosody generation pipeline"""
        enhanced = self.analyze_sentence_structure(phoneme_details)
        prosodic_phonemes = self.apply_intonation(enhanced, sentence_type)
        
        # Calculate rhythm metrics
        durations = [p['duration'] for p in prosodic_phonemes]
        pitches = [p['pitch'] for p in prosodic_phonemes]
        
        rhythm = {
            'avg_duration': np.mean(durations),
            'duration_variance': np.var(durations),
            'avg_pitch': np.mean(pitches),
            'pitch_range': max(pitches) - min(pitches),
            'speech_rate': len(phoneme_details) / sum(durations)
        }
        
        return {
            'phonemes': prosodic_phonemes,
            'rhythm': rhythm,
            'sentence_type': sentence_type
        }

def process_gujarati_text(text: str, sentence_type: str = "statement") -> Dict[str, Any]:
    """Process Gujarati text through the full pipeline"""
    # Initialize components
    phoneme_dict = GujaratiPhonemeDictionary()
    prosody_model = GujaratiProsodyModel()
    
    # Normalize text
    normalized_text = re.sub(r'[^\u0A80-\u0AFF\s,?!]', '', text.strip())
    normalized_text = re.sub(r'\s+', ' ', normalized_text)
    
    # Phoneme extraction
    characters = list(normalized_text)
    phonemes = []
    phoneme_details = []
    graphemes = []
    
    i = 0
    while i < len(characters):
        current_char = characters[i]
        
        # Handle consonants
        if current_char in phoneme_dict.consonants:
            consonant_phoneme = phoneme_dict.consonants[current_char]
            
            # Check for vowel modifier
            if i + 1 < len(characters) and characters[i+1] in phoneme_dict.vowel_modifiers:
                vowel_modifier = phoneme_dict.vowel_modifiers[characters[i+1]]
                combined_phoneme = f"{consonant_phoneme[:-1]}{vowel_modifier}"  # Remove duplicate vowel
                phonemes.append(combined_phoneme)
                phoneme_details.append({
                    'type': 'consonant-vowel',
                    'base': consonant_phoneme,
                    'modifier': vowel_modifier,
                    'grapheme': current_char + characters[i+1]
                })
                graphemes.append(current_char + characters[i+1])
                i += 2
            else:
                phonemes.append(consonant_phoneme)
                phoneme_details.append({
                    'type': 'consonant',
                    'base': consonant_phoneme,
                    'grapheme': current_char
                })
                graphemes.append(current_char)
                i += 1
        
        # Handle vowels
        elif current_char in phoneme_dict.vowels:
            vowel_phoneme = phoneme_dict.vowels[current_char]
            phonemes.append(vowel_phoneme)
            phoneme_details.append({
                'type': 'vowel',
                'base': vowel_phoneme,
                'grapheme': current_char
            })
            graphemes.append(current_char)
            i += 1
        
        # Handle punctuation and spaces
        else:
            if current_char.strip():  # If not whitespace
                phonemes.append(current_char)
                phoneme_details.append({
                    'type': 'punctuation',
                    'base': current_char,
                    'grapheme': current_char
                })
                graphemes.append(current_char)
            i += 1
    
    # Prosody modeling (excluding punctuation)
    prosody_result = prosody_model.generate_prosody(
        [p for p in phoneme_details if p['type'] != 'punctuation'],
        sentence_type
    )
    
    return {
        'original_text': text,
        'normalized_text': normalized_text,
        'graphemes': graphemes,
        'phonemes': phonemes,
        'phoneme_details': phoneme_details,
        'prosody': prosody_result
    }