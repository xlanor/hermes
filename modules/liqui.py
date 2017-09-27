#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Module for liqui API
# Based on tw_ether by thwin
# For hermes
# Written by xlanor
##
import json
import logging
import requests
from currency_converter import CurrencyConverter

class Liqui():
	def knceth(self):
		knc = requests.get("https://api.liqui.io/api/3/ticker/knc_eth").json()
		knc_buy_price = knc["knc_eth"]["buy"]
		knc_sell_price = knc["knc_eth"]["sell"]
		ethersgd = self.ethsgd()
		etherusd = self.ethusd()
		for each in ethersgd:
			if "esellsgd" in each:
				ethsgd = each['esellsgd']
		for each in etherusd:
			if "esellusd" in each:
				ethusd = each['esellusd']
		#Liqui does not support eth -> SGD/USD.
		#We're going to use coinhako's rate to calculate.
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

	def geteth(self):
		eth = requests.get("https://api.gemini.com/v1/pubticker/ethusd").json()
		return eth	

	def ethusd(self):
		eth = self.geteth()
		ethli = []
		eth_buy_price = eth['bid']
		eth_sell_price = eth['ask']
		ethli.append({"ebuyusd":eth_buy_price})
		ethli.append({"esellusd":eth_sell_price})
		return ethli

	def ethsgd(self):
		eth = self.geteth()
		ethli = []
		eth_buy_price = eth['bid']
		eth_sell_price = eth['ask']
		c = CurrencyConverter()
		converted_eth_buy_price = c.convert(float(eth_buy_price),'USD','SGD')
		converted_eth_sell_price = c.convert(float(eth_sell_price),'USD','SGD')
		ethli.append({"ebuysgd":converted_eth_buy_price})
		ethli.append({"esellsgd":converted_eth_sell_price})
		return ethli

