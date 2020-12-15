# -*- coding: utf-8 -*-
"""
basic elements of blockchain
"""

import hashlib as hasher
import datetime as date
class Block:
    def __init__(self, index,  data, previous_hash):
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

def create_genesis_block(data):
  # Manually construct a block with
  # index zero and arbitrary previous hash
    return Block(0,  data, "0")

def next_block(last_block,data):
      this_index = last_block.index + 1
      # this_timestamp = date.datetime.now()
      this_data = data
      this_hash = last_block.hash
      return Block(this_index,  this_data, this_hash)


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
        # if block[i].timestamp >block[i+1].timestamp:
        #     flag = False
        # if verbose:
            # print(f'Backdating at block {i}.')
    if flag==True:
        print('No modification')
    return flag


if __name__ == '__main__':  
    # Create the blockchain and add the genesis block
    blockchain = [create_genesis_block('original')]
    previous_block = blockchain[0]
    

    # after the genesis block
    num_of_blocks_to_add = 20
    
    # Add blocks to the chain
    for i in range(0, num_of_blocks_to_add):
      block_to_add = next_block(previous_block,data='block')
      blockchain.append(block_to_add,)
      previous_block = block_to_add
      # Tell everyone about it!
      print ('Block {0} has been added to the blockchain!'.format(block_to_add.index))
      print ("Hash: {0}\n".format(block_to_add.hash)) 
    
    #Modeify one part
    blockchain[5].data="Hey! I'm block 2.0"
    blockchain_new=blockchain
    verify(blockchain)
