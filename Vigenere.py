import numpy as np
import nltk as nlp 
import sys
import os.path 
import matplotlib.pylab as plt

# This is a vigenere encryption tool. The purpose of this code is to take as input some text, encrypt it, then return the ecrypted message. 
# Recall how the vigenere cipher works. It is a polyalphabetic cipher that does the following: 
#               1) We choose a key
#               2) We repeat the key until it is the same length as the plaintext (this is known as the keystream  
#               3) We then proceed character by character encrypting with e_i = (p_i + k_i) mod (26)

################### INPUT #########################################

# prompt user for file path
plaintext_file_name = sys.argv[1]  

#prompt user for file action mode 
mode = input("In what mode would you like to open the file r, w, a or rt?")

#opening and storing file 
f = open(plaintext_file_name, mode)
plaintext = f.read() 
# prompt user for key 
key = sys.argv[2]  

#store sizes of key and plaintext 
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
    #note that 
    #creates a file "ciphertext.txt" if the file doesn't already exist. If it does exist, 
    #clears the file contents 
    with open("ciphertext.txt", "w+", encoding = "utf-8") as ciphertext: 
        for i in range(plain_text_size): 
            ciphertext.write( chr( (ord(plaintext[i]) + ord(keystream[i])) % 255) )
            #ciphertext = ciphertext + (chr((ord(plaintext[i]) + ord(keystream[i])) % 255))
    
    #closing file     
    ciphertext.close()
    return ciphertext 

#decrypting file 
def decrypt(keystream, cipherfile): 

# note that now ciphertext is a file object. So, the argument "ciphertext" should actually be the name of the file contianing the ciphertext. 

    cipher_f = open(cipherfile.name, "rt", encoding="utf8")
    ciphertext = cipher_f.read()
    #ciphertext = cipher_f.read() 
    with open("recovered.txt", "w+", encoding = "utf-8") as recovered_text:
        for i in range(plain_text_size): 
            recovered_text.write(chr((ord(ciphertext[i]) - ord(keystream[i])) % 255))
            #recovered_text = recovered_text + (chr((ord(ciphertext[i]) - ord(keystream[i])) % 255))
    
    cipher_f.close()
    recovered_text.close() 
    return recovered_text 

######################### ANALYSIS ###########################################

# Here, we want to do some simply analysis to show how the Vigenere cipher works. We want to plot the character frequency of the plaintext file, then the character frequency of the ciphertext file. We can compare the frequency data in some interesting ways. Eventually, we might even be able to look at how various parameters of the key affect the character frequency data associated with the ciphertext. 

# We also have the text of each document stored as 
#   1) plaintext 
#   2) ciphertext
#   3) recovered 

#first we create an array of all the ascii characters we are using in the vigenere cipher 

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


