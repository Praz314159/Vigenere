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
    start = 0 
    stop = 255
    with open("key_bank.txt", "w+", encoding = "utf-8") as key_bank: 
        for keylen in range(2,25): 
            #generate random key from ASCII characters --> range 0-255  
            for keynum in range(5):
                key = "" 
                ASCII_ords = [random.randint(start, stop) for ch_ord in range(keylen)]

                #convert list of ASCII orders into chars and write to key bank 
                for ASCII in ASCII_ords: 
                    key += chr(ASCII)
                    
                key_bank.write(key + "\n") 

    return key_bank 

# we have nltk.book texts. These are texts 1 - 10 
# for each of these texts, we want to return the sorted factor frequency list 
# But, first I just want to check how often I'm guessing the correct key length with the 
# current heuristic 
def validate_guess(keylens, fileids, alphabet): 
                      
    keys = list(keylens.keys()) 
    #for each fileid, we will want to check whether the correct guess is made
    #for all keys
    found = 0
    not_found = 0
 
    for fileid in fileids:
        #print("PLAINTEXT: ", fileid) 
        #setting plaintext 
        plaintext = corpus.gutenberg.raw(fileid)
        plaintext = plaintext[0:300]
 
        for key in keys: 
            keystream = vg.create_key_stream(key, plaintext, alphabet) 
            ciphertext, ciphertext_file = vg.encrypt(keystream, fileid, alphabet) 
            ciphertext = ciphertext[0:300] 

            #getting most likely key lengths
            cipher_match_indices, cipher_matches = vg.find_matches(ciphertext) 
            most_likely_lengths, factor_counts = vg.likely_key_lengths(ciphertext)
           
            if keylens.get(key) in most_likely_lengths: 
                found += 1
            else: 
                not_found += 1 

    percent_top5 = (found)/(found + not_found) 
    return percent_top5

def main(): 
    #creating ASCII alphabet 
    char_array = []
    for i in range(255):
        char_array.append(chr(i))
    
    alphabet = char_array 

    #generating random key bank 
    key_bank = gen_keys() 
    
    #creating string literal dictionary of keys in keybank                 
    keylens = {}  
    with open("key_bank.txt", "rt", encoding = "utf-8") as key_bank:
        for count, line in enumerate(key_bank):
            keylens.update({line: len(line)}) 
    
    #listifying keys 
    #keys = list(keylens.keys())
    
    #getting list of fileids 
    fileids = corpus.gutenberg.fileids() 
    
    percent_top5 = validate_guess(keylens, fileids, alphabet) 
    print("% CORRECT: ", percent_correct) 
    print("PERCENT CORRECT KEY LEN APPEARS IN FIVE MOST FREQUENCE FACTORS: ", percent_top5) 

if __name__ == "__main__": 
    main() 
















