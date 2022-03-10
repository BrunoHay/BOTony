from discord.ext import commands
from BOTony import sign
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

    @commands.command(name ='calc',help='Calculadora.')
    async def calculate(self,ctx,*expression):
        if len(expression)==0:
            await ctx.send('Número de argumentos inválido!')
            return
        
        expression = ''.join(expression)
        response = eval(expression)
        await ctx.send('Ans= {}'.format(response))
        
    @commands.command(name='report',help='Reporta algum bug ou possível melhoria para o BOT.')
    async def report(self, ctx, *msg):
        
        if len(msg) == 0:
            await ctx.send('Número de argumentos inválido!')
            return
        else:
            channel = self.bot.get_channel(950215017310072892)
            msg = ' '.join(msg)
            author = ctx.author
            await channel.send(f'De: {author}\n"{msg}"')
            await ctx.send('Obrigado pelo report! Sua mensagem foi enviada ao desenvolvedor.')
            
    @commands.command(name='repeat',help='Repete a mensagem')
    async def repeat(self, ctx,*msg):
        if len(msg) == 0:
            await ctx.send('Número de argumentos inválido!')
            return
        else:
            msg = ' '.join(msg)
            print(msg)
            await ctx.send(msg)
            
def setup(bot):
    bot.add_cog(Utility(bot))
    
