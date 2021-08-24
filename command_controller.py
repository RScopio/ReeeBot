import discord
import asyncio
import datetime

# spams the mentioned user
async def spam_command(tokens, message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + ' ~spam command')
    # escape
    if  (not (len(tokens) == 3 and tokens[2].isdigit())):
        await message.channel.send('usage: ~spam @User tagCount')
        return

    # spam
    for _ in range(0, min(abs(int(tokens[2])), 25)):
        await message.channel.send(tokens[1])

# clears the users last messages in commanded channel
async def clearme_command(tokens, message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + ' ~clearme command')
    # escape
    if(not (len(tokens) == 2 and tokens[1].isdigit())):
        await message.channel.send('usage: ~clearme postCount')
        return

    # clear
    async for m in message.channel.history(limit=int(tokens[1])):
        if m.author == message.author:
            await m.delete()
            await asyncio.sleep(1.2)
    await message.channel.send('Your regrets have been scrubbed away... what are you hiding ￣へ￣ ??')

# clears all messages in the channel
async def clearall_command(tokens, message: discord.Message):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + ' ~clearall command')
    # escape
    if(not (len(tokens) == 2 and tokens[1].isdigit())):
        await message.channel.send('usage: ~clearall postCount')
        return

    # clear
    async for m in message.channel.history(limit=int(tokens[1])):
        await m.delete()
    await message.channel.send('(╯°□°）╯︵ ┻━┻ Thread Nuked! None of you could play nicely so your toys have been taken away! （︶^︶）')
        
# scans the message for commands
async def scan_message(message: discord.Message):
    # escape
    if not message.content.startswith('~'):
        return

    # setup
    tokens = message.content.split(" ")
    command = tokens[0]

    # switch controller
    if ('~spam' in command):
        await spam_command(tokens, message)
    elif ('~clearall' in command):
        await clearall_command(tokens, message)
    elif ('~clearme' in command):
        await clearme_command(tokens, message)
