from discord.ext import commands
import discord
import random
import asuna_api
import math
import aiohttp
import gtts, io, chardet
import chardet
import mystbin

class Extra(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command(brief="a way to look up minecraft usernames",help="using the official minecraft api, looking up minecraft information has never been easier(tis only gives minecraft account history relating to name changes)")
  async def mchistory(self,ctx,*,args=None):
    
    if args is None:
      await ctx.send("Please pick a minecraft user.")

    if args:
      asuna = asuna_api.Client()
      minecraft_info=await asuna.mc_user(args)
      await asuna.close()
      embed=discord.Embed(title=f"Minecraft Username: {args}",color=random.randint(0, 16777215))
      embed.set_footer(text=f"Minecraft UUID: {minecraft_info.uuid}")
      embed.add_field(name="Orginal Name:",value=minecraft_info.name)
      y = 0
      for x in minecraft_info.history:
        if y > 0:
          embed.add_field(name=f"Username:\n{x['name']}",value=f"Date Changed:\n{x['changedToAt']}\n \nTime Changed: \n {x['timeChangedAt']}")

        y = y + 1
      embed.set_author(name=f"Requested by {ctx.author}",icon_url=(ctx.author.avatar_url))
      await ctx.send(embed=embed)

  @commands.command(help="This gives random history using Sp46's api.",brief="a command that uses SP46's api's random history command to give you random history responses")
  async def random_history(self,ctx,*,args=None):
    if args is None:
      args = 1
    asuna = asuna_api.Client()
    response = await asuna.random_history(args)
    await asuna.close()
    for x in response:
      await ctx.send(f":earth_africa: {x}")

  @commands.command(brief="gives you the digits of pi that Python knows")
  async def pi(self,ctx):
    await ctx.send(math.pi)

  @commands.command(brief="reverses text")
  async def reverse(self,ctx,*,args=None):
    if args:
      await ctx.send(args[::-1])
    if args is None:
      await ctx.send("Try sending actual to reverse")

  @commands.command(brief="Oh no Dad Jokes, AHHHHHH!")
  async def dadjoke(self,ctx):
    async with aiohttp.ClientSession() as session:
      async with session.get("https://icanhazdadjoke.com/",headers={"Accept": "application/json"}) as response:
        joke=await response.json()
    embed = discord.Embed(title="Random Dad Joke:",color=random.randint(0, 16777215))
    embed.set_author(name=f"Dad Joke Requested by {ctx.author}",icon_url=(ctx.author.avatar_url))
    embed.add_field(name="Dad Joke:",value=joke["joke"])
    embed.set_footer(text=f"View here:\n https://icanhazdadjoke.com/j/{joke['id']}")
    await ctx.send(embed=embed)

  @commands.command(brief="gets a panel from the xkcd comic",aliases=["astrojoke","astro_joke"])
  async def xkcd(self,ctx):
    async with aiohttp.ClientSession() as session:
      async with session.get("https://xkcd.com/info.0.json") as response:
        info=await response.json()

    num = random.randint(1,info["num"])
    async with aiohttp.ClientSession() as session:
      async with session.get(f"https://xkcd.com/{num}/info.0.json") as comic:
        data=await comic.json()
        title = data["title"]
        embed=discord.Embed(title=f"Title: {title}",color=random.randint(0, 16777215))
        embed.set_image(url=data["img"])
        embed.set_footer(text=f"Made on {data['month']}/{data['day']}/{data['year']}")
        await ctx.send(embed=embed)

  @commands.command(help="Gives advice from JDJG api.",aliases=["ad"])
  async def advice(self,ctx):
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://jdjgapi.nom.mu/api/advice') as r:
        res = await r.json()
    embed = discord.Embed(title = "Here is some advice for you!",color=random.randint(0, 16777215))
    embed.add_field(name = f"{res['text']}", value = "Hopefully this helped!")
    embed.set_footer(text="Powered by JDJG Api!")
    await ctx.send(embed=embed)

  @commands.command(help="gives random compliment")
  async def compliment(self,ctx):
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://jdjgapi.nom.mu/api/compliment') as r:
        res = await r.json()
    embed = discord.Embed(title = "Here is a compliment:",color=random.randint(0, 16777215))
    embed.add_field(name = f"{res['text']}", value = "Hopefully this helped your day!")
    embed.set_footer(text="Powered by JDJG Api!")
    await ctx.send(embed=embed)

  @commands.command(help="gives an insult")
  async def insult(self,ctx):
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://jdjgapi.nom.mu/api/insult') as r:
        res = await r.json()
    embed = discord.Embed(title = "Here is a insult:",color=random.randint(0, 16777215))
    embed.add_field(name = f"{res['text']}", value = "Hopefully this Helped?")
    embed.set_footer(text="Powered by JDJG Api!")
    await ctx.send(embed=embed)

  @commands.command(help="gives response to slur")
  async def noslur(self,ctx):
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://jdjgapi.nom.mu/api/noslur') as r:
        res = await r.json()
    embed = discord.Embed(title = "Don't Swear",color=random.randint(0, 16777215))
    embed.add_field(name = f"{res['text']}", value = "WHY MUST YOU SWEAR?")
    embed.set_footer(text="Powered by JDJG Api!")
    await ctx.send(embed=embed)

  @commands.command(help="gives random message",aliases=["rm"])
  async def random_message(self,ctx):
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://jdjgapi.nom.mu/api/randomMessage') as r:
        res = await r.json()
    embed = discord.Embed(title = "Random Message:",color=random.randint(0, 16777215))
    embed.add_field(name="Here:",value=res["text"])
    embed.set_footer(text="Powered by JDJG Api!")
    await ctx.send(embed=embed)

  async def google_tts(self,ctx,text):
    await ctx.send("if you have a lot of text it may take a bit")
    mp3_fp = io.BytesIO()
    tts=gtts.gTTS(text=text,lang='en')
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    file = discord.File(mp3_fp,"tts.mp3")
    await ctx.send(file=file)

  @commands.command(help="a command to talk to Google TTS",brief="using the power of the GTTS module you can now do tts")
  async def tts(self,ctx,*,args=None):
    if args:
      await self.google_tts(ctx,args)
    
    if ctx.message.attachments:
      for x in ctx.message.attachments:
        file=await x.read()
        if len(file) > 0:
          encoding=chardet.detect(file)["encoding"]
          if encoding:
            text = file.decode(encoding)
            await self.google_tts(ctx,text)
          if encoding is None:
            await ctx.send("it looks like it couldn't decode this file, if this is an issue DM JDJG Inc. Official#3439")
        if len(file ) < 1:
          await ctx.send("this doesn't contain any bytes.")
          

    if args is None and len(ctx.message.attachments) < 1:
      await ctx.send("You didn't specify any value.")

  @commands.command(help="learn about a secret custom xbox controller",brief="this will give you a message of JDJG's classic wanted xbox design.")
  async def secret_controller(self,ctx):
    embed = discord.Embed(color=random.randint(0, 16777215))
    embed.set_author(name="Secret Xbox Image:")
    embed.add_field(name="Body:",value="Zest Orange")
    embed.add_field(name="Back:",value="Zest Orange")
    embed.add_field(name="Bumpers:",value="Zest Orange")
    embed.add_field(name="Triggers:",value="Zest Orange")
    embed.add_field(name="D-pad:",value="Electric Green")
    embed.add_field(name="Thumbsticks:",value="Electric Green")
    embed.add_field(name="ABXY:",value="Colors on Black")
    embed.add_field(name="View & Menu:",value="White on Black")
    embed.add_field(name="Engraving(not suggested):",value="JDJG Inc.")
    embed.add_field(name="Disclaimer:",value="I do not work at microsoft,or suggest you buy this I just wanted a place to represent a controller that I designed a while back.")
    embed.set_image(url="https://i.imgur.com/QCh4M2W.png")
    embed.set_footer(text="This is Xbox's custom controller design that I picked for myself.\nXbox is owned by Microsoft. I don't own the image")
    await ctx.send(embed=embed)

  @commands.command(brief="repeats what you say",help="a command that repeats what you say the orginal message is deleted")
  async def say(self,ctx,*,args=None):
    if args:
      args = discord.utils.escape_mentions(args)
      args=discord.utils.escape_markdown(args,as_needed=False,ignore_links=False)
      try:
        await ctx.message.delete()

      except discord.errors.Forbidden:
        pass

      await ctx.send(args)
    
    if args is None:
      await ctx.send("You didn't give us any text to use.")
  
  @commands.command(brief="a command to backup text",help="please don't upload any private files that aren't meant to be seen")
  async def text_backup(self,ctx):
    if ctx.message.attachments:
      for x in ctx.message.attachments:
        file=await x.read()
        if len(file) > 0:
          encoding=chardet.detect(file)["encoding"]
          if encoding:
            text = file.decode(encoding)
            mystbin_client = mystbin.Client()
            paste = await mystbin_client.post(text)
            await ctx.send(content=f"Added text file to mystbin: \n{paste.url}")
            await mystbin_client.close()
          if encoding is None:
            await ctx.send("it looks like it couldn't decode this file, if this is an issue DM JDJG Inc. Official#3439 or it wasn't a text file.")
        if len(file ) < 1:
          await ctx.send("this doesn't contain any bytes.")
  
  @commands.group(name="apply",invoke_without_command=True)
  async def apply(self,ctx):
    await ctx.send("this command is meant to apply")

  @apply.command(brief="a command to apply for our Bloopers.",help="a command to apply for our bloopers.")
  async def bloopers(self,ctx,*,args=None):
    if args is None:
      await ctx.send("You didn't give us any info.")
    if args:
      if isinstance(ctx.message.channel, discord.TextChannel):
        await ctx.message.delete()

      for x in [708167737381486614,168422909482762240]:
        apply_user = self.client.get_user(x)
      
      if (apply_user.dm_channel is None):
        await apply_user.create_dm()
      
      embed_message = discord.Embed(title=args,color=random.randint(0, 16777215),timestamp=(ctx.message.created_at))
      embed_message.set_author(name=f"Application from {ctx.author}",icon_url=(ctx.author.avatar_url))
      embed_message.set_footer(text = f"{ctx.author.id}")
      embed_message.set_thumbnail(url="https://i.imgur.com/PfWlEd5.png")
      await apply_user.send(embed=embed_message)
  
def setup(client):
  client.add_cog(Extra(client))