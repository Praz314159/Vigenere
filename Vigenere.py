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

########################## METHODS ################################ 

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

############################ TESTING ####################################### 

keystream = create_key_stream(key) #creating keystream 
ciphertext_file = encrypt(keystream, plaintext) #encrypt createst ciphertext file obj
recovered_plaintext_file = decrypt(keystream, ciphertext_file) #decrypte creates recovered plaintext file obj

print("made it here") 

ciphertext = open(ciphertext_file.name, "rt", encoding = "utf8").read() 
recovered_plaintext = open(recovered_plaintext_file.name, "rt", encoding = "utf8").read() 

print("Plaintext: ", plaintext)
print("Encrypted File: ", ciphertext) 
print("Recovered Plaintext: ", recovered_plaintext)

if plaintext == recovered_plaintext: 
    print("Congratulations, decryption successful!")
else:
    print("Oh no! The decryption wasn't successful...") 
 
# We want to take a file, read it, encrypt it, store the encryption in a new file, then return that new file
# We want the same functionality for the decryption method. Instead of simply returning text, we want to be able to write the recovered text in a new file as we're recovering it, then return that new file. 
# To check whether or not the recovered file matches the original plaintext file, we can do a file comparison 

######################### ANALYSIS ###########################################

# Here, we want to do some simply analysis to show how the Vigenere cipher works. We want to plot the character frequency of the plaintext file, then the character frequency of the ciphertext file. We can compare the frequency data in some interesting ways. Eventually, we might even be able to look at how various parameters of the key affect the character frequency data associated with the ciphertext. 

#Note that now we have the following files: 
#   1) plaintext.txt
#   2) ciphertext.txt
#   3) recovered.txt 

# We also have the text of each document stored as 
#   1) plaintext 
#   2) ciphertext
#   3) recovered 

#first we create an array of all the ascii characters we are using in the vigenere cipher 

ASCII_char_array = []

for i in range(255):
    ASCII_char_array.append(chr(i))

#print(ASCII_char_array) 

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

# Now we've done a basic frequency analysis! But, this won't really help us crack a Vigenere cipher until we are able to guess the correct length of the key. Now, we use Kasiski examination and the Friedman test in order to determine the key length of the Vigener cipher. This will, in fact, be quite interesting considering the classic Vigenere Cipher uses only a 26 letter alphabet. Here, sicne we are using ASCII, we have an alphabet that is roughly 10 times as large. :x









