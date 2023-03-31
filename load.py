##5 * * * * /home/aspera/my_script.sh

from twitch_listener import utils
from twitch_listener import listener
import argparse
import json
import sqlite3
import time
import csv
import pandas as pd
import os


# ************************************************************
# Read in channels to listen to from arguments.
# ************************************************************
# parser = argparse.ArgumentParser(description='Get list of channels')
# parser.add_argument('-l','--channels', nargs='+', help='<Required> set channels', required=True)

# for _, value in parser.parse_args()._get_kwargs():
#     if value is not None:
#         channels_to_listen_to = value

# skip_loading = False

# ************************************************************
# Define tokens        
# ************************************************************
with open('config.json', 'r') as file_to_read:
    json_data = json.load(file_to_read)
    OPENAI_API_KEY = json_data["OPENAI_API_KEY"]
    nickname = json_data["NICKNAME"]
    oauth_chat = json_data["OAUTH_CHAT"]
    client_id = json_data["CLIENT_ID"]
    oauth_api = json_data["OAUTH_API"]


# ************************************************************
# Connect to chat server
# ************************************************************
bot = listener.connect_twitch(nickname, 
                             oauth_chat, 
                             client_id,
                             oauth_api)

# Returns list of live channels
channels_to_listen_to = ['cryocells','jingggxd','gmhikaru','lirik','zackrawrr','katarinafps','cdawgva','stewie2k','summit1g','tarik']
channels_to_listen_to = utils.is_live(channels_to_listen_to)

# ************************************************************
# Get Broadcast ID for API calls
# ************************************************************
channels_to_listen_to = utils.get_broadcast_id(channels_to_listen_to, client_id, oauth_api)
print(" channels live now - ",channels_to_listen_to)
# ************************************************************
# Scrape live chat data, viewers, followers, etc into sqlite database (Duration is seconds).
# ************************************************************
bot.listen(channels_to_listen_to, duration = 30, until_offline = True, debug = False) 
print("Database loading completed.")
# ************************************************************