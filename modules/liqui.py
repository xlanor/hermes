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

class Liqui():
	def knceth(self):
		knc = requests.get("https://api.liqui.io/api/3/ticker/knc_eth").json()
		knc_buy_price = knc["knc_eth"]["buy"]
		knc_sell_price = knc["knc_eth"]["sell"]
		ethersgd = self.ethersgd()
		etherusd = self.etherusd()
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
	def ethersgd(self):
		ether = requests.get("https://www.coinhako.com/api/v1/price/currency/ETHSGD").json()
		e_buy_price = ether['data']['buy_price']
		e_selling_price = ether['data']['sell_price']
		ethersgd = []
		ethersgd.append({"ebuysgd":e_buy_price})
		ethersgd.append({"esellsgd":e_selling_price})
		return ethersgd
	def etherusd(self):
		ether = requests.get("https://www.coinhako.com/api/v1/price/currency/ETHUSD").json()
		e_buy_price = ether['data']['buy_price']
		e_selling_price = ether['data']['sell_price']
		etherusd = []
		etherusd.append({"ebuyusd":e_buy_price})
		etherusd.append({"esellusd":e_selling_price})
		return etherusd
