import random
from turtle import title
from unicodedata import name
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import art
import requests

import settings
import nevsor
import hangman
import foghato


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
async def help(ctx, arg = None):
    szin = random.randint(0,4)
    helpembed = discord.Embed(colour=szinek[szin], timestamp=ctx.message.created_at, title="Parancsok", description="Többi parancs leírásához használd ezeket:\n`/help fun`\n`/help eco`")
    if not arg:
        helpembed.add_field(name="Hetesek", value="Kiírja a megadott számú hét hetesei nevét.\nHasználat:\n```/hetesek\n/hetes```")
        helpembed.add_field(name="Dice", value="Kiír egy random számot 1 és 6 között.\nHa jól tippelsz, a feltett pénzed hatszorosát kapod vissza.\nHasználat:\n```/dice [tipp] [pénz]```")
        helpembed.add_field(name="Coinflip", value="Fej vagy írás.\nHa jól tippelsz, a feltett pénzed háromszorosát kapod vissza.\nHasználat:\n```/coin [tipp] [pénz]\n/coinflip [tipp] [pénz]```")
        helpembed.add_field(name="Slotmachine", value="Félkarú rabló.\nHasználat:\n```/slotmachine [pénz]\n/slot [pénz]```")
        helpembed.add_field(name="User info", value="Kiírja egy adott felhasználó adatait.\nHasználat:\n```/whois @valaki\n/userinfo @valaki```")
    if arg == "fun":
        helpembed.add_field(name="Kimi says", value="Küld egy random Kimi Räikkönen idézetet.\nHasználat:\n```/kimi\n/raikonnen\n/f1quote```")
        helpembed.add_field(name="Fun facts", value="Küld egy random tényt.\nHasználat:\n```/tények\n/uselessfact\n/useless\n/fact\n/tény\n/funfact```")
        helpembed.add_field(name="Catboy", value="Küld egy random cicafiú képet UwU\nHasználat:\n```/catboy\n/cicafiú\n/cicafiu```")
        helpembed.add_field(name="Fox", value="Küld egy random rókás képet.\nHasználat:\n```/fox\n/róka```")
        helpembed.add_field(name="Dog", value="Küld egy random kutyás képet.\nHasználat:\n```/dog\n/kutya\n/lutyuly\n/tilimancs```")
        helpembed.add_field(name="Hangman", value="Játszik egy akasztófa játékot.\nA parancs futtatása után üzenetenként egy betűt szabad írni.\nHasználat:\n```/akasztofa [valami]```\n```a```\n```b```\n```c```")
    if arg == "eco" or arg == "economy":
        helpembed.add_field(name="Work", value="5 percenként használható. Random pénzt kapsz érte.\nHasználat:\n```/work```")
        helpembed.add_field(name="Shop", value="Kiírja a megvehető tárgyak listáját és azok árát.\nHasználat:\n```/shop```")
        helpembed.add_field(name="Buy", value="Megveheted a boltban lévő tárgyakat.\nHasználat:\n```/buy [tárgy]```")
        helpembed.add_field(name="Sell", value="Leltáradban lévő tárgyakat el tudod adni.\nHasználat:\n```/sell [tárgy]```")
        helpembed.add_field(name="Fish", value="Horgászhatsz.\nHasználat:\n```/fish```")
        helpembed.add_field(name="Inventory", value="Kiíratja a leltáradban lévő tárgyak listáját.\nHasználat:\n```/inv\n/inventory```")
        helpembed.add_field(name="Balance", value="Kiíratja, hogy mennyi pénzed van.\nHasználat:\n```/bal\n/balance```")
    await ctx.send(embed=helpembed)

