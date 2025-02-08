import re
import unicodedata

# 1. NUMBER CONVERSION DATA AND FUNCTIONS

# Mapping for Gujarati cardinal numbers (0-99).
cardinal_dict = {
    0: "શૂન્ય",
    1: "એક",
    2: "બે",
    3: "ત્રણ",
    4: "ચાર",
    5: "પાંચ",
    6: "છ",
    7: "સાત",
    8: "આઠ",
    9: "નવ",
    10: "દસ",
    11: "અગિયાર",
    12: "બાર",
    13: "તેર",
    14: "ચૌદ",
    15: "પંદર",
    16: "સોળ",
    17: "સતાર",
    18: "અઠાર",
    19: "ઉન્નીસ",
    20: "વીસ",
    21: "એકવીસ",
    22: "બાવીસ",
    23: "ત્રેવીસ",
    24: "ચોવીસ",
    25: "પચ્ચીસ",
    26: "છવીસ",
    27: "સત્તાવીસ",
    28: "અઠ્ઠાવીસ",
    29: "ઓગણત્રીસ",
    30: "ત્રીસ",
    31: "એકત્રીસ",
    32: "બત્રીસ",
    33: "ત્રેત્રીસ",
    34: "ચોત્રીસ",
    35: "પંસ્ત્રીસ",
    36: "છત્રીસ",
    37: "સડત્રીસ",
    38: "અડત્રીસ",
    39: "ઓગણચાલીસ",
    40: "ચાલીસ",
    41: "એકતાળીસ",
    42: "બેયતાળીસ",
    43: "ત્રેયતાળીસ",
    44: "ચૌતાળીસ",
    45: "પંચતાળીસ",
    46: "છયતાળીસ",
    47: "સડતાળીસ",
    48: "અડતાળીસ",
    49: "ઓગણપચાસ",
    50: "પચાસ",
    51: "એકાવન",
    52: "બાવન",
    53: "ત્રેપન",
    54: "ચોપ્પન",
    55: "પંચાવન",
    56: "છપ્પન",
    57: "સત્તાવન",
    58: "અઠ્ઠાવન",
    59: "ઓગણસઠ",
    60: "સાઠ",
    61: "એકસઠ",
    62: "બાસઠ",
    63: "ત્રેસઠ",
    64: "ચોસઠ",
    65: "પાંસઠ",
    66: "છાસઠ",
    67: "સડસઠ",
    68: "અડસઠ",
    69: "ઓગણસિત્તેર",
    70: "સિત્તેર",
    71: "એકહતર",
    72: "બય્યાસી",
    73: "ત્ર્યાસી",
    74: "ચોર્યાસી",
    75: "પંચ્યાસી",
    76: "છ્યાસી",
    77: "સત્ત્યાસી",
    78: "અઠ્યોતેર",
    79: "ઓગણઅસ્સી",
    80: "એંસી",
    81: "એક્યાસી",
    82: "બ્યાસી",
    83: "ત્ર્યાસી",
    84: "ચોર્યાસી",
    85: "પંચ્યાસી",
    86: "છ્યાસી",
    87: "સત્ત્યાસી",
    88: "અઢ્યાસી",
    89: "નવ્યાસી",
    90: "નવ્વેદ",
    91: "એકાનવ્વેદ",
    92: "બાનવ્વેદ",
    93: "ત્રાણવ્વેદ",
    94: "ચોરાણવ્વેદ",
    95: "પંચાનવ્વેદ",
    96: "છાનવ્વેદ",
    97: "સત્તાનવ્વેદ",
    98: "અઠ્ઠાનવ્વેદ",
    99: "નવ્વાણું"
}

# Special exceptions for ordinal numbers.
ordinal_exceptions = {
    1: "પહેલો",
    2: "બીજો",
    3: "ત્રીજો"
}

