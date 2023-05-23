# Live-Streaming-Analytics


<img width="1649" alt="Screenshot 2023-05-23 at 3 39 24 PM" src="https://github.com/NishaMDev/Live-Streaming-Analytics/assets/89233753/9ed33c04-fe70-4046-ad74-25ce2665c412">

 <img width="1649" alt="Screenshot 2023-05-23 at 3 39 29 PM" src="https://github.com/NishaMDev/Live-Streaming-Analytics/assets/89233753/6da30c81-4c47-48c1-85f5-0d89d181d973">

<img width="1649" alt="Screenshot 2023-05-23 at 3 39 35 PM" src="https://github.com/NishaMDev/Live-Streaming-Analytics/assets/89233753/47810a14-f511-4983-a4fd-9acf2bdb8f53">

<img width="1649" alt="Screenshot 2023-05-23 at 3 39 40 PM" src="https://github.com/NishaMDev/Live-Streaming-Analytics/assets/89233753/664e9122-8b0d-4f04-b29f-59c69fcd425a">

<img width="1649" alt="Screenshot 2023-05-23 at 3 39 45 PM" src="https://github.com/NishaMDev/Live-Streaming-Analytics/assets/89233753/47d75b82-e234-4955-9cbf-0d9c05420aa5">

<img width="1649" alt="Screenshot 2023-05-23 at 3 39 52 PM" src="https://github.com/NishaMDev/Live-Streaming-Analytics/assets/89233753/0e8a858a-807a-43b8-8489-ae6b0b5ea633">

## Model used:

The twitch chat are summarized by the transformer-based GPT-3 DaVinci model, using input prompts and messages.
Stream chats tile shows how the underlying fine-tuned **OPENAI's GPT-3** is a state-of-the-art (NLP) model classifies sentiments of ongoing chats.

## Technical Pipeline:

![TechnicalPipeline drawio](https://github.com/NishaMDev/Live-Streaming-Analytics/assets/89233753/204119b2-ffb5-4a9b-b651-f22529ed1518)


## Steps to run the code:

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
        
To run the web application run below commands:-
        
        export FLASK_APP=run.py
        
        flask run --host=0.0.0.0 --port=5000

