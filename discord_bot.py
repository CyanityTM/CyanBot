import discord
from discord.ext import commands

import discord_token

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",intents=intents)

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(message.content)
    if 'banana' in message.content.lower():
        channel = bot.get_channel(message.channel.id)
        if channel is not None:
            await channel.send(f'User `{message.author}` mentioned banana in channel: {message.channel}')
        else:
            print('Channel "scav" not found.')

    await bot.process_commands(message)

bot.run(discord_token.get_token())