# This is a vigenere encryption tool. The purpose of this code is to take as input some text, 
# encrypt it, then return the ecrypted message. Recall how the vigenere cipher works. 
# It is a polyalphabetic cipher that does the following: 
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
import argparse
########################## ENCRYPTION/DECRYPTION METHODS ################################ 

############## CLASSIC VIGENERE ##################

# creating keystream from key 
def create_key_stream(key, plaintext):

    keystream = ""
    key_size = len(key)
    plain_text_size = len(plaintext)
 
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
def encrypt(key, plaintext_file_name):
    plaintext_file = open(plaintext_file_name, "rt", encoding = "utf-8")
    plaintext = plaintext_file.read()
    plain_text_size = len(plaintext)
    
    keystream = create_key_stream(key, plaintext)

    with open("ciphertext.txt", "w+", encoding = "utf-8") as ciphertext_file: 
        for i in range(plain_text_size):
            ciphertext_file.write(chr((ord(plaintext[i]) + ord(keystream[i])) % 255))
       
        ciphertext = ciphertext_file.read() 
      
    ciphertext_file.close()
    plaintext_file.close() 
    return ciphertext, ciphertext_file  


#decrypting file: takes a ciphertext file and returns the recovered text as both a string literal
#and as a file 
def decrypt(key, ciphertext_file_name): 
    ciphertext_file = open(ciphertext_file_name, "rt", encoding="utf8")
    ciphertext = ciphertext_file.read()
    cipher_text_size = len(ciphertext) 
    
    keystream = create_key_stream(key, ciphertext)

    with open("recovered.txt", "w+", encoding = "utf8") as recovered_text_file:
        for i in range(cipher_text_size): 
            recovered_text_file.write(chr((ord(ciphertext[i]) - ord(keystream[i])) % 255))
    
    recovered_text = open(recovered_text_file.name, "rt", encoding = "utf-8").read() 
     
    ciphertext_file.close()
    recovered_text_file.close() 
    return recovered_text, recovered_text_file 

############## BEAUFORT VIGENERE ###################
############## RUNNING KEY VIGENERE ################
############## MULTIPLE PRIME KEY VIGENERE #########
############## AUTOKEY VIGENERE ####################

######################### FREQUENCY ANALYSIS #################################

def frequency_analysis(text):
    
    characters = []
    for i in range(255):
        characters.append(chr(i))
        
    alphabet_size = len(characters)

    #builds character array from the text 
    text_array = list(text) 
    
    #create dictionary associating characters with their counts and initializing 
    #all counts to 0  
    char_count_dict = {} 
    for char in characters:
        char_count_dict.update({char: 0})

    #counting characters and addding their counts to char_count_dict 
    for text_char in text_array:
        for alph_char in characters:
            if text_char == alph_char:
                new_count = char_count_dict.get(alph_char) + 1
                char_count_dict.update({alph_char: new_count}) 
    
    return char_count_dict 


#helper function that returns the alphabet sorted by character
#in the text
def frequency_order(text):
    char_counts = frequency_analysis(text)
    text_freq_order = sorted(char_counts, key = char_counts.get, reverse = True)
    return text_freq_order


def frequency_match_score(text, alphabet_by_frequency):
    #alphabet_by_frequency is a sorted list of the alphabet by general frequency in language
    text_freq_order = frequency_order(text)
    lower_by_freq = alphabet_by_frequency.lower()
    match_score = 0
   
    matches = []
    for common_char in text_freq_order[:5]:
        if (common_char in alphabet_by_frequency[:5]) or (common_char in lower_by_freq[:5]):
            match_score += 1
            matches.append(common_char)
        else: 
            pass 

    for uncommon_char in text_freq_order[-5:]:
        if (uncommon_char in alphabet_by_frequency[-5:]) or (uncommon_char in lower_by_freq[-5:]):
            match_score += 1
            matches.append(uncommon_char)
        else: 
            pass 

    return match_score, matches 


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

