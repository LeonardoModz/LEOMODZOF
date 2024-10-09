#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 - 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Don't use the bot on real servers or use it to spam because this is breaking
discord's ToS, and you will be resulted in an account deletion.
"""
# discord
import discord, sys, requests, os, time
from discord.ext import commands
import asyncio
from packaging import version
from random import randint, choice, randrange, random, choices
from threading import Thread
from inputimeout import inputimeout, TimeoutOccurred
from queue import Queue
from io import BytesIO
from pathlib import Path
from math import ceil
from copy import deepcopy
import json

# style
from colorama import init, Fore


init(autoreset=True)

# 
__TITLE__ = "C-REAL"
__VERSION__ = "2.4.1"
__AUTHOR__ = "TKperson"
__LICENSE__ = "MIT"

# Global vars
per_page = 15
commands_per_page = 5
number_of_bomb_default = 250
selected_server = None
sorted_commands = []
webhook_targets = []
saved_ctx = None
nuke_on_join = False
auto_nick = False
auto_status = False
selfbot_has_perm = False
timeout = 6
fetching_members = False
bad_filename_map = dict((ord(char), None) for char in '<>:"\\/|?*')
grant_all_permissions = False
# normal functions==============
def exit():
    try:
        input('Press enter to exit...')
    except (EOFError, KeyboardInterrupt):
        pass
    sys.exit(1)

def banner():
    """Handler for non-unicode consoles"""
    sys.stdout.buffer.write(f'''\
 ██████╗                  ██████╗ ███████╗ █████╗ ██╗     
██╔════╝                  ██╔══██╗██╔════╝██╔══██╗██║   Version: {__VERSION__}
██║         █████╗        ██████╔╝█████╗  ███████║██║     Made by:
██║         ╚════╝        ██╔══██╗██╔══╝  ██╔══██║██║       TKperson
╚██████╗                  ██║  ██║███████╗██║  ██║███████╗    and
 ╚═════╝                  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝      cyxl
'''.encode('utf8'))

# Check for > 1.5.1 discord version
if version.parse('1.5.1') > version.parse(discord.__version__):
    print('Please update your discord.py.')
    exit()

settings = {
        "token": None,
        "permissions": [],
        "bot_permission": "2146958847",
        "command_prefix": ".",
        "bot_status": "offline",
        "verbose": 15,
        "bomb_messages": {
            "random": 10,
             "fixed": ["nuked"]
         },
        "webhook_spam": {
            "usernames": ["nuked"],
            "pfp_urls": [None],
            "contents": ["@everyone"]
        },
        "after": [],
        "proxies": [],
        "ban_whitelist": []
}

def setUp():
    # check location 
    from glob import glob
    config = None
    config_parent_dir = os.path.join(Path().absolute().__str__(), 'data')
    config_path = os.path.join(config_parent_dir, 'default.json')
    json_paths = glob(os.path.join(Path().absolute().__str__(), 'data', '*.json'))

    def getConfig(choice, timeout):
        while True:
            # it really doesn't matter if I use triple quotes or not.... the speed is going to be the same and doing this looks better
            print('=========================')
            print('|                       |')
            print('| [{0}] Load default.json |'.format('1' if 1 in choice else 'x'))
            print('| [{0}] Select .json file |'.format('2' if 2 in choice else 'x'))
            print('| [{0}] Create a new json |'.format('3' if 3 in choice else 'x'))
            print('|                       |')
            print('=========================')
            print('[x] = not Available;')
            try:
                response = inputimeout(prompt='Auto boot with choice [1] in %d seconds...\nChoose 1, 2, or 3\n>> ' % timeout, timeout=timeout)
            except TimeoutOccurred:
                response = '1'

            if response == '1':
                if not os.path.isfile(config_path):
                    print(f'Unable to find file: {config_path}')
                    continue

                with open(config_path, 'r', encoding='utf8') as f:
                    try:
                        return json.loads(f.read())
                    except json.decoder.JSONDecodeError:
                        print(f'There are some errors occured when reading the configuration file. File path -> {config_path}\nI recommend you use https://jsonlint.com/?code= to help checking the configuration file. Skipping reading the default.json file...')
                break
            elif response == '2':
                while True:
                    print('=========================')
                    print('0) Go back')
                    for i, path in enumerate(json_paths):
                        print(f'{str(i+1)}) {path}')
                    index = input('Select the .json file.\n>> ')

                    if not index.isdigit() or not (0 <= (index := int(index)) <= len(json_paths)):
                        print(f'You need to enter an integer that is between or on 0 and {str(len(json_paths))}')
                        continue

                    if index == 0:
                        timeout = 999999
                        break

                    with open(json_paths[index-1], 'r', encoding='utf8') as f:
                        try:
                            return json.loads(f.read())
                        except json.decoder.JSONDecodeError:
                            print(f'There are some errors occured when reading the configuration file. File path -> {config_path}\nI recommend you use https://jsonlint.com/?code= to help checking the configuration file. Skipping reading the default.json file...')

            elif response == '3':
                break

    global settings, settings_copy
    if os.path.isfile(config_path): # have default.json
        config = getConfig([1,2,3], 5)
    
    elif len(json_paths) > 0: # dont have default.json but have other .json file
        config = getConfig([2,3], 999999)

    if config is not None:
        settings.update(config)
    else:
        try:
            # from getpass import getpass
            # settings['token'] = getpass('Enter token. Note: Whatever you entered here will not be displayed.\n>> ')
            settings['token'] = input('Enter token. If you are new refer to this guide: https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot/wiki/Basic-setup-and-knowledge-for-using-the-bot\n>> ')
            settings['permissions'].append(input('\nEnter your discord tag or user ID. It is recommended to use discord user ID because some unicode names are hard for the code to check.\n>> '))
        except KeyboardInterrupt:
            sys.exit(0)
        except EOFError:
            print('Invalid input/EOFError. This may be caused by some unicode.')
            exit()

    print('\nTips:')
    print('The default command_prefix is: .')
    print(f'Your currect command_prefix is: {settings["command_prefix"]}')
    print(f'Use {settings["command_prefix"]}config to config the settings and more info about how to config.\n')
    
    print('Join our discord https://discord.gg/FwGWvwv4mW')

    settings_copy = deepcopy(settings)

setUp()
# token, permissions, bomb_messages, webhook_spam, bot_permission, command_prefix, bot_status, verbose, after, proxies = readJson()


want_log_request = want_log_console = want_log_message = want_log_errors = 0

def updateVerbose():
    global want_log_request, want_log_console, want_log_message, want_log_errors
    verbose = settings['verbose']
    want_log_request = verbose & 1 << 0
    want_log_console = verbose & 1 << 1
    want_log_message = verbose & 1 << 2
    want_log_errors  = verbose & 1 << 3
updateVerbose()

# def randomProxy(protocol):
#     # As long it works fine then i'm using this method
#     if proxies is None or len(proxies) == 0:
#         return None
#     return {protocol: choice(proxies)}

is_selfbot = True
headers = {}

def checkToken(token=None):
    if token is None:
        token = settings['token']

    global is_selfbot, headers 
    try:
        if 'id' in requests.get(url='https://discord.com/api/v8/users/@me', timeout=timeout, headers=headers).json():
            is_selfbot = True
            return
    except (requests.exceptions.InvalidHeader, json.decoder.JSONDecodeError):
        pass

    is_selfbot = False
    try:
        headers = {'authorization': token, 'content-type': 'application/json'}
        print('Checking selfbot token.', end='\r')
        headers['authorization'] = 'Bot ' + token
        print('Checking normal bot token.', end='\r')
        if not 'id' in requests.get(url='https://discord.com/api/v8/users/@me', timeout=timeout, headers=headers).json():
            print('Invalid token is being used.')
            exit()

    except requests.exceptions.ConnectionError:
        print('You should probably consider connecting to the internet before using any discord related stuff. If you are connected to wifi and still seeing this message, then maybe try turn off your VPN/proxy/TOR node. If you are still seeing this message or you just don\'t what to turn off vpn, you can try to use websites like repl/heroku/google cloud to host the bot for you. The source code is on https://github.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot.')
        exit()
    except (requests.exceptions.InvalidHeader, json.decoder.JSONDecodeError):
        print('Invalid token is being used.')
        exit()

checkToken()

### check updates
print('Checking update...           ', end='\r')
github_version = requests.get('https://raw.githubusercontent.com/TKperson/Nuking-Discord-Server-Bot-Nuke-Bot/master/VERSION.txt').text
if version.parse(github_version) > version.parse(__VERSION__):
    print(f'New C-REAL update has been launched -> {github_version} <- :party:')

print('Loading scripts...' + ' ' * 15, end='\r')


"""
command_prefix   - command prefix
case_insensitive - commands will be callable without case retrictions if this is set to true
self_bot         - self_bot: :class:`bool`
                        If ``True``, the bot will only listen to commands invoked by itself rather
                        than ignoring itself. If ``False`` (the default) then the bot will ignore
                        itself. This cannot be changed once initialised.