@client.command()
async def dice(ctx, arg = None, arg1 = None):
    if arg and arg1:
        eco = open(f"./economydata/{ctx.message.author.id}.txt", "r")
        tarca = 0
        for i in eco:
            tarca += int(i)
        eco.close()
        if int(arg) > 6 or int(arg) < 1:
            await ctx.send("A megadott szám nem érvényes. 1-től 6-ig lehet választani.")
        else:
            if tarca >= int(arg1) and int(arg1) > 0:
                eco = open(f"./economydata/{ctx.message.author.id}.txt", "a")
                print(f"-{arg1}", file=eco)
                eco.close()
                dobas = random.randint(1, 6)
                if dobas == int(arg):
                    eco = open(f"./economydata/{ctx.message.author.id}.txt", "a")
                    print((int(arg1)*6), file=eco)
                    eco.close()
                    await ctx.send(f"Eredmény: {dobas}\n**Nyertél!**\n> Ennyit tettél fel: {arg1}ft\n> Ennyit nyertél: {int(arg1)*6}ft")
                else:
                    await ctx.send(f"Eredmény: {dobas}\nVesztettél.\n> Ennyit tettél fel: {arg1}ft")
            else:
                await ctx.send("Nincs annyi pénzed.")
    else:
        await ctx.send("Add meg a tipped és,hogy mennyit teszel fel.\nPélda:\n```/dice 5 10```")

@client.command(aliases=["coin"])
async def coinflip(ctx, arg = None, arg1 = None):
    if arg and arg1:
        eco = open(f"./economydata/{ctx.message.author.id}.txt", "r")
        tarca = 0
        for i in eco:
            tarca += int(i)
        eco.close()
        if arg != "fej" and arg != "írás":
            await ctx.send("Csak `fej` vagy `írás` adható meg tippnek.")
        else:
            if (tarca >= int(arg1) and int(arg1) > 0):
                eco = open(f"./economydata/{ctx.message.author.id}.txt", "a")
                print(f"-{arg1}", file=eco)
                eredmeny = ""
                coin = random.randint(0,1)
                if coin == 0:
                    eredmeny = "fej"
                else:
                    eredmeny = "írás"
                if arg == eredmeny:
                    print((int(arg1)*3), file=eco)
                    await ctx.send(f"Nyertél!\n> Ennyit tettél fel: {arg1}ft\n> Ennyit nyertél: {int(arg1)*3}")
                else:
                    await ctx.send(f"Vesztettél.\n> Ennyit tettél fel: {arg1}ft")
                eco.close()
            else:
                await ctx.send("Nincs annyi pénzed.")
    else:
        await ctx.send("Add meg a tipped és, hogy mennyit teszel fel.\nPélda:\n```/coin fej 10```")
    

@client.command(aliases=["slot", "slut"])
async def slotmachine(ctx, arg = None):
    if arg:
        eco = open(f"./economydata/{ctx.message.author.id}.txt", "r")
        tarca = 0
        for i in eco:
            tarca += int(i)
        eco.close()
        if tarca >= int(arg) and int(arg) > 0:
            eco = open(f"./economydata/{ctx.message.author.id}.txt", "a")
            print(f"-{arg}", file=eco)
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
                roleVer = 'Nyert slot machine-en' #role to add
                user = ctx.message.author #user
                role = roleVer # change the name from roleVer to role
                await user.add_roles(discord.utils.get(user.guild.roles, name=role))
                print((int(arg)*1000), file=eco)
                slotembed.add_field(name="Nyertél", value=f"{icons[elso]} {icons[masodik]} {icons[harmadik]}")
                slotembed.add_field(name="Ennyit tettél fel", value=f"{arg}ft")
                slotembed.add_field(name="Ennyit nyertél", value=f"{int(arg)*1000}ft")
            else:
                slotembed.add_field(name="Vesztettél", value=f"{icons[elso]} {icons[masodik]} {icons[harmadik]}")
                slotembed.add_field(name="Ennyit tettél fel", value=f"{arg}ft")
            await ctx.send(embed=slotembed)
            eco.close()
        else:
            await ctx.send("Nincs annyi pénzed.")
    else:
        await ctx.send("Add meg, hogy mennyit teszel fel.\nPélda:\n```/slot 10```")


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

@client.command(aliases = ["hetesek"])
async def hetes(ctx, arg = None):
    if arg:
        await ctx.send(nevsor.hetesek(int(arg)-1, nevsor.nevek))
    else:
        await ctx.send("Add meg a hét számát.\nPélda:\n```/hetes 41```")

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
            if len(msg.content) == 1:
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
            else:
                await ctx.send("Csak egy betűt adj meg.")
        
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
    
