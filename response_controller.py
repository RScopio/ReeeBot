import os
import random
import discord
import datetime

# routing
async def scan_message(message: discord.Message):
    if message.mention_everyone:
        await mention_everyone(message)
    elif 'twitch.tv' in message.content:
        await twitch_promo(message)
    elif 'reddit.com/r/' in message.content:
        await reddit_promo(message)
    elif message.author._user.id == int(os.getenv('bot_dad')):
        await argue_with_dad(message)
    elif len(message.mentions) > 0:
        await user_mentions(message)

# respond to everyone
async def mention_everyone(message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'everyone was tagged, sending pic')
    images = os.listdir("""./pics""")
    imagePath = './pics/' + str(random.choice(images))
    await message.reply(file=discord.File(imagePath))

# twitch promo
async def twitch_promo(message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'twitch link posted')
    await message.reply('shameless twitch promo!')

# reddit promo
async def reddit_promo(message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'reddit promo')
    await message.reply('Thats my fave subreedit 😎')

# dad
async def argue_with_dad(message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'starting argument with dad')
    if random.randint(0,100) < 69:
        await message.delete()
    elif random.randint(0,100) > 50:
        await message.reply(f"SHUT UP <@!{os.getenv('bot_dad')}>! I'm sick of your lame repetitive jokes!")
    else:
        await message.reply(content="REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", file=discord.File('./pics/q.gif'))

# mama & papa
async def user_mentions(message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + message.mentions[0].name + ' was mentioned')
    if message.mentions[0].id == int(os.getenv('user_nerdwords')):
        if random.randint(0, 100) < 7:
            await message.channel.send('papa 🖐👁👄👁🖐')
    if message.mentions[0].id == int(os.getenv('user_spitfire')):
        if random.randint(0, 100) < 7:
            await message.channel.send('mama 🖐👁👄👁🖐')