def number_to_words(n, ordinal=False):
    if n == 0:
        return cardinal_dict[0]
    if n < 100:
        if n in cardinal_dict:
            word = cardinal_dict[n]
        else:
            tens = (n // 10) * 10
            ones = n % 10
            word = (cardinal_dict.get(tens, "") + " " + cardinal_dict.get(ones, "")).strip()
        if ordinal:
            if n in ordinal_exceptions:
                return ordinal_exceptions[n]
            else:
                return word + "મી"
        else:
            return word

    parts = []
    crore = n // 10000000
    if crore > 0:
        parts.append(number_to_words(crore) + " કરોડ")
        n %= 10000000
    lakh = n // 100000
    if lakh > 0:
        parts.append(number_to_words(lakh) + " લાખ")
        n %= 100000
    thousand = n // 1000
    if thousand > 0:
        parts.append(number_to_words(thousand) + " હજાર")
        n %= 1000
    hundred = n // 100
    if hundred > 0:
        parts.append(number_to_words(hundred) + "સો")
        n %= 100
    if n > 0:
        parts.append(number_to_words(n))
    result = " ".join(parts)
    if ordinal:
        return result + "મી"
    else:
        return result

# 2. HELPER FUNCTIONS FOR DIGIT CONVERSION & INPUT VALIDATION

def convert_gujarati_to_arabic(s):
    mapping = str.maketrans("૦૧૨૩૪૫૬૭૮૯", "0123456789")
    return s.translate(mapping)

def is_valid_text(text):
    allowed_pattern = r'^[\u0A80-\u0AFFA-Za-z0-9\s\.\,\!\?\%\₹:/\-\n“”"\']*$'
    return re.match(allowed_pattern, text) is not None

# 3. ABBREVIATIONS DICTIONARY

abbrev_dict = {
    "ડૉ.": "ડોક્ટર",
    "શ્રી.": "શ્રીમાન",
    "ગુ.યુની.": "ગુજરાત યુનિવર્સિટી"
}

# 4. REGEX-BASED REPLACEMENT FUNCTIONS

def currency_replace(match):
    num_str = match.group(1)
    arabic_num = convert_gujarati_to_arabic(num_str).replace(",", "")
    if '.' in arabic_num:
        rupees_part, paise_part = arabic_num.split('.')
    else:
        rupees_part, paise_part = arabic_num, None
    rupees = int(rupees_part) if rupees_part else 0
    rupees_words = number_to_words(rupees)
    if paise_part is not None and paise_part != '' and int(paise_part) > 0:
        paise = int(paise_part)
        paise_words = number_to_words(paise)
        return "રૂપિયા " + rupees_words + " અને " + paise_words + " પૈસા"
    else:
        return "રૂપિયા " + rupees_words

def date_replace(match):
    day_str, month_str, year_str = match.groups()
    day = int(convert_gujarati_to_arabic(day_str))
    month = int(convert_gujarati_to_arabic(month_str))
    year = int(convert_gujarati_to_arabic(year_str))
    day_words = number_to_words(day, ordinal=True)
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
    year_words = number_to_words(year)
    return day_words + " " + month_words + " " + year_words

def time_replace(match):
    hour_str = match.group(1)
    minute_str = match.group(2)
    hour = int(convert_gujarati_to_arabic(hour_str))
    minute = int(convert_gujarati_to_arabic(minute_str))
    hour_words = number_to_words(hour)
    minute_words = number_to_words(minute)
    return hour_words + " વાગ્યા " + minute_words + " મિનિટે"

def percent_replace(match):
    num_str = match.group(1)
    num = int(convert_gujarati_to_arabic(num_str).replace(",", ""))
    num_words = number_to_words(num)
    return num_words + " ટકા"

def ordinal_replace(match):
    num_str, suffix = match.groups()
    num = int(convert_gujarati_to_arabic(num_str).replace(",", ""))
    return number_to_words(num, ordinal=True)

def number_replace(match):
    num_str = match.group(1)
    num_clean = convert_gujarati_to_arabic(num_str.replace(",", ""))
    try:
        num = int(num_clean)
        return number_to_words(num)
    except ValueError:
        return num_str

# 5. MAIN NORMALIZATION FUNCTION

def normalize_text(text):
    # A. Unicode normalization (NFC) and removal of zero-width joiners/non-joiners.
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'[\u200C\u200D]', '', text)
    
    # Now check for invalid characters.
    if text == "":
        return ""
    if not is_valid_text(text):
        return "[Error: Invalid characters]"

    # B. Expand abbreviations.
    for abbr, full in abbrev_dict.items():
        text = re.sub(re.escape(abbr), full, text)

    # C. Currency conversion (e.g. ₹૨૩.૫૦ -> રૂપિયા ત્રેવીસ અને પચાસ પૈસા)
    text = re.sub(r'₹\s*([૦૧૨૩૪૫૬૭૮૯0-9,]+(?:\.[૦૧૨૩૪૫૬૭૮૯0-9]+)?)', currency_replace, text)

    # D. Date conversion (handles "/" and "-" delimiters)
    text = re.sub(r'([૦૧૨૩૪૫૬૭૮૯0-9]{1,2})[/-]([૦૧૨૩૪૫૬૭૮૯0-9]{1,2})[/-]([૦૧૨૩૪૫૬૭૮૯0-9]{2,4})', date_replace, text)

    # E. Time conversion.
    text = re.sub(r'\b([૦૧૨૩૪૫૬૭૮૯0-9]{1,2}):([૦૧૨૩૪૫૬૭૮૯0-9]{1,2})(\s*વાગ્યે)?', time_replace, text)

    # F. Percentage conversion (e.g. ૨૫% -> પચ્ચીસ ટકા)
    text = re.sub(r'([૦૧૨૩૪૫૬૭૮૯0-9,]+)%', percent_replace, text)

    # G. Ordinal numbers conversion.
    text = re.sub(r'(?<![\d\u0A80-\u0AFF,])([૦૧૨૩૪૫૬૭૮૯0-9,]+)(મી|લો|જો)(?![\d\u0A80-\u0AFF])', ordinal_replace, text)

    # H. General number conversion (remaining standalone numbers)
    text = re.sub(r'\b([૦૧૨૩૪૫૬૭૮૯0-9,]+)\b', number_replace, text)

    # I. Punctuation normalization.
    # Handle ellipsis: remove extra dots when followed by punctuation or at the end.
    text = re.sub(r'\.{2,}(?=[\?\!\,])', '', text)
    text = re.sub(r'\.{2,}$', '.', text)
    text = re.sub(r'\.{2,}', ' ', text)
    # Remove quotes (straight or fancy)
    text = re.sub(r'[“”"]', '', text)
    # Remove stray commas.
    text = re.sub(r',', '', text)

    # J. Normalize whitespace.
    text = re.sub(r'\s+', ' ', text).strip()

    return text