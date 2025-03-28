from g2p import grapheme2phoneme

test_cases = [
    ("કેમ", ['/k/', '/eː/', '/m/']),
    ("મોટા", ['/m/', '/oː/', '/ʈ/', '/aː/']),
    
    ("સાંજ", ['/s/', '/aː/', '/ŋ/', '/dʒ/']),
    ("અઃ", ['/ə/', '/h/']),
    
    ("ક્રમ", ['/k/', '/ɾ/', '/ə/', '/m/']),
    ("શ્રદ્ધા", ['/ʃ/', '/ɾ/', '/ə/', '/d̪/', '/d̪ʱ/', '/aː/']),
    
    ("કુંભ", ['/k/', '/u/', '/ŋ/', '/bʱ/']),
    ("", []),
    
    ("ફોન", ['/f/', '/oː/', '/n/']),
    ("બસ", ['/b/', '/ə/', '/s/']),
    
    ("તમારે શું કરવું છે?", [
        '/t/', '/ə/', '/m/', '/aː/', '/ɾ/', '/eː/',
        '/ʃ/', '/u/', '/ŋ/', '/k/', '/ə/', '/ɾ/',
        '/ʋ/', '/u/', '/ŋ/', '/tʃʰ/', '/eː/'
    ]),
    
    ("૧૨૩", ['1', '2', '3']),
    ("૦૧/૦૧/૨૦૨૪", [
        '0', '1', '/', '0', '1', '/', '2', '0', '2', '4'
    ]),
    
    ("§©®™", ["[Error: Invalid characters]"]),
    ("પ્રેમ", ['/p/', '/ɾ/', '/eː/', '/m/']),
    ("વિદ્યાર્થી", ['/ʋ/', '/i/', '/d̪/', '/j/', '/aː/', '/ɾ/', '/t̪ʰ/', '/iː/'])
]

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
