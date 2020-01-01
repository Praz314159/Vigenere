# This script is meant to run the key guess on many encrypted files using many of keywords
# The key guess function has the option of returning list of factors (candidates for 
# key length) ranked by frequency 
# Once we have this ranked list of key length candidates, we want to know how often the
# correct key length can be found in the top 5 candidate factors, top 10, and so on
# In the end, this script shoudl return the bucket in which the correct keylength is most likely 
# to appear 

#import Kasisky_debug as kd 
import Vigenere as vg 
from nltk.book import * 
from nltk import corpus
import sys 

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
    #encrypting for each key 
    for key in keys:
        correct = False 
        keystream = vg.create_key_stream(key) 
        ciphertext = vg.encrypt(keystream, plaintext)
        
        #guessing key length 
        cipher_match_indices, cipher_matches = vg.find_matches(ciphertext) 
        key_length_guess = vg.guess_key_length(cipher_match_indices)

        if key_length_guess == keylens.get(key):
            correct = True
            print(correct) 


#ideally, we are able to create a plot that has key length on the x axis and percent correct guesses
#on the y axis 


















