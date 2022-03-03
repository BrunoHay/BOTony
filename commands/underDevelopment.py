from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time




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

    @commands.command(name='sheets', help = 'Edita uma planilha.')
    async def sheetEdit(self, ctx, *values):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        
        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1e0Y7T5T0Sf3kIxnZ3Mb8JaYOrhCPbO_pJSj9WtgjNiM'
        SAMPLE_RANGE_NAME = 'data!A2:A10'
        
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            service = build('sheets', 'v4', credentials=creds)
        
            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
        
        
        except HttpError as err:
            print(err)

        List=[]
        for value in values:
            List.append([value])
        body = {
            'values': List
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range='data!A1',
            valueInputOption="USER_ENTERED", body=body).execute()

def setup(bot):
    bot.add_cog(UnderDevelopment(bot))