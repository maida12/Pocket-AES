import binascii
import csv

scale = 16 ## equals to hexadecimal
subnibbles={
    '0000': '1010',
    '0001': '0000',
    '0010': '1001',
    '0011':'1110',
    '0100': '0110',
    '0101': '0011',
    '0110':'1111',
    '0111': '0101',
    '1000': '0001',
    '1001': '1101',
    '1010': '1100',
    '1011': '0111',
    '1100': '1011',
    '1101': '0100',
    '1110': '0010',
    '1111': '1000'
}
subnibbles_reverse = {v: k for k, v in subnibbles.items()}
#XOR is taken on 2 binary str values
def binary_xor(str1, str2):
    # Ensure that both strings have the same length
    if len(str1) != len(str2):
        raise ValueError("Input strings must have the same length")

    # Convert each character to its integer representation and perform XOR
    xor_result = [str(int(char1) ^ int(char2)) for char1, char2 in zip(str1, str2)]

    # Join the result list into a binary string
    xor_result_str = ''.join(xor_result)

    return xor_result_str

def hex_xor(str1, str2):
    print(str1) 
    print(str2)
    int1 = int(str1, 16)
    int2 = int(str2, 16)
    print(int1)
    print(int2)

    # Perform XOR operation
    result = int1 ^ int2
    print(result)

    # Convert the result integer to a hexadecimal string with proper padding
    result_hex = f"{result:0{len(str1)}X}"

    return result_hex


# take list of nibbles  in binary and return list of nibbles having exchanged rows
def Subnibbles(nibbles):
    subnibbles={
    '0000': '1010',
    '0001': '0000',
    '0010': '1001',
    '0011':'1110',
    '0100': '0110',
    '0101': '0011',
    '0110':'1111',
    '0111': '0101',
    '1000': '0001',
    '1001': '1101',
    '1010': '1100',
    '1011': '0111',
    '1100': '1011',
    '1101': '0100',
    '1110': '0010',
    '1111': '1000'
}
    for i in range(len(nibbles)):
        if(nibbles[i] in subnibbles):
            nibbles[i]=subnibbles[nibbles[i]]
     
    return nibbles   #[1101 1010 1110 0111]

# ==============================================================================
def shiftRows(text):
    newText=''
    for i in range(4):
        if(i==0):
            newText=newText+text[2]
        elif(i==2):
            newText=newText+text[0]
        else:
            newText=newText+text[i]
   
    return newText

# ==============================================================================
def finite_field_multiplication(a, b):
    m = 0
    while b > 0:
        if b & 1:  # Check if the least significant bit of b is 1
            m ^= a  # XOR operation to add a to m
        a <<= 1  # Left shift a by 1 bit
        if a & 0b10000:  # Check if the fourth bit of a is set
            a ^= 0b10011  # XOR with irreducible polynomial x^4 + x + 1
        b >>= 1  # Right shift b by 1 bit
    return m
def finite_field_matrix_multiplication(matrix1, matrix2):
    
    result = [[0, 0], [0, 0]]  # Initialize a 2x2 result matrix with zeros
    for i in range(2):  # Iterate over rows of the first matrix
        for j in range(2):  # Iterate over columns of the second matrix
            for k in range(2):  # Iterate over elements in the row/column
                result[i][j] ^= finite_field_multiplication(matrix1[j][k], matrix2[i][k])

    return result


# =============================================================================
# get master key in binary str and generate 2 subkeys
def generateKey(master_key):
    # Define round constants
    Rcon1 = '1110'
    Rcon2 = '1010'

    # Extract the nibbles from the master key
    w0, w1, w2, w3  = [master_key[i:i+4] for i in range(0, len(master_key), 4)] #w0=0000 w1=0010 w2=1100 w3=1100


    subnibbles={
    '0000': '1010',
    '0001': '0000',
    '0010': '1001',
    '0011':'1110',
    '0100': '0110',
    '0101': '0011',
    '0110':'1111',
    '0111': '0101',
    '1000': '0001',
    '1001': '1101',
    '1010': '1100',
    '1011': '0111',
    '1100': '1011',
    '1101': '0100',
    '1110': '0010',
    '1111': '1000'
}
    # Calculate w4, w5, w6, and w7

    w4=binary_xor(w0,subnibbles[w3])
    w4=binary_xor(w4,Rcon1)     #w4=0101
    w5=binary_xor(w1,w4)        #w5=0111
    w6=binary_xor(w2,w5)
    w7=binary_xor(w3,w6)
    

    # Calculate w8, w9, w10, and w11
    w8=binary_xor(w4,subnibbles[w7])
    w8=binary_xor(w8,Rcon2)
    w9=binary_xor(w5,w8)
    w10=binary_xor(w6,w9)
    w11=binary_xor(w7,w10)

    K1 = w4 + w5 + w6 + w7
