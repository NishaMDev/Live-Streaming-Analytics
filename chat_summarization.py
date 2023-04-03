# import libraries
import json
import sqlite3
import pandas as pd
import openai
import sys

class chatSummarization:
    def __init__(self, channel_name):
        self.chat_df = pd.DataFrame()
        self.OPENAI_API_KEY = ""
        self.channel_name = channel_name

    def readDatabse(self):
        # ************************************************************
        # Read the token       
        # ************************************************************
        with open('config.json', 'r') as file_to_read:
            json_data = json.load(file_to_read)
            self.OPENAI_API_KEY = json_data["OPENAI_API_KEY"]
            openai.api_key =  self.OPENAI_API_KEY
        # channel_name = "cdawgva"
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect('data/chat_table.sqlite3',isolation_level=None)

        # The result of a "cursor.execute" can be iterated over by row
        # Load the data into a DataFrame
        self.chat_df = pd.read_sql_query('SELECT message_text from chat WHERE channel_name="self.channel_name"', conn)

        # Be sure to close the connection
        conn.close()

    def summarize(self,merged_str):
        prompt= "Generate a summary of the following Twitch chat messages:" + merged_str + "Use no more than 3-4 sentences to summarize the main sentiment and topics discussed."
        response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=0,
                    max_tokens=120,
                    top_p=0.9,
                    frequency_penalty=0.0,
                    presence_penalty=1
                    )
        return response["choices"][0]["text"]

    def mergeChat(self):
        summary_list = []
        for i in range(0, len(self.chat_df['message_text']), 35):
            merged_str = ".".join(self.chat_df['message_text'][i:i+35])
            summary_list.append(self.summarize(merged_str))
        summary_text = '.'.join(summary_list)
        summary = self.summarize(summary_text)
        data = {'channel_name': [self.channel_name], 'chat_summary': [summary]} 
        self.createTable(data)


    def createTable(self, data):
        # Create DataFrame  
        summary_df = pd.DataFrame(data)  

        # Create your connection.
        conn = sqlite3.connect("data/chat_summary.sqlite3")
        
        # Write the dataframe to sqlite
        summary_df.to_sql("chat_summary", conn, if_exists='replace', index=False)
        print("Dataframe written to sqlite")

        #Commit the change
        conn.commit()

        #Close the connection
        conn.close()

if __name__ == "__main__":
    channel_name = sys.argv[0]
    chatSummary = chatSummarization(channel_name)
    chatSummary.readDatabse()
    chatSummary.mergeChat()





