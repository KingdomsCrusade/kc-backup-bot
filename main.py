import discord
from discord.ext import commands
from backup_func import *
from backup_func2 import *
import asyncio
global online
online = True
print ("Starting.")
client = commands.Bot(command_prefix="backup!", help_command=None)


@client.event
async def on_ready():
    print ("Backup Bot is ready.")
    await client.change_presence(activity=discord.Game(name='KC Backup Bot 1.0'))


@client.command(name="start")
@commands.has_permissions(administrator=True)
async def start(ctx: commands.Context):
    while online == True:
        try:
            print ("Backup starting.")
            await ctx.channel.send("Backup starting.")
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='backing up...'))
            #from backup_func import backup_func
            backup_func()
        except OSError as err:
            await ctx.send("First backup complete.")
            print ("Backup Complete")
            try:
                await ctx.send("Starting second backup...")
                print ("Second backup starting.")
                backup_func2()
                await ctx.send("Backup complete.")
                print("Backup Complete")
                await ctx.send("Waiting for next backup to start in 6 hours.")
                print ("Waiting for next backup to start in 6 hours.")
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='waiting for next backup. play.kingdomscrusade.net'))
                await asyncio.sleep(21600)
            except OSError as err:
                print(err)
                await ctx.send("Backup complete.")
                print ("Backup Complete")
                await ctx.send("Waiting for next backup to start in 6 hours.")
                print ("Waiting for next backup to start in 6 hours.")
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='waiting for next backup. play.kingdomscrusade.net'))
                await asyncio.sleep(21600)
@client.command(name="stop")
@commands.has_permissions(administrator=True)
async def stop(ctx: commands.Context):
    await ctx.channel.send("Stopping the backup sequence.")
    global online
    online = False
    print ("Backup stopped (paused)")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='KC Backup Bot 1.0, play.kingdomscrusade.net Backup status: paused'))
@client.command(name="restart")
@commands.has_permissions(administrator=True)
async def restart(ctx: commands.Context):
    await ctx.channel.send("Restarting the backup sequence (you need to run backup!start to set it auto going again).")
    global online
    online = True
    print("Backup started (unpaused)")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Restarting backups.'))
@client.event
async def on_error(ctx, event, *args, **kwargs):
    if isinstance(FileNotFoundError):
        await ctx.send("Backup complete.")
client.run("TOKEN")

