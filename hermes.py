#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Hermes's init and commands
# Written by xlanor
##
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job
from tokens import bottoken
from commands import Commands

def hermes():
	updater = Updater(token=bottoken.token("live"))
	dispatcher = updater.dispatcher
	j = updater.job_queue
	job_minute = Job(Commands.alert, 30.0)
	j.put(job_minute, next_t=0.0)
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	hermes()

