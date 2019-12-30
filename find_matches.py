
plaintext = open("plaintext.txt").read() 

def find_matches(text): 
    index_matches = []
    matches = [] 
    text = list(text)
    
    for i in range(len(text)): 
        print("i: ", text[i])
        for j in range(i+1, len(text)):
            print("j: ", text[j])
            if text[i] == text[j]:
                print("Match at char: ", text[j]) 
                match_count = 0
                match = ''
                while i + match_count < len(text) and j + match_count < len(text):
                    if text[i + match_count] == text[j+match_count]: 
                        match += text[j+match_count] 
                        match_count += 1 
                        print(match) 
                    else: 
                        break 

                if match_count > 1: 
                    matches.append(match) 
                    index_matches.append(i) 
                    index_matches.append(j) 
                else: 
                    pass 
            else: 
                pass 


    return index_matches, matches

matched_indices, match_sequences = find_matches(plaintext) 

print("MATCHED INDICES: ", matched_indices)
print("MATCHES SEQUENCES: ", match_sequences) 











