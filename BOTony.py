import nest_asyncio
nest_asyncio.apply()
from decouple import config

#############################
mode = config('mode') #test or deploy
#############################
from discord.ext import commands
import os

if mode == 'test':
    
    sign = '!'
else:
    sign = '$'
    
bot = commands.Bot(sign)

def load_cogs(bot):
    
    bot.load_extension('manager')
    bot.load_extension('tasks.Dates')
    for file in os.listdir('commands'):
        if file.endswith('.py'):
            
            cog = file[:-3]
            bot.load_extension(f'commands.{cog}')
        
load_cogs(bot)


TOKEN = config('TOKEN')
TOKEN_TESTES = config('TOKEN_TESTES')


if mode == 'test':
    bot.run(TOKEN_TESTES)
else:
    bot.run(TOKEN)