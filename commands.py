#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Hermes's core
# Written by xlanor
##
import json
from modules.coinhako import Coinhako
from tokens import channels
import traceback,time,requests,string
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job

class Commands():
	def coinhakomsg():
		try:
			eth = "<b>Ethereum</b>\n"
			btc = "<b>Bitcoin</b>\n"
			coinhakolist = []
			coinhakolist = coinhakolist + (Coinhako().ethersgd())
			coinhakolist = coinhakolist + (Coinhako().etherusd())
			coinhakolist = coinhakolist + (Coinhako().btcsgd())
			coinhakolist = coinhakolist + (Coinhako().btcusd())
			for each in coinhakolist:
				if "ebuysgd" in each:
					eth += "🇸🇬💸SGD Buy: "
					eth += each["ebuysgd"]
					eth += "\n"
				elif "esellsgd" in each:
					eth += "🇸🇬💰SGD Sell: "
					eth += each['esellsgd']
					eth += "\n"
				elif "ebuyusd" in each:
					eth += "🇺🇸💸USD Buy: "
					eth += each['ebuyusd']
					eth += "\n"
				elif "esellusd" in each:
					eth += "🇺🇸💰USD Sell: "
					eth += each['esellusd']
					eth += "\n"
				elif "bbuysgd" in each:
					btc += "🇸🇬💸SGD Buy: "
					btc += each['bbuysgd']
					btc += "\n"
				elif "bsellsgd" in each:
					btc += "🇸🇬💰SGD Sell: "
					btc += each['bsellsgd']
					btc += "\n"
				elif "bbuyusd" in each:
					btc += "🇺🇸💸USD Buy: "
					btc += each['bbuyusd']
					btc += "\n"
				elif "bsellusd" in each:
					btc += "🇺🇸💰USD Sell: "
					btc += each['bsellusd']
					btc += "\n"
			combinedmessage = "👛<b>Coin Hako Prices</b>\n\n"+ eth + "\n" + btc
		except:
			catcherror = traceback.format_exc()
			print(catcherror)
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')
		return combinedmessage
	def alert(bot,job):
		try:
			message = Commands.coinhakomsg()
			bot.sendMessage(chat_id=channels.channellist('stagingchannel'),text=message,parse_mode='HTML')
		except:
			catcherror = traceback.format_exc()
			print(catcherror)
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')
	def hako(bot,update):
		try:
			message = Commands.coinhakomsg()
			bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
		except:
			catcherror = traceback.format_exc()
			print(catcherror)
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')
		