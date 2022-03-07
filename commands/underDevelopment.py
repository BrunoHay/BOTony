from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from decouple import config
import datetime
import asyncio

from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def initCreds():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def initSheet(creds):
    sheet = build('sheets', 'v4', credentials=creds).spreadsheets()
    return sheet
def searchRange(SS_ID,searchPage,searchColumn,searchTerm,returnColumn,returnRange=True):
    ''' Retorna as posições na coluna returnColumn se returnRange=True
        Retorna os valores da coluna returnColumn se returnRange!=False'''
    sheet=initSheet(initCreds())
    Range = "'{}'!{}2:{}".format(searchPage,searchColumn,searchColumn)
    result = sheet.values().get(spreadsheetId=SS_ID,
                                range=Range).execute()
    values = result.get('values', [])
    # values=[[Linha2],[Linha3],...[LinhaN]]
    POS = []
    VALUES = []

    if returnRange==True:
        for i, term in enumerate(values):
            if searchTerm in term[0]: 
                POS.append("'{}'!{}{}".format(searchPage,returnColumn,i+2))
                
        return POS
    else:
        for i, term in enumerate(values):
            if searchTerm in term[0]: 
                VALUES.append(sheet.values().get(spreadsheetId=SS_ID,
                                            range="'{}'!{}{}".format(searchPage,returnColumn,i+2)).execute().get('values', [])[0][0])
        return VALUES
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

    @commands.command(name='add', help = 'Adiciona novo gasto\n<descrição> <valor> <local_compra> <método_pagamento> <obs>')
    async def sheetAppend(self, ctx, *values):
        # Auxiliar Functions
        def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
        # SpreadSheet Properties
        SSP = {'pages':['data','Dashboard'],
               'columns':['Descrição','Valor','Local da compra','Método de pagamento','Obs.','Data']}
        
        if not ctx.author.id == 432384321018658826:
            await ctx.send('Desculpe, apenas disponível para o Hayashi. Se você quiser acesso contate ele.')
        else:
            creds = initCreds()
            
            try:
                sheet = initSheet(creds)
                SS_ID = config('SS_ID')
                # Adds info in order <descrição> <valor> <local_da_compra> <método_de_pagamento>
                List = [list(values)]
                if 'devendo' in List[0][3].casefold():
                    await ctx.send('Para quem você está devendo?')
                    try:
                        msg = await self.bot.wait_for('message',check = check,timeout=20)
                        List[0][3] += f' /{msg.content}'
                    except asyncio.TimeoutError:
                        await ctx.send('Demorou demais!')

                
                # Adds '/' for blank columns
                while len(List[0])<len(SSP['columns'])-1:
                    List[0].append('/')            
                List[0].append(str(datetime.datetime.now()))
                body = {
                    'values':List
                }
                # Sends body to SpreadSheet
                result = sheet.values().append(
                    spreadsheetId=SS_ID,
                    range='data!A1:E1',
                    valueInputOption="USER_ENTERED", body=body).execute()
                
                await ctx.send('Adicionado com sucesso!')
                channel = self.bot.get_channel(949181542742249482)
                #💸 💵 💰 💳
                info = '💸Nova Compra💸'
                for i in range(len(SSP['columns'])-1):
                    info += '\n{}: {}'.format(SSP['columns'][i],List[0][i])
                
                await channel.send(info)
            except HttpError as err:
                print(err)
                
                
                
    @commands.command(name='devo?', help = 'Estou devendo algo?\n<*name> é o nome da pessoa a qual se deve.')
    async def sheetCheck(self, ctx, *name):
        creds = initCreds()
        sheet = initSheet(creds)
        SS_ID = config('SS_ID')
        Range = 'compilado!AA2:AB'
        if len(name) == 0:
            # Se não tiver arg, puxa lista de nomes e valores
            
            result = sheet.values().get(spreadsheetId=SS_ID,
                                        range=Range).execute()
            values = result.get('values', [])
            ppl = 'Você deve para estas pessoas:'
            for i in range(len(values)):
                ppl += f'\n{values[i][0]}: R${values[i][1]}'
            await ctx.send(ppl)

        else:
            # Se houver arg procura o nome e retorna valor
            name = ' '.join(name)
            result = sheet.values().get(spreadsheetId=SS_ID,
                                        range=Range).execute()
            values = result.get('values', [])
            
            for i in range(len(values)):
                if name in values[i]:            
                    await ctx.send(f'Você deve R${values[i][1]} para {values[i][0]}.')
                    return
            await ctx.send(f'Não encontrei o nome {name}. Você provavelmente não deve para essa pessoa ou eu sou burro😰')
            
    
        
        
    @commands.command(name='pagar',help='Quita a dívida que você possa ter com alguém.\n <name> é o nome de para quem se deve')
    async def pay(self,ctx,name):
        # Auxiliar Functions
        def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
        # Parameters
        creds = initCreds()
        sheet = initSheet(creds)
        SS_ID = config('SS_ID')
        Range = 'compilado!AA2:AB'
        #Copying column from sheet
        result = sheet.values().get(spreadsheetId=SS_ID,
                                    range=Range).execute()
        values = result.get('values', [])
        #Looking for the name in the column
        for i in range(len(values)):
            if name in values[i]:
                await ctx.send(f'Você deve R${values[i][1]} para {values[i][0]}.\nQuanto você irá pagar?\n(all/<valor>)')
                #Wait user input
                try:
                    msg = await self.bot.wait_for('message',check = check,timeout=20)

                    #Pays all debts
                    if msg.content =='all':
                        
                        #Find position in the sheet
                        where = searchRange(SS_ID,'data','D',name,'E')
                        for i in range(len(where)):
                            result = sheet.values().update(
                                spreadsheetId=SS_ID,
                                range = where[i],
                                valueInputOption="USER_ENTERED", body={'values':[['Pago']]}).execute()
                        await ctx.send('Quitado!')
                    # Quita algumas dividas de acordo com o total e valor pago    
                    else:
                        valor = float(msg.content.replace(',','.'))
                        ##Encontrar range e subtrair dividendo
                        #Coluna Obs.
                        whereInput = searchRange(SS_ID,'data','D',name,'E')
                        #Coluna Valor
                        whereValue = searchRange(SS_ID,'compilado','X',name,'W')
                        valuesOrder = searchRange(SS_ID,'data','D',name,'E',returnRange=False)
                        for i, v in enumerate(valuesOrder):
                            if v.isalpha():
                                valuesOrder[i]=0
                            else:
                                valuesOrder[i]=float(v.replace(',','.'))
                                
                        # print(f'valuesOrder= {valuesOrder}')
                        # print(f'whereInput= {whereInput}')
                        debts = []
                        for i in range(len(whereValue)):
                            result = sheet.values().get(spreadsheetId=SS_ID,
                                                        range=whereValue[i]).execute()
                            debts.append(float(result.get('values', [])[0][0].replace(',','.')))
                        resto = valor
                        alterDebts = []
                        # print(f'debts = {debts}')
                        
                        w = 0
                        while resto>=0 and w<=len(debts):
                            resto = resto-debts[w]
                            alterDebts.append(w)
                            w += 1
                            
                        # print(f'alterDebts = {alterDebts}')
                        # print(f'resto = {resto}')

                        #para cada indice alter, inserir pago, exceto último
                        #transpor alter para sheet data
                        whereInput2=[]
                        for k in alterDebts:
                            for j in range(len(valuesOrder)):
                                if debts[k] == valuesOrder[j]:
                                    whereInput2.append(whereInput[j])

                        # print(f'whereInput2={whereInput2}')
                        
                        for i in range(len(whereInput2)-1):
                            result = sheet.values().update(
                                spreadsheetId=SS_ID,
                                range = whereInput2[i],
                                valueInputOption="USER_ENTERED", body={'values':[['Pago']]}).execute()

                        #ultimo indice alter att valor para -resto
                        body2 = {'values':[[str(-resto).replace('.',',')]]}
                        result = sheet.values().update(
                            spreadsheetId=SS_ID,
                            range = whereInput2[-1],
                            valueInputOption="USER_ENTERED", body=body2).execute()
                        await ctx.send(f'Foram quitadas {len(alterDebts)-1} dívidas de {len(debts)}')
                        await ctx.send(f'Ainda faltam R${sum(debts)-valor}')
                        return
                #If user entry lasts more than timeout
                except asyncio.TimeoutError:
                    await ctx.send('Demorou demais!')
                return
        #If name isnt found
        await ctx.send('Não encontrei o nome citado...')
#################################
    @commands.command(name='report',help='Reporta algum bug ou possível melhoria para o BOT.')
    async def report(self, ctx, *msg):
        if len(msg) == 0:
            return
        else:
            channel = self.bot.get_channel(950215017310072892)
            msg = ' '.join(msg)
            author = ctx.author
            await channel.send(f'De: {author}\n"{msg}"')
            await ctx.send('Obrigado pelo report! Sua mensagem foi enviada ao desenvolvedor.')
    @commands.command(name='repeat',help='Repete a mensagem')
    async def repeat(self, ctx,*msg):
        if len(msg) == 0:
            return
        else:
            msg = ' '.join(msg)
            print(msg)
            await ctx.send(msg)

def setup(bot):
    bot.add_cog(UnderDevelopment(bot))