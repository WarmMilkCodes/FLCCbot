# FL Community Cup Discord Bot
# Seeding / Results

import discord
import random
from discord.ext import commands 
import pandas as pd
import pymongo
from pymongo import MongoClient
from pprint import pprint
import config

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

# Result Submission - Courtesy to BrewTangClan for code assistance


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


# Auto Reply to Direct Messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if not message.guild:
        try:
            await message.channel.send("Message Warm Milk or Brindle directly with any questions you have regarding the Fettuccine Community Cup.")
        except discord.errors.Forbidden:
            pass
    else:
        pass


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

@bot.event
async def on_command_error(ctx,error):
    # Ignore these errors
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    # Begin Error Handling 
    if isinstance(error, commands.CommandOnCooldown):
        m,s = divmod(error.retry_after, 60)
        h,m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f'Please wait {int(s)} seconds to use this command!')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f'Please wait {int(m)} minutes and {int(s)} seconds to use this command!')
        else:
            await ctx.send(f'You must wait {int(h)} hours, {int(m)} minutes, and {int(s)} seconds to use this command!')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the proper permissions for this command!")
    raise error


#Bot Token
bot.run = bot.run(config.botToken)
