import discord
from discord.ext import commands
from backup_func import *
from backup_func2 import *
print ("Starting.")
client = commands.Bot(command_prefix="backup!", help_command=None)


@client.event
async def on_ready():
    print ("Backup Bot is ready.")
    await client.change_presence(activity=discord.Game(name='KC Backup Bot 1.0'))


@client.command(name="start")
@commands.has_permissions(administrator=True)
async def start(ctx: commands.Context):
    try:
        print ("Backup starting.")
        await ctx.channel.send("Backup starting.")
        #from backup_func import backup_func
        backup_func()
    except OSError as err:
        await ctx.send("First backup complete.")
        print ("Backup Complete")
        try:
            await ctx.send("Starting second backup...")
            print ("Second backup starting.")
            backup_func2()
        except OSError as err:
            print(err)
            await ctx.send("Backup complete.")
            print ("Backup Complete")
            raise exception 
@client.event
async def on_error(ctx, event, *args, **kwargs):
    if isinstance(FileNotFoundError):
        await ctx.send("Backup complete.")
client.run("TOKEN")

