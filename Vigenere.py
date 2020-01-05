# This is a vigenere encryption tool. The purpose of this code is to take as input some text, encrypt it, then return the ecrypted message. 
# Recall how the vigenere cipher works. It is a polyalphabetic cipher that does the following: 
#   1) We choose a key
#   2) We repeat the key until it is the same length as the plaintext (this is known as the keystream  
#   3) We then proceed character by character encrypting with e_i = (p_i + k_i) mod (26)

import numpy as np
import nltk as nlp 
import sys
import os.path 
import matplotlib.pylab as plt
import itertools, re
import io

########################## ENCRYPTION/DECRYPTION METHODS ################################ 

# creating keystream from key 
def create_key_stream(key, plaintext, alphabet):

    keystream = ""
    key_size = len(key)
    plain_text_size = len(plaintext)
    alphabet_size = len(alphabet)
 
    if key_size > plain_text_size:
        print("You're using a One-Time Pad!") 
        for i in range(plain_text_size): 
            keystream = keystream + key[i]
    elif key_size < plain_text_size: 
        for i in range(plain_text_size): 
            keystream = keystream + key[i % key_size] 
    else: 
        keystream = key
        print("You're using a One-Time Pad!") 

    return keystream 


#encrypting file: takes a plaintext file and returns both ciphertext string literal
# and ciphertext file 
def encrypt(keystream, plaintext_file_name, alphabet):
    plaintext = open(plaintext_file_name, "rt", encoding = "utf-8").read() 
    plain_text_size = len(plaintext)
    alphabet_size = len(alphabet)

    with open("ciphertext.txt", "w+", encoding = "utf-8") as ciphertext_file: 
        for i in range(plain_text_size):
            plain_ord = ord(plaintext[i])
            keystream_ord = ord(keystream[i])
            ciphertext_file.write( chr( (plain_ord + keystream_ord) % alphabet_size))
      
    ciphertext = ciphertext_file.read() 
      
    ciphertext_file.close()
    plaintext_file.close() 

    return ciphertext, ciphertext_file  


#decrypting file: takes a ciphertext file and returns the recovered text as both a string literal
#and as a file 
def decrypt(keystream, ciphertext_file_name, alphabet): 
    ciphertext = open(ciphertext_file_name, "rt", encoding="utf8").read()
    cipher_text_size = len(ciphertext) 
    alphabet_size = len(alphabet)

    with open("recovered.txt", "w+", encoding = "utf8") as recovered_text_file:
        for i in range(cipher_text_size): 
            recovered_text_file.write(chr((ord(ciphertext[i]) - ord(keystream[i])) % alphabet_size))
    
    recovered_text = open(recovered_text_file.name, "rt", encoding = "utf-8").read() 
     
    ciphertext_file.close()
    recovered_text_file.close() 
    return recovered_text, recovered_text_file 

######################### FREQUENCY ANALYSIS #################################

def frequency_analysis(text, alphabet): 
    characters = alphabet
    alphabet_size = len(alphabet)

    #building empty list that will store the frequency counts for each character
    count_list = []
    i = 0
    while i < alphabet_size: 
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
        while i < alphabet_size: 
            if char == characters[i]:
                count_list[i] += 1
                char_count_dict.update({char: count_list[i]}) 
            i += 1

    return char_count_dict 


#helper function that returns the alphabet sorted by character
#in the text
def frequency_order(text, alphabet):
    char_counts = frequency_analysis(text, alphabet)
    sorted_char_freq = sorted(char_counts, key = char_counts.get, reverse = True)


def frequency_match_score(text, alphabet, alphabet_by_frequency):
    #alphabet_by_frequency is a sorted list of the alphabet by general frequency in language
    text_freq_order = frequency_order(text, alphabet)  
    match_score = 0 
    for common_char in alphabet_by_frequency[:6]:
        if common_char in text_freq_order[-6:]: 
            match_score += 1
        else: 
            pass 

    for uncommon_char in alphabet_by_frequency[-6:]:
        if uncommon_char in text_freq_order[:6]:
            match_score += 1
        else: 
            pass 

    return match_score 


def normalize_frequency(count_dict):
    # TO DO: normalize -- we just want count/len(count_dict) for each character. 
    #This may or may not be useful, who knows ... 
    pass


