import json,lzma
def lzma_test():
    data = ["test1","test2"]
    f = lzma.open("test1.json","wb")
    f.write(data)
    f.close()

def json_encrypt(user_list,key):
    json_data = json.dumps(user_list)
    f = open("test1.txt","w")
    encrypt_data = encrypt(json_data,generateKey(json_data,key))
    f.write(encrypt_data)
    f.close()

def json_decrypt(key):
    f = open("test1.txt","r")
    json_data = f.read()
    json_data = decrypt(json_data,generateKey(json_data,key))
    f.close()
    json_data = json.loads(json_data)
    return json_data

def generateKey(String, key): 
    key = list(key) 
    if len(String) == len(key): 
        return(key) 
    elif len(key) < len(String): 
        for i in range(len(String) - len(key)): 
            key.append(key[i % len(key)]) 
    else:
        key = key[:len(String)]
    return("" . join(key)) 

def encrypt(string, key): 
    cipher = [] 
    for i in range(len(string)): 
        if string[i].isalpha():
            x = ((ord(string[i]) + ord(key[i])) % 26) + ord('A')
            cipher.append(chr(x))
        else:
            cipher.append(string[i]) 
    return("" . join(cipher)) 

def decrypt(cipher_text, key): 
    orig = [] 
    for i in range(len(cipher_text)): 
        if cipher_text[i].isalpha():
            x = ((ord(cipher_text[i]) - ord(key[i])) % 26) + ord('A')       
            orig.append(chr(x))
        else: 
            orig.append(cipher_text[i])           
    return("" . join(orig)) 
      
A = [1,2,3,4,5]
json_encrypt(A,"hello")
key = generateKey("thisisatest","hello")
print(key)
X = encrypt("thisisatest",key)
print(X)
print(decrypt(X,key))