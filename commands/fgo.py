from discord.ext import commands
import discord
import requests
import asyncio
class FGO(commands.Cog):
    ''' Talks with user '''
    
    def __init__(self, bot):
        self.bot = bot
   
###############################################################################   
###https://api.atlasacademy.io/rapidoc

    @commands.command(name='servant', help = 'Pesquisa dados de um servo\n[name...] é o nome do servo.')
    async def searchServant(self,ctx, *name):
    ##Functions###################
        ##Checks if the message is valid
        def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isnumeric()
        ##Gets random in-game voice lines
        def randVoiceLine(data, servantNumber):
            import re
            import random
            i = random.randrange(len(data[servantNumber]['profile']['voices']))
            j = random.randrange(len(data[servantNumber]['profile']['voices'][i]['voiceLines']))
            voiceLine = re.sub("[\[].*?[\]]", "",data[servantNumber]['profile']['voices'][i]['voiceLines'][j]['subtitle'])
            return voiceLine
    #########################
    
        ##Getting data
        name = '+'.join(name)
        data =  requests.get('https://api.atlasacademy.io/nice/NA/servant/search?lore=True&name={}'.format(name)).json()
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
                msg = await self.bot.wait_for('message',check = check,timeout=20)
            except asyncio.TimeoutError:
                await ctx.send('Demorou demais!')
                await reply.delete()
            else:
                await reply.delete()
                await msg.delete()
                servantNumber = int(msg.content)-1
                ##Images
                imageUrl = data[servantNumber]['extraAssets']['charaGraph']['ascension']['4']
                imageFace= data[servantNumber]['extraAssets']['faces']['ascension']['4']
                imageStatus = data[servantNumber]['extraAssets']['status']['ascension']['3']
                
                ##Building skills
                skills = []
                for j in range(len(data[servantNumber]['skills'])):    
                    skills.append(data[servantNumber]['skills'][j]['name'])
                ##Building Noble Phantasm
                noblePhantasm = data[servantNumber]['noblePhantasms'][0]['name'] + '\n' + data[servantNumber]['noblePhantasms'][0]['detail']
                #Building Embed
                embed = discord.Embed(
                    title = data[servantNumber]['name'].capitalize(),
                    description = randVoiceLine(data, servantNumber),
                    colour = 0x0000FF,
                    )
                
                embed.set_author(name=f"Character ID: {data[servantNumber]['id']}",icon_url = imageFace)
                embed.set_thumbnail(url = imageStatus)
                embed.set_image(url=imageUrl)
                embed.add_field(name='Class',value = data[servantNumber]['className'] )
                embed.add_field(name='Type',value = data[servantNumber]['type'] )
                embed.add_field(name='Attribute',value = data[servantNumber]['attribute'] )
                embed.add_field(name='Skills', value=skills,inline = False)
                embed.add_field(name='Noble Phantasm', value=noblePhantasm, inline = False)
                embed.set_footer(text='Brought to you by Hayashi')
                await ctx.send(embed = embed)
##FGO image search
    @commands.command(name='servantPics', help = 'Pesquisa imagens de um servo\n[name...] é o nome do servo.')
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
                        
#######################################################
##JP VERSION                     
    @commands.command(name='servantJP', help = 'Pesquisa dados de um servo no JP\n[name...] é o nome do servo.')
    async def searchServantJP(self,ctx, *name):
    ##Functions###################
        ##Checks if the message is valid
        def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isnumeric()
        ##Gets random in-game voice lines
        def randVoiceLine(data, servantNumber):
            import re
            import random
            i = random.randrange(len(data[servantNumber]['profile']['voices']))
            j = random.randrange(len(data[servantNumber]['profile']['voices'][i]['voiceLines']))
            voiceLine = re.sub("[\[].*?[\]]", "",data[servantNumber]['profile']['voices'][i]['voiceLines'][j]['subtitle'])
            return voiceLine
    #########################
    
        ##Getting data
        name = '+'.join(name)
        data =  requests.get('https://api.atlasacademy.io/nice/JP/servant/search?lore=True&name={}'.format(name)).json()
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
                msg = await self.bot.wait_for('message',check = check,timeout=20)
            except asyncio.TimeoutError:
                await ctx.send('Demorou demais!')
                await reply.delete()
            else:
                await reply.delete()
                await msg.delete()
                servantNumber = int(msg.content)-1
                ##Images
                imageUrl = data[servantNumber]['extraAssets']['charaGraph']['ascension']['4']
                imageFace= data[servantNumber]['extraAssets']['faces']['ascension']['4']
                imageStatus = data[servantNumber]['extraAssets']['status']['ascension']['3']
                
                ##Building skills
                skills = []
                for j in range(len(data[servantNumber]['skills'])):    
                    skills.append(data[servantNumber]['skills'][j]['name'])
                ##Building Noble Phantasm
                noblePhantasm = data[servantNumber]['noblePhantasms'][0]['name'] + '\n' + data[servantNumber]['noblePhantasms'][0]['detail']
                #Building Embed
                embed = discord.Embed(
                    title = data[servantNumber]['name'].capitalize(),
                    description = randVoiceLine(data, servantNumber),
                    colour = 0x0000FF,
                    )
                
                embed.set_author(name=f"Character ID: {data[servantNumber]['id']}",icon_url = imageFace)
                embed.set_thumbnail(url = imageStatus)
                embed.set_image(url=imageUrl)
                embed.add_field(name='Class',value = data[servantNumber]['className'] )
                embed.add_field(name='Type',value = data[servantNumber]['type'] )
                embed.add_field(name='Attribute',value = data[servantNumber]['attribute'] )
                embed.add_field(name='Skills', value=skills,inline = False)
                embed.add_field(name='Noble Phantasm', value=noblePhantasm, inline = False)
                embed.set_footer(text='Brought to you by Hayashi')
                await ctx.send(embed = embed)
##FGO image search
    @commands.command(name='servantPicsJP', help = 'Pesquisa imagens de um servo no JP\n[name...] é o nome do servo.')
    async def imageSearchServantsJP(self,ctx, *name):
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
        data =  requests.get('https://api.atlasacademy.io/nice/JP/servant/search?name={}'.format(name)).json()
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
def setup(bot):
    bot.add_cog(FGO(bot))