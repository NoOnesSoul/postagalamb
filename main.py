import random
import discord
from discord.ext import commands
import art

import settings
import nevsor
import hangman


szinek = [
    discord.Colour.green(),
    discord.Colour.blue(),
    discord.Colour.purple(),
    discord.Colour.red(),
    discord.Colour.magenta()
]


client = commands.Bot(command_prefix = settings.Prefix, help_command=None)

@client.event
async def on_ready():
    print('onliné')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=settings.BotStatus))


@client.command(aliases=["commands", "cmds", "cmd"])
async def help(ctx):
    szin = random.randint(0,4)
    helpembed = discord.Embed(colour=szinek[szin], timestamp=ctx.message.created_at, title="Parancsok")
    helpembed.add_field(name="Dice", value="Kiír egy random számot 1 és 6 között.\nHasználat:\n```/dice```")
    helpembed.add_field(name="Coinflip", value="Fej vagy írás.\nHasználat:\n```/coin\n/coinflip```")
    helpembed.add_field(name="Slotmachine", value="Félkarú rabló.\nHasználat:\n```/slotmachine\n/slot```")
    helpembed.add_field(name="User info", value="Kiírja egy adott felhasználó adatait.\nHasználat:\n```/whois @valaki\n/userinfo @valaki```")
    helpembed.add_field(name="Hangman", value="Játszik egy akasztófa játékot.\nA parancs futtatása után üzenetenként egy betűt szabad írni.\nHasználat:\n```/akasztofa [valami]```\n```a```\n```b```\n```c```")
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
    szin = random.randint(0,4)
    elso = random.randint(0,8)
    masodik = random.randint(0,8)
    harmadik = random.randint(0,8)

    slotembed = discord.Embed(colour=szinek[szin], timestamp=ctx.message.created_at, title="Slot machine")
    if elso == masodik == harmadik:
        slotembed.add_field(name="Nyertél", value=f"{icons[elso]} {icons[masodik]} {icons[harmadik]}")

    else:
        slotembed.add_field(name="Vesztettél", value=f"{icons[elso]} {icons[masodik]} {icons[harmadik]}")
    await ctx.send(embed=slotembed)

@client.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    szin = random.randint(0,4)
    if not member:
        member = ctx.message.author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=szinek[szin], timestamp=ctx.message.created_at,
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

@client.command()
async def akasztofa(ctx, arg):
    guesses = []
    rosszak = ""
    eddigjo = []
    jok = []
    szobetui = []
    szo = ""
    for i in arg:
        szobetui.append(i)
    guessed = ""
    for i in range(len(szobetui)):
        guessed += "_ "
        eddigjo.append("_ ")
    for i in szobetui:
        szo += i
    szin = random.randint(0,4)
    hangembed = discord.Embed(colour=szinek[szin], title="Akasztófa")
    hangembed.add_field(name="Helyzet:", value=hangman.status[len(guesses)])
    hangembed.add_field(name="Szó:", value=f"```{guessed.strip()}```")
    hangembed.add_field(name="Rossz:", value="Eddig semmi.")

    await ctx.message.delete()
    await ctx.send(embed=hangembed)


    rontasok = 0
    fasza = 0
    while rontasok <= len(hangman.status)-2 and fasza <= len(szobetui)-1:
        hangembed1 = discord.Embed(colour=szinek[szin], title="Akasztófa")
        msg = await client.wait_for('message', check=None, timeout=30)
        if msg:
            if msg.content in szobetui:
                if msg.content not in jok:
                    jok.append(msg.content)
                    for i in range(len(szobetui)):
                        if msg.content == szobetui[i]:
                            fasza += 1
                            eddigjo[i] = f"{szobetui[i]} "

                    jej = "".join(eddigjo)

                    if rontasok > 0:
                        hangembed1.add_field(name="Helyzet:", value=hangman.status[len(guesses)])
                        hangembed1.add_field(name="Szó:", value=f"```{jej.strip()}```")
                        hangembed1.add_field(name="Rossz:", value=rosszak.strip(", "))
                    else:
                        hangembed1.add_field(name="Helyzet:", value=hangman.status[len(guesses)])
                        hangembed1.add_field(name="Szó:", value=f"```{jej.strip()}```")
                        hangembed1.add_field(name="Rossz:", value="Eddig semmi.")
                    szin = random.randint(0,4)
                    await ctx.send(embed=hangembed1)
                else:
                    await ctx.send("Ezt a betűt már próbáltad.")
                    

            else:
                if msg.content not in guesses:
                    rosszak += f"{msg.content}, "
                    guesses.append(msg.content)
                    rontasok += 1
                    hangembed1.add_field(name="Helyzet:", value=hangman.status[len(guesses)])
                    if fasza == 0:
                        hangembed1.add_field(name="Szó:", value=f"```{guessed.strip()}```")
                    else:
                        hangembed1.add_field(name="Szó:", value=f"```{jej.strip()}```")
                    hangembed1.add_field(name="Rossz:", value=rosszak.strip(", "))

                    szin = random.randint(0,4)
                    await ctx.send(embed=hangembed1)
                else:
                    await ctx.send("Ezt a betűt már próbáltad.")
        
        elif TimeoutError: #Ez itt nem működik. Ha senki nem válaszol,az alább látható üzenetet kéne küldenie és vége lenne a játéknak.
            await ctx.send("Túl sokáig nem válaszolt senki.")
            break
        
    if fasza == len(szobetui):
        szin = random.randint(0,4)
        hangembed2 = discord.Embed(colour=szinek[szin], title="Akasztófa")
        hangembed2.add_field(name="Gratulálunk!", value="Megnyerted az akasztófa játékot! 🎉🎉")
        await ctx.send(embed=hangembed2)
    else:
        amivolt = "".join(szobetui)
        szin = random.randint(0,4)
        hangembed2 = discord.Embed(colour=szinek[szin], title="Akasztófa")
        hangembed2.add_field(name="Gratulálunk!", value=f"Vesztettél.\nA szó `{amivolt}` volt.")
        await ctx.send(embed=hangembed2)
    

client.run(settings.TOKEN)
