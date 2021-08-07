from streamlit import cli as stcli
from cryptocurrency import *
import streamlit as st
import sys

def register():
	pass

def login():
	pass

def make_transaction(sender, receiver, amount):
	return chain.make_new_tx(sender, receiver, amount)

def get_pending_txs():
	return chain.pending_txs

def mine_pending_txs(miner):
	return chain.mine_pending_txs(miner)

def get_balance(node):
	return chain.update_balance(node)

def menu(page):
	make_transaction('Remston', 'Renvil', 150)
	make_transaction('Renvil', 'Vilma', 100)
	make_transaction('Vilma', 'Ronald', 10)
	if page=='Make Transaction':
		print('Transaction Successful')

	if page== 'Get Pending Transactions':
		st.write(get_pending_txs())

	if page=='Mine Pending Transactions':
		miner=st.text_input('Miner')
		mine_pending_txs(miner)

	if page=='Get Balance':
		miner=st.text_input('Miner')
		mine_pending_txs(miner)

		node=st.text_input('Node')
		st.write(get_balance(node))

if __name__ == '__main__':
    if st._is_running_with_streamlit:
    	chain=Blockchain()

    	page=st.selectbox('Blockchain', ['Make Transaction', 'Get Pending Transactions', 'Mine Pending Transactions', 'Get Balance'])
    	menu(page)

    else:
        sys.argv=["streamlit","run","main.py"]
        sys.exit(stcli.main())




# print(chain.pending_txs)
# chain.mine_pending_txs('Remston')
# print(chain.blockchain)
# print(chain.update_balance('Renvil'))
# chain.mine_pending_txs('Renvil')
# print(chain.update_balance('Renvil'))
