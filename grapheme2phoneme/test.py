from phoneme_data import get_gujarati_phoneme_set

# Get the phoneme set using the function
phoneme_set = get_gujarati_phoneme_set()

# Define a function to convert graphemes to phonemes
def grapheme2phoneme(word):
    phonemes = []
    for grapheme in word:
        if grapheme in phoneme_set:
            phonemes.append(phoneme_set[grapheme])
        else:
            phonemes.append("[Error: Invalid characters]")
    return phonemes

# Define test cases: (input, expected output)
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
        '/ʋ/', '/u/', '/tʃʰ/', '/eː/'
    ]),

    # Numbers and Dates
    ("૧૨૩", ['1', '2', '3']),
    ("૦૧/૦૧/૨૦૨૪", [
        '0', '1', '/', '0', '1', '/', '2', '0', '2', '4'
    ]),

    # Edge Cases
    ("§©®™", ["[Error: Invalid characters]"]),
    ("પ્રેમ", ['/p/', '/ɾ/', '/eː/', '/m/']),
    ("વિદ્યાર્થી", ['/ʋ/', '/i/', '/d̪/', '/j/', '/aː/', '/ɾ/', '/t̪ʰ/', '/iː/'])
]

# Run tests
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
