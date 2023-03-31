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
import openai

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
csvFilePath = 'EmoteFactTable.csv'
jsonFilePath = 'emotes.json'   

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
bot.listen(channels_to_listen_to, duration = 50, until_offline = True, debug = False) 
print("Database loading completed.")

conn = sqlite3.connect('data/db.sqlite3',isolation_level=None)
# Load data into pandas DataFrame
chat_df = pd.read_sql('select username, channel_name, date, message_text from chats_table_demo', conn)
# Close the connection
conn.close()

# ************************************************************
#  Read Emote fact file , convert it to json and save it as emotes.json
# ************************************************************
utils.emote_to_json(csvFilePath,jsonFilePath)
emote_json = utils.reload_json(jsonFilePath)

# input sentence with emotes
sentence = "I just got PJSalt in my game!"

# print result
print("Result: "+ utils.replace_emoticons(sentence,emote_json))

chat_df['new_message_text'] = chat_df['message_text'].map(utils.replace_emoticons)
print("chat_df: "+ chat_df.head(10))

# ************************************************************
# Score sentiment of chat messages.
# ************************************************************
# Load model & tokenizer

openai.api_key =  OPENAI_API_KEY

print("Print first line of new message text "+chat_df['new_message_text'][0])
total_rows = chat_df.shape[0]
print("chat_len: "+ str(total_rows))

# loop through all the rows
for i in range(0, total_rows, 1000):
    # get the 1000 chats from the data frame
    chat_df_1000 = chat_df.iloc[i:i+1000]
    chat_1000_list = chat_df_1000['new_message_text'].tolist()
    
    j =1
    chat_1000_str=''
    for chat in chat_1000_list:
        chat_1000_str = chat_1000_str + str(j) +'.'+'"'+ chat +'"'+'\n'
        j=j+1

    response_genlist = utils.general_sentiments(chat_1000_str)
    response_spelist = utils.specific_sentiments(chat_1000_str) 
    
    chat_df['general_sentiment'].iloc[i:i+1000] = response_genlist
    chat_df['specific_sentiment'].iloc[i:i+1000] = response_spelist
  
    print("Completed: "+ str(i) + " out of "+ str(total_rows))
#


