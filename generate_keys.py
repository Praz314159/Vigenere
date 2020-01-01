#We want to generate various keys of length 2-30 
#For each key length, we generate 5 random keys 
import random 



def gen_keys():
    
    #create new file to write all the keywords in 

    # generate keywords and write them into file 
    start = 0 
    stop = 255 
    for keylen in range(2,30): 
        #generate random key from ASCII characters --> range 0-255 
        #generate 5 keys 
        for keynum in range(5):
            key = "" 
            ASCII_ords = [random.randint(start, stop) for ch_ord in range(keylen)
            print(ASCII_ords) 
            
            #converte list of ASCII orders into chars 
            for ASCII in ASCII_ords: 
                key += chr(ASCII)