#plots character frequencies as a simple bar graph
def plot_frequencies(text, bar_color):
    text_counts = frequency_analysis(text)
    plt.bar(text_counts.keys(), text_counts.values(), color = bar_color)
    plt.show() 



######################### NLP FUNCTIONARLY ###################################

def clean_text(text):
    '''
    TO DO: 

    1. Everything to upper or lower case 
    2. Get rid of punctuation 
    3. Get rid of spaces 

    '''
    pass 

def is_english(text): 
    #Should check if a text is likely to be english or not 
    #perhaps return a probability? 
    #It would be super useful if there was some sort of NLP ML 
    #that could recognize whether a certain text was the same 
    #language as that of a corpus of text. 
    pass 


######################### KASISKI EXAMINATION ################################

#helper function to check (if necessary) whether two sequences
#disjoint or not 
def disjoint(start_1, end_1, start_2, end_2):  
    disjoint = True 
    # if condition is true, then intervals are overlapping 
    if start_1 <= end_2 and start_2 <= end_1:
        disjoint = False

    return disjoint 


#helper function to all the repeated sequences 
#in a text and the indices at which those repeated 
#sequences occur. 
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


#helper function to get all factors of a number
def get_factors(n):
    factors = [] 
    for i in range(1, n+1): 
        if n%i == 0:
            factors.append(i)
    return factors 


def likely_key_lengths(ciphertext): 
    #computes the distances between pairs of consecutive elements of the match_indices
    #list, factors each of these distances, then counts the frequencies of each factor. 
    match_indices, matches = find_matches(ciphertext) 
    match_dists = [] 
    
    #Getting distances between starting index of repeated sequences 
    for i in range(len(match_indices)): 
        if (i % 2) == 0:
            match_distance = match_indices[i+1] - match_indices[i]
            match_dists.append(match_distance) 

    #print("Distances: ", match_dists) 
    factor_counts = {} 
    for i in range(len(match_dists)):
        factors = get_factors(match_dists[i]) 
        #print("Factors of ", match_dists[i], "are: ", factors)

        for j in range(len(factors)): 
            if factors[j] != 1: 
                if factors[j] not in factor_counts.keys():
                    factor_counts.update({factors[j]: 1})
                else:
                    factor_counts[factors[j]] += 1
            else:
                pass 
    
    #we now have a dictionary that stores all the factors of all the distances between 
    #repeated sequences and their frequencies. We want the most likely key lengths, which
    #correspond to the most frequenctly occuring factors. We'll take the five most common. 
    if not factor_counts: 
        key_length_guess = -1
        most_likely_lengths = -1
        sorted_factor_counts = -1
        factor_counts = -1
    else:      
        sorted_factor_counts = sorted(factor_counts, key = factor_counts.get, reverse = True) 
        most_likely_lengths = sorted_factor_counts[:5] 

    return most_likely_lengths, sorted_factor_counts  


def cipher_cuts(ciphertext, likely_key_length): 
    #we group every n_th character of the ciphertext
    #each of these groups are encrypted using one-alphabet substitution 
    cipher_segments = {} 

    for i in range(len(ciphertext)):
        if (i % likely_key_length) not in cipher_segments.keys(): 
            cipher_segments.update({i%likely_key_length: ciphertext[i]})
        else:
            cipher_segments[i % likely_key_length] = cipher_segments[i % likely_key_length]\
                    + ciphertext[i]

    cipher_cuts = list(cipher_segments.values()) 
    return cipher_cuts 


#Produces a list of all possible keys given a likely key length and 
#how the characters that likely occupy each position in the key
def get_key_combos(candidate_key_chars, likely_key_len):
    candidate_keys = []

    #I have no idea how this iteration works .... return to 
    for indexes in itertools.product(range(4), repeat = likely_len):
            key_candidate = ""
            for i in range(likely_len):
                key_candidate += candidate_key_chars[i][indexes[i]][0]
                candidate_keys.append(key_candidate) 
    
    return candidate_keys 


