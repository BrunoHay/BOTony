from discord.ext import commands, tasks
import discord

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from BOTony import mode
infoVelha = [['Alteração de matrícula 1º semestre de 2022',
  'Caso você tenha perdido o prazo de matrícula, ou queira efetuar alguma modificação, é possível solicitar inclusão ou exclusão de disciplinas no período de alteração de matrícula.',
  'Publicado em 07/02/2022'],
 ['Comprovante vacinação',
  'Os estudantes ingressantes tem até 5 dias após a matrícula para fazer a inserção do documento no sistema e-DAC.',
  'Publicado em 01/02/2022'],
 ['ProFIS - Ingresso na Graduação 2022',
  'Confira a lista dos estudantes do ProFIS - Concluintes 2021 com respectiva vaga obtida em curso de Graduação Unicamp em 2022.',
  'Publicado em 01/02/2022'],
 ['Lista PROFIS - Concluintes 2021',
  'Confira aqui a lista dos alunos concluintes do ProFIS de 2021, em ordem decrescente de CRO:',
  'Publicado em 24/01/2022'],
 ['Manutenção Programada - Sistemas SIGA/E-DAC e SIG/Estágios, Portais DAC e SAE - 30/01',
  'Neste domingo (30/01) será realizada uma manutenção programada nos sistemas SIGA/E-DAC e SIG, Portais DAC e SAE. Durante a janela de manutenção os serviços ficarão indisponíveis.',
  'Publicado em 23/01/2022'],
 ['Atendimento da DAC - via Fale Conosco',
  'Durante o período de suspensão das atividades presenciais, o atendimento da DAC está prestando seus serviços normalmente - de forma remota - por meio do Fale Conosco.',
  'Publicado em 07/01/2022'],
 ['Deliberação CEPE A-21/21',
  'Fique atento: Deliberação CEPE-A-21/2021 de 07/12/2021 que dispõe sobre a obrigatoriedade de apresentação do comprovante de vacinação contra a Covid-19 pelos discentes da Unicamp e dá outras providências.',
  'Publicado em 14/12/2021'],
 ['Resolução GR nº. 81/2021',
  'Altera a Resolução GR-074/2021, de 12/11/2021 que dispõe sobre a retomada das atividades presenciais dos alunos de graduação, pós-graduação, extensão e colégios técnicos nos campi da Universidade Estadual de Campinas no 1º semestre de 2022 e sobre a adoção de medidas emergenciais e temporárias, com objetivo de minimizar a transmissão e disseminação da Covid-19.',
  'Publicado em 10/12/2021'],
 ['Titulo Velho 1','Subtitulo Velho 1', 'Data Velha 1'],
 ['Titulo Velho 2','Subtitulo Velho 2', 'Data Velha 2']]
def initSelenium():
    global mode
    chrome_options = webdriver.ChromeOptions()
    if mode == 'test':
        chrome_options.add_argument('headless')
        driver = webdriver.Chrome(options=chrome_options)
    else:
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'),options=chrome_options)
    return driver

class Dates(commands.Cog):
    ''' Works with dates '''

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.dacNoticias.start()
        pass
    

    @tasks.loop(hours=24)
    async def dacNoticias(self):
        channel = self.bot.get_channel(950944575910998158)
        driver =initSelenium()
        global infoVelha
        driver.get('https://www.dac.unicamp.br/portal/noticias')
        Titulo = driver.title
        post = driver.find_element(By.CLASS_NAME  , 'post-list')
        heads = post.find_elements(By.TAG_NAME , 'h4')
        excerpts = post.find_elements(By.CLASS_NAME , 'excerpt')
        dates = post.find_elements(By.CLASS_NAME , 'info')
        unicampLogo = driver.find_element(By.XPATH , '//*[@id="navegacao-fixed-top"]/nav/div[1]/a[1]')
        dacLogo = driver.find_element(By.XPATH , '//*[@id="navegacao-fixed-top"]/nav/div[1]/a[2]')
        unicampLogoUrl = unicampLogo.value_of_css_property("background-image").split('"')[1]
        dacLogoUrl = dacLogo.value_of_css_property("background-image").split('"')[1]
        #info[i][0]=titulo
        #info[i][1]=subtitulo
        #info[i][2]=data
        info = [[heads[i].text,excerpts[i].text,dates[i].text] for i in range(len(heads))]
        
        dif = [noticia for noticia in info if not noticia in infoVelha ]
        embed = discord.Embed(
            title = Titulo,
            description = 'Notícias Fresquinhas!',
            colour = 0xffffff,
            )
        
        embed.set_author(name='Unicamp')     
        embed.set_footer(text=driver.current_url)
        if len(dif)!=0:
            infoVelha = info
           
            for noticia in dif:
                embed.add_field(name=noticia[0], value=noticia[1], inline = False)
                
            await channel.send(embed = embed)
        else:       
            await channel.send(f'Sem notícias novas em {Titulo}!')
            
            
        driver.quit()
    
def setup(bot):
    bot.add_cog(Dates(bot))
    