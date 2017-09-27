#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Module for ethplorer API
# Based on tw_ether by thwin
# For hermes
# Written by xlanor
##
import json
import logging
import requests
import sys
import pymysql
from web3 import Web3, HTTPProvider, IPCProvider
from contextlib import closing
sys.path.append("/home/elanor/ftp/files/modules")
from modules.cryptocompare import Cryptocompare
sys.path.append("/home/elanor/ftp/files/hermes")
from tokens import SQL

class Ethplorer():
	def scanaddress(self,address):
		url = "https://api.ethplorer.io/getAddressInfo/"+address+"?apiKey=freekey"
		walleturl = requests.get(url).json()
		print(walleturl)
		if "error" in walleturl:
			return "boo"
		else: 
			walletdetails = {}
			web3 = Web3(HTTPProvider('http://localhost:8545'))
			ethbalance = walleturl["ETH"]["balance"]
			walletdetails["ETH"] = [{"balance":ethbalance}]
			ethval = Cryptocompare().geturl("ETH")
			walletdetails["ETH"].append({"name":"Ethereum"})
			for each in ethval:
				if "sgd" in each:
					walletdetails["ETH"].append({"sgd":each['sgd']})
				elif "usd" in each:
					walletdetails["ETH"].append({"usd":each['usd']})
			for token in walleturl['tokens']:
				symbol = token['tokenInfo']['symbol']
				print('\n'+symbol)
				fiatval = Cryptocompare().geturl(symbol)
				balance = token['balance']
				convertedbalance = web3.fromWei(balance,'ether')
				name = token['tokenInfo']['name']
				walletdetails[symbol] = [{"balance":convertedbalance}]
				walletdetails[symbol].append({"name":name})
				for each in fiatval:
					if "sgd" in each:
						walletdetails[symbol].append({"sgd":each['sgd']})
					elif "usd" in each:
						walletdetails[symbol].append({"usd":each['usd']})
			print(walletdetails)
			return walletdetails
		


