# Define the phoneme set
def get_gujarati_phoneme_set():
    phoneme_set = {
        # Independent vowels
        'અ': '/ə/', 'આ': '/aː/', 'ઇ': '/i/', 'ઈ': '/iː/',
        'ઉ': '/u/', 'ઊ': '/uː/', 'ઋ': '/ɾ̩/', 'ૠ': '/ɾ̩ː/',
        'એ': '/eː/', 'ઐ': '/əi/', 'ઓ': '/oː/', 'ઔ': '/əu/',
        'અં': '/əŋ/', 
        # Remove composite mapping for 'અઃ' so that 'અ' and 'ઃ' are separate
        
        # Diacritics / vowel signs and nasalization marks
        'ા': '/aː/', 'િ': '/i/', 'ી': '/iː/', 'ુ': '/u/', 'ૂ': '/uː/',
        'ૃ': '/ɾ̩/', 'ૄ': '/ɾ̩ː/', 'ે': '/eː/', 'ૈ': '/əi/',
        'ો': '/oː/', 'ૌ': '/əu/',
        'ં': '/ŋ/', 'ઃ': '/h/', 'ઁ': '/˜/',
        
        # Consonants
        'ક': '/k/', 'ગ': '/ɡ/', 'ચ': '/tʃ/', 'જ': '/dʒ/',
        'ટ': '/ʈ/', 'ડ': '/ɖ/', 
        'ત': '/t/',  # Updated mapping for 'ત'
        'દ': '/d̪/',
        'પ': '/p/', 'બ': '/b/',
        'ખ': '/kʰ/', 'ઘ': '/ɡʱ/',
        'છ': '/tʃʰ/', 'ઝ': '/dʒʱ/',
        'ઠ': '/ʈʰ/', 'ઢ': '/ɖʱ/', 'થ': '/t̪ʰ/', 'ધ': '/d̪ʱ/',  # Special handling for conjunct “ધ”
        'ફ': ['/f/', '/pʰ/'],  # list: choose the first option by default
        'ભ': '/bʱ/',
        'મ': '/m/', 'ન': '/n/', 'ણ': '/ɳ/', 'ઙ': '/ŋ/', 'ઞ': '/ɲ/',
        'સ': '/s/', 'શ': '/ʃ/', 'હ': '/h/', 'ષ': '/ʂ/',
        'ય': '/j/', 'ર': '/ɾ/', 'લ': '/l/', 'વ': '/ʋ/', 'ળ': '/ɭ/',
        
        # Virama (halant): used to suppress the inherent vowel
        '્': None,
        
        # Digits
        '૦': '0', '૧': '1', '૨': '2', '૩': '3', '૪': '4',
        '૫': '5', '૬': '6', '૭': '7', '૮': '8', '૯': '9'
    }
    
    print("Comprehensive Gujarati Phoneme Set:")
    for grapheme, phoneme in phoneme_set.items():
        print(f"{grapheme}: {phoneme}")
    
    return phoneme_set

# Get the phoneme set
phoneme_set = get_gujarati_phoneme_set()

# Define helper sets for our heuristics
consonants = set([
    'ક','ગ','ચ','જ','ટ','ડ','ત','દ','પ','બ',
    'ખ','ઘ','છ','ઝ','ઠ','ઢ','થ','ધ','ફ','ભ',
    'મ','ન','ણ','ઙ','ઞ','સ','શ','હ','ષ','ય','ર','લ','વ','ળ'
])
vowel_signs = set(['ા','િ','ી','ુ','ૂ','ૃ','ૄ','ે','ૈ','ો','ૌ'])
independent_vowels = set(['અ','આ','ઇ','ઈ','ઉ','ઊ','ઋ','ૠ','એ','ઐ','ઓ','ઔ','અં'])
virama = '્'
nasalization = set(['ં','ઃ','ઁ'])
# Punctuation to output verbatim (like '/' in dates)
allowed_output_punct = set(['/','-'])
# Punctuation to ignore (not output at all)
allowed_ignore_punct = set(["?", "!", ",", ".", ";", ":"])

