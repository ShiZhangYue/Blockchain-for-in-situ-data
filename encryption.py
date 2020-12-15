# -*- coding: utf-8 -*-
"""
Blockchain-based G-code protection 
G-code encryption/decryption using RSA
Implement detection on unintended modification
"""

#%%import G-code
import pandas as pd
data = pd.read_csv("D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/simulation.csv")
data=data.round(decimals=2)
data=data.applymap(str)
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
for i in range(data_encrypted.shape[0]):

    temp=bytes(data_encrypted['x'][i], 'utf-8')
    data_encrypted.at[i,'x'] = cipher.encrypt(temp)
end_time=datetime.datetime.now()

print("running time is \n")
print(end_time-start_time)
#%%
data = pd.read_csv("D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/simulation.csv")
data=data.round(decimals=2)
data=data.applymap(str)
#%% Store encrypted G-code into blockchain

import hashlib as hasher
import tiny_blockchain as block

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
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

blockchain = [block.create_genesis_block(data=data_encrypted['x'][0])]
previous_block = blockchain[0]
Hash_ori.append(blockchain[0].hash)

# after the genesis block
num_of_blocks_to_add = data_encrypted.shape[0]-1

# Add blocks to the blockchain
for i in range(0, num_of_blocks_to_add):
      block_to_add = block.next_block(previous_block,data_encrypted['x'][i+1])
      blockchain.append(block_to_add)
      previous_block = block_to_add
      Hash_ori.append(block_to_add.hash)


#%% RSA_cryptography Decryption
data_decrypted=[]
start_time=datetime.datetime.now()
decrypt = PKCS1_OAEP.new(key=pr_key)

#Decrypting the message with the PKCS1_OAEP object
for i in range(len(blockchain)):
    # temp=[]

    decrypted_message = decrypt.decrypt(blockchain[i].data)
    decrypted_message=decrypted_message.decode("utf-8")
    # temp.append(decrypted_message)
    data_decrypted.append(decrypted_message)
end_time=datetime.datetime.now()       
print("\n running time is ")
print(end_time-start_time)

data_decrypted=pd.DataFrame(data_decrypted,columns=list('x'))
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
        print("No unintended modification occurs")
        
end_time=datetime.datetime.now()       
print("running time is")
print(end_time-start_time)

#%% Chain detection
start_time=datetime.datetime.now()
block.verify(blockchain)
end_time=datetime.datetime.now()       
print("\n running time is ")
print(end_time-start_time)
