#We want to generate various keys of length 2-30 
#For each key length, we generate 5 random keys 
import random 

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



