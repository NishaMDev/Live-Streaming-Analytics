# Live-Streaming-Analytics


<img src="https://github.com/NishaMDev/Live-Streaming-Analytics/assets/89233753/1ab318dc-5f97-4a70-bf90-ad1fd449dd22" width="900"/>

 
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
