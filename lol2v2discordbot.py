import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import random
import openai

load_dotenv()

# Load environment variables
discord_token = os.getenv("DISCORD_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not discord_token:
    raise ValueError("Missing Discord token .env file.")

# Set OpenAI API key
openai.api_key = openai_api_key

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
category_list = """PROJECT Skins
Animal Companions
Champs in a Band
Blue
Assassins
Armored Champs
Bandle City
Enchanters
Star Guardian Skins
Void
Exposed Bell
Ixtal
Hat/Headwear
Mecha Skins
Demacia
Mages
One-Eyed Champs
Global Ultimates
Matching Skin Lines
Bruisers
Champs with Ultimate Skin
Ranged
Freljord
Tanks
Darkin
Yordle
5 Randoms
Noxus
Short Kings/Queens (Short-statured Champions)
Fire and Ice (Champions with fire or ice abilities)
AD Only
Top 5 Mastery
First Letter of Last Name
One-Trick Champions
Champs with Worlds Team Skins
Duelists
Shurima
Old Random
Artists
Hard CC Masters
Odyssey Skins
Weapon Wielders
RNG (Randomized Picks)
Flying Champs
Wombo Combo
Orange
Piltover
Least 5 Mastery
Purple
Silencers
Spin Again
Bearded Champs
Non-Humanoid
Ionia
Masked Champs
Yellow
Undead
Green
Zaun
Targon
Speedsters (Enhanced Movement Speed)
Supports
Shield Bearers
Villains
Elderwood Skins
Pentakill Potentials
AP Only
Skillshot Masters
Animal Like
Red
Festive Skins (Holiday-themed Skins)
First Letter of First Name
Bilgewater
Shape Shifters
Bare Hands (Champions without weapons)
Shadow Isles
Reworked Champs
Tall Champs
Heroes"""

@client.event
async def on_ready():
    print("---------- League 2v2 Bot is ready ----------")

# Message logging as personal preference
@client.event
async def on_message(message):

    print(f"Message from {message.author}: {message.content}")
    await client.process_commands(message)

# Randomise category list to use a set category
@client.command()
async def roll(ctx):
    """
    Randomly selects an item from a hardcoded list with a delay and posts it in the discord.
    Usage: !roll
    """
    # Hardcoded list
    options = category_list.splitlines()

    await ctx.send("🎲 Rolling...")
    await asyncio.sleep(3)

    # Randomly select a choice
    selected_item = random.choice(options)

    # Send option to discord
    await ctx.send(f"🎲 The category is... **{selected_item}**!")

@client.command()
async def category(ctx):
    """
    Generates a custom category list using ChatGPT, then randomly selects one.
    NOTE: If this is not working, please check you have set the API key in a .env file.
    Usage: !category
    """

    if not openai_api_key:
        raise ValueError("Missing OpenAI API key .env file.")

    # Indicate the bot is generating the list
    await ctx.send("🧠 Thinking... Generating categories...")

    try:
        # Send a request to OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a highly creative assistant specializing in a logical but unique and diverse category generation."},
                {"role": "user", "content": f""" 
                    Generate 1 unique category for selecting champions for a League of Legends 2v2 ARAM game.
                    The category must be based on specific in-game mechanics, items, champion abilities, or team compositions.
                    Avoid vague or overly general names, be specific but its ok to sometimes be simple.
                    Also avoid anything to do with the league of legends rune system.
                    Try to make sure the category would fit for approximately 6 or more champions.
                    Here are some example categories: {category_list}. You may use an ideas from this list.
                    For example from the above list, 'Freljord' includes champions only from that part of Runeterra (e.g. Anivia, Ashe, Braum),
                    or 'High Risk' includes champs with high-risk, high-reward playstyles (Rengar, Qiyana, Irelia).
                    Structure your output to **only include the category name**, with a brief description in brackets (but dont include any champion names or abilities), and make it bold.
                """}
            ],
            max_tokens=100,
            temperature=1.15,
            top_p=0.9
        )
        category_text = response.choices[0].message.content

        # Send the selected category to discord
        await ctx.send(f"🎲 The category is...\n\n{category_text}!")
    except Exception as e:
        await ctx.send("⚠️ Sorry, I couldn't generate categories. Please try again later.")
        print(f"Error: {e}")

client.run(discord_token)