#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Hermes Tokens
# Written by xlanor
##
class bottoken():
	def token(x):
		if x == "live":
			return 'bot api key'
class channels():
	def channellist(x):
		if x == "livechannel":
			return "live channel id"
		elif x == "errorchannel":
			return "error channel id"
			
	def admin(x):
		adminlist = [adminid]
		if x in adminlist:
			return "admin"
		else:
			return "notadmin"