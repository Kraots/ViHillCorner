import discord
from discord.ext import commands

class ReactionRoles(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.client.get_guild(750160850077089853)


                    # REGIONS


        Europe = guild.get_role(750160850236604541)
        Australia = guild.get_role(750322356869791756)
        North_America = guild.get_role(750160850236604540)
        South_America = guild.get_role(750160850236604539)
        Asia = guild.get_role(750160850236604543)
        Oceania = guild.get_role(750160850236604542)
        Africa = guild.get_role(750160850236604544)
        REGIONMSG = 779279687711981588


                    # GENDER


        Female = guild.get_role(750160850270027852)
        Male = guild.get_role(750160850270027853)
        Other_Gender = guild.get_role(750160850270027851)
        GENDERMSG = 779281303770103828

                    # PRONOUNS
            
        He_Him = guild.get_role(750160850270027850)
        She_Her = guild.get_role(750160850270027848)
        They_Them = guild.get_role(750160850270027849)
        PRONOUNSMSG = 779282022631473172


                    # AGE


        age13 = guild.get_role(750160850270027847)
        age14 = guild.get_role(750160850270027846)
        age15 = guild.get_role(750160850253512853)
        age16 = guild.get_role(750160850253512852)
        age17 = guild.get_role(750160850253512851)
        age18 = guild.get_role(750160850253512850)
        AGEMSG = 779282780332621874


                    # SEXUALITY


        Straight = guild.get_role(750160850286936077)
        Lesbian = guild.get_role(750160850286936076)
        Gay = guild.get_role(750160850286936078)
        Bisexual = guild.get_role(750160850286936075)
        Pansexual = guild.get_role(750160850286936074)
        Ace_Umbrella = guild.get_role(750160850270027855)
        Other_Sexuality = guild.get_role(750160850270027854)
        SEXUALITYMSG = 779285751845617676


                    # STATUS

        Single = guild.get_role(750160850253512849)
        Taken = guild.get_role(750160850253512846)
        Looking = guild.get_role(750160850253512848)
        Not_Looking = guild.get_role(750160850253512847)
        STATUSMSG = 779287055804661770


                    # DM'S 


        Open = guild.get_role(750160850253512844)
        Closed = guild.get_role(750160850236604545)
        Ask = guild.get_role(750160850253512845)
        DMSMSG = 779293467527348225


                    # PINGS


        Chat_Revive = guild.get_role(750160850236604537)
        Welcomer = guild.get_role(750160850077089856)
        Update = guild.get_role(750160850077089858)
        Poll = guild.get_role(750160850077089860)
        Partnership = guild.get_role(750160850077089861)
        Event = guild.get_role(750160850236604536)
        VC = guild.get_role(750160850077089857)
        WYR = guild.get_role(750160850077089855)
        Random = guild.get_role(750160850077089859)
        PINGSMSG = 779293503821709322


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
        COLORSMSG1 = 779389485573079071
        COLORSMSG2 = 779389533875601451


        message_id = payload.message_id
        member = payload.member


                # REGION


        if message_id == REGIONMSG:
            
            if payload.emoji.name == "\U00000031\U0000fe0f\U000020e3": # EUROPE
                await member.add_roles(Europe)
                await member.remove_roles(Australia)
                await member.remove_roles(North_America)
                await member.remove_roles(South_America)
                await member.remove_roles(Asia)
                await member.remove_roles(Oceania)
                await member.remove_roles(Africa)
                return

            if payload.emoji.name == "\U00000032\U0000fe0f\U000020e3": # AUSTRALIA
                await member.add_roles(Australia)
                await member.remove_roles(Europe)
                await member.remove_roles(North_America)
                await member.remove_roles(South_America)
                await member.remove_roles(Asia)
                await member.remove_roles(Oceania)
                await member.remove_roles(Africa)
                return

            if payload.emoji.name == "\U00000033\U0000fe0f\U000020e3": # NORTH AMERICA
                await member.add_roles(North_America)
                await member.remove_roles(Australia)
                await member.remove_roles(Europe)
                await member.remove_roles(South_America)
                await member.remove_roles(Asia)
                await member.remove_roles(Oceania)
                await member.remove_roles(Africa)
                return

            if payload.emoji.name == "\U00000034\U0000fe0f\U000020e3": # SOUTH AMERICA
                await member.add_roles(South_America)
                await member.remove_roles(Australia)
                await member.remove_roles(North_America)
                await member.remove_roles(Europe)
                await member.remove_roles(Asia)
                await member.remove_roles(Oceania)
                await member.remove_roles(Africa)
                return

            if payload.emoji.name == "\U00000035\U0000fe0f\U000020e3": # ASIA
                await member.add_roles(Asia)
                await member.remove_roles(Australia)
                await member.remove_roles(North_America)
                await member.remove_roles(South_America)
                await member.remove_roles(Europe)
                await member.remove_roles(Oceania)
                await member.remove_roles(Africa)
                return

            if payload.emoji.name == "\U00000036\U0000fe0f\U000020e3": # OCEANIA
                await member.add_roles(Oceania)
                await member.remove_roles(Australia)
                await member.remove_roles(North_America)
                await member.remove_roles(South_America)
                await member.remove_roles(Asia)
                await member.remove_roles(Europe)
                await member.remove_roles(Africa)
                return

            if payload.emoji.name == "\U00000031\U0000fe0f\U000020e3": # AFRICA
                await member.add_roles(Africa)
                await member.remove_roles(Australia)
                await member.remove_roles(North_America)
                await member.remove_roles(South_America)
                await member.remove_roles(Asia)
                await member.remove_roles(Oceania)
                await member.remove_roles(Europe)
                return


                # GENDER


        if message_id == GENDERMSG: 
            
            if payload.emoji.name == "\U00002640\U0000fe0f": # FEMALE
                await member.add_roles(Female)
                await member.remove_roles(Male)
                await member.remove_roles(Other_Gender)
                return

            if payload.emoji.name == "\U00002642\U0000fe0f": # MALE
                await member.add_roles(Male)
                await member.remove_roles(Female)
                await member.remove_roles(Other_Gender)
                return

            if payload.emoji.name == "\U00002754": # OTHER | GENDER
                await member.add_roles(Other_Gender)
                await member.remove_roles(Female)
                await member.remove_roles(Male) 
                return


                # PRONOUNS


        if message_id == PRONOUNSMSG:
            
            if payload.emoji.name == "\U0001f466": # HE / HIM
                await member.add_roles(He_Him)
                await member.remove_roles(She_Her)
                await member.remove_roles(They_Them)
                return

            if payload.emoji.name == "\U0001f467": # SHE / HER
                await member.add_roles(She_Her)
                await member.remove_roles(He_Him)
                await member.remove_roles(They_Them)
                return

            if payload.emoji.name == "\U0001f41e": # THEY / THEM
                await member.add_roles(They_Them)
                await member.remove_roles(She_Her)
                await member.remove_roles(He_Him)
                return


                # AGE

        
        if message_id == AGEMSG:
            
            if payload.emoji.name == "\U00000031\U0000fe0f\U000020e3": # 13 
                await member.add_roles(age13)
                await member.remove_roles(age14)
                await member.remove_roles(age15)
                await member.remove_roles(age16)
                await member.remove_roles(age17)
                await member.remove_roles(age18)
                return

            if payload.emoji.name == "\U00000032\U0000fe0f\U000020e3": # 14 
                await member.add_roles(age14)
                await member.remove_roles(age13)
                await member.remove_roles(age15)
                await member.remove_roles(age16)
                await member.remove_roles(age17)
                await member.remove_roles(age18)
                return

            if payload.emoji.name == '\U00000033\U0000fe0f\U000020e3': # 15
                await member.add_roles(age15)
                await member.remove_roles(age14)
                await member.remove_roles(age13)
                await member.remove_roles(age16)
                await member.remove_roles(age17)
                await member.remove_roles(age18)
                return

            if payload.emoji.name == "\U00000034\U0000fe0f\U000020e3": # 16
                await member.add_roles(age16)
                await member.remove_roles(age14)
                await member.remove_roles(age15)
                await member.remove_roles(age13)
                await member.remove_roles(age17)
                await member.remove_roles(age18)
                return

            if payload.emoji.name == "\U00000035\U0000fe0f\U000020e3": # 17
                await member.add_roles(age17)
                await member.remove_roles(age14)
                await member.remove_roles(age15)
                await member.remove_roles(age16)
                await member.remove_roles(age13)
                await member.remove_roles(age18)
                return

            if payload.emoji.name == "\U00000036\U0000fe0f\U000020e3": # 18
                await member.add_roles(age18)
                await member.remove_roles(age14)
                await member.remove_roles(age15)
                await member.remove_roles(age16)
                await member.remove_roles(age17)
                await member.remove_roles(age13)
                return


                # SEXUALITY


        if message_id == SEXUALITYMSG:
            
            if payload.emoji.name == 'hug': # STRAIGHT
                await member.add_roles(Straight)
                await member.remove_roles(Lesbian)
                await member.remove_roles(Gay)
                await member.remove_roles(Bisexual)
                await member.remove_roles(Pansexual)
                await member.remove_roles(Ace_Umbrella)
                await member.remove_roles(Other_Sexuality)
                return

            if payload.emoji.name == 'bloblove': # LESBIAN
                await member.add_roles(Lesbian)
                await member.remove_roles(Straight)
                await member.remove_roles(Gay)
                await member.remove_roles(Bisexual)
                await member.remove_roles(Pansexual)
                await member.remove_roles(Ace_Umbrella)
                await member.remove_roles(Other_Sexuality)
                return

            if payload.emoji.name == 'blob_love': # GAY
                await member.add_roles(Gay)
                await member.remove_roles(Lesbian)
                await member.remove_roles(Straight)
                await member.remove_roles(Bisexual)
                await member.remove_roles(Pansexual)
                await member.remove_roles(Ace_Umbrella)
                await member.remove_roles(Other_Sexuality)
                return

            if payload.emoji.name == 'smiling': # BISEXUAL
                await member.add_roles(Bisexual)
                await member.remove_roles(Lesbian)
                await member.remove_roles(Gay)
                await member.remove_roles(Straight)
                await member.remove_roles(Pansexual)
                await member.remove_roles(Ace_Umbrella)
                await member.remove_roles(Other_Sexuality)
                return

            if payload.emoji.name == 'peepoBlush': # PANSEXUAL
                await member.add_roles(Pansexual)
                await member.remove_roles(Lesbian)
                await member.remove_roles(Gay)
                await member.remove_roles(Bisexual)
                await member.remove_roles(Straight)
                await member.remove_roles(Ace_Umbrella)
                await member.remove_roles(Other_Sexuality)
                return

            if payload.emoji.name == 'LoveHeart': # ACE UMBRELLA
                await member.add_roles(Ace_Umbrella)
                await member.remove_roles(Lesbian)
                await member.remove_roles(Gay)
                await member.remove_roles(Bisexual)
                await member.remove_roles(Pansexual)
                await member.remove_roles(Straight)
                await member.remove_roles(Other_Sexuality)
                return

            if payload.emoji.name == 'vampy': # OTHER | SEXUALITY
                await member.add_roles(Other_Sexuality)
                await member.remove_roles(Lesbian)
                await member.remove_roles(Gay)
                await member.remove_roles(Bisexual)
                await member.remove_roles(Pansexual)
                await member.remove_roles(Ace_Umbrella)
                await member.remove_roles(Straight)
                return


                # STATUS


        if message_id == STATUSMSG:
            
            if payload.emoji.name == 'salute': # SINGLE
                await member.add_roles(Single)
                await member.remove_roles(Taken)
                return

            if payload.emoji.name == 'zerotwo_yay': # TAKEN
                await member.add_roles(Taken)
                await member.remove_roles(Single)
                return

            if payload.emoji.name == 'zerotwo_wow': # LOOKING
                await member.add_roles(Looking)
                await member.remove_roles(Not_Looking)
                return
            
            if payload.emoji.name == 'hehe_blush': # NOT LOOKING
                await member.add_roles(Not_Looking)
                await member.remove_roles(Looking)
                return


                # DMS


        if message_id == DMSMSG:

            if payload.emoji.name == 'vampy_yay': # OPEN
                await member.add_roles(Open)
                await member.remove_roles(Closed)
                await member.remove_roles(Ask)
                return

            if payload.emoji.name == 'vampy_cry': # CLOSED
                await member.add_roles(Closed)
                await member.remove_roles(Open)
                await member.remove_roles(Ask)
                return

            if payload.emoji.name == 'weird': # ASK
                await member.add_roles(Ask)
                await member.remove_roles(Open)
                await member.remove_roles(Closed)
                return

                
                # PINGS


        if message_id == PINGSMSG:
            
            if payload.emoji.name == '\U00000031\U0000fe0f\U000020e3': # CHAT REVIVE
                await member.add_roles(Chat_Revive)
                return

            if payload.emoji.name == '\U00000032\U0000fe0f\U000020e3': # WELCOMER
                await member.add_roles(Welcomer)
                return
            
            if payload.emoji.name == '\U00000033\U0000fe0f\U000020e3': # UPDATE
                await member.add_roles(Update)
                return

            if payload.emoji.name == '\U00000034\U0000fe0f\U000020e3': # POLL
                await member.add_roles(Poll)
                return

            if payload.emoji.name == '\U00000035\U0000fe0f\U000020e3': # PARTNERSHIP
                await member.add_roles(Partnership)
                return
            
            if payload.emoji.name == '\U00000036\U0000fe0f\U000020e3': # EVENT
                await member.add_roles(Event)
                return

            if payload.emoji.name == '\U00000037\U0000fe0f\U000020e3': # VC
                await member.add_roles(VC)
                return

            if payload.emoji.name == '\U00000038\U0000fe0f\U000020e3': # WYR
                await member.add_roles(WYR)
                return

            if payload.emoji.name == '\U00000039\U0000fe0f\U000020e3': # RANDOM
                await member.add_roles(Random)
                return


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
                return



    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.client.get_guild(750160850077089853)


                    # REGIONS


        Europe = guild.get_role(750160850236604541)
        Australia = guild.get_role(750322356869791756)
        North_America = guild.get_role(750160850236604540)
        South_America = guild.get_role(750160850236604539)
        Asia = guild.get_role(750160850236604543)
        Oceania = guild.get_role(750160850236604542)
        Africa = guild.get_role(750160850236604544)
        REGIONMSG = 779279687711981588


                    # GENDER


        Female = guild.get_role(750160850270027852)
        Male = guild.get_role(750160850270027853)
        Other_Gender = guild.get_role(750160850270027851)
        GENDERMSG = 779281303770103828

                    # PRONOUNS
            
        He_Him = guild.get_role(750160850270027850)
        She_Her = guild.get_role(750160850270027848)
        They_Them = guild.get_role(750160850270027849)
        PRONOUNSMSG = 779282022631473172


                    # AGE


        age13 = guild.get_role(750160850270027847)
        age14 = guild.get_role(750160850270027846)
        age15 = guild.get_role(750160850253512853)
        age16 = guild.get_role(750160850253512852)
        age17 = guild.get_role(750160850253512851)
        age18 = guild.get_role(750160850253512850)
        AGEMSG = 779282780332621874


                    # SEXUALITY


        Straight = guild.get_role(750160850286936077)
        Lesbian = guild.get_role(750160850286936076)
        Gay = guild.get_role(750160850286936078)
        Bisexual = guild.get_role(750160850286936075)
        Pansexual = guild.get_role(750160850286936074)
        Ace_Umbrella = guild.get_role(750160850270027855)
        Other_Sexuality = guild.get_role(750160850270027854)
        SEXUALITYMSG = 779285751845617676


                    # STATUS

        Single = guild.get_role(750160850253512849)
        Taken = guild.get_role(750160850253512846)
        Looking = guild.get_role(750160850253512848)
        Not_Looking = guild.get_role(750160850253512847)
        STATUSMSG = 779287055804661770


                    # DM'S 


        Open = guild.get_role(750160850253512844)
        Closed = guild.get_role(750160850236604545)
        Ask = guild.get_role(750160850253512845)
        DMSMSG = 779293467527348225


                    # PINGS


        Chat_Revive = guild.get_role(750160850236604537)
        Welcomer = guild.get_role(750160850077089856)
        Update = guild.get_role(750160850077089858)
        Poll = guild.get_role(750160850077089860)
        Partnership = guild.get_role(750160850077089861)
        Event = guild.get_role(750160850236604536)
        VC = guild.get_role(750160850077089857)
        WYR = guild.get_role(750160850077089855)
        Random = guild.get_role(750160850077089859)
        PINGSMSG = 779293503821709322


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
        COLORSMSG1 = 779389485573079071
        COLORSMSG2 = 779389533875601451


        message_id = payload.message_id
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)


                # REGION


        if message_id == REGIONMSG:
            
            if payload.emoji.name == "\U00000031\U0000fe0f\U000020e3": # EUROPE
                await member.remove_roles(Europe)
                return

            if payload.emoji.name == "\U00000032\U0000fe0f\U000020e3": # AUSTRALIA
                await member.remove_roles(Australia)
                return

            if payload.emoji.name == "\U00000033\U0000fe0f\U000020e3": # NORTH AMERICA
                await member.remove_roles(North_America)
                return

            if payload.emoji.name == "\U00000034\U0000fe0f\U000020e3": # SOUTH AMERICA
                await member.remove_roles(South_America)
                return

            if payload.emoji.name == "\U00000035\U0000fe0f\U000020e3": # ASIA
                await member.remove_roles(Asia)
                return

            if payload.emoji.name == "\U00000036\U0000fe0f\U000020e3": # OCEANIA
                await member.remove_roles(Oceania)
                return

            if payload.emoji.name == "\U00000031\U0000fe0f\U000020e3": # AFRICA
                await member.remove_roles(Africa)
                return


                # GENDER


        if message_id == GENDERMSG: 
            
            if payload.emoji.name == "\U00002640\U0000fe0f": # FEMALE
                await member.remove_roles(Female)
                return

            if payload.emoji.name == "\U00002642\U0000fe0f": # MALE
                await member.remove_roles(Male)
                return

            if payload.emoji.name == "\U00002754": # OTHER | GENDER
                await member.remove_roles(Other_Gender)
                return


                # PRONOUNS


        if message_id == PRONOUNSMSG:
            
            if payload.emoji.name == "\U0001f466": # HE / HIM
                await member.remove_roles(He_Him)
                return

            if payload.emoji.name == "\U0001f467": # SHE / HER
                await member.remove_roles(She_Her)
                return

            if payload.emoji.name == "\U0001f41e": # THEY / THEM
                await member.remove_roles(They_Them)
                return


                # AGE

        
        if message_id == AGEMSG:
            
            if payload.emoji.name == "\U00000031\U0000fe0f\U000020e3": # 13 
                await member.remove_roles(age13)
                return

            if payload.emoji.name == "\U00000032\U0000fe0f\U000020e3": # 14 
                await member.remove_roles(age14)
                return

            if payload.emoji.name == '\U00000033\U0000fe0f\U000020e3': # 15
                await member.remove_roles(age15)
                return

            if payload.emoji.name == "\U00000034\U0000fe0f\U000020e3": # 16
                await member.remove_roles(age16)
                return

            if payload.emoji.name == "\U00000035\U0000fe0f\U000020e3": # 17
                await member.remove_roles(age17)
                return

            if payload.emoji.name == "\U00000036\U0000fe0f\U000020e3": # 18
                await member.remove_roles(age18)
                return


                # SEXUALITY


        if message_id == SEXUALITYMSG:
            
            if payload.emoji.name == 'hug': # STRAIGHT
                await member.remove_roles(Straight)
                return

            if payload.emoji.name == 'bloblove': # LESBIAN
                await member.remove_roles(Lesbian)
                return

            if payload.emoji.name == 'blob_love': # GAY
                await member.remove_roles(Gay)
                return

            if payload.emoji.name == 'smiling': # BISEXUAL
                await member.remove_roles(Bisexual)
                return

            if payload.emoji.name == 'peepoBlush': # PANSEXUAL
                await member.remove_roles(Pansexual)
                return

            if payload.emoji.name == 'LoveHeart': # ACE UMBRELLA
                await member.remove_roles(Ace_Umbrella)
                return

            if payload.emoji.name == 'vampy': # OTHER | SEXUALITY
                await member.remove_roles(Other_Sexuality)
                return


                # STATUS


        if message_id == STATUSMSG:
            
            if payload.emoji.name == 'salute': # SINGLE
                await member.remove_roles(Single)
                return

            if payload.emoji.name == 'zerotwo_yay': # TAKEN
                await member.remove_roles(Taken)
                return

            if payload.emoji.name == 'zerotwo_wow': # LOOKING
                await member.remove_roles(Looking)
                return
            
            if payload.emoji.name == 'hehe_blush': # NOT LOOKING
                await member.remove_roles(Not_Looking)
                return


                # DMS


        if message_id == DMSMSG:

            if payload.emoji.name == 'vampy_yay': # OPEN
                await member.remove_roles(Open)
                return

            if payload.emoji.name == 'vampy_cry': # CLOSED
                await member.remove_roles(Closed)
                return

            if payload.emoji.name == 'weird': # ASK
                await member.remove_roles(Ask)
                return

                
                # PINGS


        if message_id == PINGSMSG:
            
            if payload.emoji.name == '\U00000031\U0000fe0f\U000020e3': # CHAT REVIVE
                await member.remove_roles(Chat_Revive)
                return

            if payload.emoji.name == '\U00000032\U0000fe0f\U000020e3': # WELCOMER
                await member.remove_roles(Welcomer)
                return
            
            if payload.emoji.name == '\U00000033\U0000fe0f\U000020e3': # UPDATE
                await member.remove_roles(Update)
                return

            if payload.emoji.name == '\U00000034\U0000fe0f\U000020e3': # POLL
                await member.remove_roles(Poll)
                return

            if payload.emoji.name == '\U00000035\U0000fe0f\U000020e3': # PARTNERSHIP
                await member.remove_roles(Partnership)
                return
            
            if payload.emoji.name == '\U00000036\U0000fe0f\U000020e3': # EVENT
                await member.remove_roles(Event)
                return

            if payload.emoji.name == '\U00000037\U0000fe0f\U000020e3': # VC
                await member.remove_roles(VC)
                return

            if payload.emoji.name == '\U00000038\U0000fe0f\U000020e3': # WYR
                await member.remove_roles(WYR)
                return

            if payload.emoji.name == '\U00000039\U0000fe0f\U000020e3': # RANDOM
                await member.remove_roles(Random)
                return


                # COLORS


        if message_id == COLORSMSG1:
            
            if payload.emoji.name == '\U00000031\U0000fe0f\U000020e3': # COLOR 1 
                await member.remove_roles(color1)
                return

            if payload.emoji.name == '\U00000032\U0000fe0f\U000020e3': # COLOR 2 
                await member.remove_roles(color2)
                return
            
            if payload.emoji.name == '\U00000033\U0000fe0f\U000020e3': # COLOR 3 
                await member.remove_roles(color3)
                return

            if payload.emoji.name == '\U00000034\U0000fe0f\U000020e3': # COLOR 4 
                await member.remove_roles(color4)
                return

            if payload.emoji.name == '\U00000035\U0000fe0f\U000020e3': # COLOR 5 
                await member.remove_roles(color5)
                return
            
            if payload.emoji.name == '\U00000036\U0000fe0f\U000020e3': # COLOR 6
                await member.remove_roles(color6)
                return

            if payload.emoji.name == '\U00000037\U0000fe0f\U000020e3': # COLOR 7
                await member.remove_roles(color7)
                return

            if payload.emoji.name == '\U00000038\U0000fe0f\U000020e3': # COLOR 8
                await member.remove_roles(color8)
                return

            if payload.emoji.name == '\U00000039\U0000fe0f\U000020e3': # COLOR 9
                await member.remove_roles(color9)
                return

            
        if message_id == COLORSMSG2:
            
            if payload.emoji.name == '\U00000031\U0000fe0f\U000020e3': # COLOR 1 
                await member.remove_roles(color10)
                return

            if payload.emoji.name == '\U00000032\U0000fe0f\U000020e3': # COLOR 2 
                await member.remove_roles(color11)
                return
            
            if payload.emoji.name == '\U00000033\U0000fe0f\U000020e3': # COLOR 3 
                await member.remove_roles(color12)
                return

            if payload.emoji.name == '\U00000034\U0000fe0f\U000020e3': # COLOR 4 
                await member.remove_roles(color13)
                return

            if payload.emoji.name == '\U00000035\U0000fe0f\U000020e3': # COLOR 5 
                await member.remove_roles(color14)
                return
            
            if payload.emoji.name == '\U00000036\U0000fe0f\U000020e3': # COLOR 6
                await member.remove_roles(color15)
                return

            if payload.emoji.name == '\U00000037\U0000fe0f\U000020e3': # COLOR 7
                await member.remove_roles(color16)
                return

            if payload.emoji.name == '\U00000038\U0000fe0f\U000020e3': # COLOR 8
                await member.remove_roles(color17)
                return

            if payload.emoji.name == '\U00000039\U0000fe0f\U000020e3': # COLOR 9
                await member.remove_roles(color18)
                return


def setup (client):
    client.add_cog(ReactionRoles(client))