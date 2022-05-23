import random
from unicodedata import name
import discord
from discord.ext import commands
import art

import settings
import nevsor

client = commands.Bot(command_prefix = settings.Prefix, help_command=None)

@client.event
async def on_ready():
    print('onliné')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=settings.BotStatus))


@client.command(aliases=["commands", "cmds", "cmd"])
async def help(ctx):
    helpembed = discord.Embed(colour=discord.Colour.green(), timestamp=ctx.message.created_at, title="Parancsok")
    helpembed.add_field(name="Dice", value="Kiír egy random számot 1 és 6 között.\nHasználat:\n```/dice```")
    helpembed.add_field(name="Coinflip", value="Fej vagy írás.\nHasználat:\n```/coin\n/coinflip```")
    helpembed.add_field(name="Slotmachine", value="Félkarú rabló.\nHasználat:\n```/slotmachine\n/slot```")
    helpembed.add_field(name="User info", value="Kiírja egy adott felhasználó adatait.\nHasználat:\n```/whois @valaki\n/userinfo @valaki```")
    await ctx.send(embed=helpembed)



@client.command()
async def dice(ctx):
    await ctx.send(random.randint(1, 6))

@client.command(aliases=["coin"])
async def coinflip(ctx):
    coin = random.randint(0,1)
    if coin == 0:
        await ctx.send("Fej")
    else:
        await ctx.send("Írás")

@client.command(aliases=["slot", "slut"])
async def slotmachine(ctx):
    icons = [
        "🔷", "🍋", "🍉",
        "❤️", "7️⃣", "🔔",
        "🍀", "🍒", "🚥"
    ]
    elso = random.randint(0,8)
    masodik = random.randint(0,8)
    harmadik = random.randint(0,8)

    slotembed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at, title="Slot machine")
    if elso == masodik == harmadik:
        slotembed.add_field(name="Nyertél", value=f"{icons[elso]} {icons[masodik]} {icons[harmadik]}")

    else:
        slotembed.add_field(name="Vesztettél", value=f"{icons[elso]} {icons[masodik]} {icons[harmadik]}")
    await ctx.send(embed=slotembed)

@client.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)

@client.command()
async def ascii(ctx, arg):
    my_art = art.text2art(arg)
    print(my_art)
    await ctx.send(my_art)

@client.command()
async def hetes(ctx, arg):
    await ctx.send(nevsor.hetesek(int(arg)-1, nevsor.nevek))

client.run(settings.TOKEN)