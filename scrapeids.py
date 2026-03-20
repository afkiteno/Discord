import discord
import json

with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config['TOKEN']

intents = discord.Intents.default()
intents.guilds = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():        
    found_ids = []

    for i in range(31):
        target_name = str(i).zfill(2)
        
        guild = discord.utils.get(bot.guilds, name=target_name)
        
        if guild:
            found_ids.append(str(guild.id))
            print(f"Found: {target_name} (ID: {guild.id})")
        else:
            print(f"Missing: {target_name}")

    print(f"\nTotal servers found: {len(found_ids)}")
    
    config['ServerIDs'] = found_ids
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
        
    print("\nconfig.json has been updated with the sorted IDs.")
    
    await bot.close()

bot.run(TOKEN)