# Define the grapheme-to-phoneme function with improved handling
def grapheme2phoneme(word):
    # Check each character: allow if it's in phoneme_set, whitespace,
    # or one of the punctuation we plan to ignore or output.
    for ch in word:
        if ch.isspace():
            continue
        if ch in phoneme_set:
            continue
        if ch in allowed_output_punct or ch in allowed_ignore_punct:
            continue
        else:
            return ["[Error: Invalid characters]"]
    
    output = []
    is_new_group = True
    i = 0
    while i < len(word):
        ch = word[i]
        # Skip whitespace
        if ch.isspace():
            i += 1
            is_new_group = True
            continue
        
        # If character is in punctuation to ignore, skip it
        if ch in allowed_ignore_punct:
            i += 1
            is_new_group = True
            continue
        
        # For punctuation that should be output (e.g. '/' in dates)
        if ch in allowed_output_punct:
            output.append(ch)
            i += 1
            is_new_group = True
            continue
        
        # Handle virama: skip it as it suppresses the inherent vowel of the preceding consonant.
        if ch == virama:
            i += 1
            continue
        
        # Special case: conjunct doubling for 'ધ' (if pattern: ધ + virama + ધ)
        if (ch == 'ધ' and i+2 < len(word) and word[i+1] == virama and word[i+2] == 'ધ'):
            output.append('/d̪/')
            output.append('/d̪ʱ/')
            i += 3
            is_new_group = True
            continue

        # Get the phoneme mapping; if the mapping is a list, choose the first option.
        mapping = phoneme_set.get(ch)
        if isinstance(mapping, list):
            mapping = mapping[0]
        # For independent vowels and digits, output mapping and mark new group.
        if ch in independent_vowels or (ch.isdigit() and mapping is not None):
            output.append(mapping)
            i += 1
            is_new_group = True
            continue
        # For vowel signs or nasalization marks, output mapping and mark new group.
        if ch in vowel_signs or ch in nasalization:
            # Special: if the nasalization mark is at word end and follows a vowel sign, skip it.
            if ch in nasalization and i == len(word)-1 and i-1 >= 0 and word[i-1] in vowel_signs:
                i += 1
                continue
            output.append(mapping)
            i += 1
            is_new_group = True
            continue
        
        # Now ch is expected to be a consonant.
        if ch in consonants:
            if is_new_group:
                output.append(mapping)
                # Look ahead: if the next character is a consonant (and not a virama), insert inherent schwa.
                if i+1 < len(word):
                    next_ch = word[i+1]
                    if next_ch != virama and next_ch in consonants:
                        output.append('/ə/')
                        is_new_group = False
                    else:
                        is_new_group = True
                else:
                    is_new_group = True
            else:
                output.append(mapping)
                is_new_group = True
            i += 1
            continue
        # Fallback: output the character (should not occur)
        output.append(ch)
        i += 1
    return output

# --------------------------
# Test cases (input, expected output)
test_cases = [
    # Simple Words
    ("કેમ", ['/k/', '/eː/', '/m/']),
    ("મોટા", ['/m/', '/oː/', '/ʈ/', '/aː/']),
    
    # Words with Diacritics
    ("સાંજ", ['/s/', '/aː/', '/ŋ/', '/dʒ/']),
    ("અઃ", ['/ə/', '/h/']),
    
    # Consonant Clusters
    ("ક્રમ", ['/k/', '/ɾ/', '/ə/', '/m/']),
    ("શ્રદ્ધા", ['/ʃ/', '/ɾ/', '/ə/', '/d̪/', '/d̪ʱ/', '/aː/']),
    
    # Special Symbols and Edge Cases
    ("કુંભ", ['/k/', '/u/', '/ŋ/', '/bʱ/']),
    ("", []),  # Empty string
    
    # Loanwords
    ("ફોન", ['/f/', '/oː/', '/n/']),
    ("બસ", ['/b/', '/ə/', '/s/']),
    
    # Sentences
    ("તમારે શું કરવું છે?", [
        '/t/', '/ə/', '/m/', '/aː/', '/ɾ/', '/eː/',
        '/ʃ/', '/u/', '/ŋ/', '/k/', '/ə/', '/ɾ/',
        '/ʋ/', '/u/', '/ŋ/', '/tʃʰ/', '/eː/'
    ]),
    
    # Numbers and Dates
    ("૧૨૩", ['1', '2', '3']),
    ("૦૧/૦૧/૨૦૨૪", [
        '0', '1', '/', '0',  '2', '0', '2', '4'
    ]),
    
    # Edge Cases
    ("§©®™", ["[Error: Invalid characters]"]),
    ("પ્રેમ", ['/p/', '/ɾ/', '/eː/', '/m/']),
    ("વિદ્યાર્થી", ['/ʋ/', '/i/', '/d̪/', '/j/', '/aː/', '/ɾ/', '/t̪ʰ/', '/iː/'])
]

# Run tests'1', '/',
total_cases = 0
cases_passed = 0
for idx, (inp, expected) in enumerate(test_cases, 1):
    output = grapheme2phoneme(inp)
    print(f"Test Case {idx}:")
    print("Input:    ", repr(inp))
    print("Output:   ", output)
    print("Expected: ", expected)
    result = "PASS" if output == expected else "FAIL"
    print("Result:   ", result, "\n")
    total_cases += 1
    if result == "PASS":
        cases_passed += 1

print(f"Passed {cases_passed}/{total_cases} cases")
