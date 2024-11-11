import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Load configuration from config.json
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Error: config.json file not found. Please create it using config_template.json as a guide.")
    exit()

MUTE_LOG_CHANNEL_ID = config.get("MUTE_LOG_CHANNEL_ID")
DETAIN_ROLE_ID = config.get("DETAIN_ROLE_ID")
DETAIN_LOG_CHANNEL_ID = config.get("DETAIN_LOG_CHANNEL_ID")
VOICEMASTER_BOT_ID = config.get("VOICEMASTER_BOT_ID")

# Define bot intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.voice_states = True

# Initialize bot
bot = commands.Bot(command_prefix=".", intents=intents)

# Track auto-unmute and mute permissions
auto_unmute_cache = set()
mute_permission_granted = {}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = bot.get_channel(MUTE_LOG_CHANNEL_ID)
    if not log_channel:
        print("Mute log channel not found. Ensure the ID is set in config.json.")
        return

    # Auto-unmute logic
    if (before.channel is None and after.channel is not None) or (before.channel != after.channel):
        if after.mute:
            await member.edit(mute=False)  # Automatically unmute
            embed = discord.Embed(
                title="Voice Auto Unmute",
                description=f"User **{member}** was automatically unmuted after joining or switching channels.",
                color=0x00FF00,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=f"User ID: {member.id}")
            await log_channel.send(embed=embed)
            await member.send("You have been automatically unmuted after joining or switching channels.")
            auto_unmute_cache.add(member.id)
            return

    # Log manual mute/unmute actions
    if before.mute != after.mute:
        guild = member.guild
        action = discord.AuditLogAction.member_update
        async for entry in guild.audit_logs(action=action, limit=10):
            if entry.target.id == member.id:
                moderator = entry.user
                if moderator == bot.user:
                    return
                action_desc = (f"User **{member}** was manually muted by **{moderator}**."
                               if after.mute else
                               f"User **{member}** was manually unmuted by **{moderator}**.")
                embed = discord.Embed(
                    title="Voice Mute Update",
                    description=action_desc,
                    color=0xFF5733 if after.mute else 0x00FF00,
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text=f"User ID: {member.id}")
                await log_channel.send(embed=embed)
                await member.send(f"You have been {'muted' if after.mute else 'unmuted'} by {moderator}.")
                break


@bot.event
async def on_member_update(before, after):
    detain_role = discord.utils.get(after.guild.roles, id=DETAIN_ROLE_ID)
    log_channel = bot.get_channel(DETAIN_LOG_CHANNEL_ID)
    if not detain_role or not log_channel:
        print("Detain role or log channel not found. Check config.json.")
        return

    # Detain/Undetain role updates
    if detain_role in after.roles and detain_role not in before.roles:
        embed = discord.Embed(
            title="Detain Role Update",
            description=f"User **{after}** was detained.",
            color=0xFF0000,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"User ID: {after.id}")
        await log_channel.send(embed=embed)
        await after.send("You have been detained in the server.")

    elif detain_role not in after.roles and detain_role in before.roles:
        embed = discord.Embed(
            title="Detain Role Update",
            description=f"User **{after}** was undetained.",
            color=0x00FF00,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"User ID: {after.id}")
        await log_channel.send(embed=embed)
        await after.send("You have been undetained in the server.")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def detain(ctx, member: discord.Member):
    detain_role = discord.utils.get(ctx.guild.roles, id=DETAIN_ROLE_ID)
    if not detain_role:
        await ctx.send("Detain role not found. Check config.json.")
        return
    await member.add_roles(detain_role)
    await ctx.send(f"User **{member}** has been detained.")
    await member.send("You have been detained in the server.")
    log_channel = bot.get_channel(DETAIN_LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="Detain Role Update",
            description=f"User **{member}** was detained.",
            color=0xFF0000,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"User ID: {member.id}")
        await log_channel.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def undetain(ctx, member: discord.Member):
    detain_role = discord.utils.get(ctx.guild.roles, id=DETAIN_ROLE_ID)
    if not detain_role:
        await ctx.send("Detain role not found. Check config.json.")
        return
    await member.remove_roles(detain_role)
    await ctx.send(f"User **{member}** has been undetained.")
    await member.send("You have been undetained in the server.")
    log_channel = bot.get_channel(DETAIN_LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="Detain Role Update",
            description=f"User **{member}** was undetained.",
            color=0x00FF00,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"User ID: {member.id}")
        await log_channel.send(embed=embed)


# Run the bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("Bot token is not set. Please add it to the .env file.")


## Credits
This bot was created and maintained by **Artur Pedrotti**.

Feel free to contribute or reach out for any queries!
