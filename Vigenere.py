# This is a vigenere encryption tool. The purpose of this code is to take as input some text, encrypt it, then return the ecrypted message. 
# Recall how the vigenere cipher works. It is a polyalphabetic cipher that does the following: 
#               1) We choose a key
#               2) We repeat the key until it is the same length as the plaintext (this is known as the keystream  
#               3) We then proceed character by character encrypting with e_i = (p_i + k_i) mod (26)

import numpy as np
import nltk as nlp 
import sys
import os.path 
import matplotlib.pylab as plt

########################## ENCRYPTION/DECRYPTION METHODS ################################ 

# creating keystream from key 
def create_key_stream(key, plaintext):

    keystream = ""
    key_size = len(key)
    plain_text_size = len(plaintext) 
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
    plain_text_size = len(plaintext)
    #print("PLAINTEXT SIZE: ", len(plaintext)) 
    #print("KEYSTREAM SIZE: ", len(keystream))
    with open("ciphertext.txt", "w+", encoding = "utf-8") as ciphertext: 
        for i in range(plain_text_size):
            plain_ord = ord(plaintext[i])
            keystream_ord = ord(keystream[i])
            ciphertext.write( chr( (plain_ord + keystream_ord) % 255))
            #ciphertext = ciphertext + (chr((ord(plaintext[i]) + ord(keystream[i])) % 255))
    
    #closing file     
    ciphertext.close()
    return ciphertext 

#decrypting file 
def decrypt(keystream, cipherfile): 

# note that now ciphertext is a file object. So, the argument "ciphertext" should actually be the name of the file contianing the ciphertext. 

    cipher_f = open(cipherfile.name, "rt", encoding="utf8")
    ciphertext = cipher_f.read()
    cipher_text_size = len(ciphertext) 

    with open("recovered.txt", "w+", encoding = "utf8") as recovered_text:
        for i in range(cipher_text_size): 
            recovered_text.write(chr((ord(ciphertext[i]) - ord(keystream[i])) % 255))
   
    cipher_f.close()
    recovered_text.close() 
    return recovered_text 

######################### ANALYSIS ###########################################
######################### FREQUENCY ANALYSIS #################################

def frequency_analysis(text): 
    ASCII_char_array = []
    for i in range(255):
        ASCII_char_array.append(chr(i))

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

    #create dictionary associating characters with their counts and initializing 
    #all counts to 0  
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

def normalize_frequency(count_dict):
    # TO DO: normalize -- we just want count/len(count_dict) for each character. This may or may not be useful, who knows ... 
    pass

def plot_frequencies(text, c):
    text_counts = frequency_analysis(text)
    plt.bar(text_counts.keys(), text_counts.values(), color = c)
    plt.show() 

######################### KASISKI EXAMINATION ################################

#Some helper functions for the kasiski exam 

def disjoint(start_1, end_1, start_2, end_2):
    #we check whether two intervals are disjoint or not 
    disjoint = True 
    # if condition is true, then intervals are overlapping 
    if start_1 <= end_2 and start_2 <= end_1:
        disjoint = False

    return disjoint 

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

    #print("Distances: ", match_dists) 
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
    
    #we now have a dictionary that stores all the factors of all the distances between 
    #repeated sequences and their frequencies. We want the factor with the max frequency.
    
    if not factor_counts: 
        key_length_guess = -1
        most_likely_lengths = -1
        sorted_factor_counts = -1
        factor_counts = -1
    else:      
        sorted_factor_counts = sorted(factor_counts, key = factor_counts.get) 
        most_likely_lengths = sorted_factor_counts[-3:] 
        key_length_guess = max(most_likely_lengths) 
        #counts = list(factor_counts.values()) 
        #factors = list(factor_counts.keys()) 
        #key_length_guess = factors[counts.index(max(counts))] 
    
    # The kasisky analysis shouldn't necessarily return exactly the max frequency factor
    # Rather, it should return the longest high frequency factor 
    # How do we guess intelligently, given this? 

    return key_length_guess, most_likely_lengths, sorted_factor_counts, factor_counts  
 

def kasiski_exam(ciphertext): 
    match_indices, matches = find_matches(ciphertext) 
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

def main(): 
    # prompt user for file path
    plaintext_file_name = sys.argv[1]  
    #opening and storing file 
    plaintext = open(plaintext_file_name, "rt").read()
    # prompt user for key 
    key = sys.argv[2]  

    keystream = create_key_stream(key, plaintext) #creating keystream 
    ciphertext_file = encrypt(keystream, plaintext) #creating ciphertext file obj
    recovered_plaintext_file = decrypt(keystream, ciphertext_file) #creating plaintext file obj
    ciphertext = open(ciphertext_file.name, "rt", encoding = "utf8").read() 
    recovered_plaintext = open(recovered_plaintext_file.name, "rt", encoding = "utf8").read() 
  
    ################## CRYPTANALYSIS ###################

    #guess key_length 
    cipher_match_indices, cipher_matches = find_matches(ciphertext) 
    key_length, most_likely_lengths, sorted_factor_counts, factor_counts = guess_key_length(cipher_match_indices) 
    
    #generate cipher segments 
    cipher_segments = kasiski_exam(ciphertext) 
    #once we have the cipher segments, we have to run the frequency analysis on each 
    #individual segment. Then we find what the highest frequency 

    print("KEY LENGTH GUESS: ", key_length) 
    if key_length == len(key):
        print("WE GUESSED CORRECT! KEY LENGTH IS: ", key_length)
    else:
        print("INCORRCT KEY LENGTH")
        print(sorted_factor_counts)
    
if __name__ == "__main__":
    main() 

########################################################################################
'''
Let's do a review of what we have at the moment First, we have a bunch of methods: 
    1. create_key_stream() 
    2. encrypt()
    3. decrypt()
    4. frequency_analysis()
    5. normalize_frequencies() 
    6. plot_frequencies() 
    7. disjoint()
    8. find_matches()
    9. get_factors()
    10. guess_key_length() 
    11. kasiski_exam() 
    12. main() 

Currently, our main challenge is that it's difficult to guess the correct key_length.
This isn't so bad, though. We can check what percentage of the time the correct key is within
the five most common factors and so on. This will determine how we decide to choose likely 
key lengths. Once we know how many candidate key lengths to return, we turn our attention
to the problem of selecting the correct key length from amongst the candidates. This can be
done by running attempted decryptions and checking which key length makes the most sense. 
However, running decryptions using various key length candidates will defacto return the key. 
That is, both the correct keylength and key will be discovered simultaneously. The next question
is what the decryption process looks like using candidate keylengths. Clearly, the first step
is to split the ciphertext into text segments that represent "residue classes" mod candidate 
key length. Then we decreypt each ciphersegment with each of the 255 possible ASCII characters.
The one that produces, for each cipher segment, a character frequency profile that most closely 
resembles the character frequency profile of the English language will be the ASCII char
most likely to occupy the place in the key representing the "residue class" that is that
cipher segment. Once we have the most likely characters for each position in the key, 
we brute force decrypt until we find a non-gibberish recovered text. 





