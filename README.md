# Live-Streaming-Analytics

Twitch API tokens are present in json file.

Steps:

Run the load.py to load chats in sqlite

        python load.py


Run main.py to read chats from db and perform sentimental analysis on them and load in chat table.

        python main.py
