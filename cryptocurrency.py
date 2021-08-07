import streamlit as st
from datetime import *
import hashlib
import json

class Blockchain:
	def __init__(self):
		self.blockchain=[]
		self.first_tx=[Transaction('Owner', 'Public', 100)]
		self.add_new_block(self.create_genesis_block())
		self.pending_txs=[]
		self.difficulty=2
		self.block_size=10
		self.miner_rewards=50

	def get_last_block(self):
		return self.blockchain[-1]

	def add_new_block(self, block):
		if len(self.blockchain)>0:
			block.prev_hash=self.get_last_block().hash
		else:
			block.prev_hash=None
		self.blockchain.append(block)

	def create_genesis_block(self):
		genesis_block=Block(self.first_tx, len(self.blockchain))
		return genesis_block

	def generate_keys():
		pass

	def is_blockchain_valid(self):
		for i in range(1, len(self.blockchain)):
			prev_block=self.blockchain[i-1]
			curr_block=self.blockchain[i]

			if curr_block.prev_hash!=prev_block.hash:
				print(f'Block:{curr_block} not part of the chain')
				return False
			if curr_block.hash!=curr_block.calculate_block_hash():
				print(f'Block:{curr_block} has been Tampered')
				return False
			if not curr_block.is_block_txs_valid():
				print(f'Transactions are invalid in Block:{curr_block}')
				return False

		return True

	def make_new_tx(self, sender, receiver, amount):
		if not sender or not receiver or not amount:
			print('Insufficient Transaction Information')
			return False

		new_tx=Transaction(sender, receiver, amount)

		if not new_tx.is_tx_valid():
			print('Transaction is not valid')
			return False

		self.pending_txs.append(new_tx)

		return True

	def mine_pending_txs(self, miner):
		size=len(self.pending_txs)
		for i in range(0, size, self.block_size):
			end=i+self.block_size

			if i>=size:
				end=size

			tx_slice=self.pending_txs[i:end]
			new_block=Block(tx_slice,len(self.blockchain))

			if new_block.is_block_txs_valid():
				new_block.mine_block(self.difficulty)
				self.add_new_block(new_block)
				miner_rewards=Transaction('Owner', miner, self.miner_rewards)
				self.pending_txs=[miner_rewards]
				return True
			return False
		return False

	def update_balance(self, node):
		balance=0
		for block in self.blockchain:
			for transaction in block.transactions:
				if transaction.sender==node:
					balance-=transaction.amount
				if transaction.receiver==node:
					balance+=transaction.amount
		return balance

class Block:
	def __init__(self, transactions, index):
		self.index=index
		self.time=datetime.now().strftime('%m/%d/%y, %H:%M:%S')
		self.transactions=transactions
		self.nonce=0
		self.prev_hash=None
		self.hash=self.calculate_block_hash()

	def calculate_block_hash(self):
		self.tx_string=[str(transaction) for transaction in self.transactions]
		hash_string=str(self.index)+self.time+''.join(self.tx_string)+str(self.prev_hash)+str(self.nonce)
		hash_encode=json.dumps(hash_string,sort_keys=True).encode()
		return hashlib.sha256(hash_encode).hexdigest()

	def is_block_txs_valid(self):
		for transaction in self.transactions:
			if transaction.is_tx_valid():
				continue
			return False
		return True

	def mine_block(self, difficulty):
		hash_puzzle=''.join(map(str, range(0,difficulty)))
		while self.hash[:difficulty]!=hash_puzzle:
			self.nonce+=1
			self.hash=self.calculate_block_hash()

			print(f'Block Nonce: {self.nonce}')
			print(f'Block Hash: {self.hash}')
			print(f'\n')
			

		st.write(f'Block Mined Successfully:')
		st.write(f'Block Nonce: {self.nonce}')
		st.write(f'Block Hash: {self.hash}')

		return True

class Transaction:
	def __init__(self, sender, receiver, amount):
		self.sender=sender
		self.receiver=receiver
		self.amount=amount
		self.time=datetime.now().strftime('%m/%d/%y, %H:%M:%S')
		self.hash=self.calculate_tx_hash()

	def calculate_tx_hash(self):
		hash_string=self.sender+self.receiver+str(self.amount)+self.time
		hash_encode=json.dumps(hash_string, sort_keys=True).encode()
		return hashlib.sha256(hash_encode).hexdigest()

	def sign_tx():
		pass

	def is_tx_valid(self):
		if self.hash!=self.calculate_tx_hash():
			print('Transaction Data Tampered')
			return False
		elif self.sender==self.receiver:
			print('Sender & Receiver cannot be the same')
			return False
		return True
