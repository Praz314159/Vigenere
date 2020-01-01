# This script is meant to run the key guess on many encrypted files using many of keywords
# The key guess function has the option of returning list of factors (candidates for 
# key length) ranked by frequency 
# Once we have this ranked list of key length candidates, we want to know how often the
# correct key length can be found in the top 5 candidate factors, top 10, and so on
# In the end, this script shoudl return the bucket in which the correct keylength is most likely 
# to appear 

import kasisky_debug as kd 
import vigenere as vg 
from nltk.book import * 
from nltk import corpus
import sys 

# we have nltk.book texts. These are texts 1 - 10 
# for each of these texts, we want to return the sorted factor frequency list 
# But, first I just want to check how often I'm guessing the correct key length with the 
# current heuristic 

#key = sys.argv[1]
#key_len = len(key)

keylens = {}  
with open("key_bank.txt", "rt", encoding = "utf-8") as key_bank :
    for count, line in enumerate(keybank):
        keys.update(line: len(line)) 

keys = list(keylens.keys())

#for each fileid, we will want to check whether the correct guess is made
#for all keys 
fileids = corpus.gutenberg.fileids() 
for fileid in fileids:
    #encrypting file 
    plaintext = corpus.gutenberg.raw(fileid)
    ciphertext = vg.encrypt(plaintext)
    #guessing key length 
    
    #guess key_length for each of the 
    cipher_match_indices, cipher_matches = vg.find_matches(ciphertext) 
    key_length = vg.guess_key_length(cipher_match_indices) 


















