import logging
import requests
import json
from scripts.twitch_listener import sqlite_handler
import random
import os
import torch
import csv
import openai

def setup_loggers(name, log_file, level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s — %(message)s')
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(formatter)
    
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

def setup_sqllite_loggers(channel_name, level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s — %(message)s')
        #handler = logging.FileHandler(sqlite_handler.SQLiteHandler('db.sqlite3'))        
        #handler.setFormatter(formatter)
    
        logger = logging.getLogger(channel_name)
        logger.setLevel(level)
        logger.addHandler(sqlite_handler.SQLiteHandler('../data/db.sqlite3'
                                                       , channel_name))
        
#         logger = logging.getLogger('someLoggerNameLikeDebugOrWhatever')
#         logger.setLevel(logging.DEBUG)
#         logger.addHandler(SQLiteHandler('db.sqlite3'))
#         logger.debug('Test 1')
#         logger.warning('Some warning')
#         logger.error('Alarma!')

        return logger
    
def emote_to_json(csvFilePath,jsonFilePath):
# ************************************************************
#  Read Emote fact file , convert it to json and save it as emotes.json
# ************************************************************
    csvFilePath = csvFilePath
    jsonFilePath = jsonFilePath
    data = {}
    
    with open(csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            emotes = rows['Emote']
            desc = rows['Definition 1']
            data[emotes] = desc

    with open(jsonFilePath, 'w') as jsonFile:
        jsonFile.write(json.dumps(data, indent=4))
        
def reload_json(jsonFilePath):
# ************************************************************
# Load emotes.json , use it to replace the twitch emotes in the chat text with its meaning and save it in a new column - 'new_message_text' .
# this new column will be used for further processing.
# ************************************************************
    with open(jsonFilePath, 'r') as json_file:
        data = json.load(json_file)

    return data

def replace_emoticons(text,emote_json): 
    # loop through each emote
    for emote in emote_json:
    # replace emote with meaning
      text = text.replace(emote, emote_json[emote])
  
    # Return the result
    return text

def is_live(channel_list):
    
    live_channels = []
    for channel in channel_list:
        contents = requests.get('https://www.twitch.tv/' +channel).content.decode('utf-8')

        if 'isLiveBroadcast' in contents:
            live_channels.append(channel)
        
    return live_channels

def get_broadcast_id(channel_list, client_id, o_auth_api):
    
    id_list = {}
    for channel in channel_list:
        contents = requests.get('https://api.twitch.tv/helix/users?login=' + channel,
                        headers={"Authorization":o_auth_api, "Client-Id": client_id}).content.decode('utf-8')
        user_data = json.loads(contents)
        id_list[channel] = user_data['data'][0]['id']  
        
    return id_list


def view_count(chatter_count):
    
    if chatter_count > 5000:
        viewer_count = round(chatter_count / .7)
    elif chatter_count <= 5000:
        viewer_count = round(chatter_count / .8)
    else:
        viewer_count = round(chatter_count / .8)
        
    viewer_count = random.randint(round(viewer_count *.95), round(viewer_count * 1.1))
                                    
        
    return viewer_count

def general_sentiments(chat_1000_str):
    prompt_general="Classify the sentiment in these tweets:\n" + chat_1000_str + "\n Tweet sentiment ratings in terms of Positive, Negative or Neutral:"
    response_general = openai.Completion.create(
                              model="text-davinci-003",
                              prompt=prompt_general,
                              temperature=0,
                              max_tokens=1000,
                              top_p=1.0,
                              frequency_penalty=0.0,
                              presence_penalty=0.0)
    
    response_genlist = ((response_general["choices"][0]["text"]).split('\n'))[1:]
    response_genlist = [i.strip('1234567890. ') for i in response_genlist]

    for i in range(len(response_genlist)):
        if response_genlist[i] == 'Positive':
            response_genlist[i] = '1'
        elif response_genlist[i] == 'Negative':
            response_genlist[i] = '-1'
        else:
            response_genlist[i] = '0'
   
    return response_genlist

def specific_sentiments(chat_1000_str):
    prompt_specific="Classify the sentiment in these tweets:\n" + chat_1000_str + "\n Tweet sentiment ratings in one word :"  
    print("prompt_specific - ",prompt_specific)
    response_specific = openai.Completion.create(
                              model="text-davinci-003",
                              prompt=prompt_specific,
                              temperature=0,
                              max_tokens=1000,
                              top_p=1.0,
                              frequency_penalty=0.0,
                              presence_penalty=0.0)
    response_spelist = ((response_specific["choices"][0]["text"]).split('\n'))[1:] 
    response_spelist = [i.strip('1234567890. ') for i in response_spelist]
    return response_spelist

def sentiment_probability(chat_str):
    prompt_senti_probability="Classify the sentiment in these tweets:\n" + chat_str + "\n .Tweet sentiment ratings in terms \
    of Positive, Negative or Neutral in terms of prediction probability for each classes in the format of \
    dictionary {Positive: probability, Negative: probability, Neutral: probability}"  
    print("prompt_senti_probability - ",prompt_senti_probability)
    response_senti_probability = openai.Completion.create(
                              model="text-davinci-003",
                              prompt=prompt_senti_probability,
                              temperature=0,
                              max_tokens=1000,
                              top_p=1.0,
                              frequency_penalty=0.0,
                              presence_penalty=0.0)
    response_proba = ((response_senti_probability["choices"][0]["text"]).split('\n'))[1:] 
    response_proba = response_proba[1]
    result =dict((x.strip(), float(y.strip())) for x, y in (element.split(':') for element in response_proba.strip('{}').split(',')))
    return result

def subscriber_count(followers):
    
    if followers >= 10000:
        subscribers = round(followers / 80)
    elif followers >= 5000:
        subscribers = round(followers / 50)
    elif followers >= 200:
        subscribers = round(followers / 30)
    elif followers >= 100:
        subscribers = round(followers / 25)
    elif followers >= 0:
        subscribers = round(followers / 25)
    else:
        subscribers = round(followers / 25)
    
    subscribers = random.randint(round(subscribers *.95), round(subscribers * 1.1))
                                    
        
    return subscribers


    
    