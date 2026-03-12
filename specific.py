import discord
import json

with open('config.json', 'r') as f:
    config = json.load(f)
TOKEN = config['TOKEN']

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    message_id = int(input("Enter the message ID: "))
    
    channel = bot.get_channel(12345678901234567890) # Replace with Real Channel ID
    if channel:
        try:
            message = await channel.fetch_message(message_id)
            print(f'Message Content: {message.content}')
            if message.embeds:
                for embed in message.embeds:
                    print(f'Embed Title: {embed.title}')
                    print(f'Embed Description: {embed.description}')
                    print(f'Embed URL: {embed.url}')
                    
                    if embed.thumbnail and embed.thumbnail.url:
                        print(f'Embed Thumbnail URL: {embed.thumbnail.url}')

                    print('Embed Fields:')
                    for field in embed.fields:
                        print(f'  Name: {field.name}')
                        print(f'  Value: {field.value}')
                        print(f'  Inline: {field.inline}')
        except discord.NotFound:
            print("Message not found.")
        except discord.Forbidden:
            print("Insufficient permissions to fetch message.")
        except discord.HTTPException as e:
            print(f"Error fetching message: {e}")
    else:
        print("Invalid channel ID or bot not connected to the channel.")

bot.run(TOKEN)