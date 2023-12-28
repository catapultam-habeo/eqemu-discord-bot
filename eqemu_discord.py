import discord
import sys
import os
from discord.ext import commands, tasks
from eqemu_db import get_db_connection, get_character_data
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN           = os.getenv('DISCORD_TOKEN')
ALLOWED_ROLES   = os.getenv('ALLOWED_ROLES').split(',')
MAX_ACCOUNTS    = int(os.getenv('MAX_ACCOUNTS', '1'))  # Default to 1 if not specified

# Initialize the bot with the members intent
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Data structure to hold the mapping
discord_user_characters = {}

# Sync commands when the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")    

    # Establish database connection
    conn = get_db_connection()
    if conn is not None:
        global discord_user_characters
        discord_user_characters = get_character_data(conn)

        # Print the dictionary
        print("Discord User Characters Mapping:")
        for discord_id, characters in discord_user_characters.items():
            print(f"Discord ID: {discord_id}, Characters: {characters}")
    
    await bot.sync_commands()  # Sync commands with Discord


# Run the bot
bot.run(TOKEN)