@client.command()
async def bal(ctx):
    tarca = 0
    penzek = []
    eco = open(f"./economydata/{ctx.message.author.id}.txt", "r")
    for i in eco:
        penzek.append(int(i))
    for i in penzek:
        tarca += i
    await ctx.send(f"**{ctx.message.author.name}** pénze: {tarca}ft")



items = [
        "weird_object", "maid_outfit", "sword", "fishing_pole", "axe", "pickaxe"
    ]
prices = [
    1000, 4000, 6000, 3000, 5000, 5000
]

@client.command()
async def shop(ctx):
    itemsandprices = [
        "weird_object - 1000ft", "maid_outfit - 4000ft", "sword - 6000ft", "fishing_pole - 3000ft", "axe - 5000ft", "pickaxe - 5000ft"
    ]
    await ctx.send("\n".join(itemsandprices))

@client.command()
async def buy(ctx, arg = None):
    if arg:
        if arg in items:
            eco = open(f"./economydata/{ctx.message.author.id}.txt", "r")
            tarca = 0
            for i in eco:
                tarca += int(i)
            eco.close()
            if tarca >= prices[items.index(arg)]:
                inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "a", encoding="utf-8")
                eco = open(f"./economydata/{ctx.message.author.id}.txt", "a")
                print(arg, file=inv)
                print(f"-{prices[items.index(arg)]}", file=eco)
                await ctx.send(f"Sikeresen megvásároltad ezt: **{arg}**")
                inv.close()
                eco.close()
            else:
                await ctx.send("Nincs elég pénzed a tárgyat megvásárolni.")
        else:
            await ctx.send("Az adott tárgy nincs a boltban.")
    else:
        await ctx.send("Add meg mit szeretnél vásárolni.\nPélda:\n```/buy sword```")

@client.command(aliases = ["inv"])
async def inventory(ctx):
    inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "r", encoding="utf-8")
    cuccok = []
    for i in inv:
        cuccok.append(i.strip())
    inventoryy = set(cuccok)
    invlist = list(inventoryy)
    invlist.sort()
    for i in range(len(invlist)):
        invlist[i] = f"{invlist[i]} ({cuccok.count(invlist[i])}db)"
    if len(cuccok) != 0:
        x = "\n"
    else:
        x = "- Még nincs semmije -"
    await ctx.send(f"**{ctx.message.author.name}** készlete:\n`{x.join(invlist)}`")

@client.command()
async def fish(ctx):
    inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "r", encoding="utf-8")
    cuccok = []
    for i in inv:
        cuccok.append(i.strip())
    inv.close()
    if "fishing_pole" in cuccok:
        rate = random.randint(0, len(foghato.foghatosag)-1)
        if foghato.foghatosag[rate] == "common_fish":
            inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "a")
            print("common_fish", file=inv)
            inv.close()
            await ctx.send("Fogtál egy átlagos halat.")
        elif foghato.foghatosag[rate] == "trash":
            inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "a")
            print("trash", file=inv)
            inv.close()
            await ctx.send("Szemét akadt a horgodra.")
        elif foghato.foghatosag[rate] == "nothing":
            await ctx.send("Nem fogtál semmit.")
        elif foghato.foghatosag[rate] == "rare_fish":
            kapas = random.randint(0, len(foghato.rare_fish)-1)
            if foghato.rare_fish[kapas] == "gold_fish":
                inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "a")
                print("gold_fish", file=inv)
                inv.close()
                await ctx.send("Fogtál egy aranyhalat.")
            elif foghato.rare_fish[kapas] == "puffer_fish":
                inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "a")
                print("puffer_fish", file=inv)
                inv.close()
                await ctx.send("Fogtál egy gömbhalat.")
            elif foghato.rare_fish[kapas] == "baby_shark":
                inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "a")
                print("baby_shark", file=inv)
                inv.close()
                await ctx.send("Fogtál egy bébi cápát.")
        elif foghato.foghatosag[rate] == "treasure":
            kincs = random.randint(0, len(foghato.treasure)-1)
            eco = open(f"./economydata/{ctx.message.author.id}.txt", "a")
            print(foghato.treasure[kincs], file=eco)
            eco.close()
            await ctx.send(f"Fogtál egy kincsesládát.\nA ládában {foghato.treasure[kincs]}ft volt.")
    else:
        await ctx.send("Először vegyél egy horgászbotot.\n```/buy fishing_pole```")

