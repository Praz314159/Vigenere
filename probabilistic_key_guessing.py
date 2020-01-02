# This script is meant to run the key guess on many encrypted files using many of keywords
# The key guess function has the option of returning list of factors (candidates for 
# key length) ranked by frequency 
# Once we have this ranked list of key length candidates, we want to know how often the
# correct key length can be found in the top 5 candidate factors, top 10, and so on
# In the end, this script shoudl return the bucket in which the correct keylength is most likely 
# to appear 

import Vigenere as vg  
from nltk import corpus
import sys 
import random

#We want to generate various keys of length 2-30 
#each key length, we generate 5 random keys
def gen_keys():
    #generate keywords and write them into file 
    start = 0 
    stop = 255
    with open("key_bank.txt", "w+", encoding = "utf-8") as key_bank: 
        for keylen in range(2,25): 
            #generate random key from ASCII characters --> range 0-255 
            #generate 5 keys 
            for keynum in range(5):
                key = "" 
                ASCII_ords = [random.randint(start, stop) for ch_ord in range(keylen)]
                #print(ASCII_ords) 

                #convert list of ASCII orders into chars and write to key bank 
                for ASCII in ASCII_ords: 
                    key += chr(ASCII)
                    
                key_bank.write(key + "\n") 

    return key_bank 

# we have nltk.book texts. These are texts 1 - 10 
# for each of these texts, we want to return the sorted factor frequency list 
# But, first I just want to check how often I'm guessing the correct key length with the 
# current heuristic 
def validate_guess(keys, fileids): 
    
    #creating string literal dictionary of keys in keybank                 
    keylens = {}  
    with open("key_bank.txt", "rt", encoding = "utf-8") as key_bank:
        for count, line in enumerate(key_bank):
            keylens.update({line: len(line)}) 

    #for each fileid, we will want to check whether the correct guess is made
    #for all keys
    correct_count = 0 
    incorrect_count = 0

    found = 0
    not_found = 0
    for fileid in fileids:
        #print("PLAINTEXT: ", fileid) 
        #setting plaintext 
        plaintext = corpus.gutenberg.raw(fileid)
        plaintext = plaintext[0:300]
        #encrypting for each key 
        for key in keys:
            #correct = False 
            keystream = vg.create_key_stream(key, plaintext)
            #print(len(keystream)) 
            ciphertext_file = vg.encrypt(keystream, plaintext)
            ciphertext = open(ciphertext_file.name, "rt", encoding = "utf-8").read() 
            #guessing key length 
            cipher_match_indices, cipher_matches = vg.find_matches(ciphertext) 
            key_length_guess, most_likely_lengths, sorted_factor_counts, factor_counts = vg.guess_key_length(cipher_match_indices)
            
            if key_length_guess != keylens.get(key):
                incorrect_count += 1 
                #print("NO MATCH \n|key: ", key, "\n| guess: ", key_length_guess, "\n| true: ",\
                #        keylens.get(key)) 
            else: 
                correct_count += 1
            
            if keylens.get(key) in sorted_factor_counts[-5:]: 
                found += 1
            else: 
                not_found += 1 

    percent_top5 = (found)/(found + not_found) 
    percent_correct = (correct_count)/(correct_count + incorrect_count)
    return percent_top5, percent_correct 

def main(): 
    #generating random key bank 
    key_bank = gen_keys() 
    
    #creating string literal dictionary of keys in keybank                 
    keylens = {}  
    with open("key_bank.txt", "rt", encoding = "utf-8") as key_bank:
        for count, line in enumerate(key_bank):
            keylens.update({line: len(line)}) 
    

    #listifying keys 
    keys = list(keylens.keys())

    #getting list of fileids 
    fileids = corpus.gutenberg.fileids() 

    percent_top5, percent_correct = validate_guess(keys, fileids) 
    print("% CORRECT: ", percent_correct) 
    print("PERCENT CORRECT KEY LEN APPEARS IN FIVE MOST FREQUENCE FACTORS: ", percent_top5) 

if __name__ == "__main__": 
    main() 
















