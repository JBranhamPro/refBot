# Imports required for Discord integration
import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import asyncio
# Imports for all proprietary functionality needs
import random
from random import randint
import operator
import requests
import json
from itertools import permutations
# Imports of all refBot files
import APICalls
a = APICalls
import Methods
m = Methods
import DbCalls
d = DbCalls
import Secrets

refBot = commands.Bot(command_prefix="!")

@refBot.command()
async def add(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	m.onAddCmd(summonerName)

@refBot.command()
async def aye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	response = m.onAyeCmd(summonerName)
	await refBot.say(resp)

@refBot.command()
async def bye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	response = m.onByeCmd(summonerName)
	await refBot.say(response)

@refBot.command()
async def draft(typeOpt):
	draftType = typeOpt.upper()

	if draftType == 'MANUAL':
		draftGame = m.manualDraft()
	elif draftType == 'RANDOM':
		draftGame = m.randomDraft()
	elif draftType == 'MATCHMADE':
		draftGame = m.matchmadeDraft()

	await refBot.say(draftGame)

@refBot.command()
async def e105r8945fjie48567rr():
		d.setupSummonerDb()

@refBot.command()
async def get(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	summonerData = d.getSummoner(summonerName)
	await refBot.say(summonerData)

@refBot.command()
async def options(option, value):
	m.setDraftOptions(option, value)

refBot.run(Secrets.botToken)