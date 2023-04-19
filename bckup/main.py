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
    
csvFilePath = 'data/facttable/EmoteFactTable.csv'
jsonFilePath = 'data/emotes.json'   

# # ************************************************************
# # Connect to chat server
# # ************************************************************
# bot = listener.connect_twitch(nickname, 
#                              oauth_chat, 
#                              client_id,
#                              oauth_api)

# # Returns list of live channels
# channels_to_listen_to = ['cryocells','jingggxd','gmhikaru','lirik','zackrawrr','katarinafps','cdawgva','stewie2k','summit1g','tarik']
# channels_to_listen_to = utils.is_live(channels_to_listen_to)

# # ************************************************************
# # Get Broadcast ID for API calls
# # ************************************************************
# channels_to_listen_to = utils.get_broadcast_id(channels_to_listen_to, client_id, oauth_api)
# print(" channels live now - ",channels_to_listen_to)
# # ************************************************************
# # Scrape live chat data, viewers, followers, etc into sqlite database (Duration is seconds).
# # ************************************************************
# bot.listen(channels_to_listen_to, duration = 50, until_offline = True, debug = False) 
# print("Database loading completed.")

conn = sqlite3.connect('data/db.sqlite3',isolation_level=None)
# Load data into pandas DataFrame
chat_df = pd.read_sql('select date,stream_datetime, stream_length, username, message_text, channel_name,stream_topic,stream_title, chatter_count, viewer_count, subscriber_count, stream_date, stream_id from chats_table_demo', conn)
# Close the connection
conn.close()

# ************************************************************
#  Read Emote fact file , convert it to json and save it as emotes.json
# ************************************************************
utils.emote_to_json(csvFilePath,jsonFilePath)
emote_json = utils.reload_json(jsonFilePath)

# # input sentence with emotes
# sentence = "I just got PJSalt in my game!"
# # print result
# print("Result: "+ utils.replace_emoticons(sentence,emote_json))

# chat_df['new_message_text'] = chat_df['message_text'].map(utils.replace_emoticons)
chat_df['new_message_text'] = chat_df['message_text'].map(lambda x: utils.replace_emoticons(x, emote_json))
# print(chat_df.head(10))

# ************************************************************
# Score sentiment of chat messages.
# ************************************************************
batch_size = 80
openai.api_key =  OPENAI_API_KEY

print("Print first line of new message text "+chat_df['new_message_text'][0])
total_rows = chat_df.shape[0]
print("chat_len: "+ str(total_rows))

chat_df['general_sentiment'] =''
chat_df['specific_sentiment'] =''

# loop through all the rows
for i in range(0, total_rows, batch_size):
    # get the 1000 chats from the data frame
    chat_df_batch = chat_df.iloc[i:i+batch_size]
    chat_batch_list = chat_df_batch['new_message_text'].tolist()
    # print("chat_batch_list: "+ str(chat_batch_list))
    
    j = 1
    chat_batch_str=''
    for chat in chat_batch_list:
        chat_batch_str = chat_batch_str + str(j) +'.'+'"'+ chat +'"'+'\n'
        j=j+1

    response_genlist = utils.general_sentiments(chat_batch_str)
    response_spelist = utils.specific_sentiments(chat_batch_str) 

    #chat_df.loc[i:i+batch_size, 'general_sentiment'] = response_genlist
    chat_df['general_sentiment'].iloc[i:i+batch_size] = response_genlist
    chat_df['specific_sentiment'].iloc[i:i+batch_size] = response_spelist
  
    print("Completed: "+ str(i) + " out of "+ str(total_rows))
    
# Create your connection.
conn = sqlite3.connect("data/chat_table.sqlite3")
 
# Write the dataframe to sqlite
chat_df.to_sql("chat", conn, if_exists='replace', index=False)
print("Dataframe written to sqlite")

#Commit the change
conn.commit()

#Close the connection
conn.close()
#