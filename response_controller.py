import os
import random
import discord
import datetime

async def mention_everyone(message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'everyone was tagged, sending pic')
    images = os.listdir("""./pics""")
    imagePath = './pics/' + str(random.choice(images))
    await message.channel.send(file=discord.File(imagePath))

async def twitch_promo(message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'twitch link posted')
    await message.channel.send('shameless twitch promo!')

async def user_mentions(message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + message.mentions[0].name + ' was mentioned')

    if message.mentions[0].id == int(os.getenv('user_nerdwords')):
        if random.randint(0, 3) < 7:
            await message.channel.send('papa 🖐👁👄👁🖐')
    if message.mentions[0].id == int(os.getenv('user_spitfire')):
        if random.randint(0, 4) < 7:
            await message.channel.send('mama 🖐👁👄👁🖐')

async def reddit_promo(message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + ' reddit promo')
    await message.channel.send('Thats my fave subreedit 😎')

async def scan_message(message: discord.Message):
    if message.mention_everyone:
        await mention_everyone(message)
    elif 'twitch.tv' in message.content:
        await twitch_promo(message)
    elif len(message.mentions) > 0:
        await user_mentions(message)
    elif 'reddit.com/r/' in message.content:
        await reddit_promo(message)
