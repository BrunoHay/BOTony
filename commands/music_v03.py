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
            

        
        
        
        
        
        
def setup(bot):
    bot.add_cog(Music(bot))
    