from preprocessor import normalize_text

test_cases = [
    # 1. Number Conversion Cases
    ("મારી પાસે ૨૩ કિતાબો છે.", "મારી પાસે ત્રેવીસ કિતાબો છે."),
    ("૧,૨૩,૪૫૬", "એક લાખ ત્રેવીસ હજાર ચારસો છપ્પન"),
    # Ordinal Numbers
    ("તે ૨૩મી જાન્યુઆરી એ આવ્યો.", "તે ત્રેવીસમી જાન્યુઆરી એ આવ્યો."),
    ("૧લો, ૨જો, ૩જો", "પહેલો બીજો ત્રીજો"),
    # Mixed Numbers (Currency)
    ("કિંમત ₹૨૩.૫૦ છે", "કિંમત રૂપિયા ત્રેવીસ અને પચાસ પૈસા છે"),
    
    # 2. Date and Time Cases
    ("૨૩/૦૧/૨૦૨૪", "ત્રેવીસમી જાન્યુઆરી બે હજાર ચોવીસ"),
    ("૨૩-૦૧-૨૦૨૪", "ત્રેવીસમી જાન્યુઆરી બે હજાર ચોવીસ"),
    ("સવારે ૯:૩૦ વાગ્યે", "સવારે નવ વાગ્યા ત્રીસ મિનિટે"),
    
    # 3. Abbreviation Cases
    ("ડૉ. પટેલ અને શ્રી. મહેતા", "ડોક્ટર પટેલ અને શ્રીમાન મહેતા"),
    ("ગુ.યુની.", "ગુજરાત યુનિવર્સિટી"),
    
    # 4. Special Character Cases
    ("તમે ક્યાં છો...?","તમે ક્યાં છો?"),
    ('તે કહે છે કે, "હું આવીશ"', "તે કહે છે કે હું આવીશ"),
    ("૨૫% લોકો", "પચ્ચીસ ટકા લોકો"),
    
    # 5. Unicode Normalization Cases
    ("પ્રશ્ન", "પ્રશ્ન"),
    ("વિદ્યા\u200dર્થી", "વિદ્યાર્થી"),
    
    # 6. Whitespace Cases
    ("રામ    અને    શ્યામ", "રામ અને શ્યામ"),
    ("રામ\n\n\nશ્યામ", "રામ શ્યામ"),
    
    # 7. Mixed Complex Cases
    ("ડૉ. પટેલે ૨૩/૦૧/૨૦૨૪ ના રોજ ₹૧,૨૩,૪૫૬.૭૮ માં ૨૫% છૂટ આપી...",
        "ડોક્ટર પટેલે ત્રેવીસમી જાન્યુઆરી બે હજાર ચોવીસ ના રોજ રૂપિયા એક લાખ ત્રેવીસ હજાર ચારસો છપ્પન અને અઠ્યોતેર પૈસા માં પચ્ચીસ ટકા છૂટ આપી."),
    
    # 8. Edge Cases
    ("", ""),
    ("§₩₩₩§", "[Error: Invalid characters]"),
    ("૯૯,૯૯,૯૯,૯૯૯", "નવ્વાણું કરોડ નવ્વાણું લાખ નવ્વાણું હજાર નવસો નવ્વાણું"),
    ("My name is રમેશ and I am ૨૩ years old", "My name is રમેશ and I am ત્રેવીસ years old")
]

for idx, (inp, expected) in enumerate(test_cases, 1):
    output = normalize_text(inp)
    print(f"Test Case {idx}:")
    print("Input:    ", repr(inp))
    print("Output:   ", output)
    print("Expected: ", expected)
    print("Result:   ", "PASS" if output == expected else "FAIL", "\n")