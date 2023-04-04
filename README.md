# Live-Streaming-Analytics

Twitch API tokens are present in json file.

Steps:

Run the load.py to load chats in sqlite

        python load.py


Run sentiment_analysis.py to read chats from db and perform sentimental analysis on them and load in chat table.

        python sentiment_analysis.py
        
        
Run chat_summarization.py to read chats from db and perform chat summarization on them and load in chat summary table.

        python chat_summarization.py        