#function should return the most likely key 
def kasiski_exam_hack(ciphertext_file, alphabet, alphabet_by_frequency):
    
    ciphertext = open(ciphertext_file.name, "rt", encoding = "utf-8").read() 
    likely_lens, sorted_factor_counts = likely_key_lengths(ciphertext) 

    alphabet_size = len(alphabet)
    best_key_guess = ""
    for likely_len in likely_key_lens:
        cipher_cuts = cipher_cuts(ciphertext, likely_len)
        candidate_key_chars = []
        for i in range(len(cipher_cuts)):
            cut = cipher_cuts[i]
            cut_match_score_dict = {}

            for char in alphabet:
                decrypted_cut = ""
                for j in range(len(cut)):
                    decrypted_cut += chr((ord(cut[j]) - ord(char)) % alphabet_size)
        
                match_score = frequency_match_score(ciphertext, alphabet, alphabet_by_frequency)
                cut_match_score_dict.update({char: match_score})
            #now we have a dictionary of match scores for each char in the alphabet 
            #we want to get the chars with the max scores from the dictionary
            #if multiple chars have the same max match scores, then we want all of them 
            #getting max scores 
            sorted_match_scores = sorted(cut_match_score_dict, key = cut_match_score_dict.get,\
                    reverse = True)
            candidates = sorted_match_scores[:4]
            #instead of dictionary, create list of lists that is length likely_len
            candidate_key_chars.append(candidates)

        #getting all possible keys given best guesses about which chars comprise the key of a 
        #given length 
        possible_keys = get_key_combos(candidate_key_chars, likely_len)

        #brute forcing through possible keys to see if any of them are plausible
        #only one should actually produce coherent text in english 
        for key in possible_keys: 
            keystream = create_key_stream(key, text)
            trial_recovery_file = decrypt(ciphertext, keystream, alphabet) 
            trial_recovery_text = open(trial_recovery_file.name, "rt", encoding = "utf-8").read()
            
            #TO DO: write is_english method 
            if is_english(trial_recovery_text) == True: 
                best_key_guess = key 
            else:
                pass

    if best_key_guess == "":
        print("Reasonable key guess not found. \
               Consider using manual hack mode to break the cipher.") 
    
    return best_key_guess 

def main():
    #creating alphabet default is using ASCII alphabet. 
    char_array = []
    for i in range(255):
        char_array.append(chr(i))
    
    alphabet = char_array 
    alphabet_by_freq = list("ETAOINSHRDLCUMWFGYPBVKJXQZ")
    
    plaintext_file_name = sys.argv[1]   
    plaintext = open(plaintext_file_name, "rt").read()
    key = sys.argv[2]  

    keystream = create_key_stream(key, plaintext) 
    ciphertext_file = encrypt(keystream, plaintext, alphabet)
    recovered_plaintext_file = decrypt(keystream, ciphertext_file, alphabet)
    ciphertext = open(ciphertext_file.name, "rt", encoding = "utf8").read() 
    recovered_plaintext = open(recovered_plaintext_file.name, "rt", encoding = "utf8").read() 
  
    ################## CRYPTANALYSIS ###################
    #do some text cleaning first 
    best_key_guess = kasiski_exam_hack(ciphertext_file.name, alphabet, alphabet_by_frequency) 
    
    if best_key_guess == key: 
        print("You are a motherfucking beast")
    else: 
        print("You sad sack of shit") 
   
if __name__ == "__main__":
    main() 

########################################################################################
'''
Let's do a review of what we have at the moment First, we have a bunch of methods: 
    1. create_key_stream() 
    2. encrypt()
    3. decrypt()
    4. frequency_analysis()
    5. frequency_order()
    6. frequency_match_score() 
    6. normalize_frequencies() 
    7. plot_frequencies() 
    8. disjoint()
    9. find_matches()
    10. get_factors()
    11. guess_key_length() 
    12. cipher_cuts()
    13. get_key_combos()
    14: kasiski_exam()
    15. main() 

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

-- modify text so that any alphabet can be used -- let's stick to english??? 
-- use argparser to run cryptanalysis with preset alphabets (cyrillic, english, french, etc.) 
-- use argparser to create cmd vigenere encryption tool 
-- Perhaps move this to a object-oriented architecture 
-- include text cleaning ability -- use nltk? lowercase, get rid of punctuation and spaces, etc.  
'''



