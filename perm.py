import discord
import json

with open('config.json', 'r') as f:
    config = json.load(f)
TOKEN = config['TOKEN']
Slate = config['Slate']

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    channel_to_post = bot.get_channel(Slate)
    await channel_to_post.purge(limit=100)
    
    invite_lines = []

    for i in range(31):
        target_name = str(i).zfill(2)
        guild = discord.utils.get(bot.guilds, name=target_name)
        
        if guild:
            try:
                old_invites = await guild.invites()
                for inv in old_invites:
                    if inv.inviter.id == bot.user.id:
                        await inv.delete()
            except:
                pass

            invite_channel = guild.system_channel or next(
                (c for c in guild.text_channels if c.permissions_for(guild.me).create_instant_invite), 
                None
            )
            
            if invite_channel:
                try:
                    invite = await invite_channel.create_invite(max_age=0, max_uses=0)
                    
                    # Format: [`00`] - url
                    invite_lines.append(f"[`{guild.name}`] - {invite.url}")
                    print(f"{target_name} - {invite.url}")
                except:
                    print(f"Failed to create invite for {target_name}")
        else:
            print(f"Server {target_name} not found")

    if invite_lines:
        print("Sending embed")
        invite_lines.sort()
        description_text = "\n".join(invite_lines)
        
        embed = discord.Embed(description=description_text, color=discord.Color.blue())
        await channel_to_post.send(embed=embed)

    print("Task complete.")
    await bot.close()

bot.run(TOKEN)