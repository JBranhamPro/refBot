import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import asyncio
import random
from random import randint
import operator
import requests
import json
from itertools import permutations
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

	m.addNewSummoner(summonerName)

@refBot.command()
async def aye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	m.onAyeCmd(summonerName)

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

refBot.run(Secrets.botToken)