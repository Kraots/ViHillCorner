import discord
from discord.ext import commands

class ReactionRoles(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.client.get_guild(750160850077089853)



                    # COLORS


        color1 = guild.get_role(750272224170082365)
        color2 = guild.get_role(750160850299387977)
        color3 = guild.get_role(750160850299387976)
        color4 = guild.get_role(750160850299387975)
        color5 = guild.get_role(750160850299387974)
        color6 = guild.get_role(750160850299518985)
        color7 = guild.get_role(750160850299518984)
        color8 = guild.get_role(750160850299518983)
        color9 = guild.get_role(750160850299518982)
        color10 = guild.get_role(750160850299518981)
        color11 = guild.get_role(750160850299518980)
        color12 = guild.get_role(750160850299518979)
        color13 = guild.get_role(750160850299518978)
        color14 = guild.get_role(750160850299518977)
        color15 = guild.get_role(750160850295324752)
        color16 = guild.get_role(750160850299518976)
        color17 = guild.get_role(750160850295324751)
        color18 = guild.get_role(750272729533644850)
        color19 = guild.get_role(788112413261168660)
        COLORSMSG1 = 779389485573079071
        COLORSMSG2 = 779389533875601451
        COLORSMSG3 = 788117110475718728


        message_id = payload.message_id
        member = payload.member



                # COLORS


        if message_id == COLORSMSG1:

            if payload.emoji.name == '\U00000031\U0000fe0f\U000020e3': # COLOR1
                await member.add_roles(color1)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000032\U0000fe0f\U000020e3': # COLOR2 
                await member.add_roles(color2)
                await member.remove_roles(color1)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return
            
            if payload.emoji.name == '\U00000033\U0000fe0f\U000020e3': # COLOR3 
                await member.add_roles(color3)
                await member.remove_roles(color2)
                await member.remove_roles(color1)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000034\U0000fe0f\U000020e3': # COLOR4 
                await member.add_roles(color4)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color1)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000035\U0000fe0f\U000020e3': # COLOR5 
                await member.add_roles(color5)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color1)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return
            
            if payload.emoji.name == '\U00000036\U0000fe0f\U000020e3': # COLOR6 
                await member.add_roles(color6)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color1)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000037\U0000fe0f\U000020e3': # COLOR7 
                await member.add_roles(color7)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color1)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000038\U0000fe0f\U000020e3': # COLOR8 
                await member.add_roles(color8)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color1)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000039\U0000fe0f\U000020e3': # COLOR9
                await member.add_roles(color9)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color1)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return
            
        if message_id == COLORSMSG2:

            if payload.emoji.name == '\U00000031\U0000fe0f\U000020e3': # COLOR1
                await member.add_roles(color10)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color11)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000032\U0000fe0f\U000020e3': # COLOR1
                await member.add_roles(color11)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color1)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000033\U0000fe0f\U000020e3': # COLOR1
                await member.add_roles(color12)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color1)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return
            
            if payload.emoji.name == '\U00000034\U0000fe0f\U000020e3': # COLOR1
                await member.add_roles(color13)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color1)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000035\U0000fe0f\U000020e3': # COLOR1
                await member.add_roles(color14)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color1)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000036\U0000fe0f\U000020e3': # COLOR1
                await member.add_roles(color15)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color1)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000037\U0000fe0f\U000020e3': # COLOR1
                await member.add_roles(color16)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color1)
                await member.remove_roles(color17)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000038\U0000fe0f\U000020e3': # COLOR1
                await member.add_roles(color17)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color1)
                await member.remove_roles(color18)
                await member.remove_roles(color19)
                return

            if payload.emoji.name == '\U00000039\U0000fe0f\U000020e3': # COLOR1
                await member.add_roles(color18)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color1)
                await member.remove_roles(color19)
                return



							# WHITE
        
        
        if message_id == COLORSMSG3:

            if payload.emoji.name == '\U00000031\U0000fe0f\U000020e3': # COLOR 1
                await member.add_roles(color19)
                await member.remove_roles(color2)
                await member.remove_roles(color3)
                await member.remove_roles(color4)
                await member.remove_roles(color5)
                await member.remove_roles(color6)
                await member.remove_roles(color7)
                await member.remove_roles(color8)
                await member.remove_roles(color9)
                await member.remove_roles(color10)
                await member.remove_roles(color11)
                await member.remove_roles(color12)
                await member.remove_roles(color13)
                await member.remove_roles(color14)
                await member.remove_roles(color15)
                await member.remove_roles(color16)
                await member.remove_roles(color17)
                await member.remove_roles(color1)
                await member.remove_roles(color18)
                return


def setup (client):
    client.add_cog(ReactionRoles(client))