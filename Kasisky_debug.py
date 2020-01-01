import numpy as np
import nltk as nlp 
import sys
import os.path 
import matplotlib.pylab as plt

################### INPUT ########################################
plaintext_file_name = sys.argv[1] 
key = sys.argv[2]
mode = input("In what mode would you like to open the file r, w, a or rt?")

f = open(plaintext_file_name, mode)
plaintext = f.read() 
 
key_size = len(key)
plain_text_size = len(plaintext) 

########################## ENCRYPTION/DECRYPTION METHODS ################################ 

# creating keystream from key 
def create_key_stream(key):

    keystream = ""

    # if the keysize is greater than plaintext size, then truncate key to size of plaintext. 
    if key_size > plain_text_size:
        print("You're using a One-Time Pad!") 
        for i in range(plain_text_size): 
            keystream = keystream + key[i]

    # if key_size < plain_text_size 
    elif key_size < plain_text_size: 
        for i in range(plain_text_size): 
            keystream = keystream + key[i % key_size]

    # if key_size = plain_text_size --> in this case, the cipher is a one time pad 
    else: 
        keystream = key
        print("You're using a One-Time Pad!") 

    return keystream 

# encrypting file 
def encrypt(keystream, plaintext): 
    #note that open creates a file "ciphertext.txt" if the file doesn't already exist. If it does exist, 
    #clears the file contents 
    with open("ciphertext.txt", "w+", encoding = "utf8") as ciphertext: 
        for i in range(plain_text_size): 
            ciphertext.write( chr( (ord(plaintext[i]) + ord(keystream[i])) % 255) )
            #ciphertext = ciphertext + (chr((ord(plaintext[i]) + ord(keystream[i])) % 255))
    
    #closing file     
    ciphertext.close()
    return ciphertext 

#decrypting file 
def decrypt(keystream, cipherfile): 

    cipher_f = open(cipherfile.name, "rt", encoding="utf8")
    ciphertext = cipher_f.read()
    #ciphertext = cipher_f.read() 
    with open("recovered.txt", "w+", encoding = "utf8") as recovered_text:
        for i in range(plain_text_size): 
            recovered_text.write(chr((ord(ciphertext[i]) - ord(keystream[i])) % 255))
            
    cipher_f.close()
    recovered_text.close() 
    return recovered_text 

######################### ANALYSIS ############################################ 

ASCII_char_array = []

for i in range(255):
    ASCII_char_array.append(chr(i))

##################################### KASISKI EXAMINATION ##########################################

#Here, we take a ciphertext and return the most probable key, after finding the 
#keylength by searching for repeated charactersequences in the ciphertext and 
#analyzing the distances between them 

#Some helper functions for the kasiski exam 

def disjoint(start_1, end_1, start_2, end_2):
    #we check whether two intervals are disjoint or not 
    disjoint = True 
    # if condition is true, then intervals are overlapping 
    if start_1 <= end_2 and start_2 <= end_1:
        disjoint = False

    return disjoint 

#return starting indices for matching substrings and the matches themselves  

def find_matches(text): 
    index_matches = []
    matches = [] 
    text = list(text)
    
    for i in range(len(text)): 
        #print("i: ", text[i])
        for j in range(i+1, len(text)):
            #print("j: ", text[j])
            if text[i] == text[j]:
                #print("Match at char: ", text[j]) 
                match_count = 0
                match = ''
                while i + match_count < len(text) and j + match_count < len(text):
                    if text[i + match_count] == text[j+match_count]: 
                        match += text[j+match_count] 
                        match_count += 1 
                        #print("Match: ", match) 
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

def get_factors(n):
    #get all factors helper function
    factors = [] 
    for i in range(1, n+1): 
        if n%i == 0:
            factors.append(i)
    return factors 

