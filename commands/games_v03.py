from discord.ext import commands
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Games(commands.Cog):
    ''' Silly games support '''
    
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name = 'teams', help = 'Divide pessoas em times. \n<nTeams> é o tamanho de cada time\n[args...] é uma lista de nomes separados por espaço')
    async def doTeams(self, ctx, nTeams,*args, orderSensitive = True):
        cond = True
        while cond == True:
            qnt = len(args)
            teams = {}
            members = list(args)
            for i in range(int(nTeams)):
                for j in range(qnt // int(nTeams)):
                    if j == 0:
                        teams[i]=[members.pop(members.index(random.choice(members)))]
                    else:
                        teams[i].append(members.pop(members.index(random.choice(members))))
            ##Para pessoas que sobraram
            for k in range(qnt%int(nTeams)):
                teams[k].append(members.pop(members.index(random.choice(members))))
            ##Verificação orderSensitive
            if orderSensitive == False:
                break
            else:
                members = list(args)
                for x in range(int(nTeams)):
                    if set(teams[x]) == set(members[x*(qnt//int(nTeams)):x*(qnt//int(nTeams))+qnt//int(nTeams)]):
                        break
                    else:
                        cond = False
                continue
        response = 'Os times serão: '
        for t in range(int(nTeams)):
            response += '\n Time {}: {} '.format( t+1,', '.join(teams[t]))      
        await ctx.send(response)

 
    @commands.command(name='letsPlay', help = 'Cria salas online para jogar certos jogos. \n<game> é o nome do jogo.')
    async def newRoom(self, ctx, game):

        games = {'Broken Picture Phone':('https://www.brokenpicturephone.com/?room=manjuba',None),
                 'Colonist':('https://colonist.io/', 
                                     '//*[@id="landingpage_enter_lobby_button"]', 
                                     '//*[@id="lobby_cta_create"]', 
                                     '//*[@id="room_center_checkbox_privategame"]'),
                 'Codenames':('https://codenames.game/', None)}
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
                await ctx.send(f'Aqui está o link!{games[game]}')
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

    
def setup(bot):
    bot.add_cog(Games(bot))
    