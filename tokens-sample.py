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
class SQL():
	def sqlinfo(x):
		if x == "host":
			return "localhost"
		elif x == "usn":
			return "username"
		elif x == "pw":
			return "password"
		elif x == "db":
			return "db"
class apikey():
	def apikey(x):
		if x == "etherscan":
			return "etherscanapikey"