#helper function to remove non letters
def clean_text(text, alphabet):
    letters_and_space = alphabet + alphabet.lower() + " \t\n"

    only_letters = []
    for char in text:
        if char in letters_and_space:
            only_letters.append(char)

    clean_text = "".join(only_letters) 
    return clean_text


def load_dictionary(dictionary_name):
    with open(dictionary_name, "rt", encoding = "utf-8", errors = "ignore") as dictionary: 
        english_words = {}

        for word in dictionary.read().split("\n"):
            english_words[word] = None

    dictionary.close()
    return english_words 

def english_count(text, alphabet, dictionary_name):
    english_words = load_dictionary(dictionary_name)
    text = text.upper()
    text = clean_text(text, alphabet)
    candidate_words = text.split() 
    
    num_matches = 0
    matches = []
    if len(candidate_words) != 0: 
        for word in candidate_words:
            num_matches += 1
            matches.append(word) 
    else:
        num_matches = -1 

    match_frequency = float(num_matches)/len(candidate_words)
    return match_frequency, matches


def is_english(text, alphabet, dictionary_name, word_percentage, letter_percentage): 
    match_frequency, matches = english_count(text, alphabet, dictionary_name)
    word_match_percentage = match_frequency*100 
    
    #get letter percentage 
    num_letters = len(clean_text(text, alphabet)) 
    letter_match_percentage = (float(num_letters/len(text)))*100 
    matched = False

    if word_match_percentage >= word_percentage \
        and letter_match_percentage >= letter_percentage:
        matched = True 

    return matched 

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
        for j in range(i+1, len(text)):
            if text[i] == text[j]: 
                match_count = 0
                match = ''
                while i + match_count < len(text) and j + match_count < len(text):
                    if text[i + match_count] == text[j+match_count]: 
                        match += text[j+match_count] 
                        match_count += 1  
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
 
    factor_counts = {} 
    for i in range(len(match_dists)):
        factors = get_factors(match_dists[i]) 

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
        most_likely_lengths = sorted_factor_counts[:7] 
    
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
def get_key_combos(candidate_key_chars, likely_len):
    candidate_keys = []
    
    #I have no idea how this iteration works .... return to 
    for indexes in itertools.product(range(4), repeat = likely_len):
            key_candidate = ""
            for i in range(likely_len):
                key_candidate += candidate_key_chars[i][indexes[i]][0]
                candidate_keys.append(key_candidate)

    final_candidates = [candidate for candidate in candidate_keys if len(candidate) == likely_len]
    return final_candidates 


#function should return the most likely key 
def kasiski_exam_hack(ciphertext_file_name, alphabet, alphabet_by_frequency, word_percentage, letter_percentage):
    
    ciphertext = open(ciphertext_file_name, "rt", encoding = "utf-8").read() 
    likely_lens, sorted_factor_counts = likely_key_lengths(ciphertext) 
    
    if type(likely_lens) == int:
        print("No repeated sequences found in ciphertext. Cannot decrypt.")
        return

    alphabet_size = len(alphabet)
    best_key_guesses = [] 
    for likely_len in likely_lens: 
        cuts = cipher_cuts(ciphertext, likely_len)
        candidate_key_chars = []
        
        for i in range(len(cuts)):
            cut = cuts[i]
            cut_match_score_dict = {}
            
            for char in alphabet:
                decrypted_cut = ""
                
                for j in range(len(cut)):
                    decrypted_cut += chr((ord(cut[j]) - ord(char)) % 255)
                
                match_score, matches = frequency_match_score(decrypted_cut, alphabet_by_frequency)
                cut_match_score_dict.update({char: match_score})
 
            sorted_match_scores = sorted(cut_match_score_dict, key = cut_match_score_dict.get,reverse = True)
            candidates = sorted_match_scores[:5]
            candidate_key_chars.append(candidates)

        possible_keys = get_key_combos(candidate_key_chars, likely_len)

        for key in possible_keys:
            trial_recovery_text, trial_recovery_file = decrypt(key, ciphertext_file_name) 
            if is_english(trial_recovery_text, alphabet, "engmix.txt", word_percentage, letter_percentage):
                best_key_guesses.append(key)
            else:
                pass

        if len(best_key_guesses) != 0:
            break

    if not best_key_guesses:
        print("Reasonable key guess not found. \
               Consider using manual hack mode to break the cipher.")

    return best_key_guesses 

