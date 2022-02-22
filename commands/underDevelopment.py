from discord.ext import commands
import discord
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import asyncio

class UnderDevelopment(commands.Cog):
    ''' Still under development '''
    
    
    def __init__(self, bot):
        self.bot = bot
###########################################
##Prepare game room
    @commands.command(name='letsPlay', help = 'Cria salas para certos jogos. \n[game...] é o nome do jogo.')
    async def newRoom(self, ctx, *game):

        games = {'Broken Picture Phone':('https://www.brokenpicturephone.com/?room=manjuba',None),
                 'Colonist':('https://colonist.io/#UMJC', None),
                 'Codenames':('https://codenames.game/room/quack-ant-meter', None)}
        game = ' '.join(game)
        ##Se o jogo n estiver no catalogo
        if not game in games:
            await ctx.send('Não encontrei este jogo no meu catálogo. Por favor escolha um dentre os seguintes:')
            response =''
            for name in games:
                response += f'\n{name}'
            await ctx.send(response)
        else:
            ##Se o jogo não precisa criar uma nova sala
            if games[game][1]==None:
                await ctx.send(f'Aqui está o link! {games[game][0]}')
            else:
                ##Cria nova sala clicando nos botoes estipulados
                driver = webdriver.Chrome()
                driver.get(games[game][0])
    
                for i in range(1,len(games[game])):
                    time.sleep(1)
                    elemento = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,games[game][i])))
                    elemento.click()
                await ctx.send(f'Aqui está o link!{driver.current_url}')
                driver.quit()




################################


def setup(bot):
    bot.add_cog(UnderDevelopment(bot))