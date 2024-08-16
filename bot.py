import discord
import os
import autoPredict as ap
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Ensure this is enabled

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print(f'Bot is connected to the following guilds:')
    for guild in client.guilds:
        print(f' - {guild.name} (id: {guild.id})')

@client.event
async def on_message(message):
    print("Message received")  # Debug print
    if message.author == client.user:
        return
    print(f'{message.author}: {message.content}')
    harcelement=ap.predict(str(message.content))
    print(harcelement)
    if harcelement == 1:
        print("detection de harcelement")
#replace the bot tocken with the actual tocken
client.run("discord token")
