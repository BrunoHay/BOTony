from discord.ext import commands
import random

class Games(commands.Cog):
    ''' Silly games support '''
    
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name = 'teams', help = 'Divide pessoas em times. Args=(número_de_times, *nomes)')
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
    reactionsOn1 = 0
    reactionsOn2 = 0
 
def setup(bot):
    bot.add_cog(Games(bot))
    