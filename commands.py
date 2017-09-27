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
from modules.etherscan import etherscan
from modules.ethplorer import Ethplorer
from modules.cryptocompare import Cryptocompare
from modules.checkaddress import web3check
from modules.portfoliomessage import Pmessage
from modules.cryptocomparemsg import CryptoComparemsg
from tokens import channels,SQL
from contextlib import closing
import traceback,time,requests,string,pymysql,datetime
from telegram import ReplyKeyboardMarkup,ChatAction
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job,ConversationHandler

WALLET, USERNAME, UPDATE, NEWWALLET = range(4) #declares states for hermes. Imported in main folder
class Commands():
	def register(bot,update): #checks if usn exists.
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					uid = update.message.from_user.id
					cur.execute("""SELECT telegram_id FROM mew WHERE telegram_id = %s""",(uid,))
					#if telegram ID does not exist, begin register process
					if cur.rowcount == 0: 
						message = "Hi! Lets get started by registering you with Hermes \n"
						message += "Can I have your name, please?\n"
						message += "To abort this process , please type /cancel"
						update.message.reply_text(message,parse_mode='HTML')
						#returns USERNAME, defined in states in hermes.
						return USERNAME 
					#else, TG username exist, update wallet ID?
					else: 
						message = "You are registered with Hermes.\n"
						message = "Would you like to update your wallet ID?"
						reply_kb = [['Yes'],['No']]
						markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard=True)
						update.message.reply_text(message,reply_markup=markup,parse_mode='HTML')
						#returns UPDATE, defined in states in hermes.
						return UPDATE 
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')

	def name (bot,update): #Enter name.
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					name = update.message.text
					uid = update.message.from_user.id
					#check if name > 50 (DB Column set at 50 varchar.)
					if len(name) > 50: 
						message="Please send me a name that is under 50 characters"
						update.message.reply_text(message,parse_mode='HTML')
						#returns username state again.
						return USERNAME 
					#if name entered < 50, Insert DB, continue.
					else:
						cur.execute("""INSERT INTO mew VALUES(NULL,%s,%s,NULL)""",(name,uid,))
						message = "Can I have the address of your wallet?\n"
						message += "<b>Please send me your address, not your private key!</b>"
						update.message.reply_text(message,parse_mode='HTML')
						return WALLET #return wallet state, check hermes file.
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')

	def wallet(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					#gets wallet address
					wallet = update.message.text
					#retrieve user ID from telegram
					uid = update.message.from_user.id
					#runs check module (return True or False)
					check = web3check().web3check(wallet)
					#if invalid,
					if check is False:
						message = wallet
						message += " is not a valid Ethereum address!\n"
						message += "Please enter your wallet address again\n"
						message += "Your address should look something like this:\n"
						message += "0xCe9F2Bf18150f57512C2380231401dAF44A614e4\n"
						message += "<b>Be sure send me your address, not your private key!</b>"
						update.message.reply_text(message,parse_mode='HTML')
						#re-runs this process.
						return WALLET 
					#else, insert db
					else:
						cur.execute("""UPDATE mew SET mew_address = %s WHERE telegram_id = %s""",(wallet,uid,))
						cur.execute("""SELECT user_name FROM mew WHERE telegram_id = %s""",(uid,))
						if cur.rowcount > 0:
							data = cur.fetchone()
							name = data[0]
						else:
							name = "-"
						message = "Sucessfully binded "+wallet+" to "+name
						message += "\n"
						message += "You may now use /portfolio to generate a report."
						update.message.reply_text(message,parse_mode='HTML')
						#ends conversation state.
						return ConversationHandler.END 
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')

	def newwallet(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					#if user has a uid registered, and wants to update their wallet addresses,
					message = "Please enter your new wallet address"
					update.message.reply_text(message,parse_mode='HTML')
					#goes back to wallet.
					return WALLET
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')

	def cancel(bot,update):
		#cancels conversation state.
		message = "Did I make you uncomfortable? =(\n"
		message += "Here's a seal for you to play with. Goodbye! (ᵔᴥᵔ)"
		update.message.reply_text(message, parse_mode='HTML')
		return ConversationHandler.END

	def alert(bot,job): 
		try:
			cryptocompare = Commands.cryptocomparemsg()
			print(cryptocompare)
			liquimessage = Commands.liquimsg()
			fullmessage = cryptocompare + "\n" + liquimessage 
			fullmessage += "\n "
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
						eth = "<b>Based on 👛Cryptocompare, "+str(ethereum)+" ETH is worth ... </b>\n"
						ethlist = []
						ethlist = ethlist + (Cryptocompare().geturl('ETH'))
						for each in ethlist:
							if "sgd" in each:
								eth += "🇸🇬SGD** $"
								eth += str(round((ethereum * float(each["sgd"])),2))
								eth += "\n"
							elif "usd" in each:
								eth += "🇺🇸USD $"
								eth += str(round((ethereum * float(each["usd"])),2))
								eth += "\n"

						eth += "<i>* All values are rounded to 2 decimals</i>\n <i>**Calculated using CEB rates</i>"
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
							eth = "<b>Based on 👛Cryptocompare, $"+str(fiat)+" can buy ... </b>\n"
							ethlist = []
							ethlist = ethlist + (Cryptocompare().geturl('ETH'))
							for each in ethlist:
								if "sgd" in each:
									eth += "🇸🇬SGD** $"
									eth += str(fiat)
									eth += " can buy "
									eth += str(round(((1/float(each["sgd"]))*fiat),2))
									eth += " ETH\n"
								elif "usd" in each:
									eth += "🇺🇸USD $"
									eth += str(fiat)
									eth += " can buy "
									eth += str(round(((1/float(each["usd"]))*fiat),2))
									eth += " ETH\n"

							eth += "<i>** All values are rounded to 2 decimals</i>\n <i>**Calculated using CEB rates</i>"
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
						knc = "<b>"+str(kyber)+" kyber tokens is worth ... </b>\n"
						knc += "<b>Based on 🚀Liqui, </b>"
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
						cryptocomparelist = []
						cryptocomparelist = cryptocomparelist + (Cryptocompare().geturl('KNC'))
						knc += "<b>Based on 💱CryptoCompare, </b>"
						for each in cryptocomparelist:
							if "sgd" in each:
								knc += "🇸🇬SGD Buy: $"
								knc += str(round((kyber * each["sgd"]),2))
								knc += "\n"
							elif "usd" in each:
								knc += "🇺🇸💸USD : $"
								knc += str(round((kyber * each["usd"]),2))
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

	def portfolio(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					uid = update.message.from_user.id
					cur.execute("""SELECT * FROM mew WHERE telegram_id = %s""",(uid,))
					if cur.rowcount > 0:
						data = cur.fetchone()
						try:
							address = data[3]
						except:
							msg = "You do not have an address registered! Use /register to get registered"
							bot.sendMessage(chat_id=update.message.chat_id, text=msg,parse_mode='HTML')
						else:
							username = data[1]
							address = data[3]
							waitingmsg = "This will take awhile, please wait :)\n"
							waitingmsg += "Here's a baby seal to pass the time ◕ᴥ◕"
							bot.sendMessage(chat_id=update.message.chat_id, text=waitingmsg,parse_mode='HTML')
							bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
							ethplorerscan = Ethplorer().scanaddress(address)
							msg = Pmessage().pmsg(address,username,ethplorerscan)
							bot.sendMessage(chat_id=update.message.chat_id, text=msg,parse_mode='HTML')
					else:
						msg = "You are currently not registered! Please register with /register"
						bot.sendMessage(chat_id=update.message.chat_id, text=msg,parse_mode='HTML')
		except:
			catcherror = traceback.format_exc()
			bot.sendMessage(chat_id=channels.channellist('errorchannel'), text=str(catcherror),parse_mode='HTML')

	def cryptocomparemsg():
		btcprice = Cryptocompare().geturl('BTC')
		ethprice = Cryptocompare().geturl('ETH')
		kncprice = Cryptocompare().geturl('KNC')
		ltcprice = Cryptocompare().geturl('LTC')

		msg = "💱 CryptoCompare Prices\n"
		msg += "<b>Bitcoin</b>\n"
		msg += CryptoComparemsg().cryptomsg(btcprice)
		msg += "<b>Ethereum</b>\n"
		msg += CryptoComparemsg().cryptomsg(ethprice)
		msg += "<b>Kyber Network Crystals</b>\n"
		msg += CryptoComparemsg().cryptomsg(kncprice)
		msg += "<b>LiteCoin</b>\n"
		msg += CryptoComparemsg().cryptomsg(ltcprice)
		return msg

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

 