This project will be known henceforth as Vigenere. The purpose of this project is to create a suite of cmd tools to deal fluently with Vigenere ciphers. 
This project has the following goals: 

SECURE COMMUNICATION: 

Assumed: key known and either plaintext known or ciphertext known (but not both) 

1) Be able to encrypt a file and send it to a particular ip address 
2) Be able to decrypt an incoming encrypted file

3) Varaint Beaufort functionality (reciprocal cipher) 
4) Running key variant functionality 
5) Multiple prime key functionality 
6) Autokey cipher functionality 

 
CRYPTANALYSIS: 

Assumed: key unknown, ciphertext known 

1) Given an encrypted file, first use Kasiski examination in order to determine the key length
2) Use Friedman test to approximate key length, then compare to actual key length (also use ciph	ciphertext/key matrix method)  
3) Once key length is determined, use frequency analysis to determine exact key 
4) Use found key to decrypt ciphertext and retrieve plaintext 
5) key elimination functionality 




