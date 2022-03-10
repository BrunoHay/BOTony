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
    
class Gastos(commands.Cog):
    ''' Gerenciador de gastos pessoais '''
    
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='add', help = 'Adiciona novo gasto\n<descrição> <valor> <local_compra> <método_pagamento> <obs>')
    async def sheetAppend(self, ctx, *values):
        if len(values)==0:
            await ctx.send('Número de argumentos inválido!')
            return
        # Auxiliar Functions
        def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
        # SpreadSheet Properties
        SSP = {'pages':['data','compilado','Dashboard'],
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
                #List = [['Arg0', 'Arg1', 'Arg2', 'Arg3']]
                
                # For longer description, use ""
                firstArg=''
                ap =[]
                #Encontra a posição dos argumentos com "
                for i, arg in enumerate(List[0]):
                    if '"' in arg:                   
                        ap.append(i)
                
                if not len(ap)==0: 
                    #Para cada par inicio/final...
                    for k in range(len(ap)//2):
                        #Cria um j q vai do inicio até o final da primeira dupla inicio/final
                        for j in range(ap[2*k],ap[2*k+1]+1):
                            #mapeia primeiro valor
                            if j == ap[k*2]:
                                inicio = j
                                firstArg += List[0][inicio] 
                            else:
                                #Corta e cola cada arg entre inicio/final no primeiro arg
                                firstArg += ' '+List[0].pop(inicio+1)
                    List[0][inicio]= firstArg.replace('"','')
                
                if 'devendo' in List[0][3].casefold():
                    await ctx.send('Para quem você está devendo?')
                    try:
                        msg = await self.bot.wait_for('message',check = check,timeout=20)
                        List[0][3] += f' /{msg.content}'
                        List[0].append(List[0][1])
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
        if not ctx.author.id == 432384321018658826:
            await ctx.send('Desculpe, apenas disponível para o Hayashi. Se você quiser acesso contate ele.')
            return
        creds = initCreds()
        sheet = initSheet(creds)
        SS_ID = config('SS_ID')
        Range = 'compilado!AA2:AB'
        if len(name) == 0:
            # Se não tiver arg, puxa lista de nomes e valores
            
            result = sheet.values().get(spreadsheetId=SS_ID,
                                        range=Range).execute()
            values = result.get('values', [])
            if '#' in values[0][0]:
                await ctx.send('Você não deve nada a ninguém')
            else:         
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
        if not ctx.author.id == 432384321018658826:
            await ctx.send('Desculpe, apenas disponível para o Hayashi. Se você quiser acesso contate ele.')
            return
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
                        resto = round(resto,2)
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
                        await ctx.send(f'Ainda faltam R${round(sum(debts)-valor,2)}')
                        return
                #If user entry lasts more than timeout
                except asyncio.TimeoutError:
                    await ctx.send('Demorou demais!')
                return
        #If name isnt found
        await ctx.send('Não encontrei o nome citado...')

    @commands.command(name='ver',help='Retorna algum valor.\n ')
    async def look(self,ctx):
        if not ctx.author.id == 432384321018658826:
            await ctx.send('Desculpe, apenas disponível para o Hayashi. Se você quiser acesso contate ele.')
            return
        creds = initCreds()
        sheet = initSheet(creds)
        SS_ID = config('SS_ID')
        Range = 'compilado!AA2:AB'
      
        result = sheet.values().get(spreadsheetId=SS_ID,
                                    range=Range).execute()
        values = result.get('values', [])
        
        
def setup(bot):
    bot.add_cog(Gastos(bot))