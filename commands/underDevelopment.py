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

##FGO image search
    @commands.command(name='ServantPics', help = 'Pesquisa imagens de um servo\n[name...] é o nome do servo.')
    async def imageSearchServants(self,ctx, *name):
    ##Functions###################
        ##Checks if the message is valid
        def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.replace(' ','').isnumeric()
        def chooseAscension(servantNumber,data, msg):
            images = []
            ascensions = msg.strip().split(' ')
            for i, ascension in enumerate(ascensions):
                try:
                    images.append(data[servantNumber]['extraAssets']['charaGraph']['ascension'][ascension])
                except:
                    images.append(f'Não encontrei imagem para a ascenção {ascension}')
            return images
        ##Dados
        name = '+'.join(name)
        data =  requests.get('https://api.atlasacademy.io/nice/NA/servant/search?name={}'.format(name)).json()
        ##Checking data
        if len(data)== 0:
            await ctx.send('Não foram encontrados servos')
        else:
            ##Working with data
            response = f'Foram encontrados {len(data)} resultados:'
            for i in range(len(data)):
                response += '\n'+ str(i+1) + ' - ' + data[i]['name']
            response += '\nDigite o número correspondente'
            reply = await ctx.send(response)
    
            ##Waits for user entry
            try:
                msg = await self.bot.wait_for('message',check = check,timeout=30)
            except asyncio.TimeoutError:
                await ctx.send('Demorou demais!')
                await reply.delete()
            else:
                await reply.delete()
                await msg.delete()
                servantNumber = int(msg.content)-1
                
                reply = await ctx.send('Escolha as ascenções! Digite os valores separados por espaço.')
               ##Waits for user entry
                try:
                    msg = await self.bot.wait_for('message',check = check,timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send('Demorou demais!')
                    await reply.delete()
                else:    
                    await reply.delete()
                    await msg.delete()

                   
                    images = chooseAscension(servantNumber,data, msg.content)
                    for i in images:    
                        await ctx.send(i)
                    
                    #await ctx.send(embed = embed)
################################


def setup(bot):
    bot.add_cog(UnderDevelopment(bot))