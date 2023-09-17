# Pocket-AES
I have written three CLI programs:
# 1. Working of pocketAES
 I have written a program that demonstrates the working of individual PocketAES encryption stages
shown in figure 1. Prompt the user for text block and key inputs, in the form of 16-bit
hexadecimal numbers. Compute and show the outputs of applying SubNibbles, ShiftRow,
MixColumns and GenerareRoundKeys on those two. 
![Uploading Screenshot 2023-09-17 144044.png…]()


# 2.Implemented one block decryption scheme 
 I have written a program for decrypting one block of ciphertext according to PocketAES algorithm of Section A. Receive the ciphertext and key as hex inputs from user. Decrypted block should be outputted in the same hex format.
# 3. Implemented the ASCII text decryption 
 I have written a program that
reads encrypted text from a file ‘secret.txt’, decrypts it and creates an output file ‘output.txt’.
Key should be obtained from user input. Input will contain a series of ciphertext blocks in
hex. Output data should be in ASCII text. I took care of the null
padding that may be present in ciphertext.
# 4. Analyzed the encryption scheme discussed in Section B. 
It has some security flaws:
Yes it has flaws 
 The key is same throughout the process and thus it is vulnerable to attacks
 The key is not large enough to be secure
 The key is not random
 The key is not authenticated
 The text is also not authenticated and third party can easily esdrop on the communication 
 and can change the text and send it from his side
