# FL Community Cup Discord Bot
# Seeding / Results

import discord
import random
from discord.ext import commands 
import pandas as pd
import pymongo
from pymongo import MongoClient
from pprint import pprint
from config import bot_token

# MongoDB Stuff

cluster = MongoClient(config.MongClient)
db = cluster.flcc
collection = db.gameResults

# Set Bot Prefix
bot = commands.Bot(command_prefix = '!', case_insensitive=True)
guild = discord.Guild

# Informal Bot Verison
bot.version = "0.1"

# Notification that Bot is online
@bot.event
async def on_ready():
    print(f'{bot.user} is ready.')
    await bot.change_presence(activity=discord.Game(name='Fettuccine Community Cup'))


@bot.command()
@commands.has_role('BotApproved')
async def submit(ctx, round_number:int, winner:str, loser:str):
    await ctx.reply("%s wins round %s against %s" % (winner, round_number, loser))
    await ctx.reply("Sucessfully submitted.")

    dict = []
    dict = {
        "round_number":round_number,
        "winner":winner,
        "loser":loser
    }
    collection.insert_many([dict])
    pprint('Submission Successful')

#### Add command to mass remove captain roles


#### Add command to get captain name from website and give roles if in server


#### Add command to vote for All Star (season 13)


# Latency Test
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')

# Seeding Command
@bot.command(name="seed")
@commands.has_role('FL League Director')
async def seed(ctx):
    teams = ['POR','JER','MTL','NEV','NSH','SDA','CLE','NOC','SFC','UTA','DET','BAL','SFK','OTT','LVT','CHI','PHX','DEN','SAR','BUF','KCC','PHI']
    random.shuffle(teams)
    await ctx.send(', '.join(teams))

#Bot Token
bot.run = bot.run(config.bot_token)