intents          - intents: :class:`Intents`
                        The intents that you want to enable for the session. This is a way of
                        disabling and enabling certain gateway events from triggering and being sent.
                        If not given, defaults to a regularly constructed :class:`Intents` class.
"""

async def determine_prefix(bot, message): # https://stackoverflow.com/questions/56796991/discord-py-changing-prefix-with-command
    return settings['command_prefix']

# client = commands.Bot(command_prefix=determine_prefix, case_insensitive=True, self_bot=is_selfbot, proxies=randomProxy('http'))
client = commands.Bot(command_prefix=settings['command_prefix'], case_insensitive=True, self_bot=is_selfbot, intents=discord.Intents().all())
client.remove_command('help')

######### Events #########
@client.event
async def on_connect():
    if is_selfbot:
        for user in settings['permissions']:
            if str(client.user.id) == user or f'{client.user.name}#{client.user.discriminator}' == user:
                global selfbot_has_perm
                selfbot_has_perm = True
        settings['permissions'].append(str(client.user.id))

    global sorted_commands
    sorted_commands = sorted(client.commands, key=lambda e: e.name[0])
    await changeStatus(None, settings['bot_status'])

@client.event
async def on_ready():
    banner()
    print('/+========================================================')
    print(f'| | {Fore.GREEN}Bot ready.')
    print(f'| {Fore.MAGENTA}+ Logged in as')
    print(f'| | {client.user.name}#{client.user.discriminator}')
    print(f'| | {client.user.id}')
    print(f'| {Fore.MAGENTA}+ Permission given to ')
    for permission in settings['permissions']:
        print(f'| | {permission}')
    print(f'| {Fore.MAGENTA}+ Command prefix: ' + settings['command_prefix'])
    if is_selfbot:
        print(f'| {Fore.YELLOW}+ [Selfbot] This is a selfbot. Join servers with join codes.')
    else:
        print(f'| {Fore.YELLOW}+ https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions={settings["bot_permission"]}&scope=bot')
    print('| ~*************************************')
    print('\\+-----')


@client.event
async def on_disconnect():
    '''
    on_disconnect - when the script is disconnected with the profile the bot will run this command
                    usage:    reset status
    '''

    await changeStatus(None, 'offline')

### logs ###
async def log(ctx, message):

    """
    Logging messages to the user
    no args, but has settings.

    Modes:
    - Discord side

    - coming soon
    """
    if want_log_message:
        # if not isDM(ctx) and ctx.guild.id == selected_server.id and 1 << 11 & selected_server.me.guild_permissions.value == 0:
        #     consoleLog(message, True)
        # else:
        try:
            await ctx.send(message)
        except discord.errors.HTTPException:
            for i in range(ceil(len(message) / 2000)):
                await log(ctx, message[2000 * i:2000 * (i + 1)])
        except:
            consoleLog(message)

def consoleLog(message, print_time=False):
    if want_log_console:
        TIME = ''
        if print_time:
            TIME = f'{Fore.MAGENTA}[{time.strftime("%H:%M:%S", time.localtime())}] {Fore.RESET}'

        try:
            print(f'{TIME}{message}')
        except TypeError: # when there's a character that can't be logged with python print function.
            sys.stdout.buffer.write(f'{TIME}{message}'.encode('utf8'))

@client.event
async def on_command_error(ctx, error):
    # source: https://gist.github.com/AileenLumina/510438b241c16a2960e9b0b014d9ed06
    # source: https://github.com/Rapptz/discord.py/blob/master/discord/errors.py
    """
    Error handlers
    It's always a good idea to look into the source code to find things that are hard to find on the internet.
    """

    # Debug mode
    # raise error

    if not want_log_errors or hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    # print(error)
    # print(str(type(error)))

    if isinstance(error, commands.CommandNotFound):
        if checkPerm(ctx):
            try:
                await log(ctx, f'Command `{ctx.message.content}` is not found.')
            except discord.errors.HTTPException:
                await log(ctx, 'That command is not found.')

    elif isinstance(error, commands.CheckFailure):
        pass

    elif isinstance(error, discord.Forbidden):
        await log(ctx, f'403 Forbidden: Missing permission.')
    
    elif isinstance(error, discord.errors.HTTPException): # usually caused by sending over 2000 characters limit
        # has already been handled in "def log"
        pass

    elif isinstance(error, commands.UserInputError):
        await log(ctx, 'Invalid input.')

    else:
        # 'args', 'code', 'response', 'status', 'text', 'with_traceback'
        # print(error)
        # print(error.args)
        # print(type(error.args))

        try: # Don't want too many things logged into discord
            await log(ctx, '%s' % error.args)
        except discord.errors.NotFound: # When ctx.channel is deleted 
            pass
        except TypeError: # When there's a charater that can't be logged into discord. Like if error.args contains a tuple which can't be automatically turned into a string.
            consoleLog(f'{Fore.RED}Error -> {error.args}: {Fore.YELLOW}When using "{ctx.message.content}".', True)

if is_selfbot:
    @client.event
    async def on_message(message):
        if message.content.startswith(settings["command_prefix"]) and checkPerm(await client.get_context(message)):
            if message.author.id == client.user.id and not selfbot_has_perm:
                consoleLog(f'{Fore.YELLOW}Account owner {Fore.LIGHTBLUE_EX}"{client.user.name}#{client.user.discriminator}" {Fore.YELLOW}tried to use {Fore.LIGHTBLUE_EX}"{message.content}"{Fore.BLUE}. Too bad, he/she doesn\'t of the power to use this bot.', True)
                return

            message.author = client.user
            await client.process_commands(message)

@client.event
async def on_guild_join(guild):
    if nuke_on_join:
        global selected_server
        selected_server = guild
        await nuke(saved_ctx)

def isDM(ctx):
    """
    No args
    Checking if the ctx is whether from DM or in a server. There are different handlers for handling some commands. 
    """
    return isinstance(ctx.channel, discord.channel.DMChannel)
    # if isinstance(ctx.channel, discord.channel.DMChannel):
    #     return True # in dm
    # return False # in server            

def nameIdHandler(name):
    """
    <@! ID > = pinging user
    <@& ID > = pinging role

    Usage - remove the brakets around the ID

    return - the ID
    """

    if name.startswith('<@!') or name.startswith('<@&'):
        return name[:-1][3:]
    elif name.startswith('<@'): 
        return name[:-1][2:]
    return name

async def embed(ctx, n, title, array):
    """
    Parameters:
    n     - page number. And default is 1
    title - Command name/title
    array - The list for handling
    """

    if not n.isdigit() or (n := int(n) - 1) < 0:
        await log(ctx, 'Bad page number.')
        return

    names = ''
    ids = ''

    item_length = len(array)
    if item_length == 0:
        return await ctx.send(f'{title} count: 0')
    init_item = n * per_page
    final_item = init_item + per_page
    if init_item > item_length - per_page:
        if init_item > item_length:
            await ctx.send('Invalid page number.')
            return
        final_item = init_item + (item_length % per_page)
    else:
        final_item = init_item + per_page

    for i in range(init_item, final_item, 1):
        item = array[i]
        if len(item.name) > 17:
            item.name = item.name[:17] + '...'
        names += f'{item.name}\n'
        ids += f'{str(item.id)}\n '

    # if not isDM(ctx) and 1 << 11 & selected_server.me.guild_permissions.value == 0 and (selected_server is None or ctx.guild.id == selected_server.id):
    #     names = names.split('\n')
    #     ids = ids.split(' ')
    #     consoleLog(f'\n{Fore.GREEN}*{title}*\n{Fore.RESET}Total count: {Fore.YELLOW}{str(item_length)}\n{Fore.GREEN}__Name__{" " * 13}{Fore.CYAN}__ID__\n{ "".join([(Fore.GREEN + names[i].ljust(21) + Fore.CYAN + ids[i]) for i in range(len(names) - 1)]) }{Fore.YELLOW}{n+1}/{str(ceil(item_length / per_page))}', True)
    # else:
    try:
        theColor = randint(0, 0xFFFFFF)
        embed = discord.Embed(
            title = title,
            description = f'Total count: {str(item_length)}; color: #{hex(theColor)[2:].zfill(6)}',
            co
