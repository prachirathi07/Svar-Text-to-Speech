def get_gujarati_phoneme_set():
    phoneme_set = {
        'અ': '/ə/', 'આ': '/aː/', 'ઇ': '/i/', 'ઈ': '/iː/',
        'ઉ': '/u/', 'ઊ': '/uː/', 'ઋ': '/ɾ̩/', 'ૠ': '/ɾ̩ː/',
        'એ': '/eː/', 'ઐ': '/əi/', 'ઓ': '/oː/', 'ઔ': '/əu/',
        'અં': '/əŋ/', 
        
        'ા': '/aː/', 'િ': '/i/', 'ી': '/iː/', 'ુ': '/u/', 'ૂ': '/uː/',
        'ૃ': '/ɾ̩/', 'ૄ': '/ɾ̩ː/', 'ે': '/eː/', 'ૈ': '/əi/',
        'ો': '/oː/', 'ૌ': '/əu/',
        'ં': '/ŋ/', 'ઃ': '/h/', 'ઁ': '/˜/',
        
        'ક': '/k/', 'ગ': '/ɡ/', 'ચ': '/tʃ/', 'જ': '/dʒ/',
        'ટ': '/ʈ/', 'ડ': '/ɖ/', 
        'ત': '/t/',
        'દ': '/d̪/',
        'પ': '/p/', 'બ': '/b/',
        'ખ': '/kʰ/', 'ઘ': '/ɡʱ/',
        'છ': '/tʃʰ/', 'ઝ': '/dʒʱ/',
        'ઠ': '/ʈʰ/', 'ઢ': '/ɖʱ/', 'થ': '/t̪ʰ/', 'ધ': '/d̪ʱ/',
        'ફ': ['/f/', '/pʰ/'],
        'ભ': '/bʱ/',
        'મ': '/m/', 'ન': '/n/', 'ણ': '/ɳ/', 'ઙ': '/ŋ/', 'ઞ': '/ɲ/',
        'સ': '/s/', 'શ': '/ʃ/', 'હ': '/h/', 'ષ': '/ʂ/',
        'ય': '/j/', 'ર': '/ɾ/', 'લ': '/l/', 'વ': '/ʋ/', 'ળ': '/ɭ/',
        
        '્': None,
        
        '૦': '0', '૧': '1', '૨': '2', '૩': '3', '૪': '4',
        '૫': '5', '૬': '6', '૭': '7', '૮': '8', '૯': '9'
    }
    
    print("Comprehensive Gujarati Phoneme Set:")
    for grapheme, phoneme in phoneme_set.items():
        print(f"{grapheme}: {phoneme}")
    
    return phoneme_set

phoneme_set = get_gujarati_phoneme_set()

consonants = set([
    'ક','ગ','ચ','જ','ટ','ડ','ત','દ','પ','બ',
    'ખ','ઘ','છ','ઝ','ઠ','ઢ','થ','ધ','ફ','ભ',
    'મ','ન','ણ','ઙ','ઞ','સ','શ','હ','ષ','ય','ર','લ','વ','ળ'
])
vowel_signs = set(['ા','િ','ી','ુ','ૂ','ૃ','ૄ','ે','ૈ','ો','ૌ'])
independent_vowels = set(['અ','આ','ઇ','ઈ','ઉ','ઊ','ઋ','ૠ','એ','ઐ','ઓ','ઔ','અં'])
virama = '્'
nasalization = set(['ં','ઃ','ઁ'])
allowed_output_punct = set(['/','-'])
allowed_ignore_punct = set(["?", "!", ",", ".", ";", ":"])

def grapheme2phoneme(word):
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
        if ch.isspace():
            i += 1
            is_new_group = True
            continue
        
        if ch in allowed_ignore_punct:
            i += 1
            is_new_group = True
            continue
        
        if ch in allowed_output_punct:
            output.append(ch)
            i += 1
            is_new_group = True
            continue
        
        if ch == virama:
            i += 1
            continue
        
        if (ch == 'ધ' and i+2 < len(word) and word[i+1] == virama and word[i+2] == 'ધ'):
            output.append('/d̪/')
            output.append('/d̪ʱ/')
            i += 3
            is_new_group = True
            continue

        mapping = phoneme_set.get(ch)
        if isinstance(mapping, list):
            mapping = mapping[0]
        if ch in independent_vowels or (ch.isdigit() and mapping is not None):
            output.append(mapping)
            i += 1
            is_new_group = True
            continue
        if ch in vowel_signs or ch in nasalization:
            if ch in nasalization and i == len(word)-1 and i-1 >= 0 and word[i-1] in vowel_signs:
                i += 1
                continue
            output.append(mapping)
            i += 1
            is_new_group = True
            continue
        
        if ch in consonants:
            if is_new_group:
                output.append(mapping)
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
        output.append(ch)
        i += 1
    return output