@client.command()
async def chop(ctx):
    inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "r", encoding="utf-8")
    cuccok = []
    for i in inv:
        cuccok.append(i.strip())
    inv.close()
    if "axe" in cuccok:
        amount = random.randint(1,5)
        inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "a")
        for i in range(amount):
            print("wood", file=inv)
        inv.close()
        await ctx.send(f"Fát vágtál. Kaptál {amount}db fát.")
    else:
        await ctx.send("Először vegyél egy baltát.\n```/buy axe```")

@client.command()
async def mine(ctx):
    inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "r", encoding="utf-8")
    cuccok = []
    for i in inv:
        cuccok.append(i.strip())
    inv.close()
    if "pickaxe" in cuccok:
        ercek = [
            "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone",
            "coal", "coal", "coal", "coal", "coal", "coal",
            "iron", "iron", "iron", "iron",
            "diamond", "xbox_live", "iron"
        ]
        erc = random.randint(0,len(ercek)-1)
        amount = random.randint(1,3)
        inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "a")
        if ercek[erc] == "stone":
            for i in range(amount):
                print("stone", file=inv)
            inv.close()
            await ctx.send(f"Bányásztál. Kaptál {amount}db követ.")
        elif ercek[erc] == "coal":
            for i in range(amount):
                print("coal", file=inv)
            inv.close()
            await ctx.send(f"Bányásztál. Kaptál {amount}db szenet.")
        elif ercek[erc] == "iron":
            for i in range(amount):
                print("iron", file=inv)
            inv.close()
            await ctx.send(f"Bányásztál. Kaptál {amount}db vasat.")
        elif ercek[erc] == "diamond":
            for i in range(amount):
                print("diamond", file=inv)
            inv.close()
            await ctx.send(f"Bányásztál. Kaptál {amount}db gyémántot.")
        elif ercek[erc] == "xbox_live":
            print("xbox_live", file=inv)
            inv.close()
            await ctx.send(f"Bányásztál. Kaptál 1db XBOX LIVE-ot.")
    else:
        await ctx.send("Először vegyél egy csákányt.\n```/buy pickaxe```")

@client.command()
async def sell(ctx, arg = None):
    if arg:
        if arg == "trash" or arg == "weird_object" or arg == "axe" or arg == "coal" or arg == "iron" or arg == "common_fish" or\
            arg == "maid_outfit" or arg == "pickaxe" or arg == "sword" or arg == "stone" or arg == "wood":
            eco = open(f"./economydata/{ctx.message.author.id}.txt", "a")
            ar = random.randint(100,500)
            print(ar, file=eco)
            eco.close()
            inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "r")
            cuccok = []
            for i in inv:
                cuccok.append(i.strip())
            inv.close()
            if arg in cuccok:
                cuccok.remove(arg)
                inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "w")
                z = "\n"
                print(z.join(cuccok), file=inv)
                inv.close()
                await ctx.send(f"Sikeresen eladtad ezt: **{arg}**\nEnnyit kaptál érte: **{ar}ft**")
            else:
                await ctx.send("Nincs nálad ilyen tárgy.")
        if arg == "diamond" or arg == "xbox_live":
            eco = open(f"./economydata/{ctx.message.author.id}.txt", "a")
            ar = random.randint(10000,30000)
            print(ar, file=eco)
            eco.close()
            inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "r")
            cuccok = []
            for i in inv:
                cuccok.append(i.strip())
            inv.close()
            if arg in cuccok:
                cuccok.remove(arg)
                inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "w")
                z = "\n"
                print(z.join(cuccok), file=inv)
                inv.close()
                await ctx.send(f"Sikeresen eladtad ezt: **{arg}**\nEnnyit kaptál érte: **{ar}ft**")
            else:
                await ctx.send("Nincs nálad ilyen tárgy.")
        if arg == "baby_shark" or arg == "puffer_fish" or arg == "gold_fish":
            eco = open(f"./economydata/{ctx.message.author.id}.txt", "a")
            ar = random.randint(5000,8000)
            print(ar, file=eco)
            eco.close()
            inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "r")
            cuccok = []
            for i in inv:
                cuccok.append(i.strip())
            inv.close()
            if arg in cuccok:
                cuccok.remove(arg)
                inv = open(f"./inventorydata/{ctx.message.author.id}.txt", "w")
                z = "\n"
                print(z.join(cuccok), file=inv)
                inv.close()
                await ctx.send(f"Sikeresen eladtad ezt: **{arg}**\nEnnyit kaptál érte: **{ar}ft**")
            else:
                await ctx.send("Nincs nálad ilyen tárgy.")
        #else:
            #await ctx.send("Nincs nálad ilyen tárgy.")
    else:
        await ctx.send("Add meg mit szeretnél eladni.\nPélda:\n```/sell trash```")
