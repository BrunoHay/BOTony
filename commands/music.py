import discord
from discord.ext import commands

class Music(commands.Cog):
    ''' Plays music form yt '''
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='entrar', help = 'Insere bot na chamada de audio')
    async def enter(self,ctx):
        try:
            channel = ctx.author.voice.channel
            await channel.connect() 
            #await self.bot.join_voice_channel(channel)
        except discord.errors.InvalidArgument:
            await ctx.send("O bot ja esta em um canal de voz")
        except Exception as error:
            await ctx.send("Ein Error: ```{error}```".format(error=error))
            
    @commands.command(name='sair', help = 'Tira o bot da chamada')
    async def leave(self, ctx):
        try:
            mscleave = discord.Embed(
                title="\n",
                color=0xF7FE2E,
                description="Sai do canal de voz e a musica parou!"
            )

            await ctx.send(embed=mscleave)
            await ctx.voice_client.disconnect()
        except AttributeError:
            await ctx.send("O bot não esta em nenhum canal de voz.")
        except Exception as Hugo:
            await ctx.send("Ein Error: ```{haus}```".format(haus=Hugo))
            
    @commands.command(name='play', help = 'toca a música')
    async def play(self, ctx):
        players = {}
        try:
            yt_url = ctx.message.content[6:]
            if self.bot.is_voice_connected(ctx.voice_client):
                try:
                    #voice = self.bot.voice_client_in(ctx.voice_client)
                    voice = ctx.voice_client
                    players[ctx].stop()
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[ctx] = player
                    player.start()
                    mscemb = discord.Embed(
                        title="Música para tocar:",
                        color=0xF7FE2E
                    )
                    mscemb.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb.add_field(name="Enviado em:", value="`{}`".format(player.uploaded_date))
                    mscemb.add_field(name="Enviado por:", value="`{}`".format(player.uploadeder))
                    mscemb.add_field(name="Duraçao:", value="`{}`".format(player.uploadeder))
                    mscemb.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                    await ctx.send(embed=mscemb)
                except Exception as e:
                    await ctx.send("Error1: [{error}]".format(error=e))

            if not self.bot.is_voice_connected(ctx.voice_client):
                try:
                    channel = ctx.author.voice.channel
                    voice = await channel.connect() 
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[ctx] = player
                    player.start()
                    mscemb2 = discord.Embed(
                        title="Música para tocar:",
                        color=0xF7FE2E
                    )
                    mscemb2.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb2.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb2.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                    mscemb2.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                    mscemb2.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                    mscemb2.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb2.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                    await ctx.send(embed=mscemb2)
                except Exception as error:
                    await ctx.send("Error2: [{error}]".format(error=error))
        except Exception as e:
            await ctx.send("Error3: [{error}]".format(error=e))
        
        
        
        
        
        
def setup(bot):
    bot.add_cog(Music(bot))
    