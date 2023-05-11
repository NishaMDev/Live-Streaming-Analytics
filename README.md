# Live-Streaming-Analytics

 
Twitch API tokens are present in json file.

Steps:

Run the load.py to load chats in sqlite

        python load.py

Run the dataPreparation.py to replace emotes in chats in update chats in sqlite

        python dataPreparation.py

Run sentiment_analysis.py to read chats from db and perform sentimental analysis on them and load in chat table.

        python sentimentAnalysis.py

Run chatSummarization.py to read chats from db and perform chat summarization on them and load in chat summary table.

        python chatSummarization.py

Run topicRecommendation.py to read chats from db and perform topic recommendation on them and load in chat summary table.

        python topicRecommendation.py
