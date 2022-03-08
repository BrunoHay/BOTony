from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time




    
    
def initSelenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'),options=chrome_options)
    return driver
#######################################
class UnderDevelopment(commands.Cog):
    ''' Still under development '''
    
    
    def __init__(self, bot):
        self.bot = bot
###########################################
    @commands.command(name='seleniumTest',help = 'Testing selenium imp')
    async def seleniumT(self,ctx):
        driver =initSelenium()
        driver.get('https://www.dac.unicamp.br/portal/')
        elemento = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/section[1]/div/div/div[2]/ul/li[5]/a')))
        elemento.click()
        print(driver.title)
        elemento = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="conteudo"]/div[1]/table/tbody/tr[2]/td[1]/a')))
        elemento.click()
        print(driver.title)
        print(driver.current_url)
        

##Prepare game room
    @commands.command(name='letsPlay', help = 'Cria salas para certos jogos. \n[game...] é o nome do jogo.')
    async def newRoom(self, ctx, *game):
        await ctx.send('Oops, este comando está em construção!')
        return
        print('VC NÃO DEVIA VER ISSO')
        games = {'Broken Picture Phone':('https://www.brokenpicturephone.com/?room=manjuba',None),
                 'Colonist':('https://colonist.io', '//*[@id="landingpage_enter_lobby_button"]',
                             '//*[@id="lobby_cta_create"]','//*[@id="room_center_checkbox_privategame"]'),
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
                driver = initSelenium()
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