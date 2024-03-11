import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
import random
import string

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='verify')
async def verify(ctx):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.verification
    codes_collection = db.codes
    codes_collection.insert_one({'discord_id': ctx.author.id, 'code': code, 'verified': False})
    await ctx.send(f'Your verification code is: {code}')
    mongo_client.close()

bot.run(TOKEN)
