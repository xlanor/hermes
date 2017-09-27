#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Module for cryptocompare API
# Based on tw_ether by thwin
# For hermes
# Written by xlanor
##
import json,logging,requests,sys,traceback,pymysql
from contextlib import closing
from currency_converter import CurrencyConverter
sys.path.append("/home/elanor/ftp/files/hermes")
from tokens import SQL
sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries = 20)
sess.mount('https://', adapter)

class Cryptocompare():
	def geturl(self,coin):
		url = "https://min-api.cryptocompare.com/data/price?fsym="+coin+"&tsyms=USD"
		coinurl = sess.get(url).json()
		coinli = []
		if "Response" in coinurl:
			coinli.append({"usd":"-"})
			coinli.append({"sgd":"-"})
			return coinli
		else:
			usdval = coinurl['USD']
			sgdval = self.convertusdsgd(usdval)
			get24h = self.get24h(coin)
			coinli.append({"usd":usdval})
			coinli.append({"sgd":sgdval})
			coinli = coinli + get24h
			print(get24h)
			print(coinli)
			return coinli

	def convertusdsgd(self,value):
		c = CurrencyConverter()
		sgdval = c.convert(float(value),'USD','SGD')
		return sgdval

	def get24h(self,fsymbol):
		hli = []
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					cur.execute("""SELECT ticker_id FROM cmc_ticker WHERE ticker_symbol = %s""",(fsymbol,))
					if cur.rowcount > 0:
						data = cur.fetchone()
						ticker_id = data[0]
						url = "https://api.coinmarketcap.com/v1/ticker/"+ticker_id+"/"
						cmcjson = sess.get(url).json()
						cmcurl = cmcjson[0]
						try:
							cmcurl['percent_change_1h']
							cmcurl['percent_change_24h']
							cmcurl['percent_change_7d']
						except:
							hli.append({"1h":'-'})
							hli.append({"24h":'-'})
							hli.append({"7d":'-'})
						else:
							hli.append({"1h":cmcurl['percent_change_1h']})
							hli.append({"24h":cmcurl['percent_change_24h']})
							hli.append({"7d":cmcurl['percent_change_7d']})
					else:
						print("cant find")
						hli.append({"1h":'-'})
						hli.append({"24h":'-'})
						hli.append({"7d":'-'})
			return hli
		except:	
			catcherror = traceback.format_exc()
			print(catcherror)
			hli.append({"1h":'-'})
			hli.append({"24h":'-'})
			hli.append({"7d":'-'})
			return hli

