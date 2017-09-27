#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Module to check for validity of ETH address
# Using the web3.py library
# Based on tw_ether by thwin
# For hermes
# Written by xlanor
##
from web3 import Web3, HTTPProvider, IPCProvider

class web3check():
	def web3check(self,address):
		#initialises web3
		web3 = Web3(HTTPProvider('http://localhost:8545'))
		#uses the isAddress feature in web3 to check.
		check = web3.isAddress(address)
		if check is False:
			return False #if address does not exist
		else:
			return True #if address exists
			