# Convert the combined binary string to a hexadecimal string
    K1 = hex(int(K1, 2))[2:]
     
    K2 = w8 + w9 + w10 + w11

# Convert the combined binary string to a hexadecimal string
    K2 = hex(int(K2, 2))[2:]

    print(K1)  # Output: "57b7"
    print(K2)  # Output: "ad61"

    return K1,K2

def AddRoundKey(text2bin,master_key):
    w0, w1, w2, w3  = [master_key[i:i+4] for i in range(0, len(master_key), 4)] #w0=0000 w1=0010 w2=1100 w3=1100
    w4,w5,w6,w7=[text2bin[i:i+4] for i in range(0, len(text2bin), 4)]
    w0=binary_xor(w0,w4)
    w1=binary_xor(w1,w5)
    w2=binary_xor(w2,w6)
    w3=binary_xor(w3,w7)
    k1=w0+w1+w2+w3
    k1 = hex(int(k1, 2))[2:]
    return k1

def reverse_substitute_nibbles(nibbles):
    for i in range(len(nibbles)):
        if nibbles[i] in subnibbles_reverse:
            nibbles[i] = subnibbles_reverse[nibbles[i]]
def paddingHex(text):
    if(len(text)<4):
     # Calculate the number of '0' characters to add
        num_zeros_to_add = 4 - len(text)
        text = '0' * num_zeros_to_add + text
    return text

# =============================================================================



# main
# text=input("Enter a text: ")
# if(len(text)<4):
#      # Calculate the number of '0' characters to add
#     num_zeros_to_add = 4 - len(text)
#     text = '0' * num_zeros_to_add + text
# # convert hex into binary
# res=bin(int(text, scale))[2:].zfill(16)

# # Remove the '0b' prefix if it exists
# if res.startswith("0b"):
#     res = res[2:]

# # Split the binary string into 4-bit nibbles
# nibbles = [res[i:i+4] for i in range(0, len(res), 4)]       #1001 0000 0011 1011
# chunk=4
# matrix = [[int(chunk,2 ) for chunk in nibbles[:2]],         #9 0 3 b
#           [int(chunk, 2) for chunk in nibbles[2:]]]


# Subnibbles(nibbles)
# # convert list of nibbles into hex
# h=''
# for i in range(4):
#    he=(hex(int(nibbles[i], 2)))
#    if(he.startswith("0x")):
#        he=he[2:]
#    h=h+he
# print("After subnibbles()",h)

# text=shiftRows(text)
# print("After ShiftRows()" ,text)
# matrix1 = [[1, 4], [4, 1]]
# result=finite_field_matrix_multiplication(matrix1,matrix)
# flattened_list = [str(item) for sublist in result for item in sublist]
# # Join the elements into a single string
# result_string = ''.join(flattened_list)
# print("After MixColumns",result_string)



# key=input("Enter a key: ")
# # if key is less than 4 bytes, pad it with 0
# if(len(key)<4):
#      # Calculate the number of '0' characters to add
#     num_zeros_to_add = 4 - len(key)
#     key = '0' * num_zeros_to_add + key


# master_key = bin(int(key, 16))[2:].zfill(16)
# print("master key",master_key)
# # Remove the '0b' prefix if it exists
# if master_key.startswith("0b"):
#     master_key = master_key[2:]


# k1,k2=generateKey(master_key)
# print("k1",k1)
# print("k2",k2)

#================================================

# text2=input("Enter a text: ")
# if(len(text2)<4):
#      # Calculate the number of '0' characters to add
#     num_zeros_to_add = 4 - len(text2)
#     text2 = '0' * num_zeros_to_add + text2
# key1=input("Enter a key: ")
# # if key is less than 4 bytes, pad it with 0
# if(len(key1)<4):
#      # Calculate the number of '0' characters to add
#     num_zeros_to_add = 4 - len(key1)
#     key1 = '0' * num_zeros_to_add + key1

# master_key = bin(int(key1, 16))[2:].zfill(16)
# K1,K2=generateKey(master_key)

# K2=bin(int(K2, scale))[2:].zfill(16)

# text2=shiftRows(text2)
# print("After ShiftRows()" ,text2)
# text2bin=bin(int(text2, scale))[2:].zfill(16)

# round1=AddRoundKey(text2bin,K2)
# print("After key round1",round1)


# res2=bin(int(round1, scale))[2:].zfill(16)
# if res2.startswith("0b"):
#     res2 = res2[2:]

