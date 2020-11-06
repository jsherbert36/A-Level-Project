import json,lzma
def lzma_test():
    data = ["test1","test2"]
    f = lzma.open("test1.json","wb")
    f.write(data)
    f.close()

def json_caesar():
    f = open("test1.json","r")
    data = f.read()
    Keyword = "test_key"
    encrypt_data = encrypt(data,generateKey(data,Keyword))

def generateKey(string, key): 
    key = list(key) 
    if len(string) == len(key): 
        return(key) 
    else: 
        for i in range(len(string) - len(key)): 
            key.append(key[i % len(key)]) 
    return("" . join(key)) 

def encrypt(string, key): 
    cipher = [] 
    for i in range(len(string)): 
        if string[i].isalpha():
            x = ((ord(string[i]) + ord(key[i])) % 26)+ ord('A')
            cipher.append(chr(x))
        else:
            cipher.append(string[i]) 
    return("" . join(cipher)) 

def decrypt(cipher_text, key): 
    orig = [] 
    for i in range(len(cipher_text)): 
        if cipher_text[i].isalpha():
            x = ((ord(cipher_text[i])- ord(key[i]))%26)+ ord('A')         
            orig.append(chr(x))
        else: 
            orig.append(cipher_text[i])           
    return("" . join(orig)) 
      
json_caesar()