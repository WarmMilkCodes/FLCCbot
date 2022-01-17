# FL Community Cup Discord Bot
# Seeding / Results

import discord
import random
from discord.ext import commands 
import pandas as pd
import pymongo
from pymongo import MongoClient
import config

# MongoDB Stuff

cluster = MongoClient(config.MongClient)

db = cluster.business

collection = db.userCollection

# Set Bot Prefix
bot = commands.Bot(command_prefix = '!', case_insensitive=True)

guild = discord.Guild


# Informal Bot Verison
bot.version = "0.1"

# Notification that Bot is online
@bot.event
async def on_ready():
    print(f'{bot.user} is ready.')
    await bot.change_presence(activity=discord.Game(name='United Rogue FLCC Bot'))

# MongoDB Test 
# Needs a little more work - nearly there (maybe)


@bot.command()
async def result(ctx):
    global times_used
    await ctx.send('What round are you submitting?')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["1", "2", "3", "4"]

    msg = await bot.wait_for("message", check=check)
    dict = {}
    dict['round'] = msg.content.lower()
    if msg.content.lower() == "1":
        await ctx.send("You are submitting for Round 1")
    
    elif msg.content.lower() == "2":
        await ctx.send("You are submitting for Round 2")
        
    elif msg.content.lower() == "3":
        await ctx.send("You are submitting for Round 3")
        
    elif msg.content.lower() == "4":
        await ctx.send("You are submitting for Round 4")
        
    else:  
        await ctx.send("You did not submit a valid round.")
    


    dict['losingTeam'] = msg.content.lower()
    await ctx.send('Losing team - 3 letter abbreviation')
    collection.insert_one(dict)




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
