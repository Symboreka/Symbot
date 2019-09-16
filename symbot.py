#!/usr/bin/python3.7
# Discord bot for the SymboArmy Server, creatively named SymBot
print('Starting SymBot')
import discord, asyncio, io, random
from utils_symbot import Commandmanager
version = str('Too Young (0.1)')
adminid = 117038989248036870

#reading token from file
token = open("/home/pi/Symbot/token.txt").read()
client = discord.Client()
mngr = Commandmanager()

#checkerthread removed because it broke
#chkrthrd = threading.Thread(target=mngr.command_checker, args=(), kwargs={})
#chkrthrd.start()
#required rights to create commands
authpos = 7

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' with ID: ' + str(client.user.id))
    #set default playing game in presence
    await client.change_presence(activity=discord.Game(name="with fire >:)"))
@client.event
async def on_message(message):
    #extracting message for formatting
    content = message.content.lower()
    #creating variable to save processing power if a command served its purpose
    satisfied = False

    #command to list available commands of importance
    if content.startswith('>help'):
        embed = discord.Embed(title= "Here's help for ya " + message.author.name , description="Available commands for SymBot", color=0x00ff00)

        embed.add_field(name="Main Commands", value='''
>SymBot - Shows that this thing is working
>Version - Shows SymBot's current version
>Info - Giving Info about your membership
>discord - Gives you a nice invite link from discord.me
*
''', inline="False")

        embed.add_field(name="Fun Commands", value='''
>coin - Coinflip! 50/50
>woah - Woah
*
        ''', inline="False")

        embed.add_field(name="Custom command stuff :3", value='''
>addcommand - adds a custom command with an expire date (level5+)
>command_expire_date -  checks the expire date of a command
*
        ''', inline="False")

        embed.add_field(name="Commands about the Community and Symboreka", value='''
>anime - Shows you my animelist
>mal - does that too
>btag - Battletag if you want to add me there for whatever reason
>steamgroup - gives you a link to our steamgroup :3
>twitter - i dont really use that thing anymore but here you go
>youtube - guess
>yt - guess again
*
        ''', inline="False")

        embed.add_field(name="Game specific commands", value='''
[BDO]>failstacks - Gives a useful failstack chart
[Trove]>trove - referral link to me if you want to try this game
*
        ''', inline="False")

        embed.set_footer(text="there are also some hidden thingys like stream insiders but hey, you'll do just fine, promise sweetheart")
        await message.channel.send( embed=embed)
        satisfied=True


    #command to test if symbot works
    if content.startswith('>symbot'):
        await message.channel.send( "I'm here and working as intended!")
        satisfied = True

    if content.startswith('>version'):
        await message.channel.send( "I'm running at Version: "+ str(version))
        satisfied = True

    #coinflip, 50/50 chance
    if content.startswith('>coin'):
        choice = random.randint(1,2)
        if choice == 1:
            await message.channel.send( "Head!")
        else:
            await message.channel.send( "Tail!")
        satisfied = True


    #changing game command for admins only

    if content.startswith('>setgame') and message.author.id == str(adminid):
        game = message.content[9:]
        await client.change_presence(game=discord.Game(name=game))
        await message.channel.send( "Changed game to " + game)

        satisfied = True
    #giving user info
    if content.startswith('>info'):
        user = message.author
        roles = user.roles
        #placeholder for member object
        mbr = None
        # gets account creation data, stringing it to desired format
        acccreatedate = user.created_at.strftime("%d.%m.%Y %H:%M:%S")

        #getting the date where user joined Server
        for member in message.guild.members:
            if member == message.author:
                mbr = member
        joinedat = mbr.joined_at.strftime("%d.%m.%Y %H:%M:%S")
        embed = discord.Embed(title="Info of " + user.name, description="------------", color=0x00ff00)

        embed.add_field(name="Account creation date:", value=str(acccreatedate), inline="False")
        embed.add_field(name="Joined "+ str(message.guild) + " at:", value=joinedat, inline="False")
        embed.add_field(name="Progress: ", value="Consists of following roles:", inline="False")
        #adding roles, 1 field for each role
        for idx, role in enumerate(roles):
            embed.add_field(name="Role " + str(idx + 1) + " : ", value=roles[idx].name)

        embed.set_footer(text="ideas for more info to show? tell me.")
        await message.channel.send( embed=embed)


        satisfied = True

    if content.startswith('>command_expire_date'):
        ask = message.content[21:]
        if ask == '':
            await message.channel.send( 'Soooooooo, you want to ask for an expire date of what? - Oh! I know, your milk is expired since 1978.')
        elif ask[0] == '>' and len(ask) > 1:
            out = mngr.get_expire_date(ask)
            if out == None:
                await message.channel.send( 'Command you entered does not exist, or has no expire date. Unlike the milk in your fridge, drink it. ')
            else:
                # out will return in seconds, parsing to human readable here

                if out // (60*60*24) > 1:
                    n = int(out //(60*60*24))
                    #n will be in  Days
                    await message.channel.send( str(n) + ' Days until ' + ask + ' expires')
                elif out //(60*60) > 1:
                    n = int(out //(60*60))
                    # n will be in hours
                    await message.channel.send( str(n) + ' Hours until ' + ask + ' expires')
                elif out // 60 > 1:
                    n = int(out //60)
                    #n will be in minutes
                    await message.channel.send( str(n) + ' Minutes until ' + ask + ' expires')
                else:
                    #using out instead of n because out is already in seconds
                    await message.channel.send( str(out) + ' Seconds until ' + ask + ' expires')
        else:
            await message.channel.send( 'Please enter a valid command (including the ">")')

        satisfied = True



    if content.startswith('>save_commands'):
        if message.author.id == str(adminid):
            mngr.save_state()
            await message.channel.send( 'Commands have been saved!')
        else:
            await message.channel.send( 'Only Admins can save commands!')
        satisfied = True

    if content.startswith('>read_commands'):
        if str(message.author.id) == str(adminid):
            commands = mngr.read_dynamic_commands()
            if commands != None:
                await message.channel.send( str(commands) + " commands initialized")
            else:
                await message.channel.send( 'No commands found!')
        else:
            await message.channel.send("You do not have permissions to do that!")
        satisfied = True

    if message.content.startswith('>read_perm_commands'):
        if str(message.author.id) == str(adminid):
            out = mngr.read_perm_commands()
            if type(out) is int and out > 0:
                await message.channel.send( str(out) + ' commands have been initialized' )
            else:
                await message.channel.send( 'Could not initialize commands')
        else:
            await message.channel.send("You do not have permissions to do that!")
        satisfied = True

    #woah meme
    if content.startswith('>woah'):
        await message.channel.send(None, file=discord.File('img/woah.png', 'woah.png'))
        satisfied=True


    if content.startswith('>addcommand'):
        # desired syntax: >addcommand >examplename This is going to be an awesome command!
        if message.author.top_role.position > authpos:
            full_command = message.content[12:]
            split = full_command.split(' ', 1)
            try:
                if split[0] == '':
                    await message.channel.send( 'I did what you wanted, which is nothing! Yay! :yum:')
                else:
                    if split[1] == '' or split[0][0] != '>':
                        await message.channel.send( 'You fool! (syntax should be: >addcommand >*Commandname* *CommandText*)')
                    else:
                        if split[1][0] == '>':
                            await message.channel.send( '*Snaps you on your fingers* :   No tailpicking!!! :rage:')
                        else:
                            name = split[0]
                            content = split[1]
                            check = mngr.add_dynamic_command(name.lower(), content)
                            if check == 1:
                                await message.channel.send( 'Command has been added!')
                            else:
                                await message.channel.send( 'Something went wrong!! Does the command already exist?')
            except:
                await message.channel.send( 'You fool! (syntax should be: >addcommand >*Commandname* *CommandText*)')
        else:
            await message.channel.send( "No touchy dis command!! (you need to be Level5 or higher to use this)")
        satisfied = True


    #loop to read out all permanent commands if satisfied is False, doing it first because they are prioritized
    if satisfied != True and message.content.startswith('>') == True:
        if content != ">":
            ctx = mngr.run_command(content)
            await message.channel.send( ctx)

@client.event
async def on_member_join(member):
    await client.send_message(member.guild, "Welcome " + member + " to SymboArmy! Have a wonderful time here! :heart_eyes:")

#   self.makeitwork()
client.run(token)

print('\nSymbot Ended')
