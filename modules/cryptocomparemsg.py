#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Module for Cryptocompare message 
# Based on tw_ether by thwin
# For hermes
# Written by xlanor
##

class CryptoComparemsg():
	def cryptomsg(self,variable):
		msg = ""
		for each in variable:
			if "sgd" in each:
				msg += "🇸🇬SGD :$"
				msg += str(round(each['sgd'],2))
				msg += "\n"
			elif "usd" in each:
				msg += "🇺🇸USD :$"
				msg += str(round(each['usd'],2))
				msg += "\n"
			elif "1h" in each:
				if "1h" is None:
					onehr = "-"
				else:
					onehr = each['1h']
			elif "24h" in each:
				if "24h" is None:
					twentyfourhr = "-"
				else:
					twentyfourhr = each['24h']
			elif "7d" in each:
				if "7d" is None:
					sevendays = "-"
				else:
					sevendays = each['7d']
		msg+= ("1H | <b>"+str(onehr)+"%</b> | 24H | <b>"+str(twentyfourhr)+"%</b> | 7D | <b>"+str(sevendays)+"%</b>\n")
		return msg

