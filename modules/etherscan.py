#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Module for Etherscan API
# Based on tw_ether by thwin
# For hermes
# Written by xlanor
##
from web3 import Web3, HTTPProvider, IPCProvider
import json
import logging
import requests
import sys
import pymysql
from contextlib import closing
sys.path.append("/home/elanor/ftp/files/hermes")
from tokens import apikey,SQL

class etherscan():
	def ethbal(user_id):
		with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					cur.execute("""SELECT mew_address FROM mew WHERE telegram_id = %s""",(user_id,))
					if cur.rowcount > 0:
						data = cur.fetchone()
						mew_address = data[0]
					api_key = apikey.apikey("etherscan")
					details = []
					url = "https://api.etherscan.io/api?module=account&action=balance&address="+mew_address+"&tag=latest&apikey="+api_key
					ethscan = requests.get(url).json()
					result = ethscan['result']
					web3 = Web3(HTTPProvider('http://localhost:8545'))
					convertedeth = web3.fromWei(float(result),'ether')
					details.append({"convertedeth":convertedeth})
					kyberurl = "https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xdd974D5C2e2928deA5F71b9825b8b646686BD200&address="
					kyberurl += mew_address
					kyberurl += "&tag=latest&apikey="
					kyberurl += api_key
					kyberscan = requests.get(kyberurl).json()
					kyberresult = kyberscan['result']
					convertedkyber = web3.fromWei(float(kyberresult),'ether')
					details.append({"convertedkyber":convertedkyber})
					return details




		

