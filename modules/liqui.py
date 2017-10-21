#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Module for liqui API
# Based on tw_ether by thwin
# For hermes
# Written by xlanor
##
import json,logging,requests
from currency_converter import CurrencyConverter
import sys
sys.path.append("/home/elanor/ftp/files/modules")
from modules.cryptocompare import Cryptocompare

sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries = 20)
sess.mount('https://', adapter)

class Liqui():
	def knceth(self):
		knc = sess.get("https://api.liqui.io/api/3/ticker/knc_eth").json()
		knc_buy_price = knc["knc_eth"]["buy"]
		knc_sell_price = knc["knc_eth"]["sell"]
		ethval = Cryptocompare().geturl('ETH')
		for each in ethval:
			if "sgd" in each:
				ethsgd = each['sgd']
			elif "usd" in each:
				ethusd = each['usd']
		#Liqui does not support eth -> SGD/USD.
		#We're going to use cryptocompare's rate to calculate.
		#We're using the sell price for this calculation.
		kncbuysgd = float(knc_buy_price) * float(ethsgd)
		kncbuyusd = float(knc_buy_price) * float(ethusd)
		kncsellsgd = float(knc_sell_price) * float(ethsgd)
		kncsellusd = float(knc_sell_price) * float(ethusd)
		kncli = []
		kncli.append({"kncbuy":knc_buy_price})
		kncli.append({"kncsell":knc_sell_price})
		kncli.append({"kncbuysgd":kncbuysgd})
		kncli.append({"kncsellsgd":kncsellsgd})
		kncli.append({"kncbuyusd":kncbuyusd})
		kncli.append({"kncsellusd":kncsellusd})
		return kncli

	
