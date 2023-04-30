from flask import render_template, redirect, url_for, request, jsonify
from flask import Blueprint
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import random
import os
import sqlite3
import pandas as pd

import scripts.data_gathering_functions as dg
from scripts.read_sentiments_from_db import read_sentiments
from . import db

main = Blueprint('main', __name__)

@main.route('/index')
@login_required
def index():
    return render_template('index.html', segment='index')

@main.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  

@main.route('/test')
# @login_required
def testfn():
    # GET request
    if request.method == 'GET':
        message = {'greeting':'Hello from Flask!!!'}
        return jsonify(message)  
    
    # POST request
    if request.method == 'POST':
        return 'Sucesss', 200



@main.route('/read_random_sentiments')
# @login_required
def get_rand_sentiments():
   return read_sentiments()


@main.route('/refresh_sentiments')
# @login_required
def get_sentiments():
   num = random.uniform(0, 1)
   print('Hello from refresh_sentiments: ', num)
   return str(num)



@main.route('/index')
# @login_required
def home():
   return render_template('index.html')


### Tiles Data Pull

@main.route('/total_messages')
# @login_required
def total_chat_messages():
    """
    Calls get_message_count and returns the total message count of the stream
    output: total_messages (int)
    """
    streamer_choose_id = request.args.get('streamer_choose_id')
    streamer_choose_dt = request.args.get('streamer_choose_dt')
    
    total_messages = dg.get_message_count(streamer_choose_id, streamer_choose_dt)
    print('in dq total_messages: ', total_messages)
    str_total_messages = '{:,}'.format(round(total_messages))
    print('in dq str_total_messages: ', str_total_messages)
    return '<p>'+str_total_messages+'</p>'

@main.route('/average_viewers')
# @login_required
def average_viewers():
    """
    Calls get_average_view_count and returns the average view count of the stream``
    output: average_viewers (float)
    """
    streamer_choose_id = request.args.get('streamer_choose_id')
    streamer_choose_dt = request.args.get('streamer_choose_dt')
    
    average_viewers = dg.get_average_view_count(streamer_choose_id, streamer_choose_dt)
    print('average_viewers: ', average_viewers)
    str_average_viewers = '{:,}'.format(round(average_viewers))
    return '<p>'+str_average_viewers+'</p>'

@main.route('/followers_change')
# @login_required
def new_followers():
    """
    Calls get_follower_change and returns the change in followers from the start to end of the stream
    output: follower_change (int)
    """
    streamer_choose_id = request.args.get('streamer_choose_id')
    streamer_choose_dt = request.args.get('streamer_choose_dt')
    
    follower_change = dg.get_follower_change(streamer_choose_id, streamer_choose_dt)
    
    if follower_change > 0:
         follower_change_str = '+' + '{:,}'.format(follower_change)
    elif follower_change < 0:
         follower_change_str = '{:,}'.format(follower_change)
    else:
        follower_change_str = '{:,}'.format(follower_change)

    return follower_change_str


@main.route('/pct_follower_change')
# @login_required
def pct_new_followers():
    """
    Calls get_follower_change and returns the change in followers from the start to end of the stream
    output: follower_change (int)
    """
    streamer_choose_id = request.args.get('streamer_choose_id')
    streamer_choose_dt = request.args.get('streamer_choose_dt')
    
    follower_change_pct = dg.get_pct_follower_change(streamer_choose_id, streamer_choose_dt)
    print('follower_change_pct: ', follower_change_pct)
    
    if follower_change_pct > 0:
        follower_change_pct_str = str(follower_change_pct) + '% Gain'
    elif follower_change_pct < 0:
        follower_change_pct_str = str(follower_change_pct) + '% Loss'
    else:
        follower_change_pct_str = str(follower_change_pct) + '% Change'
    
    return follower_change_pct_str