def guess_key_length(match_indices): 
    #computes the distances between pairs of consecutive elements of the match_indices
    #list, factors each of these distances, then counts the frequencies of each factor.
    #The most common factor is the most likely key length, and will be our guess 
    match_dists = [] 
    
    #Getting distances between starting index of repeated sequences 
    for i in range(len(match_indices)): 
        if (i % 2) == 0:
            match_distance = match_indices[i+1] - match_indices[i]
            match_dists.append(match_distance) 

    print("Distances: ", match_dists) 
    #we create a dictionary that stores factors and their counts
    factor_counts = {} 
    for i in range(len(match_dists)):
        #getting the factors for each distance 
        factors = get_factors(match_dists[i]) 

        #print("Factors of ", match_dists[i], "are: ", factors)
        for j in range(len(factors)): 
            if factors[j] != 1: 
                if factors[j] not in factor_counts.keys():
                    #if the factor isn't a key in the dictionary
                    #add the factor to the dictionary and 
                    #update its count to 1
                    factor_counts.update({factors[j]: 1})
                else:
                    #if the factor is already a key in the dictionary
                    #update the factor's count 
                    factor_counts[factors[j]] += 1
            else:
                pass 
    
    print("Sorted Factors: ", sorted(factor_counts))
    print("Unsorted Factor Frequencies: ", factor_counts)
    print("Factor Frequencies: ", sorted(factor_counts, key = factor_counts.get))  
    #we now have a dictionary that stores all the factors of all the distances between 
    #repeated sequences and their frequencies. We want the factor with the max frequency.
    
    #sorted_factor_counts = sorted(factor_counts, key = factor_counts.get) 
    #most_likely_lengths = sorted_factor_counts[-3:] 
    #key_length_guess = max(most_likely_lengths) 
    counts = list(factor_counts.values()) 
    factors = list(factor_counts.keys()) 
    key_length_guess = factors[counts.index(max(counts))] 
    
    # The kasisky analysis shouldn't necessarily return exactly the max frequency factor
    # Rather, it should return the longest high frequency factor 
    # How do we guess intelligently, given this? 

    return key_length_guess 
 

def kasiski_exam(ciphertext): 
    match_indices, matches = find_disjoint_matches(ciphertext) 
    key_length = guess_key_length(match_indices) 

    #we group every n_th character of the ciphertext
    #each of these groups are encrypted using one-alphabet substitution 
    cipher_segments = {} 

    for i in range(len(ciphertext)):
        if (i % key_length) not in cipher_segments.keys(): 
            cipher_segments.update({i%key_length: ciphertext[i]})
        else:
            cipher_segments[i % key_length] = cipher_segments[i % key_length] + ciphertext[i]

    #Now we should have a dictionary that stores cipher_segments as values associated with the
    #residue classes of key_length 
    
    return list(cipher_segments.values()) 


######################################## FREQUENCY ANALYSIS ######################################

def frequency_analysis(text): 
    characters = ASCII_char_array
    
    #building empty list that will store the frequency counts for each character
    count_list = []
    i = 0
    while i < 255: 
        count_list.append(0)
        i += 1 

    #builds character array from the text 
    text_array = [] 
    for char in text:
        text_array.append(char)

    #create dictionary associating characters with their counts and initializing all counts to 0  
    char_count_dict = {} 
    for i in range(len(characters)):
            char_count_dict.update({characters[i]: 0}) 
   
    #counting characters and addding their counts to char_count_dict 
    for char in text_array:
        i = 0
        while i < 255: 
            if char == characters[i]:
                count_list[i] += 1
                char_count_dict.update({char: count_list[i]}) 
            i += 1

    #create a dictionary associating characters with their 
    return char_count_dict 

                    ############ TESTING ###########
############ ENCRYPTION PLAINTEXT, DECRYPTING CIPHERTEXT ################

keystream = create_key_stream(key) 
ciphertext_file = encrypt(keystream, plaintext)
recovered_plaintext_file = decrypt(keystream, ciphertext_file) 
ciphertext = open(ciphertext_file.name, "rt", encoding = "utf8").read() 
recovered_plaintext = open(recovered_plaintext_file.name, "rt", encoding = "utf8").read() 

print("Plaintext: ", plaintext)
print("Encrypted File: ", ciphertext)
print("Recovered Plaintext: ", recovered_plaintext)
print("Plaintext size: ", len(plaintext)) 
print("Keystream size: ", len(keystream)) 
print("Ciphertext size: ", len(ciphertext)) 

#################### CRYPTANALYSIS ###################

print("CRYPTANALYSIS") 

#guess key_length 
cipher_match_indices, cipher_matches = find_matches(ciphertext) 

#print("CIPHER MATCHES: ", cipher_matches)
#print("CIPHER MATCH INDICES: ", cipher_match_indices)

key_length = guess_key_length(cipher_match_indices) 

#generate cipher segments 
#cipher_segments = kasiski_exam(ciphertext)

#disjoint_matches for plaintext 
#plaintext_match_indices, plain_matches = find_disjoint_matches(plaintext) 
#print("PLAIN MATCHES: ", plain_matches) 
#print("PLAIN MATCH INDICES: ", plaintext_match_indices) 

print("KEY LENGTH GUESS: ", key_length) 
if key_length == len(key):
    print("WE GUESSED CORRECT! KEY LENGTH IS: ", key_length) 
else:
    print("INCORRCT KEY LENGTH") 

#print(cipher_segments) 





