# -*- coding: utf-8 -*-
"""
Blockchain-based G-code protection
G-code encryption/decryption using RSA
Inversible Camouflage
Implement detection on unintended modification
Data scource: Dr. Tian
"""
import scipy.io
import numpy as np
import pandas as pd



# data = scipy.io.loadmat('C:/Users/zhshi/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/raw_data_case2.mat')
data = scipy.io.loadmat('D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/raw_data_case2.mat')

#C:\Users\zhshi\OneDrive - Oklahoma A and M System\Zhangyue\Code Library\Blockchain for in-situ data\Blockchain-for-in-situ-data
dat_print_1=data['dat_print_1'][:,0]

data=[]

window_number=460
window_size=int(np.shape(dat_print_1)[0]/window_number)
for i in range(window_number):
    a=list(dat_print_1[window_size*i:window_size*(i+1)])
    res = " ".join([str(i) for i in a])
    data.append(str(res))
    


# #data storage
# original_example = dat_print_1[0:window_size]
# import csv

# for i in range(10):
#     file = open('original data '+ str(i+1)+'.csv', 'w+', newline ='') 
#     original_example = dat_print_1[window_size*i:window_size*(i+1)]
#     # writing the data into the file 
#     with file:     
#         write = csv.writer(file) 
#         # write.writerows(camouflage_example)
#         write.writerows(map(lambda x: [x], original_example))

#%%  RSA_cryptography encryption

#Importing necessary modules
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


#Generating private key (RsaKey object) of key length of 1024 bits
private_key = RSA.generate(1024)
#Generating the public key (RsaKey object) from the private key
public_key = private_key.publickey()

#Converting the RsaKey objects to string 
private_pem = private_key.exportKey().decode()
public_pem = public_key.exportKey().decode()

#Writing down the private and public keys to 'pem' files
with open('private_pem.pem', 'w') as pr:
    pr.write(private_pem)
with open('public_pem.pem', 'w') as pu:
    pu.write(public_pem)
    

#Importing keys from files, converting it into the RsaKey object   
pr_key = RSA.importKey(open('private_pem.pem', 'r').read())
pu_key = RSA.importKey(open('public_pem.pem', 'r').read())

#Instantiating PKCS1_OAEP object with the public key for encryption
cipher = PKCS1_OAEP.new(key=pu_key)


data_encrypted=data
#%%
import datetime
start_time=datetime.datetime.now()

#Encrypting the message with the PKCS1_OAEP object
for i in range(len(data_encrypted)):
    temp=bytes(data[i], 'utf-8')
    a= cipher.encrypt(temp)
    data_encrypted[i]=a
# end_time=datetime.datetime.now()

# print("running time is")
# print(end_time-start_time)


#camouflage data
import matplotlib.pyplot as plt

import math
import binascii

def convertToNumber (s):
    return int.from_bytes(s.encode(), 'little')

def convertFromNumber (n):
    return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()

# start_time=datetime.datetime.now()
# data_mask=binascii.b2a_base64(data_encrypted)
data_mask=pd.DataFrame(data_encrypted)
data_mask=data_mask.applymap(binascii.b2a_base64)
data_mask=data_mask.rename(columns={0:'x'})
# data_mask=data_encrypted.applymap(binascii.b2a_hex)
for i in range(data_mask.shape[0]):
    # data_mask=data_mask.applymap(str)
    data_mask.at[i,'x']=data_mask.at[i,'x'].decode('utf-8')
    # data_mask.at[i,'x']=int(data_mask.at[i,'x'],16)
    data_mask.at[i,'x']=convertToNumber(data_mask.at[i,'x'])


data_camouflage=[]
for i in range(len(data_mask)):
    data_camouflage.append(list(str(data_mask['x'][i])))

end_time=datetime.datetime.now()
print("\nrunning time is")
print(end_time-start_time)

# Output Camouflage Example 

a=str(data_mask['x'][0])
camouflage_size=8
camouflage_number=len(a)/camouflage_size
camouflage_example=[]

for i in range(int(camouflage_number)):
    camouflage_example.append(a[i*camouflage_size:(i+1)*camouflage_size])


camouflage_example = ["0."+i for i in camouflage_example]


camouflage_example_revover=[i[2:] for i in camouflage_example]

camouflage_example = [float(i) for i in camouflage_example]


import csv

  
# opening the csv file in 'w+' mode 
file = open('camouflage data 1.csv', 'w+', newline ='') 
  
