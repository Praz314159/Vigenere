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
import matplotlib.pylab as plt

#We want to generate various keys of length 2-30 
#each key length, we generate 5 random keys
def gen_keys(min_key_len, max_key_len):
    start = 0 
    stop = 255
    with open("key_bank.txt", "w+", encoding = "utf-8") as key_bank: 
        for keylen in range(min_key_len,max_key_len): 
            #generate random key from ASCII characters --> range 0-255  
            for keynum in range(2):
                key = "" 
                ASCII_ords = [random.randint(start, stop) for ch_ord in range(keylen)]

                #convert list of ASCII orders into chars and write to key bank 
                for ASCII in ASCII_ords: 
                    key += chr(ASCII)
                    
                key_bank.write(key + "\n") 

    return key_bank 

def get_key_lens(keybank_name):
    keylens = {}  
    with open(keybank_name, "rt", encoding = "utf-8") as key_bank:
        for count, line in enumerate(key_bank):
            keylens.update({line: len(line)}) 
    
    return keylens 

# we have nltk.book texts. These are texts 1 - 10 
# for each of these texts, we want to return the sorted factor frequency list 
# But, first I just want to check how often I'm guessing the correct key length with the 
# current heuristic 
def validate_guess(keylens, fileids, alphabet, num_candidates):                  
    keys = list(keylens.keys()) 
    #for each fileid, we will want to check whether the correct guess is made
    #for all keys
    found = 0
    not_found = 0
    indecipherable = 0
 
    for fileid in fileids:
        #print("PLAINTEXT: ", fileid) 
        #setting plaintext 
        plaintext = corpus.gutenberg.raw(fileid)
        plaintext = plaintext[0:300]
 
        for key in keys:  
            ciphertext, ciphertext_file = vg.encrypt(key, plaintext) 

            #getting most likely key lengths
            cipher_match_indices, cipher_matches = vg.find_matches(ciphertext) 
            most_likely_lengths, sorted_factor_counts = vg.likely_key_lengths(ciphertext)
            
            if type(sorted_factor_counts) == int:
                indecipherable += 1
                continue 

            most_likely_lengths = sorted_factor_counts[:num_candidates]
            #print("Included: ", keylens.get(key) in most_likely_lengths, "|Key length: ", keylens.get(key), "|Choices: ", most_likely_lengths)
            if keylens.get(key) != 1:
                if keylens.get(key) in most_likely_lengths: 
                    #print("Included: ", True, "|Key length: ", keylens.get(key), "|Choices: ", most_likely_lengths)
                    found += 1
                else: 
                    print("Included: ", False, "|Key length: ", keylens.get(key), "|Choices: ",\
                           most_likely_lengths, "|Next: ", sorted_factor_counts[:num_candidates+1])
                    not_found += 1 

    percent_top5 = (found)/(found + not_found)
    percent_indecipherable = (indecipherable)/(found+not_found+indecipherable)
    return percent_top5, percent_indecipherable
    
def main(): 
    #creating ASCII alphabet 
    char_array = []
    for i in range(255):
        char_array.append(chr(i))
    
    alphabet = char_array 
    
    #max_key_len = int(sys.argv[1])
    num_candidates = int(sys.argv[1])
    min_key_len = int(sys.argv[2])
    max_key_len = int(sys.argv[3])

    #generating random key bank 
    #key_bank = gen_keys(42) 
    
    #getting list of fileids 
    fileids = corpus.gutenberg.fileids()

    #keylens = get_key_lens("key_bank.txt")
    #efficiency = validate_guess(keylens, fileids, alphabet, num_candidates)
    #print("EFFICIENCY: ", efficiency)

    #plotting max key length vs efficiency
    efficiencies = {}
    indecipherable = {}
    for min_len in range(min_key_len, max_key_len-5):
        key_bank = gen_keys(min_len, max_key_len)
        keylens = get_key_lens("key_bank.txt")
        efficiency, p_indecipherable = validate_guess(keylens, fileids, alphabet, num_candidates)
        efficiencies.update({min_len: efficiency})
        indecipherable.update({min_len: p_indecipherable})
        print("MIN KEY LENGTH: ", min_len, "|EFFICIENCY: ", efficiency, \
                "|% INDECIPHERABLE: ", p_indecipherable)

    lists_1 = sorted(efficiencies.items())
    min_len_1, efficiency = zip(*lists_1)

    lists_2 = sorted(indecipherable.items())
    min_len_2, p_indecipherable = zip(*lists_2)
    
    plt.plot(min_len_1, efficiency)
    plt.plot(min_len_2, p_indecipherable)
    plt.title("Moving Min Key Length with Fixed Max_Key_Length and Num_Candidates")
    plt.xlabel("Min Key Length") 
    plt.ylabel("% Efficiency, % Indecipherable") 
    plt.show()
    #percent_top5 = validate_guess(keylens, fileids, alphabet, num_candidates) 
    #print("PERCENT CORRECT KEY LEN APPEARS IN FIVE MOST FREQUENCE FACTORS: ", percent_top5) 
    
if __name__ == "__main__": 
    main() 
















