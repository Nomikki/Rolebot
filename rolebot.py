import discord
import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

COMMAND_NAME_GAMEROLE_ADD =  os.getenv('COMMAND_NAME_GAMEROLE_ADD')
COMMAND_NAME_GAMEROLE_DEL =  os.getenv('COMMAND_NAME_GAMEROLE_DEL')

MESSAGE_ID = int(os.getenv('MESSAGE_ID'))
RESPONSE_CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
ROLE_PREFIX = os.getenv('ROLE_PREFIX')

ROLE_MAPPING_FILE = "role_mapping.json"

def load_role_mapping():
    if os.path.exists(ROLE_MAPPING_FILE):
        with open(ROLE_MAPPING_FILE, "r") as file:
            return json.load(file)
    return {}


def save_role_mapping(role_mapping):
    with open(ROLE_MAPPING_FILE, "w") as file:
        json.dump(role_mapping, file, indent=4)

ROLE_MAPPING = load_role_mapping()

intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


async def send_message(msg):
  channel = bot.get_channel(RESPONSE_CHANNEL_ID) 
  if channel is None:
    return
  await channel.send(msg)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == MESSAGE_ID:
        guild = bot.get_guild(payload.guild_id)
        if guild is None:
            return

        rolename = ROLE_MAPPING.get(str(payload.emoji))
        if rolename is None:
            return

        role = discord.utils.get(guild.roles, name=rolename)
        if role is None:
            await send_message(f"Role with the name {rolename} not found!")
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            return

        await member.add_roles(role)
        await send_message(f"Role {role.name} assigned to {member.name}!")


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == MESSAGE_ID:
        guild = bot.get_guild(payload.guild_id)
        if guild is None:
            return

        rolename = ROLE_MAPPING.get(str(payload.emoji))
        if rolename is None:
            return

        role = discord.utils.get(guild.roles, name=rolename)
        if role is None:
            await send_message(f"Role with the name {rolename} not found!")
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            return

        await member.remove_roles(role)
        await send_message(f"Role {role.name} removed from user {member.name}!")


@bot.command()
@commands.has_role(ADMIN_ROLE) 
async def add_gamerole(ctx, emoji: str, rolename: str):
    guild = ctx.guild

    rolename_with_prefix = ROLE_PREFIX + rolename

    role = discord.utils.get(guild.roles, name=rolename_with_prefix)
    if role is None:
        await send_message(f"Role {rolename} not found.")
        await ctx.guild.create_role(name=rolename_with_prefix, colour=0x00FF00)
        await send_message(f"New game role {rolename} is created!")

    ROLE_MAPPING[emoji] = rolename_with_prefix
    save_role_mapping(ROLE_MAPPING)

    await send_message(f"Role {rolename} added to emoji {emoji}!")


@add_gamerole.error
async def add_gamerole_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await send_message("You don't have the required permissions to add roles.")


@bot.event
async def on_ready():
  print ('Successful login as {0.user}'.format(bot)) 


bot.run(TOKEN)