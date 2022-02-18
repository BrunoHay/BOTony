from discord.ext import commands
import discord
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class UnderDevelopment(commands.Cog):
    ''' Still under development '''
    
    
    def __init__(self, bot):
        self.bot = bot
#####Plays music
    @commands.command(name='play', help = 'toca a música')
    async def play(self, ctx):
        players = {}
        try:
            yt_url = ctx.message.content[6:]
            if self.bot.is_voice_connected(ctx.voice_client):
                try:
                    #voice = self.bot.voice_client_in(ctx.voice_client)
                    voice = ctx.voice_client
                    players[ctx].stop()
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[ctx] = player
                    player.start()
                    mscemb = discord.Embed(
                        title="Música para tocar:",
                        color=0xF7FE2E
                    )
                    mscemb.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb.add_field(name="Enviado em:", value="`{}`".format(player.uploaded_date))
                    mscemb.add_field(name="Enviado por:", value="`{}`".format(player.uploadeder))
                    mscemb.add_field(name="Duraçao:", value="`{}`".format(player.uploadeder))
                    mscemb.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                    await ctx.send(embed=mscemb)
                except Exception as e:
                    await ctx.send("Error1: [{error}]".format(error=e))

            if not self.bot.is_voice_connected(ctx.voice_client):
                try:
                    channel = ctx.author.voice.channel
                    voice = await channel.connect() 
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[ctx] = player
                    player.start()
                    mscemb2 = discord.Embed(
                        title="Música para tocar:",
                        color=0xF7FE2E
                    )
                    mscemb2.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb2.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb2.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                    mscemb2.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                    mscemb2.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                    mscemb2.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb2.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                    await ctx.send(embed=mscemb2)
                except Exception as error:
                    await ctx.send("Error2: [{error}]".format(error=error))
        except Exception as e:
            await ctx.send("Error3: [{error}]".format(error=e))
##Prepare game room
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
##


def setup(bot):
    bot.add_cog(UnderDevelopment(bot))