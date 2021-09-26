import disnake
from disnake.ext import commands, tasks
from utils import time
import utils.colors as color
import textwrap
import datetime
import asyncio

class Reminders(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db1['Reminders']
        self.prefix = "!"
        self.check_current_reminders.start()
    def cog_check(self, ctx):
        return ctx.prefix == self.prefix
    
    
    @commands.group(invoke_without_command = True, case_insensitive = True, aliases=['reminder'])
    async def remind(self, ctx, *, when: time.UserFriendlyTime(commands.clean_content, default='\u2026')):
        """Set your reminder."""
        
        results = await self.db.find().sort([("_id", -1)]).to_list(1)

        for result in results:
            newID = result['_id'] + 1
        
        try:
            newID = newID
        except UnboundLocalError:
            newID = 1324

        post = {"_id": newID,
                "userID": ctx.author.id,
                "channel": ctx.channel.id,
                "remindWhen": when.dt,
                "remindWhat": when.arg,
                "timeNow": datetime.datetime.utcnow(),
                "messageJumpUrl": ctx.message.jump_url	
                }
        
        await self.db.insert_one(post)
        delta = time.human_timedelta(when.dt, accuracy=3)
        await ctx.send(f"Alright {ctx.author.mention}, in **{delta}**: {when.arg}")
    
    @remind.command(name='list')
    async def remind_list(self, ctx):
        """See your list of reminders, if you have any."""

        results = await self.db.find({"userID": ctx.author.id}).sort([("remindWhen", 1)]).to_list(10)
        em = disnake.Embed(color=color.lightpink, title="Reminders")
        index = 0
        total_reminders = 0
        z = await self.db.find({"userID": ctx.author.id}).sort([("remindWhen", 1)]).to_list(100000)
        
        for x in z:
            total_reminders += 1

        for result in results:
            index += 1
            shorten = textwrap.shorten(result['remindWhat'], width=320)
            em.add_field(name=f"(ID)`{result['_id']}`: In {time.human_timedelta(result['remindWhen'])}", value=f"{shorten}\n[Click here to go there]({result['messageJumpUrl']})", inline=False)
        
        if len(em) < 12:
            await ctx.send("No currently running reminders.")
            return
        em.set_footer(text="Showing %s/%s reminders." % (index, total_reminders))
        await ctx.send(embed=em)
    
    @remind.command(name='remove', aliases=['delete', 'cancel'])
    async def remind_remove(self, ctx, id: int):
        """Remove a reminder from your list based on its id."""

        results = await self.db.find_one({"_id": id})
        if results != None:
            if results['userID'] == ctx.author.id:
                view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
                view.message = msg = await ctx.send("Are you sure you want to cancel that reminder? %s" % (ctx.author.mention), view=view)
                await view.wait()
                if view.response is True:
                    await self.db.delete_one({"_id": id})
                    e = "Succesfully canceled the reminder. %s" % (ctx.author.mention)
                    return await msg.edit(content=e, view=view)
                
                elif view.response is False:
                    e = "Reminder has not been canceled. %s" % (ctx.author.mention)
                    return await msg.edit(content=e, view=view)
            else:
                await ctx.send("That reminder is not yours!")
                return
        else:
            await ctx.send("No reminder with that ID.")
            return

    @remind.command(name='clear')
    async def remind_clear(self, ctx):
        """Delete all of your reminders."""

        results = await self.db.find_one({"userID": ctx.author.id})
        if results != None:
            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send("Are you sure you want to clear your reminders? %s" % (ctx.author.mention), view=view)
            await view.wait()
            if view.response is True:
                await self.db.delete_many({"userID": ctx.author.id})
                e = "Succesfully cleared all your reminders. %s" % (ctx.author.mention)
                return await msg.edit(content=e, view=view)
            
            elif view.response is False:
                e = "Reminders have not been cleared. %s" % (ctx.author.mention)
                return await msg.edit(content=e, view=view)
        else:
            await ctx.send("No currently running reminders.")


    @tasks.loop(seconds=5)
    async def check_current_reminders(self):
        await self.bot.wait_until_ready()
        currentTime = datetime.datetime.now()
        results = await self.db.find().to_list(100000)
        for result in results:
            expireDate = result['remindWhen']
            remindID = result['_id']
            user = result['userID']
            remindedWhen = result['timeNow']
            remindWhat = result['remindWhat']
            remindUrl = result['messageJumpUrl']
            channelID = result['channel']

            if currentTime >= expireDate:
                guild = self.bot.get_guild(750160850077089853)
                remindChannel = guild.get_channel(channelID)
                msg = f"<@!{user}>, **{time.human_timedelta(remindedWhen)}**: {remindWhat}\n\n{remindUrl}"
                await remindChannel.send(msg)
                await self.db.delete_one({"_id": remindID})

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.db.delete_many({"userID": member.id})
    
    @remind_remove.error
    async def remind_remove_error(self, ctx, error):
        if isinstance(error, commands.errors.TooManyArguments):
            return
        else:
            await self.bot.reraise(ctx, error)
        

def setup(bot):
    bot.add_cog(Reminders(bot))