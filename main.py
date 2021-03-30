# IMPORTS #
import discord
from discord.ext import commands
from backup_func import *
import datetime
import asyncio

# VARIABLES #
bot_token = "TOKEN"  # Your bot token
loop_period = 21600  # Seconds between every backup loop
info = {
    "hostname": "ip",
    "port": 22,
    "username": "username",
    "password": "password"
}
backup1 = {
    "from": "dir",
    "to": "dir"
}
backup2 = {
    "from": "dir",
    "to": "dir"
}

# STARTING BOT #
print("[BACKUP BOT]: Launching program.")
online = True
client = commands.Bot(
    command_prefix="backup!",
    help_command=None
)


# DEFINING FUNCTIONS #
@client.event
async def on_ready():
    print("[BACKUP BOT]: Program ready.")  # Announcing bot ready
    await client.change_presence(  # Changing bot status to indicate bot state
        activity=discord.Game(
            name="STATUS: IDLE"
        ),
        status=discord.Status.idle
    )


@client.command(name="start")
@commands.has_permissions(administrator=True)
async def start(ctx: commands.Context):
    """backup!start
    When used, starts a backup loop.

    Parameter: None.
    Permissions required: administrator
    """
    while online:

        # Variables
        time_now = datetime.datetime.now()  # The time now
        exp = "null"

        print("\n[BACKUP BOT]: Backup command called, executing backup tasks.")
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name='STATUS: WORKING'
            ),
            status=discord.Status.online
        )

        # Backing up using information from backup1
        print("[BACKUP TASKS]: Starting first backup.")
        first_backup = False
        try:
            first_backup = backup_func(info, backup1["from"], backup1["to"])
        except Exception as e:
            exp = e.message
        if first_backup is not True:
            print("[BACKUP TASK]: Unexpected error has occurred during the first backup! Aborting tasks")
            await client.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name='STATUS: ERROR'
                ),
                status=discord.Status.dnd
            )

            embed = discord.Embed(  # Constructing embed
                title="FIRST BACKUP FAILED",
                description="```{exception}```".format(exception=exp)
            ).set_footer(text=str(time_now))
            await ctx.channel.send(embed)  # Sending it

            return

        print("[BACKUP TASK]: First backup complete.")

        # Backing up using information from backup2
        print("[BACKUP TASK]: Starting second backup.")
        second_backup = False
        try:
            second_backup = backup_func(info, backup2["from"], backup2["to"])
        except Exception as e:
            exp = e.message

        if second_backup is not True:
            print("[BACKUP TASK]: Unexpected error has occurred during the second backup! Aborting tasks")
            await client.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name='STATUS: ERROR'
                ),
                status=discord.Status.dnd
            )

            embed = discord.Embed(  # Constructing embed
                title="SECOND BACKUP FAILED",
                description="```{exception}```".format(exception=exp)
            ).set_footer(text=str(time_now))
            await ctx.channel.send(embed)  # Sending it
            return

        print("[BACKUP TASK]: Second backup complete.")

        # Cleaning up
        print("[BACKUP TASK]: Tasks complete. Cleaning up")
        next_backup = str(time_now + datetime.timedelta(seconds=loop_period))  # The time of next backup

        embed = discord.Embed(  # Constructing embed
            title="BACKUP COMPLETE",
            description="Next backup: {time}".format(time=next_backup)
        ).set_footer(text=str(time_now))
        await ctx.channel.send(embed)  # Sending it

        await client.change_presence(  # Setting bot status to IDLE
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name='STATUS: IDLE'
            ),
            status=discord.Status.idle
        )
        await asyncio.sleep(loop_period)


@client.command(name="stop")
@commands.has_permissions(administrator=True)
async def stop(ctx: commands.Context):
    """backup!stop
    When used, stops backup from looping.

    Parameter: None
    Permissions required: administrator
    """
    await ctx.channel.send("Stopping the backup sequence.")
    global online
    online = False
    print("Backup stopped (paused)")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name='KC Backup Bot 1.0, play.kingdomscrusade.net Backup status: paused'
        )
    )


@client.command(name="restart")
@commands.has_permissions(administrator=True)
async def restart(ctx: commands.Context):
    """backup!restart
    When used, set Boolean "online" to "True".

    Parameter: None
    Permission required: administrator
    """
    await ctx.channel.send("Restarting the backup sequence (you need to run backup!start to set it auto going again).")
    global online
    online = True
    print("Backup started (unpaused)")
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name='Restarting backups.'))


@client.event
async def on_error(ctx):
    if type(ctx) is FileNotFoundError:
        await ctx.send("Backup complete.")


client.run(bot_token)