def main():
    parser = argparse.ArgumentParser() 
    # we must know which mode the user wants to operate in 
    Mode = parser.add_mutually_exclusive_group(required = True )
    #We want three main modes: encrypt, decrypt, and cryptanalyze
    Mode.add_argument("-e", "--encrypt", action = "store_true") 
    Mode.add_argument("-d", "--decrypt", action = "store_true")
    Mode.add_argument("-c", "--cryptanal", action = "store_true") 
    
    # no matter which mode the user is in, a file name must be passed. 
    # if the user is in encrypt mode the plaintext must be passed 
    # if the user is in decrypt mode the ciphertext must be passed 
    # if the user is in cryptanal mode the ciphertext must be passed 
    #File_pass = parser.add_mutually_exclusive_group(required = True)
        
    parser.add_argument("-f", "--file", required = True, help = "The name of either the plaintext file you\
            you want to encrypt, or the ciphertext file you want to \
            decrypt or analyze", type = str)
    parser.add_argument("-k","--key", required = False, help = "The key with which your plaintext file will be\
            encrypted", type = str) 
    parser.add_argument("-l", "--language", required = False, help = "This is the language you believe the\
            message to be in", default = 'English', choices = ['English'], type = str) 
    parser.add_argument("-wp", "--word_percentage", required = False, help = "When cryptanalyzing,\
            this is the percentage of matched words of the indicated language in the ciphertext\
            decrypted by a candidate keyword that must be reached in order for the candidate recovered\
            text to be considered of that language.",\
            default = 60, type = float)
    parser.add_argument("-lp", "--letter_percentage", required = False, help = "When cryptoanalyzing, this\
            is the percentage of matched letters of the indicated language in the ciphertext decrypted by\
            a candidate keyword that must be reached in order for the candidate recovered text to be\
            considered of that language.", default = 80, type = float) 

    #if we enter cryptanalysis mode, then we want to know if the analysis should be 
    #done automatically, or if it should be done manually.
    #if the analysis is to be done manually. Then, not sure ... will have to figure out
    args = parser.parse_args() 

    if args.encrypt:
        plaintext_file_name = args.file
        key = args.key 
        ciphertext, ciphertext_file = encrypt(key, plaintext_file_name) 
        print(plaintext_file_name, " has been encrypted:")
        cipher_text = open(ciphertext_file.name, "rt", encoding = "utf-8").read()
        print(cipher_text)  
    elif args.decrypt: 
        ciphertext_file_name = args.file
        key = args.key
        recovered_text, recovered_text_file = decrypt(key, ciphertext_file_name) 
        print(ciphertext_file_name, " has been decrypted:")
        recoveredtext = open(recovered_text_file.name, "rt", encoding = "utf-8").read()
        print(recoveredtext)
    elif args.cryptanal: 
        ciphertext_file_name = args.file
        if args.language == "English":
            dictionary_name = "mixeng.txt"
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            alphabet = alphabet + alphabet.lower()
            alphabet_by_freq = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
        word_percentage = args.word_percentage
        letter_percentage = args.letter_percentage
        best_key_guesses = kasiski_exam_hack(ciphertext_file_name, alphabet, alphabet_by_freq,\
                word_percentage, letter_percentage) 

        print("Key Guesses: ", best_key_guesses) 


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

-- modify text so that any alphabet can be used -- let's stick to english??? 
-- use argparser to run cryptanalysis with preset alphabets (cyrillic, english, french, etc.) 
-- use argparser to create cmd vigenere encryption tool 
-- Perhaps move this to a object-oriented architecture 

