from discord.ext import commands

class Talks(commands.Cog):
    ''' Talks with user '''
    
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='oi', help = 'Dá oi')
    async def send_hello(self, ctx):
        name = ctx.author.name
        response = 'Olá ' + name
        await ctx.send(response)
        
def setup(bot):
    bot.add_cog(Talks(bot))
    