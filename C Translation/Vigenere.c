

char* create_key_stream(char* key, char* plaintext)
{
	char *keystream = (char *)malloc(sizeof(char)*sizeof(plaintext)); 
}



/*
def create_key_stream(key, plaintext):

    keystream = ""
    key_size = len(key)
    plain_text_size = len(plaintext)
 
    if key_size > plain_text_size:
        print("You're using a One-Time Pad!") 
        for i in range(plain_text_size): 
            keystream = keystream + key[i]
    elif key_size < plain_text_size: 
        for i in range(plain_text_size): 
            keystream = keystream + key[i % key_size] 
    else: 
        keystream = key
        print("You're using a One-Time Pad!") 

    return keystream 


#encrypting file: takes a plaintext file and returns both ciphertext string literal
# and ciphertext file 
def encrypt(key, plaintext_file_name):
    plaintext_file = open(plaintext_file_name, "rt", encoding = "utf-8")
    plaintext = plaintext_file.read()
    plain_text_size = len(plaintext)
    
    keystream = create_key_stream(key, plaintext)

    with open("ciphertext.txt", "w+", encoding = "utf-8") as ciphertext_file: 
        for i in range(plain_text_size):
            ciphertext_file.write(chr((ord(plaintext[i]) + ord(keystream[i])) % 255))
       
        ciphertext = ciphertext_file.read() 
      
    ciphertext_file.close()
    plaintext_file.close() 
    return ciphertext, ciphertext_file  
*/


