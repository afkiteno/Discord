import discord
import json

with open('config.json', 'r') as f:
    config = json.load(f)
TOKEN = config['TOKEN']

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

@bot.event
async def on_message(message):
    if message.channel.id != 12345678901234567890: # Replace with Real Channel ID
        return
    
    print(f'Message Content: {message.content}')
    if message.embeds:
        for embed in message.embeds:
            print(f'Embed Title: {embed.title}')
            print(f'Embed Description: {embed.description}')
            print(f'Embed Image URL: {embed.image.url if embed.image else None}')
            print(f'Embed URL: {embed.url}')
            print('Embed Fields:')
            for field in embed.fields:
                print(f'  Name: {field.name}')
                print(f'  Value: {field.value}')
                print(f'  Inline: {field.inline}')

bot.run(TOKEN)