def find_disjoint_matches(ciphertext): 
    #we'll start by including two traversers that simultaneously move through the 
    #ciphertext in order to compare each character to every other letter, sequentially
    #searching for repeated character groups     
    match_start_indices = []
    
    i = 0

    while i < len(ciphertext):
        traveler_1 = ciphertext[i]
        j = i+1 #we only want to start searching from i+1
        #print("i is: ", i) 
        match_1_start = i
        match_1_end = i
        match_2_start = i
        match_2_end = i
        
        while j < len(ciphertext):
            #begin by finding the next time in the ciphertext the same character repeats 
            traveler_2 = ciphertext[j] 
            #print("j is: ", j)
            if traveler_1 == traveler_2: 
                #the next appearance of the same character occurs at index j 
                #Now we want to find out how long repeated characters continue 
                match_2_start = j 
                #print("CHAR MATCH AT IND: ", match_1_start, "and ", match_2_start) 

                match_counter = 0 
                match = "" 
                while (j+match_counter) < len(ciphertext) and ciphertext[i + match_counter] == \
                        ciphertext[j + match_counter]:
                    #print("MATCH COUNTER: ", match_counter)
                    #print("i = ", i) 
                    #print("j = ", j) 
                    match += ciphertext[i + match_counter] 
                    match_counter += 1 
                
                #check if there is a repeated sequence 
                if match_counter > 1:
                    #print("MATCH SEQUENCE LEN: ", match_counter) 
                    #print("MATCH: ", match) 
                    #check if repeated sequences are disjoint 
                    if not disjoint(match_1_start, match_1_start + match_counter, \
                            match_2_start, match_2_start + match_counter):
                        #we just increment j until we find a disjoint matched sequence 
                        #print("MATCH NOT DISJOINT, KEEP GOING!") 
                        j += 1 
                    else: 
                        print("DISJOINT MATCH: ", match) 
                        match_1_end = match_1_start + match_counter #where sequence 1 ends 
                        match_2_end = match_2_start + match_counter #where sequence 2 ends
                    
                        #starts of both sequences are now consecutive items in the list 
                        match_start_indices.append(match_1_start) 
                        match_start_indices.append(match_2_start)
                        break 
                        #now we have the end indices of two disjoint sequences
                        #we want to break out of this while statement, then move 
                        #the i counter to match_1_end then look for the next 
                else: 
                    j+=1 
            else: 
            #if we don't have a match, we simply increment j 
                j += 1 
        #now we reset i 
        #print("MATCH 1 END: ", match_1_end)
        if match_1_end == i:
            i += 1
        else: 
            i = match_1_end 
        
    #END OF FINDING START INDICES OF DISJOINT REPEATED SEQUENCES 

    return match_start_indices 


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

    #print("Factor Frequencies: ", factor_counts) 
    #we now have a dictionary that stores all the factors of all the distances between 
    #repeated sequences and their frequencies. We want the factor with the max frequency. 
    counts = list(factor_counts.values()) 
    factors = list(factor_counts.keys()) 
    key_length_guess = factors[counts.index(max(counts))] 

    return key_length_guess 
 

def kasiski_exam(ciphertext): 
    match_indices = find_disjoint_matches(ciphertext) 
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

def normalize_frequency(count_dict):
    # TO DO: normalize -- we just want count/len(count_dict) for each character. This may or may not be useful, who knows ... 
    pass 

##################################################### TESTING ###############################################

############ ENCRYPTION PLAINTEXT, DECRYPTING CIPHERTEXT ################

keystream = create_key_stream(key) #creating keystream 
ciphertext_file = encrypt(keystream, plaintext) #encrypt createst ciphertext file obj
recovered_plaintext_file = decrypt(keystream, ciphertext_file) #decrypte creates recovered plaintext file obj

ciphertext = open(ciphertext_file.name, "rt", encoding = "utf8").read() 
recovered_plaintext = open(recovered_plaintext_file.name, "rt", encoding = "utf8").read() 

print("Plaintext: ", plaintext)
print("Encrypted File: ", ciphertext) 
print("Recovered Plaintext: ", recovered_plaintext)

if plaintext == recovered_plaintext: 
    print("Congratulations, decryption successful!")
else:
    print("Oh no! The decryption wasn't successful...") 


#################### CRYPTANALYSIS ###################

print("CRYPTANALYSIS") 

#guess key_length 
match_indices = find_disjoint_matches(ciphertext) 
key_length = guess_key_length(match_indices) 

#generate cipher segments 
cipher_segments = kasiski_exam(ciphertext) 

print("KEY LENGTH GUESS: ", key_length) 
if key_length == len(key):
    print("WE GUESSED CORRECT! KEY LENGTH IS: ", key_length)
else:
    print("INCORRCT KEY LENGTH") 

print(cipher_segments) 

#getting frequency count dictionary for plaintext
plaintext_counts = frequency_analysis(plaintext) 

plain_lists = sorted(plaintext_counts.items()) #sorted by key, return a list of tuples 
plain_char, plain_count = zip(*plain_lists) #unpack list of pairs into two tuples and store in char and count 

ciphertext_counts = frequency_analysis(ciphertext) 
cipher_lists = sorted(ciphertext_counts.items()) 
cipher_char, cipher_count = zip(*cipher_lists) 

plt.plot(plain_char, plain_count) 
plt.plot(cipher_char, cipher_count) 
plt.show() 

# Now we've done a basic frequency analysis! But, this won't really help us crack a Vigenere cipher until we are able to guess the correct length of the key. Now, we use Kasiski examination and the Friedman test in order to determine the key length of the Vigener cipher. This will, in fact, be quite interesting considering the classic Vigenere Cipher uses only a 26 letter alphabet. Here, sicne we are using ASCII, we have an alphabet that is roughly 10 times as large.








