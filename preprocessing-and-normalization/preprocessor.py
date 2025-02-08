import re
import unicodedata
import regex

class GujaratiTextPreprocessor:
    def __init__(self):
        # Character standardization mappings
        self._unicode_normalization_map = {
            # Add common Unicode character variations
            'ઁ': 'ં',   # Nasalization variations
            'ઽ': 'અ',  # Special character replacements
        }
        
        # Numeral conversion maps
        self._gujarati_numerals = {
            '૦': 'શૂન્ય', '૧': 'એક', '૨': 'બે', 
            '૩': 'ત્રણ', '૪': 'ચાર', '૫': 'પાંચ', 
            '૬': 'છ', '૭': 'સાત', '૮': 'આઠ', 
            '૯': 'નવ'
        }
        
        # Number word representations
        self._number_words = {
            1: 'એક', 2: 'બે', 3: 'ત્રણ', 4: 'ચાર', 
            5: 'પાંચ', 6: 'છ', 7: 'સાત', 
            8: 'આઠ', 9: 'નવ', 10: 'દસ'
        }
        
        # Ordinal suffix
        self._ordinal_suffix = 'મો'
        
        # Abbreviation expansion dictionary
        self._abbreviations = {
            'ડૉ.': 'ડૉક્ટર',
            'પ્રૉ.': 'પ્રોફેસર',
            'કેમ.': 'કેમિકલ',
            'મે.': 'મેનેજર'
        }

    def normalize_characters(self, text: str) -> str:
        """
        Standardize Gujarati characters using Unicode normalization
        and predefined mapping rules.
        """
        # Normalize to NFC form (Normalization Form Canonical Composition)
        text = unicodedata.normalize('NFC', text)
        
        # Apply custom Unicode normalization
        for old, new in self._unicode_normalization_map.items():
            text = text.replace(old, new)
        
        return text

    def convert_numerals(self, text: str) -> str:
        """
        Convert numeric digits to Gujarati word representations.
        """
        def converter(match):
            num = match.group(0)
            # Handle Arabic/Gujarati numeral conversion
            word = self._number_to_words(int(num))
            return word

        # Convert Arabic numerals
        text = regex.sub(r'\d+', converter, text)
        
        # Convert Gujarati numerals
        for numeral, word in self._gujarati_numerals.items():
            text = text.replace(numeral, word)
        
        return text

    def _number_to_words(self, number: int) -> str:
        """
        Convert a number to its Gujarati word representation.
        """
        # Handle teen numbers
        if 10 < number < 20:
            return self._special_teen_words(number)
        
        # Handle two-digit numbers
        if number < 100:
            return self._two_digit_words(number)
        
        # Handle larger numbers (simplified)
        if number < 1000:
            return self._three_digit_words(number)
        
        return str(number)  # Fallback for complex numbers

    def _special_teen_words(self, number: int) -> str:
        """
        Special handling for teen numbers in Gujarati
        """
        teen_words = {
            11: 'અગિયાર', 12: 'બાર', 13: 'તેર', 
            14: 'ચૌદ', 15: 'પંદર', 16: 'સોળ', 
            17: 'સત્ર', 18: 'અઢાર', 19: 'તેર'
        }
        return teen_words.get(number, str(number))

    def _two_digit_words(self, number: int) -> str:
        """
        Convert two-digit numbers to Gujarati words
        """
        if number < 10:
            return self._number_words.get(number, str(number))
        
        tens = number // 10
        ones = number % 10
        
        tens_words = {
            2: 'વીસ', 3: 'ત્રીસ', 4: 'ચાલીસ', 
            5: 'પચાસ', 6: 'સાઠ', 7: 'સિત્તેર', 
            8: 'ઐંસી', 9: 'નવ્વેર'
        }
        
        if ones == 0:
            return tens_words.get(tens, str(number))
        
        return f"{self._number_words.get(ones, str(ones))}{tens_words.get(tens, str(tens))}"

    def _three_digit_words(self, number: int) -> str:
        """
        Convert three-digit numbers to Gujarati words
        """
        hundreds = number // 100
        remainder = number % 100
        
        word = f"{self._number_words.get(hundreds, str(hundreds))} સો"
        
        if remainder > 0:
            word += " " + self._number_to_words(remainder)
        
        return word

    def process_abbreviations(self, text: str) -> str:
        """
        Expand common abbreviations to full words
        """
        for abbr, full_word in self._abbreviations.items():
            text = text.replace(abbr, full_word)
        
        return text

    def normalize_text_structure(self, text: str) -> str:
        """
        Normalize text structure by handling whitespaces and formatting
        """
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading and trailing whitespaces
        text = text.strip()
        
        return text

    def process_special_cases(self, text: str) -> str:
        """
        Handle special linguistic nuances in Gujarati text
        """
        text = text.replace('ઽ', 'અ')  # Handle special character
        
        return text

    def preprocess(self, text: str) -> str:
        """
        Main preprocessing pipeline
        """
        preprocessors = [
            self.normalize_characters,
            self.convert_numerals,
            self.process_abbreviations,
            self.normalize_text_structure,
            self.process_special_cases
        ]
        
        for processor in preprocessors:
            text = processor(text)
        
        return text