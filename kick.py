import discord
import json

with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config['TOKEN']

user_id = int(input("Enter the user ID to kick: "))

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

async def kick_user(user_id: int):
    for guild in bot.guilds:
        try:
            member = guild.get_member(user_id)
            if member:
                await member.kick()
                print(f"Kicked {member} from {guild.name}.")
            else:
                print(f"User with ID {user_id} not found in {guild.name}.")
        except discord.DiscordException as e:
            print(f"Error kicking user in {guild.name}: {e}")

@bot.event
async def on_ready():
    await kick_user(user_id)
    await bot.close()
    
bot.run(TOKEN)