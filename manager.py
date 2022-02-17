from discord.ext import commands

from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound
class Manager(commands.Cog):
    ''' Manages the bot '''
    
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Pronto para rodar')
        #current_time.start()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error,MissingRequiredArgument):
            await ctx.send('Número de argumentos inválidos. Digite $help para ver os comandos disponíveis')
        elif isinstance(error,CommandNotFound):
            await ctx.send('Comando não encontrado. Digite $help para ver os comandos disponíveis')
        else:
            raise error
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if 'palavrão' in message.content:
            await message.channel.send(
                f'Por favor, {message.author.name}, não ofenda os demais usuários'
                )
            await message.delete()
        ##await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(Manager(bot))
    