"""
@client.command()
async def teszt(ctx):
    await ctx.send(file = discord.File(f"./economydata/{ctx.message.author.id}.txt"))
"""

@client.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def work(ctx):
    payment = random.randint(100, 500)
    eco = open(f"./economydata/{ctx.message.author.id}.txt", "a")
    print(payment, file=eco)
    eco.close()
    worked = discord.Embed(title="Dolgoztál.", description=f"Kaptál érte **{payment}ft**-ot.", colour=discord.Colour.green())
    await ctx.send(embed=worked)

@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        perc = ""
        if error.retry_after > 60:
            perc = f"{int(error.retry_after/60)} perc"
        else:
            perc = f"{int(error.retry_after)} másodperc"
        em = discord.Embed(title=f"Várnod kell.", description=f"Próbáld meg {perc} múlva.", colour=discord.Colour.red())
        await ctx.send(embed=em)

# API parancsok


@client.command(aliases=["róka"])
async def fox(ctx):
    foxpic = requests.get("https://randomfox.ca/floof/").json()['image']

    embed = discord.Embed(colour=discord.Colour.dark_gold(), timestamp=ctx.message.created_at,
                          title=f"Róka API")
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.set_image(url=foxpic)
    await ctx.send(embed=embed)


@client.command(aliases=["kutya", "lutyuly", "tilimancs"])
async def dog(ctx):
    dogpic = requests.get("https://random.dog/woof.json").json()['url']

    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"Kutya API")
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.set_image(url=dogpic)
    await ctx.send(embed=embed)


@client.command(aliases=["cicafiú", "cicafiu"])
async def catboy(ctx):
    catboypic = requests.get("https://api.catboys.com/img").json()['url']

    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"Catboy API")
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.set_image(url=catboypic)
    await ctx.send(embed=embed)


@client.command(aliases=["tények", "uselessfact"])
async def useless(ctx):
    uselessFact = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()['text']
    uselessSource = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()['source_url']

    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"Useless API")
    embed.add_field(name="Useless Fact!", value=f"{uselessFact}\n[Source]({uselessSource})")
    embed.set_footer(text=f"Requested by {ctx.author}")

    await ctx.send(embed=embed)


@client.command(aliases=["tény", "fact"])
async def funfact(ctx):
    uselessFact = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()['text']
    uselessSource = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()['source_url']

    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"Useless API")
    embed.add_field(name="Useless Fact!", value=f"{uselessFact}\n[Source]({uselessSource})")
    embed.set_footer(text=f"Requested by {ctx.author}")

    await ctx.send(embed=embed)


@client.command(aliases=["raikonnen", "f1quote"])
async def kimi(ctx):
    kimiqList = requests.get("https://kimiquotes.herokuapp.com/quotes").json()
    i = random.randint(0, len(kimiqList))
    kimiquote = kimiqList[i]['quote']

    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"Kimi Räikkönen Radio API")
    embed.add_field(name="Kimi Räikkönen says...", value=kimiquote)
    embed.set_footer(text=f"Requested by {ctx.author}")

    await ctx.send(embed=embed)

client.run(settings.TOKEN)
