#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Hermes's core
# Written by xlanor
##
import json
from modules.coinhako import Coinhako
from modules.liqui import Liqui
from tokens import channels
import traceback,time,requests,string
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job

class Commands():
	def coinhakomsg():
		eth = "<b>Ethereum</b>\n"
		btc = "<b>Bitcoin</b>\n"
		coinhakolist = []
		coinhakolist = coinhakolist + (Coinhako().ethersgd())
		coinhakolist = coinhakolist + (Coinhako().etherusd())
		coinhakolist = coinhakolist + (Coinhako().btcsgd())
		coinhakolist = coinhakolist + (Coinhako().btcusd())
		for each in coinhakolist:
			if "ebuysgd" in each:
				eth += "🇸🇬💸SGD Buy: $"
				eth += each["ebuysgd"]
				eth += "\n"
			elif "esellsgd" in each:
				eth += "🇸🇬💰SGD Sell: $"
				eth += each['esellsgd']
				eth += "\n"
			elif "ebuyusd" in each:
				eth += "🇺🇸💸USD Buy: $"
				eth += each['ebuyusd']
				eth += "\n"
			elif "esellusd" in each:
				eth += "🇺🇸💰USD Sell: $"
				eth += each['esellusd']
				eth += "\n"
			elif "bbuysgd" in each:
				btc += "🇸🇬💸SGD Buy: $"
				btc += each['bbuysgd']
				btc += "\n"
			elif "bsellsgd" in each:
				btc += "🇸🇬💰SGD Sell: $"
				btc += each['bsellsgd']
				btc += "\n"
			elif "bbuyusd" in each:
				btc += "🇺🇸💸USD Buy: $"
				btc += each['bbuyusd']
				btc += "\n"
			elif "bsellusd" in each:
				btc += "🇺🇸💰USD Sell: $"
				btc += each['bsellusd']
				btc += "\n"
		combinedmessage = "👛<b>CoinHako Prices</b>\n"+ eth + "\n" + btc
		return combinedmessage

	def liquimsg():
		knc = "<b>Kyber Token Price: </b>\n"
		knclist = []
		knclist = knclist + (Liqui().knceth())
		for each in knclist:
			if "kncbuy" in each:
				knc += "💸Buy: "
				knc += str(each["kncbuy"])
				knc += "ETH \n"
			elif "kncsell" in each:
				knc += "💰Sell: "
				knc += str(each["kncsell"])
				knc += "ETH \n"
			elif "kncbuysgd" in each:
				knc += "🇸🇬💸SGD Buy: $"
				knc += str(round(each["kncbuysgd"],2))
				knc += "\n"
			elif "kncsellsgd" in each:
				knc += "🇸🇬💰SGD Sell: $"
				knc += str(round(each["kncsellsgd"],2))
				knc += "\n"
			elif "kncbuyusd" in each:
				knc += "🇺🇸💸USD Buy: $"
				knc += str(round(each["kncbuyusd"],2))
				knc += "\n"
			elif "kncsellusd" in each:
				knc += "🇺🇸💰USD Sell: $"
				knc += str(round(each["kncsellusd"],2))
				knc += "\n"

		combinedmessage = "🚀<b>Liqui Prices</b>\n" + knc
		return combinedmessage

	def alert(bot,job):
		try:
			coinhakomessage = Commands.coinhakomsg()
			liquimessage = Commands.liquimsg()
			fullmessage = coinhakomessage + "\n" + liquimessage
			bot.sendMessage(chat_id=channels.channellist('stagingchannel'),text=fullmessage,parse_mode='HTML')
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')

	def hako(bot,update):
		try:
			message = Commands.coinhakomsg()
			bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')
	def liqui(bot,update):
		try:
			message = Commands.liquimsg()
			bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')
	def calculatekyber(bot,update):
		try:
			kyber = (update.message.text)[11:]
			try:
				float(kyber)
			except:
				bot.sendMessage(chat_id=update.message.chat_id, text='Please enter a numerical value!',parse_mode='HTML')
			else:
				kyber = float(kyber)
				knclist = []
				knclist = knclist + (Liqui().knceth())
				knc = "<b>Based on 🚀Liqui, "+str(kyber)+"kyber tokens is worth ... </b>\n"
				for each in knclist:
					if "kncbuysgd" in each:
						knc += "🇸🇬💸SGD Buy: $"
						knc += str(round((kyber * each["kncbuysgd"]),2))
						knc += "\n"
					elif "kncsellsgd" in each:
						knc += "🇸🇬💰SGD Sell: $"
						knc += str(round((kyber * each["kncsellsgd"]),2))
						knc += "\n"
					elif "kncbuyusd" in each:
						knc += "🇺🇸💸USD Buy: $"
						knc += str(round((kyber * each["kncbuyusd"]),2))
						knc += "\n"
					elif "kncsellusd" in each:
						knc += "🇺🇸💰USD Sell: $"
						knc += str(round((kyber * each["kncsellusd"]),2))
						knc += "\n"

				bot.sendMessage(chat_id=update.message.chat_id, text=knc,parse_mode='HTML')
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')

		