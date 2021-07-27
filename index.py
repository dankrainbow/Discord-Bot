import discord
import time
import inspect
from discord.ext import commands
import os
import contextlib
import io
import textwrap
import ast
import asyncio
from discord.ext.commands.bot import AutoShardedBot
import requests
import random
import string
bot = commands.Bot(command_prefix='>')
ownersname = 'Dank Rainbow'
@bot.event
async def on_ready():
    print(f"Bot is ready")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="prefix is >"))

@bot.command(name = 'say', pass_context=True)
async def say(ctx, *, arg):
    """says something"""
    embed=discord.Embed(title="Response", description=(arg), color=discord.Color.green())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text="I was made to say this because of: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@bot.command(name="eval", usage=">eval <code>")
@commands.is_owner()
async def eval_(ctx, *, cmd):
    """An owner command to run pieces of code. Made for testing"""
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'client': ctx.bot,
        'discord': discord,
        'commands': commands,
        'asyncio': asyncio,
        'ctx': ctx,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    embed=discord.Embed(title="Eval Result", description=(result), color=discord.Color.green())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
    return
@bot.command(name = 'ping')
async def ping(ctx):
    """Sends bot's latency in milliseconds."""
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")
@bot.command(name = 'info')
async def info(ctx):
    """Supplies Basic information about the bot.""" 
    embed=discord.Embed(title="Info", color=discord.Color.blue())
    embed.add_field(name="Library", value="discord.py", inline=True)
    embed.add_field(name="Servers", value=f"{len(bot.guilds)}", inline=True)
    await ctx.send(embed=embed)
    await ctx.send(content=f"ℹ About **{bot.user}** | **1.0.0**")
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
        """shuts down the bot. Owner only"""
        await ctx.send("yes sir. shutting down")
        asyncio.sleep(1)
        try:
            await ctx.send("farewell!")
            asyncio.sleep(1.5)
            await bot.logout()
        except:
            await ctx.send("Your not owner. not shutting down")
            bot.clear()
@bot.command()
async def nitroinfo(ctx, *, code):
    """Gets the information from a nitro code using discords API."""
    x = requests.get(f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}")
    await ctx.send(x.json())
@bot.command('nitro')
async def nitro(ctx):
  """Generates a random nitro code. Made for fun!""" 
  code = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(24)])
  await ctx.send(f"discord.gift/{code}")
@bot.command()
async def hyperlink(ctx, *, link):
    """Puts https:// infront of a link. good for lazy people."""
    await ctx.send(f"https://{link}")
    asyncio.sleep(0.5)
    await ctx.send("enjoy!")
@bot.command()
async def whoismycreator(ctx):
    """Who is the creator? Run this command to find out."""
    await ctx.send(f"Hey! {ctx.author.mention}")
    await ctx.send(f'My Creator is {ownersname}')
bot.run("put your token here")