# # Split the binary string into 4-bit nibbles
# nibbles2 = [res2[i:i+4] for i in range(0, len(res2), 4)]       #1001 0000 0011 1011
# reverse_substitute_nibbles(nibbles2)
# # convert list of nibbles into hex
# h=''
# for i in range(4):
#    he=(hex(int(nibbles2[i], 2)))
#    if(he.startswith("0x")):
#        he=he[2:]
#    h=h+he
# print("After subnibbles()",h)


# h=shiftRows(h)
# print("After ShiftRows()" ,h)


# matrix = [[int(h[0],16 ),int(h[1],16)],         #9 0 3 b
#           [int(h[2], 16),int(h[3],16) ]]
# matrix1 = [[9, 2], [2, 9]]
# result=finite_field_matrix_multiplication(matrix1,matrix)
# result=[[format(cell, 'x') for cell in row] for row in result]
# flattened_list = [str(item) for sublist in result for item in sublist]
# # Join the elements into a single string
# result_string = ''.join(flattened_list)
# print("After MixColumns",result_string)

# result_stringBin=bin(int(result_string, scale))[2:].zfill(16)
# K1=bin(int(K1, scale))[2:].zfill(16)
# round2=AddRoundKey(result_stringBin,K1)
# print("After key round2",round2)

# round2=bin(int(round2, scale))[2:].zfill(16)
# if round2.startswith("0b"):
#     round2 = round2[2:]

# # Split the binary string into 4-bit nibbles
# nibbles2 = [round2[i:i+4] for i in range(0, len(round2), 4)]       #1001 0000 0011 1011
# reverse_substitute_nibbles(nibbles2)
# # convert list of nibbles into hex
# h=''
# for i in range(4):
#    he=(hex(int(nibbles2[i], 2)))
#    if(he.startswith("0x")):
#        he=he[2:]
#    h=h+he
# print("After subnibbles()",h)
# print("Plain Text iss",h)

#====================================================================================

key1=input("Enter a key: ")
paddingHex(key1)
with open('secret.txt', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Split the line into words using spaces as the delimiter
        words = line.split()
        
        # Process each word
        for word in words:
            print(word)
            paddingHex(word)
            text2=shiftRows(word)
            
            master_key = bin(int(key1, 16))[2:].zfill(16)
            K1,K2=generateKey(master_key)
            K2=bin(int(K2, scale))[2:].zfill(16)
            text2bin=bin(int(text2, scale))[2:].zfill(16)

            round1=AddRoundKey(text2bin,K2)
            

            res2=bin(int(round1, scale))[2:].zfill(16)
            if res2.startswith("0b"):
                res2 = res2[2:]

            # Split the binary string into 4-bit nibbles
            nibbles2 = [res2[i:i+4] for i in range(0, len(res2), 4)]       #1001 0000 0011 1011
            reverse_substitute_nibbles(nibbles2)
            # convert list of nibbles into hex
            h=''
            for i in range(4):
                he=(hex(int(nibbles2[i], 2)))
                if(he.startswith("0x")):
                    he=he[2:]
                h=h+he
            
            h=shiftRows(h)
            
            matrix = [[int(h[0],16 ),int(h[1],16)],         #9 0 3 b
                    [int(h[2], 16),int(h[3],16) ]]
            matrix1 = [[9, 2], [2, 9]]
            result=finite_field_matrix_multiplication(matrix1,matrix)
            result=[[format(cell, 'x') for cell in row] for row in result]
            flattened_list = [str(item) for sublist in result for item in sublist]
            # Join the elements into a single string
            result_string = ''.join(flattened_list)
            
            result_stringBin=bin(int(result_string, scale))[2:].zfill(16)
            K1=bin(int(K1, scale))[2:].zfill(16)
            round2=AddRoundKey(result_stringBin,K1)
            

            round2=bin(int(round2, scale))[2:].zfill(16)
            if round2.startswith("0b"):
                round2 = round2[2:]

            # Split the binary string into 4-bit nibbles
            nibbles2 = [round2[i:i+4] for i in range(0, len(round2), 4)]       #1001 0000 0011 1011
            reverse_substitute_nibbles(nibbles2)
            # convert list of nibbles into hex
            h=''
            for i in range(4):
                he=(hex(int(nibbles2[i], 2)))
                if(he.startswith("0x")):
                    he=he[2:]
                h=h+he
           
            if(h.endswith("00")):
                h=h[:-2]
            print("Plain Text iss",h)

            hex_bytes = binascii.unhexlify(h)
            # Convert bytes to ASCII string
            ascii_string = hex_bytes.decode('utf-8')
            print(ascii_string)
            f = open("output.txt", "a")
            f.write(ascii_string)
            f.close()














    


