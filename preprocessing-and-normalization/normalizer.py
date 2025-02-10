import re
import unicodedata
from preprocessor import GujaratiTextPreprocessor

def date_replace(match):
    preprocessor = GujaratiTextPreprocessor()

    day_str, month_str, year_str = match.groups()
    day = int(preprocessor.convert_gujarati_to_arabic(day_str))
    month = int(preprocessor.convert_gujarati_to_arabic(month_str))
    year = int(preprocessor.convert_gujarati_to_arabic(year_str))

    if day == 1:
        day_words = "પહેલી"
    elif day == 2:
        day_words = "બીજી"
    elif day == 3:
        day_words = "ત્રીજી"
    else:
        day_words = preprocessor.number_to_words_indian(day) + "મી"

    month_map = {
        1: "જાન્યુઆરી",
        2: "ફેબ્રુઆરી",
        3: "માર્ચ",
        4: "એપ્રિલ",
        5: "મે",
        6: "જૂન",
        7: "જુલાઈ",
        8: "ઑગસ્ટ",
        9: "સપ્ટેમ્બર",
        10: "ઓક્ટોબર",
        11: "નવેમ્બર",
        12: "ડિસેમ્બર"
    }
    month_words = month_map.get(month, month_str)
    year_words = preprocessor.number_to_words_indian(year)
    return day_words + " " + month_words + " " + year_words

def time_replace(match):
    preprocessor = GujaratiTextPreprocessor()

    hour_str = match.group(1)
    minute_str = match.group(2)
    orig_hour = int(preprocessor.convert_gujarati_to_arabic(hour_str))
    minute = int(preprocessor.convert_gujarati_to_arabic(minute_str))

    if orig_hour == 0 and minute == 0:
        return "મધરાત"
    if orig_hour == 0:
        return "મધરાત " + preprocessor.number_to_words_indian(minute) + " મિનિટે"
    if orig_hour == 12 and minute == 0:
        return "બપોર"
    if orig_hour == 12:
        return "બપોર " + preprocessor.number_to_words_indian(minute) + " મિનિટે"
    if orig_hour >= 18:
        new_hour = orig_hour - 12
        prefix = "રાત્રે "
    elif orig_hour > 12 and orig_hour < 18:
        new_hour = orig_hour
        prefix = ""
    else:
        new_hour = orig_hour
        prefix = ""
    return prefix + preprocessor.number_to_words_indian(new_hour) + " વાગ્યા " + preprocessor.number_to_words_indian(minute) + " મિનિટે"

def normalize_text(text):
    """
    Normalize and preprocess Gujarati text for TTS.
    Processing order:
    1. Unicode normalization and removal of zero‑width joiners.
    2. Validate allowed characters.
    3. Remove commas that occur between digits.
    4. Expand abbreviations.
    5. Process PIN codes.
    6. Date conversion.
    7. Multiplication/Division conversion.
    8. Currency conversion.
    9. Percentage conversion.
    10. Process signed numbers.
    11. Time conversion.
    12. Non‑currency decimal conversion.
    13. Fraction conversion.
    14. Ordinal conversion.
    15. General number conversion.
    16. Punctuation cleanup.
    17. Additional hack for stray suffix issues.
    18. Normalize whitespace.
    """
    # Create an instance of GujaratiTextPreprocessor
    preprocessor = GujaratiTextPreprocessor()

    # Unicode normalization and remove zero‑width joiners.
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'[\u200C\u200D]', '', text)
    
    # Validate allowed characters.
    if text.strip() == "":
        return ""
    if not preprocessor.is_valid_text(text):
        return "[Error: Invalid characters]"
    
    # Remove commas between digits (Gujarati or ASCII).
    text = re.sub(r'(?<=([\u0A80-\u0AFF]|\d)),(?=([\u0A80-\u0AFF]|\d))', '', text)
    
    # Expand abbreviations.
    for abbr, full in preprocessor.abbrev_dict.items():
        text = re.sub(re.escape(abbr), full, text)
    
    # Process PIN codes.
    text = re.sub(r'(પિન:\s*)([૦૧૨૩૪૫૬૭૮૯]+)', preprocessor.pin_replace, text)
    
    # Date conversion.
    text = re.sub(r'([૦૧૨૩૪૫૬૭૮૯0-9]{1,2})[/-]([૦૧૨૩૪૫૬૭૮૯0-9]{1,2})[/-]([૦૧૨૩૪૫૬૭૮૯0-9]{2,4})', date_replace, text)
    
    # Division conversion.
    text = re.sub(r'×\s*([૦૧૨૩૪૫૬૭૮૯0-9]+)', preprocessor.multiplication_replace, text)
    text = re.sub(r'÷\s*([૦૧૨૩૪૫૬૭૮૯0-9]+)', preprocessor.division_replace, text)
    
    # Currency conversion.
    text = re.sub(r'₹\s*([૦૧૨૩૪૫૬૭૮૯0-9]+(?:\.[૦૧૨૩૪૫૬૭૮૯0-9]+)?(?:/\-)?)([^\s\d]*)', preprocessor.currency_replace, text)
    
    # Percentage conversion.
    text = re.sub(r'([૦૧૨૩૪૫૬૭૮૯0-9]+(?:\.[૦૧૨૩૪૫૬૭૮૯0-9]+)?)%', preprocessor.percent_replace, text)
    
    # Process signed numbers.
    text = re.sub(r'([+\-])\s*([૦૧૨૩૪૫૬૭૮૯0-9]+)', preprocessor.signed_number_replace, text)
    
    # Time conversion.
    text = re.sub(r'\b([૦૧૨૩૪૫૬૭૮૯0-9]{1,2}):([૦૧૨૩૪૫૬૭૮૯0-9]{1,2})(\s*વાગ્યે)?', time_replace, text)
    
    # Non‑currency decimal conversion.
    text = re.sub(r'\b([૦૧૨૩૪૫૬૭૮૯0-9]+)\.([૦૧૨૩૪૫૬૭૮૯0-9]+)\b', preprocessor.non_currency_decimal_replace, text)
    
    # Fraction conversion.
    text = re.sub(r'\b([૦૧૨૩૪૫૬૭૮૯0-9]+)/([૦૧૨૩૪૫૬૭૮૯0-9]+)\b', preprocessor.fraction_replace, text)
    
    # Ordinal conversion.
    text = re.sub(r'(?<![\d\u0A80-\u0AFF,])([૦૧૨૩૪૫૬૭૮૯0-9]+)(મી|લો|જી|જું|મો|લા)(?![\d\u0A80-\u0AFF])', preprocessor.ordinal_replace, text)
    
    # General number conversion.
    text = re.sub(r'\b([૦૧૨૩૪૫૬૭૮૯0-9,]+)\b', preprocessor.number_replace, text)
    
    # Punctuation cleanup.
    text = re.sub(r'\.{2,}', ' ', text)
    text = re.sub(r'[!?\']', '', text)
    text = re.sub(r'[“”"]', '', text)
    text = re.sub(r',', '', text)
    text = re.sub(r'\s*[\.]+\s*$', '', text)
    
    # Additional hack to fix stray extra letters.
    text = text.replace("કિલોગ્રામમ", "કિલોગ્રામ")
    
    # Normalize whitespace.
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text