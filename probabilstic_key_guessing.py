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
        for keylen in range(2,30): 
            #generate random key from ASCII characters --> range 0-255 
            #generate 5 keys 
            for keynum in range(5):
                key = "" 
                ASCII_ords = [random.randint(start, stop) for ch_ord in range(keylen)]
                print(ASCII_ords) 

                #convert list of ASCII orders into chars and write to key bank 
                for ASCII in ASCII_ords: 
                    key += chr(ASCII)
                    
                key_bank.write(key + "\n") 

    return key_bank 

key_bank = gen_keys() 

# we have nltk.book texts. These are texts 1 - 10 
# for each of these texts, we want to return the sorted factor frequency list 
# But, first I just want to check how often I'm guessing the correct key length with the 
# current heuristic 

keylens = {}  
with open("key_bank.txt", "rt", encoding = "utf-8") as key_bank:
    for count, line in enumerate(key_bank):
        keylens.update({line: len(line)}) 

keys = list(keylens.keys())

#for each fileid, we will want to check whether the correct guess is made
#for all keys 
fileids = corpus.gutenberg.fileids() 
for fileid in fileids:
    #setting plaintext 
    plaintext = corpus.gutenberg.raw(fileid)
    plaintext = plaintext[0:500]
    #encrypting for each key 
    for key in keys:
        correct = False 
        keystream = vg.create_key_stream(key, plaintext)
        #print(len(keystream)) 
        ciphertext_file = vg.encrypt(keystream, plaintext)
        ciphertext = open(ciphertext_file.name, "rt", encoding = "utf-8").read() 
        #guessing key length 
        cipher_match_indices, cipher_matches = vg.find_matches(ciphertext) 
        key_length_guess = vg.guess_key_length(cipher_match_indices)

        if key_length_guess == keylens.get(key):
            correct = True
            print(correct, "| guess: ", key_length_guess, "| true: ", keylens.get(key), \
                    "| plaintext: ", fileid) 


#ideally, we are able to create a plot that has key length on the x axis and percent correct guesses
#on the y axis 


















