from discord.ext import commands, tasks
import datetime
class Dates(commands.Cog):
    ''' Works with dates '''
    
    def __init__(self, bot):
        self.bot = bot
    
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     self.current_time.start()
        
    @tasks.loop(hours=1)
    async def current_time(self):
        now = datetime.datetime.now()
        channel = self.bot.get_channel(938193288333262881)
        await channel.send(now)

def setup(bot):
    bot.add_cog(Dates(bot))
    