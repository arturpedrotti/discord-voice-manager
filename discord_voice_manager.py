import discord
from discord.ext import commands
from datetime import datetime
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    print("❌ Bot token not found in .env. Please set DISCORD_BOT_TOKEN.")
    exit(1)

# Load configuration from config.json
CONFIG_PATH = "config.json"
try:
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"❌ {CONFIG_PATH} not found. Please create it from config_template.json.")
    exit(1)

MUTE_LOG_CHANNEL_ID = int(config.get("MUTE_LOG_CHANNEL_ID", 0))
DETAIN_ROLE_ID = int(config.get("DETAIN_ROLE_ID", 0))
DETAIN_LOG_CHANNEL_ID = int(config.get("DETAIN_LOG_CHANNEL_ID", 0))
VOICEMASTER_BOT_ID = int(config.get("VOICEMASTER_BOT_ID", 0))

# Define bot intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.voice_states = True

# Initialize bot
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = bot.get_channel(MUTE_LOG_CHANNEL_ID)
    if not log_channel:
        print("⚠️ Mute log channel not found. Check config.json.")
        return

    if (before.channel != after.channel) and after.mute:
        await member.edit(mute=False)
        embed = discord.Embed(
            title="Voice Auto Unmute",
            description=f"{member.mention} was automatically unmuted.",
            color=0x00FF00,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"User ID: {member.id}")
        await log_channel.send(embed=embed)
        await member.send("You were auto-unmuted upon joining/switching voice channels.")

    elif before.mute != after.mute:
        async for entry in member.guild.audit_logs(limit=10, action=discord.AuditLogAction.member_update):
            if entry.target.id == member.id and entry.user != bot.user:
                action = "muted" if after.mute else "unmuted"
                embed = discord.Embed(
                    title="Voice Mute Update",
                    description=f"{member.mention} was manually {action} by {entry.user.mention}.",
                    color=0xFF5733 if after.mute else 0x00FF00,
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text=f"User ID: {member.id}")
                await log_channel.send(embed=embed)
                await member.send(f"You were manually {action} by {entry.user}.")
                break

@bot.event
async def on_member_update(before, after):
    detain_role = discord.utils.get(after.guild.roles, id=DETAIN_ROLE_ID)
    log_channel = bot.get_channel(DETAIN_LOG_CHANNEL_ID)
    if not detain_role or not log_channel:
        print("⚠️ Detain role or log channel not found.")
        return

    if detain_role in after.roles and detain_role not in before.roles:
        await log_channel.send(embed=discord.Embed(
            title="User Detained",
            description=f"{after.mention} was detained.",
            color=0xFF0000,
            timestamp=datetime.utcnow()
        ).set_footer(text=f"User ID: {after.id}"))
        await after.send("You have been detained in the server.")

    elif detain_role not in after.roles and detain_role in before.roles:
        await log_channel.send(embed=discord.Embed(
            title="User Undetained",
            description=f"{after.mention} was undetained.",
            color=0x00FF00,
            timestamp=datetime.utcnow()
        ).set_footer(text=f"User ID: {after.id}"))
        await after.send("You have been undetained in the server.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def detain(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, id=DETAIN_ROLE_ID)
    if not role:
        await ctx.send("⚠️ Detain role not found.")
        return
    await member.add_roles(role)
    await ctx.send(f"{member.mention} has been detained.")
    await member.send("You have been detained.")
    await log_embed(ctx.guild, DETAIN_LOG_CHANNEL_ID, f"{member.mention} was detained.", 0xFF0000, member.id)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def undetain(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, id=DETAIN_ROLE_ID)
    if not role:
        await ctx.send("⚠️ Detain role not found.")
        return
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} has been undetained.")
    await member.send("You have been undetained.")
    await log_embed(ctx.guild, DETAIN_LOG_CHANNEL_ID, f"{member.mention} was undetained.", 0x00FF00, member.id)

async def log_embed(guild, channel_id, description, color, user_id):
    channel = guild.get_channel(channel_id)
    if channel:
        embed = discord.Embed(
            title="Detain Role Update",
            description=description,
            color=color,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"User ID: {user_id}")
        await channel.send(embed=embed)

# Start bot
bot.run(TOKEN)
