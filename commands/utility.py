from discord.ext import commands
from BOTony_v01 import sign
class Utility(commands.Cog):
    ''' Utilities to help you '''
    
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='clc', help = 'Apaga mensagens relacionadas ao bot. \n<binSize> é o range de mensagens que o bot analiza')
    async def searchMessages(self,ctx, binSize ):
        messages = await ctx.channel.history(limit=int(binSize)).flatten()
        cnt = 0
        try:
            for msg in messages:
                if msg.content.startswith(sign) or msg.author == self.bot.user:
                    cnt += 1
                    await msg.delete()
        finally:       
            await ctx.send(f'{cnt} mensagens apagadas com sucesso!')

def setup(bot):
    bot.add_cog(Utility(bot))
    