# writing the data into the file 
with file:     
    write = csv.writer(file) 
    # write.writerows(camouflage_example)
    write.writerows(map(lambda x: [x], camouflage_example))
    
a=str(data_mask['x'][1])
camouflage_size=8
camouflage_number=len(a)/camouflage_size
camouflage_example=[]

for i in range(int(camouflage_number)):
    camouflage_example.append(a[i*camouflage_size:(i+1)*camouflage_size])


camouflage_example = ["0."+i for i in camouflage_example]


camouflage_example_revover=[i[2:] for i in camouflage_example]

camouflage_example = [float(i) for i in camouflage_example]

 

file = open('camouflage data 2.csv', 'w+', newline ='') 
  
# writing the data into the file 
with file:     
    write = csv.writer(file) 
    # write.writerows(camouflage_example)
    write.writerows(map(lambda x: [x], camouflage_example))
    
#%% Store in blockchain

import hashlib as hasher
import tiny_blockchain as block

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        # self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
    
    def hash_block(self):
        key = hasher.sha256()
        key.update(str(self.index).encode('utf-8'))
        # key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()



def verify(block, verbose=True): 
    flag = True
    for i in range(0,len(block)-1):
        if block[i].index != i:
            flag = False
            if verbose:
                print(f'!!!Wrong block index at block {i}!!!')
        if block[i].hash != block[i+1].previous_hash:
            flag = False
            if verbose:
                print(f'!!!Wrong previous hash at block {i+1}!!!')
        if block[i].hash != block[i].hash_block():
            flag = False
            if verbose:
                print(f'!!!Wrong hash at block {i}!!!')
        if block[i].timestamp >block[i+1].timestamp:
            flag = False
        if verbose:
            print(f'Backdating at block {i}.')
    return flag

   
# Create the blockchain and add the genesis block
Hash_ori=[]

blockchain = [block.create_genesis_block(data_camouflage[0])]
previous_block = blockchain[0]
Hash_ori.append(blockchain[0].hash)

# after the genesis block
num_of_blocks_to_add = data_mask.shape[0]-1

# Add blocks to the blockchain
for i in range(0, num_of_blocks_to_add):
      block_to_add = block.next_block(previous_block,data_camouflage[i+1])
      blockchain.append(block_to_add)
      previous_block = block_to_add
      Hash_ori.append(block_to_add.hash)

#%% Unintended modification detect
Hash_current=[]
start_time=datetime.datetime.now()
for i in range(len(blockchain)):
    blockchain[i].hash=blockchain[i].hash_block()
    Hash_current.append(blockchain[i].hash)

#Dimension comparison
if len(Hash_ori)!=len(blockchain):
    print('Unintended delete/add occurs!')
#Benchmark comparison
else:
    flag=0
    for i in range(len(Hash_ori)):
        if Hash_ori[i]==blockchain[i].hash:
            continue
        else:
            flag=1
            print("Unintended modification occurs at layer ", i+1)
    if flag==0:
        print("No unintended modification occurs\n")
        
end_time=datetime.datetime.now()       
print("\nrunning time is")
print(end_time-start_time)

#%%

blockchain[6].hash = "23afd97b8086f51fc696de6f874c0de2c7c13b6d576b2bfe337915c0977381bb"

#%% Chain detection
start_time=datetime.datetime.now()
block.verify(blockchain)
end_time=datetime.datetime.now()       
print("\nrunning time is ")
print(end_time-start_time)
#%% RSA_cryptography Decryption
data_decrypted=[]
start_time=datetime.datetime.now()
decrypt = PKCS1_OAEP.new(key=pr_key)


#Decrypting the message with the PKCS1_OAEP object
for i in range(len(blockchain)):
    # temp=[]
    temp=blockchain[i].data
    temp[0:len(temp)]=[''.join(temp[0:len(temp)])]
    temp=convertFromNumber(int(temp[0]))
    temp=temp.encode('utf-8')
    temp=binascii.a2b_base64(temp)
    decrypted_message = decrypt.decrypt(temp)
    decrypted_message=decrypted_message.decode("utf-8")
    # temp.append(decrypted_message)
    data_decrypted.append(decrypted_message)
end_time=datetime.datetime.now()       
print("\n running time is ")
print(end_time-start_time)

data_decrypted=pd.DataFrame(data_decrypted,columns=list('x'))
data_decrypted=list(data_decrypted['x'])

