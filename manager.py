from discord.ext import commands
import discord
import random
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
        if 'perdi' in message.content.casefold():
            await message.channel.send('Ninguém viu nada...')
            await message.delete()
        elif 'tony' in message.content.casefold():
            await message.channel.send('Os mortos não falam...')
        ##Se for o jao quem mandou mensagem
        elif message.author.id == 434893007284862977:
            opcoes = ['👁️','Eu sei o que você fez comigo...', 
                      '💀', 
                      'Minha vingança será maligna...',  
                      '👁️👁️', 
                      'Meu assassino está entre nós...', 
                      'Há um assassino entre nós.', 
                      'Seven days...',
                      'Meu assassino ainda vive...']
            if random.random()>=0.8:
                await message.channel.send(random.choice(opcoes))
            try:
                if random.random()>=0.8:
                    await message.author.send(random.choice(opcoes))
            except discord.errors.Forbidden:
                print('Jao bloqueia msgs externas')
                pass

def setup(bot):
    bot.add_cog(Manager(bot))
    
