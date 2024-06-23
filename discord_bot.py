import discord
from discord.ext import commands
import discord_token
import daily_records

DAILY_RACE_CHANNEL_ID = 962908791236612166
DAILY_RACE_BOT_ID = 955661066652778506

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)

def valid_message(message):
    global DAILY_RACE_CHANNEL_ID, DAILY_RACE_BOT_ID
    if message.channel.id == DAILY_RACE_CHANNEL_ID \
    and message.author.id == DAILY_RACE_BOT_ID \
    and 'set the new fastest time' in message.content:
        return True
    else:
        return False

async def process_record(message):
    global DAILY_RACE_CHANNEL_ID

    text = message.content

    track = text[text.find('on ')+3:text.find('!')]
    new_time = text[text.find('0:'):text.find('-')-1]

    old_time = daily_records.update(track, new_time)

    if old_time is not None:
        channel = bot.get_channel(DAILY_RACE_CHANNEL_ID)
        if channel is not None:
            await channel.send(f'New World Record on {track}!\nOld time: {old_time}\nNew time: {new_time}')
        else:
            print(f'Channel not found.')

async def read_message_history():
    global DAILY_RACE_CHANNEL_ID

    channel = bot.get_channel(DAILY_RACE_CHANNEL_ID)

    async for message in channel.history(limit=100):  # read last 100 messages
        if valid_message(message):
            await process_record(message)
    
    await channel.send('Records are up to date.')


@bot.command(name='update')
async def update(ctx):
    await read_message_history()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await read_message_history()

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if valid_message(message):
        await process_record(message)

bot.run(discord_token.get())
