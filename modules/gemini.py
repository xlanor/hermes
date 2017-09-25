#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Module for gemini API
# Based on tw_ether by thwin
# For hermes
# Written by xlanor
##
import json
import logging
import requests
from currency_converter import CurrencyConverter

class Gemini():
	def getbtc(self):
		btc = requests.get("https://api.gemini.com/v1/pubticker/btcusd").json()
		return btc

	def geteth(self):
		eth = requests.get("https://api.gemini.com/v1/pubticker/ethusd").json()
		return eth

	def btcusd(self):
		btc = self.getbtc()
		btc_buy_price = btc['bid']
		btc_sell_price = btc['ask']
		btcli = []
		btcli.append({"bbuyusd":btc_buy_price})
		btcli.append({"bsellusd":btc_sell_price})
		return btcli

	def btcsgd(self):
		btc = self.getbtc()
		btcli = []
		btc_buy_price = btc['bid']
		btc_sell_price = btc['ask']
		c = CurrencyConverter()
		converted_btc_buy_price = c.convert(float(btc_buy_price),'USD','SGD')
		converted_btc_sell_price = c.convert(float(btc_sell_price),'USD','SGD')
		btcli.append({"bbuysgd":converted_btc_buy_price})
		btcli.append({"bsellsgd":converted_btc_sell_price})
		return btcli

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


