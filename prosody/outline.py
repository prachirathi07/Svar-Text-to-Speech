import re
import numpy as np
from typing import Dict, List, Any

class GujaratiPhonemeDictionary:
    """Comprehensive Gujarati Phoneme Mapping"""
    def __init__(self):
        # Vowel Phonemes
        self.vowels = {
            'અ': 'a', 'આ': 'aa', 'ઇ': 'i', 'ઈ': 'ii',
            'ઉ': 'u', 'ઊ': 'uu', 'એ': 'e', 'ઐ': 'ai',
            'ઓ': 'o', 'ઔ': 'au'
        }
        
        # Consonant Phonemes
        self.consonants = {
                # ક વર્ગ (Velar consonants)
                  'ક': 'kə', 'ખ': 'kʰə', 'ગ': 'gə', 'ઘ': 'gʱə', 'ઙ': 'ŋə',
    
                # ચ વર્ગ (Palatal consonants)
                  'ચ': 'tʃə', 'છ': 'tʃʰə', 'જ': 'dʒə', 'ઝ': 'dʒʱə', 'ઞ': 'ɲə',
    
                # ટ વર્ગ (Retroflex consonants)
                  'ટ': 'ʈə', 'ઠ': 'ʈʰə', 'ડ': 'ɖə', 'ઢ': 'ɖʱə', 'ણ': 'ɳə',
    
                # ત વર્ગ (Dental consonants)
                  'ત': 't̪ə', 'થ': 't̪ʰə', 'દ': 'd̪ə', 'ધ': 'd̪ʱə', 'ન': 'nə',
    
                 # પ વર્ગ (Labial consonants)
                  'પ': 'pə', 'ફ': 'pʰə', 'બ': 'bə', 'ભ': 'bʱə', 'મ': 'mə',
    
                 # અંત:સ્થ (Approximants/Semivowels)
                  'ય': 'jə', 'ર': 'ɾə', 'લ': 'lə', 'વ': 'ʋə',
    
                 # ઊષ્મ (Sibilants)
                  'શ': 'ʃə', 'ષ': 'ʂə', 'સ': 'sə', 'હ': 'ɦə',
    
                 # અન્ય (Others)
                   'ળ': 'ɭə',  # Retroflex lateral
                   'ક્ષ': 'kʃə',  # Compound
                   'ત્ર': 't̪ɾə',  # Compound
                   'જ્ઞ': 'ɡɲə',  # Compound
    
                # અનુસ્વાર અને વિસર્ગ
                   'ં': 'ṁ',  # Anusvara (nasalization)
                   'ઃ': 'ḥ',   # Visarga (aspiration)
    
                # Rare consonants (Sanskrit borrowings)
                  'ઋ': 'r̩',   # ऋ
                  'ૠ': 'r̩ː',  # ॠ
                  'ઌ': 'l̩',    # ऌ
                  'ૡ': 'l̩ː',  # ॡ
        }
        
        # Vowel Modifiers (Matra)
        self.vowel_modifiers = {
            'ા': 'aa', 'િ': 'i', 'ી': 'ii', 'ુ': 'u',
            'ૂ': 'uu', 'ે': 'e', 'ૈ': 'ai', 'ો': 'o', 'ૌ': 'au'
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

def visualize_results(results: Dict[str, Any], test_case_num: int):
    """Visualize the processing results"""
    print(f"\n=== Test Case {test_case_num} ===")
    print(f"Original Text: {results['original_text']}")
    print(f"Normalized Text: {results['normalized_text']}")
    print(f"Sentence Type: {results['prosody']['sentence_type']}")
    
    print("\nGrapheme-to-Phoneme Mapping:")
    print("Graphemes:", " ".join(results['graphemes']))
    print("Phonemes: ", " ".join(results['phonemes']))
    
    print("\nDetailed Prosodic Analysis:")
    print("Idx | Grapheme | Phoneme    | Type            | Position    | Stress | Duration | Pitch")
    print("-" * 80)
    
    prosody_index = 0
    for i, (grapheme, phoneme, detail) in enumerate(zip(
        results['graphemes'],
        results['phonemes'],
        results['phoneme_details']
    )):
        if detail['type'] == 'punctuation':
            print(f"{i:3} | {grapheme:8} | {phoneme:10} | {detail['type']:15} | {'N/A':11} | {'N/A':6} | {'N/A':8} | {'N/A':5}")
        else:
            prosody = results['prosody']['phonemes'][prosody_index]
            print(f"{i:3} | {grapheme:8} | {phoneme:10} | {detail['type']:15} | {prosody['position']:11} | {prosody['stress']:6.2f} | {prosody['duration']:8.2f} | {prosody['pitch']:5.2f}")
            prosody_index += 1
    
    rhythm = results['prosody']['rhythm']
    print("\nRhythm Metrics:")
    print(f"Average Duration: {rhythm['avg_duration']:.2f}")
    print(f"Duration Variance: {rhythm['duration_variance']:.2f}")
    print(f"Average Pitch: {rhythm['avg_pitch']:.2f}")
    print(f"Pitch Range: {rhythm['pitch_range']:.2f}")
    print(f"Speech Rate: {rhythm['speech_rate']:.2f} phonemes/sec")
    print("="*60)

def run_test_cases():
    """Run multiple test cases through the pipeline"""
    test_cases = [
        {
            "text": "હેલો, તમે કેમ છો?",
            "type": "question"
        },
        {
            "text": "મને ગુજરાતી ભાષા ગમે છે!",
            "type": "exclamation"
        },
        {
            "text": "આજે હવામાન સારું છે.",
            "type": "statement"
        },
        {
            "text": "તમારું નામ શું છે?",
            "type": "question"
        },
        {
            "text": "ચાલો ફરવા જઈએ!",
            "type": "exclamation"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        results = process_gujarati_text(test_case["text"], test_case["type"])
        visualize_results(results, i)

if __name__ == "__main__":
    print("=== Gujarati Text Processing with Prosody Analysis ===")
    print("Running multiple test cases...\n")
    run_test_cases()