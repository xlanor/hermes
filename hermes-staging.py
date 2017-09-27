#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Hermes's init and commands
# Written by xlanor
##
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job, MessageHandler, Filters, RegexHandler, ConversationHandler
from tokens import bottoken
from commands import Commands
from commands import WALLET, USERNAME, UPDATE, NEWWALLET


def hermes():

	updater = Updater(token=bottoken.token("staging"))
	dispatcher = updater.dispatcher
	#commands
	start_handler = CommandHandler('hako', Commands.hako)
	dispatcher.add_handler(start_handler)
	start_handler = CommandHandler('liqui', Commands.liqui)
	dispatcher.add_handler(start_handler)
	start_handler = CommandHandler('gemini', Commands.gem)
	dispatcher.add_handler(start_handler)
	start_handler = CommandHandler('calckyber', Commands.calculatekyber)
	dispatcher.add_handler(start_handler)
	start_handler = CommandHandler('calceth', Commands.calculateeth)
	dispatcher.add_handler(start_handler)
	start_handler = CommandHandler('portfolio',Commands.portfolio)
	dispatcher.add_handler(start_handler)
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('register', Commands.register)],

		states={
			USERNAME: [MessageHandler(Filters.text,Commands.name)],
			NEWWALLET: [MessageHandler(Filters.text,Commands.wallet)],
			UPDATE: [RegexHandler('^(Yes)$', Commands.newwallet),RegexHandler('^(No)$', Commands.cancel)],
			WALLET: [MessageHandler(Filters.text,Commands.wallet)]
		},

		fallbacks=[CommandHandler('cancel', Commands.cancel)]
	)
	dispatcher.add_handler(conv_handler)
	#job for channels
	j = updater.job_queue
	job_minute = Job(Commands.alert, 75.0)
	j.put(job_minute, next_t=0.0)
	#starts the bot
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	hermes()


