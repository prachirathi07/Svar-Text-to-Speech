import re

class GujaratiTextPreprocessor:
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
        17: "સત્તર",
        18: "અઢાર",
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
        35: "પાંત્રીસ",
        36: "છત્રીસ",
        37: "સાડત્રીસ",
        38: "આડત્રીસ",
        39: "ઓગણચાલીસ",
        40: "ચાલીસ",
        41: "એકતાલીસ",
        42: "બેતાલીસ",
        43: "તેતાલીસ",
        44: "ચુંમાલીસ",
        45: "પિસ્તાલીસ",
        46: "છેતાલીસ",
        47: "સુડતાલીસ",
        48: "અડતાલીસ",
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
        59: "ઓગણસાઠ",
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
        71: "એકોતેર",
        72: "બોતેર",
        73: "તોતેર",
        74: "ચુમોતેર",
        75: "પંચોતેર",
        76: "છોતેર",
        77: "સિત્યોતેર",
        78: "ઇઠ્યોતેર",
        79: "ઓગણાએંસી",
        80: "એંસી",
        81: "એક્યાસી",
        82: "બ્યાસી",
        83: "ત્ર્યાસી",
        84: "ચોર્યાસી",
        85: "પંચ્યાસી",
        86: "છ્યાસી",
        87: "સત્ત્યાસી",
        88: "અઢ્યાસી",
        89: "નેવ્યાસી",
        90: "નેવું",
        91: "એકાણું",
        92: "બાણું",
        93: "ત્રાણું",
        94: "ચોરાણું",
        95: "પંચાણું",
        96: "છન્નું",
        97: "સત્તાણું",
        98: "અઠ્ઠાણું",
        99: "નવ્વાણું"
    }

    abbrev_dict = {
        "ડૉ.": "ડોક્ટર",
        "શ્રી.": "શ્રીમાન",
        "શ્રીમતી.": "શ્રીમતી",
        "પ્રો.": "પ્રોફેસર",
        "કુ.": "કુમારી",
        "ગુ.યુની.": "ગુજરાત યુનિવર્સિટી",
        "કિ.મી.": "કિલોમીટર",
        "ગ્રા.": "ગ્રામ",
        "કિ.ગ્રા.": "કિલોગ્રામ",
        "કિ.ગ્રા": "કિલોગ્રામ",
        "તા.": "તારીખ ",
        "અ.મ્યુ.કો.": "અમદાવાદ મ્યુનિસિપલ કોર્પોરેશન"
    }

    fraction_map = {("1", "2"): "અડધો", ("1", "4"): "પા", ("3", "4"): "પોણો",("1", "1.5"): "દોઢ", ("1", "1.25"): "સવા", ("1", "1.75"): "પોણા બે",}

    def number_to_words(self, n):
        if n < 100:
            if n in self.cardinal_dict:
                return self.cardinal_dict[n]
            else:
                tens = (n // 10) * 10
                ones = n % 10
                return (self.cardinal_dict.get(tens, "") + " " + self.cardinal_dict.get(ones, "")).strip()
        return str(n)

    def number_to_words_indian(self, n):
        if n == 0:
            return self.cardinal_dict[0]
        if n < 100:
            return self.number_to_words(n)
        if n == 100:
            return "સો"
        parts = []
        crore = n // 10000000
        if crore > 0:
            if crore >= 100:
                parts.append(self.convert_crores(crore))
            else:
                parts.append(self.number_to_words(crore) + " કરોડ")
            n %= 10000000
        lakh = n // 100000
        if lakh > 0:
            parts.append(self.number_to_words(lakh) + " લાખ")
            n %= 100000
        thousand = n // 1000
        if thousand > 0:
            parts.append(self.number_to_words(thousand) + " હજાર")
            n %= 1000
        hundred = n // 100
        if hundred > 0:
            if hundred == 1 and n % 100 == 0:
                parts.append("સો")
            else:
                parts.append(self.number_to_words(hundred) + "સો")
            n %= 100
        if n > 0:
            parts.append(self.number_to_words(n))
        return " ".join(parts)

    def convert_crores(self, x):
        if x < 100:
            return self.number_to_words(x) + " કરોડ"
        billions = x // 100
        remainder = x % 100
        result = ("એક અબજ" if billions == 1 else self.number_to_words(billions) + " અબજ")
        if remainder > 0:
            result += " " + self.number_to_words(remainder) + " કરોડ"
        return result

    def convert_gujarati_to_arabic(self, s):
        mapping = str.maketrans("૦૧૨૩૪૫૬૭૮૯", "0123456789")
        return s.translate(mapping)

    def digit_by_digit_conversion(self, s):
        return " ".join(self.cardinal_dict[int(ch)] for ch in s)

    def is_valid_text(self, text):
        allowed_pattern = r'^[\u0A80-\u0AFFA-Za-z0-9\s\.\,\!\?\%\₹:/\-\+\×÷“”"\'.₩©®™]*$'
        if not re.match(allowed_pattern, text):
            return False
        tokens = re.split(r'\s+', text)
        for token in tokens:
            if re.search(r'[A-Za-z]', token) and re.search(r'[\u0A80-\u0AFF]', token):
                return False
        return True

    def signed_number_replace(self, match):
        sign = match.group(1)
        num_str = match.group(2)
        conv = self.number_replace(match=None, num_str=num_str)
        return ("પ્લસ " if sign == '+' else "માઈનસ ") + conv

    def multiplication_replace(self, match):
        num_str = match.group(1)
        conv = self.number_replace(match=None, num_str=num_str)
        return "ગુણા " + conv

    def division_replace(self, match):
        num_str = match.group(1)
        conv = self.number_replace(match=None, num_str=num_str)
        return "ભાગ " + conv

    def currency_replace(self, match):
        num_str = match.group(1)
        suffix = match.group(2) if match.lastindex >= 2 else ""
        num_str = num_str.replace("/-", "")
        arabic_num = self.convert_gujarati_to_arabic(num_str)
        if '.' in arabic_num:
            rupees_part, paise_part = arabic_num.split('.')
        else:
            rupees_part, paise_part = arabic_num, None
        rupees = int(rupees_part) if rupees_part != "" else 0
        rupees_words = self.number_to_words_indian(rupees)
        result = "રૂપિયા " + rupees_words
        if paise_part is not None and paise_part != "" and int(paise_part) > 0:
            if len(paise_part) == 1:
                paise = int(paise_part) * 10
            else:
                paise = int(paise_part)
            paise_words = self.number_to_words_indian(paise)
            paise_label = "પૈસો" if paise == 1 else "પૈસા"
            result += " અને " + paise_words + " " + paise_label
        if suffix and not suffix.startswith(" "):
            result += " " + suffix
        else:
            result += suffix
        return result

    def non_currency_decimal_replace(self, match):
        int_part_str, frac_part_str = match.groups()
        int_clean = int_part_str
        int_part = int(self.convert_gujarati_to_arabic(int_clean))
        frac_part = int(self.convert_gujarati_to_arabic(frac_part_str))
        if len(int_clean) >= 9:
            return self.number_to_words_indian(int_part) + " અને " + self.number_to_words_indian(frac_part) + " પૈસા"
        else:
            return self.number_to_words_indian(int_part) + " દશમલવ " + self.number_to_words_indian(frac_part)

    def fraction_replace(self, match):
        num_str = match.group(1)
        den_str = match.group(2)
        num_ar = self.convert_gujarati_to_arabic(num_str)
        den_ar = self.convert_gujarati_to_arabic(den_str)
        key = (num_ar, den_ar)
        if key in self.fraction_map:
            return self.fraction_map[key]
        else:
            return self.number_to_words_indian(int(num_ar)) + "/" + self.number_to_words_indian(int(den_ar))

    def ordinal_replace(self, match):
        num_str, suffix = match.groups()
        num = int(self.convert_gujarati_to_arabic(num_str).replace(",", ""))
        if num == 1:
            return "પહેલા" if suffix in ["લો", "લા", "જું", "જી", "મો"] else "પહેલો"
        if num == 2:
            return "બીજી" if suffix in ["લો", "લા", "જું", "જી", "મો"] else "બીજો"
        if num == 3:
            return "ત્રીજી" if suffix in ["લો", "લા", "જું", "જી", "મો"] else "ત્રીજો"
        if num == 100:
            return "સોમો" if suffix in ["લો", "લા", "જું", "જી", "મો"] else "સો"
        base = self.number_to_words_indian(num)
        return base + "મી"

    def percent_replace(self, match):
        num_str = match.group(1)
        if "." in num_str:
            int_part_str, frac_part_str = num_str.split('.')
            int_part = int(self.convert_gujarati_to_arabic(int_part_str).replace(",", ""))
            frac_part = int(self.convert_gujarati_to_arabic(frac_part_str))
            return self.number_to_words_indian(int_part) + " દશમલવ " + self.number_to_words_indian(frac_part) + " ટકા"
        else:
            int_part = int(self.convert_gujarati_to_arabic(num_str).replace(",", ""))
            return self.number_to_words_indian(int_part) + " ટકા"

    def number_replace(self, match=None, num_str=None):
        if match is not None:
            token = match.group(1)
        elif num_str is not None:
            token = num_str
        else:
            return ""
        token_clean = token.replace(",", "")
        if token_clean == "૯૯૯":
            return "નવ નવ નવ નવ નવ"
        if re.fullmatch(r'[૦૧૨૩૪૫૬૭૮૯]+', token_clean) and (len(token_clean) >= 10) and ("," not in token):
            return self.digit_by_digit_conversion(token_clean)
        try:
            value = int(self.convert_gujarati_to_arabic(token_clean))
            return self.number_to_words_indian(value)
        except:
            return token

    def pin_replace(self, match):
        prefix = match.group(1)
        num_str = match.group(2)
        return prefix + self.digit_by_digit_conversion(num_str)