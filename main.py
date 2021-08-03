import shutil
import discord
from discord.ext import commands
from backup_func import *
from backup_func2 import *
import asyncio
import time
from datetime import *
global online
import os
online = True
print ("Starting.")
client = commands.Bot(command_prefix="backup!", help_command=None)
DELETE_OLD_BACKUPS_AFTER_DAYS = 3
async def backupclean1(ctx):
    today = str(datetime.today())
    #now = time.time()
    backup_location = "/media/data/BackupBot/Essentials"
    #print(f"{today} and {now}")
    directory_contents = os.listdir(backup_location)
    print(directory_contents)
    print(f"The date today is `{today}`. Comparing the backup folders to today's date.")
    list_of_datetimes = []
    # delete old backups
    for name in directory_contents:
        year, month, day = name.split('-')
        list_of_datetimes.append(datetime(int(year), int(month), int(day)))

    today = datetime.now()
    await ctx.channel.send(f"Checking for backups older than {DELETE_OLD_BACKUPS_AFTER_DAYS} day(s)...")
    for date in list_of_datetimes:
        if (today - date).days >= DELETE_OLD_BACKUPS_AFTER_DAYS:
            date = date.strftime('%Y-%m-%d')
            print(date, "is overdue and will be deleted.")
            await ctx.channel.send(
                f"The backup `{date}` is over {DELETE_OLD_BACKUPS_AFTER_DAYS} day(s) old and will be deleted.")
            deletepath = f"{backup_location}/{date}"
            shutil.rmtree(deletepath, ignore_errors=False, onerror=None)
            print("Old backup destroyed!")
        else:
            print("No old backups found.")
            await ctx.channel.send(
                f"No backups were found that were older than {DELETE_OLD_BACKUPS_AFTER_DAYS} day(s), skipping to download.")
async def backupclean2(ctx):
    today = str(datetime.today())
    #now = time.time()
    backup_location = "/media/data/BackupBot/mcMMO"
    #print(f"{today} and {now}")
    directory_contents = os.listdir(backup_location)
    print(directory_contents)
    print(f"The date today is `{today}`. Comparing the backup folders to today's date.")
    list_of_datetimes = []
    # delete old backups
    for name in directory_contents:
        year, month, day = name.split('-')
        list_of_datetimes.append(datetime(int(year), int(month), int(day)))

    today = datetime.now()
    await ctx.channel.send(f"Checking for backups older than {DELETE_OLD_BACKUPS_AFTER_DAYS} day(s)...")
    for date in list_of_datetimes:
        if (today - date).days >= DELETE_OLD_BACKUPS_AFTER_DAYS:
            date = date.strftime('%Y-%m-%d')
            print(date, "is overdue and will be deleted.")
            await ctx.channel.send(
                f"The backup `{date}` is over {DELETE_OLD_BACKUPS_AFTER_DAYS} day(s) old and will be deleted.")
            deletepath = f"{backup_location}/{date}"
            shutil.rmtree(deletepath, ignore_errors=False, onerror=None)
            print("Old backup destroyed!")
        else:
            print("No old backups found.")
            await ctx.channel.send(
                f"No backups were found that were older than {DELETE_OLD_BACKUPS_AFTER_DAYS} day(s), skipping to download.")

@client.event
async def on_ready():
    print ("Backup Bot is ready.")
    await client.change_presence(activity=discord.Game(name='KC Backup Bot 2.0'))


@client.command(name="start")
@commands.has_permissions(administrator=True)
async def start(ctx: commands.Context):
    while online == True:
        try:
            await backupclean1(ctx)
            await backupclean2(ctx)
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
@client.command(name="lpbackup.start")
@commands.has_permissions(administrator=True)
async def lpstart(ctx: commands.Context):
    await ctx.channel.send("LP Backup Set.")
    while online == True:
        datestring = str(datetime.date.today())
        f"/lp export {datestring}"
        await ctx.channel.send("/lp export {}".format(datestring))
        await asyncio.sleep(86400)
@client.event
async def on_error(ctx, event, *args, **kwargs):
    if isinstance(FileNotFoundError):
        await ctx.send("Backup complete.")


client.run("TOKEN")
