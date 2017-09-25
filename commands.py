#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Hermes's core
# Written by xlanor
##
import json
from modules.coinhako import Coinhako
from modules.liqui import Liqui
from modules.gemini import Gemini
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

	def geminimsg():
		eth = "<b>Ethereum</b>\n"
		btc = "<b>Bitcoin</b>\n"
		geminilist = []
		geminilist = geminilist + (Gemini().ethsgd())
		geminilist = geminilist + (Gemini().ethusd())
		geminilist = geminilist + (Gemini().btcsgd())
		geminilist = geminilist + (Gemini().btcusd())
		for each in geminilist:
			if "ebuysgd" in each:
				eth += "🇸🇬💸SGD Buy: $"
				eth += str(round(each["ebuysgd"],2))
				eth += "\n"
			elif "esellsgd" in each:
				eth += "🇸🇬💰SGD Sell: $"
				eth += str(round(each['esellsgd'],2))
				eth += "\n"
			elif "ebuyusd" in each:
				eth += "🇺🇸💸USD Buy: $"
				eth += str(each['ebuyusd'])
				eth += "\n"
			elif "esellusd" in each:
				eth += "🇺🇸💰USD Sell: $"
				eth += str(each['esellusd'])
				eth += "\n"
			elif "bbuysgd" in each:
				btc += "🇸🇬💸SGD Buy: $"
				btc += str(round(each['bbuysgd'],2))
				btc += "\n"
			elif "bsellsgd" in each:
				btc += "🇸🇬💰SGD Sell: $"
				btc += str(round(each['bsellsgd'],2))
				btc += "\n"
			elif "bbuyusd" in each:
				btc += "🇺🇸💸USD Buy: $"
				btc += str(each['bbuyusd'])
				btc += "\n"
			elif "bsellusd" in each:
				btc += "🇺🇸💰USD Sell: $"
				btc += str(each['bsellusd'])
				btc += "\n"
		combinedmessage = "♊<b>Gemini Prices</b>\n"+ eth + "\n" + btc
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
			geminimsg = Commands.geminimsg()
			fullmessage = coinhakomessage + "\n" + geminimsg + "\n" + liquimessage 
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
			
	def gem(bot,update):
		try:
			message = Commands.geminimsg()
			bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')

	def calculateeth(bot,update):
		try:
			ether = (update.message.text)[9:]
			if not ether.strip():
				message = "The format for this command is /calceth [float]ETH or /calceth $[float] where float is a numerical value"
				bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
			else:
				if (str(ether[-3:])).lower() == "eth":
					try:
						float(ether[:-3])
					except:
						message = "Please enter a numerical value !\n"
						message += "The bot accepts the following: /calceth [float]ETH or /calceth $[float] where float is a numerical value"
						bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
					else:
						#for eth -> fiat, we're only going to use buy value
						#this is because we're asumming you'll sell at the buy price.
						ethereum = float(ether[:-3])
						eth = "<b>Based on 👛CoinHako, "+str(ethereum)+" ETH is worth ... </b>\n"
						hakoethlist = []
						hakoethlist = hakoethlist + (Coinhako().ethersgd())
						hakoethlist = hakoethlist + (Coinhako().etherusd())
						for each in hakoethlist:
							if "ebuysgd" in each:
								eth += "🇸🇬SGD $"
								eth += str(round((ethereum * float(each["ebuysgd"])),2))
								eth += "\n"
							elif "ebuyusd" in each:
								eth += "🇺🇸USD $"
								eth += str(round((ethereum * float(each["ebuyusd"])),2))
								eth += "\n"
						geminiethlist = []
						geminiethlist = geminiethlist + (Gemini().ethsgd())
						geminiethlist = geminiethlist + (Gemini().ethusd())
						eth += "<b>Based on ♊Gemini, "+str(ethereum)+" ETH is worth ... </b>\n"
						for gem in geminiethlist:
							if "ebuysgd" in gem:
								eth += "🇸🇬SGD $"
								eth += str(round((ethereum * float(gem["ebuysgd"])),2))
								eth += "\n"
							elif "ebuyusd" in gem:
								eth += "🇺🇸USD $"
								eth += str(round((ethereum * float(gem["ebuyusd"])),2))
								eth += "\n"
						eth += "<i>** All values are rounded to 2 decimals</i>"
						bot.sendMessage(chat_id=update.message.chat_id, text=eth,parse_mode='HTML')
				else:
					#for fiat -> eth, we're only going to use sell value
					#this is because we're asumming you'll buy at the sell price.
					if ether[:1] != "$":
						message = "Please enter a recognised input !\n"
						message += "The bot accepts the following: /calceth [float]ETH or /calceth $[float] where float is a numerical value"
						bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
					else:
						try:
							float(ether[1:])
						except:
							message = "Please enter a numerical value !\n"
							message += "The bot accepts the following: /calceth [float]ETH or /calceth $[float] where float is a numerical value"
							bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
						else:
							fiat = float(ether[1:])
							eth = "<b>Based on 👛CoinHako, $"+str(fiat)+" can buy ... </b>\n"
							hakoethlist = []
							hakoethlist = hakoethlist + (Coinhako().ethersgd())
							hakoethlist = hakoethlist + (Coinhako().etherusd())
							for each in hakoethlist:
								if "esellsgd" in each:
									eth += "🇸🇬SGD $"
									eth += str(fiat)
									eth += " can buy "
									eth += str(round(((1/float(each["esellsgd"]))*fiat),2))
									eth += " ETH\n"
								elif "esellusd" in each:
									eth += "🇺🇸USD $"
									eth += str(fiat)
									eth += " can buy "
									eth += str(round(((1/float(each["esellusd"]))*fiat),2))
									eth += " ETH\n"
							geminiethlist = []
							geminiethlist = geminiethlist + (Gemini().ethsgd())
							geminiethlist = geminiethlist + (Gemini().ethusd())
							eth += "<b>Based on ♊Gemini, $"+str(fiat)+" can buy ... </b>\n"
							for gem in geminiethlist:
								if "esellsgd" in gem:
									eth += "🇸🇬SGD $"
									eth += str(fiat)
									eth += " can buy "
									eth += str(round(((1/float(gem["esellsgd"]))*fiat),2))
									eth += " ETH\n"
								elif "esellusd" in gem:
									eth += "🇺🇸USD $"
									eth += str(fiat)
									eth += " can buy "
									eth += str(round(((1/float(gem["esellusd"]))*fiat),2))
									eth += " ETH\n"
							eth += "<i>** All values are rounded to 2 decimals</i>"
							bot.sendMessage(chat_id=update.message.chat_id, text=eth,parse_mode='HTML')



		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')

	def calculatekyber(bot,update):
		try:
			kyber = (update.message.text)[11:]
			if not kyber.strip():
				message = "The format for this command is /calckyber [float]KNC or /calckyber $[float] where float is a numerical value"
				bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
			else:
				if (str(kyber[-3:])).lower() == "knc":
					try:
						float(kyber[:-3])
					except:
						message = "Please enter a numerical value !\n"
						message += "The bot accepts the following: /calckyber [float]KNC or /calckyber $[float]"
						bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
					else:
						kyber = float(kyber[:-3])
						knclist = []
						knclist = knclist + (Liqui().knceth())
						knc = "<b>Based on 🚀Liqui, "+str(kyber)+" kyber tokens is worth ... </b>\n"
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

						knc += "<i>** All values are rounded to 2 decimals</i>"
						bot.sendMessage(chat_id=update.message.chat_id, text=knc,parse_mode='HTML')
				else:
					#for fiat to knc, we're going to use the sell value.
					#this is because we're asumming that you're going to buy at their selling price.
					if kyber[:1] != "$":
						message = "Please enter a recognised input !\n"
						message += "The bot accepts the following: /calckyber [float]KNC or /calckyber $[float] where float is a numerical value"
						bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
					else:
						try:
							float(kyber[1:])
							print(kyber[1:])
						except:
							message = "Please enter a numerical value !\n"
							message += "The bot accepts the following: /calckyber [float]KNC or /calckyber $[float] where float is a numerical value"
							bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode='HTML')
						else:
							fiat = float(kyber[1:])
							knclist = []
							knclist = knclist + (Liqui().knceth())
							knc = "<b>Based on 🚀Liqui, $"+str(fiat)+" can buy... </b>\n"
							for each in knclist:
								if "kncsellsgd" in each:
									knc += "🇸🇬$"
									knc += str(fiat)
									knc += " can buy "
									knc += str(round(((1/each["kncsellsgd"])*fiat),2))
									knc += " kyber tokens\n"
								elif "kncsellusd" in each:
									knc += "🇺🇸$"
									knc += str(fiat)
									knc += " can buy "
									knc += str(round(((1/each["kncsellusd"])*fiat),2))
									knc += " kyber tokens\n"
							knc += "<i>** All values are rounded to 2 decimals</i>"
							bot.sendMessage(chat_id=update.message.chat_id, text=knc,parse_mode='HTML')
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')

		