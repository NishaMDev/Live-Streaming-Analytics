# import libraries
import sqlite3
import pandas as pd
import sys
from scripts.utils import Utils

dbPath = 'data/db.sqlite3'


class ChatSummarization:
    def __init__(self, channel_name, stream_date):
        self.chat_df = pd.DataFrame()
        self.channel_name = channel_name
        self.stream_date = stream_date
        
    def readDatabase(self):
        # channel_name = "cdawgva"
        # Create a SQL connection to our SQLite database
        try:
            conn = sqlite3.connect(dbPath,isolation_level=None)

            # Load the data into a DataFrame
            self.chat_df = pd.read_sql_query("SELECT message_text FROM chats WHERE stream_date = ? AND channel_name = ?", conn, params=(self.stream_date, self.channel_name))

            # Be sure to close the connection
            conn.close()
        
        except sqlite3.Error as error:
            print("Failed to read data from chat table", error)
        
        finally:
            if conn:
                conn.close()
        

    def summarize(self,merged_str):
        util = Utils()
        openai = util.getAPIKeys()
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
        # get the chunks for the chat messages
        text = ".".join(self.chat_df['message_text'])
        util = Utils()
        chunks = util.createChunks(2500, text)
        for chunk in chunks:
            summary_list.append(self.summarize(chunk))
        summary_text = '.'.join(summary_list)
        summary = self.summarize(summary_text)
        data = {'channel_name': [self.channel_name], 'stream_date': [self.stream_date] ,'chat_summary': [summary]} 
        self.createTable(data)


    def createTable(self, data):
        # Create DataFrame  
        summary_df = pd.DataFrame(data)  
        try:
        # Create your connection.
            conn = sqlite3.connect(dbPath)
            
            # Write the dataframe to sqlite
            summary_df.to_sql("chat_summary", conn, if_exists='replace', index=False)
            print("Dataframe written to sqlite")

            #Commit the change
            conn.commit()

            #Close the connection
            conn.close()
        except sqlite3.Error as error:
            print("Failed to create chat_summary table", error)
        
        finally:
            if conn:
                conn.close()
    
    def getChatSummary(self):
            # Create a SQL connection to our SQLite database
            try:
                conn = sqlite3.connect(dbPath,isolation_level=None)
                # Load the data into a DataFrame
                result = pd.read_sql_query("SELECT chat_summary FROM chat_summary WHERE stream_date = ? AND channel_name = ?", conn, params=(self.stream_date, self.channel_name))
                # Be sure to close the connection
                conn.close()
                return result['chat_summary'][0]

            except sqlite3.Error as error:
                print("Failed to read data from chat_summary table", error)

            finally:
                if conn:
                    conn.close()
        

if __name__ == "__main__":
    channel_name = sys.argv[1]
    stream_date = sys.argv[2]
    print("self.channel_name", channel_name)
    chatSummary = ChatSummarization(channel_name, stream_date)
    chatSummary.readDatabase()
    chatSummary.mergeChat()
    res = chatSummary.getChatSummary()
    print(res)
  




