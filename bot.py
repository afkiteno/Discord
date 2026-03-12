import discord
import json

with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config['TOKEN']

userid = int(input("Enter user ID: "))

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

async def assign_role(member, role_name):
    role = discord.utils.get(member.guild.roles, name=role_name)
    if not role:
        try:
            print(f"Role '{role_name}' not found, creating it...")
            role = await member.guild.create_role(name=role_name)
            print(f"Role '{role_name}' created successfully!")
        except discord.Forbidden:
            print(f"Permission denied: cannot create role '{role_name}'.")
            return False
        except discord.HTTPException as e:
            print(f"Failed to create role '{role_name}': {e}")
            return False

    if role in member.roles:
        print(f"User already has role '{role_name}', skipping assignment.")
        return True

    try:
        await member.add_roles(role)
        return True
    except discord.Forbidden:
        print(f"Permission denied: cannot assign role '{role_name}'.")
    except discord.HTTPException as e:
        print(f"Failed to assign role '{role_name}': {e}")
    return False

@bot.event
async def on_ready():
    for i in range(31):
        target_name = str(i).zfill(2)
        guild = discord.utils.get(bot.guilds, name=target_name)
        if not guild:
            print(f"Server '{target_name}' not found, skipping.")
            continue

        print(f"\nProcessing server: '{guild.name}'")

        member = guild.get_member(userid)
        if not member:
            print(f"User {userid} not found in this server.")
            continue

        print(f"User {member} found. Checking roles...")

        roles = [role.name for role in member.roles]
        if "catcher" in roles:
            print("User already has 'catcher' role, skipping.")
            continue
        elif "lol" in roles:
            print("User already has 'lol' role, skipping.")
            continue

        if await assign_role(member, "catcher"):
            print("'catcher' role assigned successfully!")
        elif await assign_role(member, "lol"):
            print("'lol' role assigned successfully!")
        else:
            print("Failed to assign either role.")

bot.run(TOKEN)