@main.route('/subscriber_change')
# @login_required
def new_subscribers():
    """
    Calls get_subscriber_change and returns the change in subscribers from the start to end of the stream
    output: follower_change (int)
    """
    streamer_choose_id = request.args.get('streamer_choose_id')
    streamer_choose_dt = request.args.get('streamer_choose_dt')
    print('---> test receive_streamer_visitors: [START] --> ')
    print(streamer_choose_id)
    print(streamer_choose_dt)
    print('---> test receive_streamer_visitors: [END] --> ')
    

    subscriber_change = dg.get_subscriber_change(streamer_choose_id, streamer_choose_dt)

    if subscriber_change > 0:
         subscriber_change_str = '+' + '{:,}'.format(subscriber_change)
    elif subscriber_change < 0:
        subscriber_change_str = '{:,}'.format(subscriber_change)
    else:
        subscriber_change_str = '{:,}'.format(subscriber_change)

    return subscriber_change_str

@main.route('/pct_subscriber_change')
# @login_required
def pct_new_subscribers():
    """
    Calls get_pct_subscriber_change and returns the percentage change in subscribers from
    the start to the end of the stream
    output: pct_subscriber_change (int)
    """
    streamer_choose_id = request.args.get('streamer_choose_id')
    streamer_choose_dt = request.args.get('streamer_choose_dt')
    
    
    subscriber_change_pct = dg.get_pct_subscriber_change(streamer_choose_id, streamer_choose_dt)
    print('subscriber_change_pct: ', subscriber_change_pct)
    
    if subscriber_change_pct > 0:
        subscriber_change_pct_str = str(subscriber_change_pct) + '% Gain'
    elif subscriber_change_pct < 0:
        subscriber_change_pct_str = str(subscriber_change_pct) + '% Loss'
    else:
        subscriber_change_pct_str = str(subscriber_change_pct) + '% Change'
    
    return subscriber_change_pct_str
    

@main.route('/avg_sentiment')
# @login_required
def average_sentiment():
    """
    Calls get_average_sentiment and returns the average sentiment of the stream
    output: average_sentiment (float)
    """
    streamer_choose_id = request.args.get('streamer_choose_id')
    streamer_choose_dt = request.args.get('streamer_choose_dt')
    
    average_sentiment = dg.get_average_sentiment(streamer_choose_id, streamer_choose_dt)
    print("average_sentiment - ",average_sentiment)
    return '<p>'+str(round(average_sentiment, 2))+'</p>'

@main.route('/chat_percentages')
# @login_required
def chat_percentages():
    """
    Calls get_average_sentiment and returns the average sentiment of the stream
    output: average_sentiment (float)
    """
    streamer_choose_id = request.args.get('streamer_choose_id')
    streamer_choose_dt = request.args.get('streamer_choose_dt')
    print('---> avg_sentiment')
    
    chat_percentages = dg.get_pct_positive_negative(streamer_choose_id, streamer_choose_dt)
    return chat_percentages

@main.route('/avg_chatters')
# @login_required
def average_chatters():
    """
    Calls get_average_chatters and returns the average number of chatters in the chatroom
    output: follower_change (float)
    """
    streamer_choose_id = request.args.get('streamer_choose_id')
    streamer_choose_dt = request.args.get('streamer_choose_dt')
 
    average_chatters = dg.get_average_chatters(streamer_choose_id, streamer_choose_dt)
    print("average_chatters: ", average_chatters)
    str_average_chatters = '{:,}'.format(round(average_chatters))
    return '<p>'+str_average_chatters+'</p>' 

@main.route('/rec_engine_output_table')
# @login_required
def get_recommendations():
    """
    Calls recommender_engine and a dictionary of values and scores corresponding to the recommender model
    output: recommendation_dict (dict)
    """
    streamer_choose_id = request.args.get('streamer_choose_id')
    streamer_choose_dt = request.args.get('streamer_choose_dt')
    sorted_choices = request.args.get('sorted_choices')
    
    print('Here are the sorted choices ---> ', sorted_choices)
    return dg.recommender_engine(streamer_choose_id, streamer_choose_dt, sorted_choices)
