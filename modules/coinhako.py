#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Module for coinhako API
# Based on tw_ether by thwin
# For hermes
# Written by xlanor
##
import json
import logging
import requests

class Coinhako():
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

	def btcsgd(self):
		btc = requests.get("https://www.coinhako.com/api/v1/price/currency/BTCSGD").json()
		b_buy_price = btc['data']['buy_price']
		b_selling_price = btc['data']['sell_price']
		btcsgd = []
		btcsgd.append({"bbuysgd":b_buy_price})
		btcsgd.append({"bsellsgd":b_selling_price})
		return btcsgd

	def btcusd(self):
		btc = requests.get("https://www.coinhako.com/api/v1/price/currency/BTCUSD").json()
		b_buy_price = btc['data']['buy_price']
		b_selling_price = btc['data']['sell_price']
		btcusd = []
		btcusd.append({"bbuyusd":b_buy_price})
		btcusd.append({"bsellusd":b_selling_price})
		return btcusd





