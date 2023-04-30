# import libraries
import sqlite3
import pandas as pd
import sys
from utils import Utils

class ChatSummarization:
    def __init__(self, channel_name):
        self.chat_df = pd.DataFrame()
        self.channel_name = channel_name
        
    def readDatabase(self):
        # channel_name = "cdawgva"
        # Create a SQL connection to our SQLite database
        try:
            conn = sqlite3.connect('../data/chat_table.sqlite3',isolation_level=None)

            # The result of a "cursor.execute" can be iterated over by row
            # Load the data into a DataFrame
            self.chat_df = pd.read_sql_query('SELECT message_text from chats WHERE channel_name="self.channel_name"', conn)

            # Be sure to close the connection
            conn.close()
            print(self.chat_df['message_text'])
        
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
        data = {'channel_name': [self.channel_name], 'chat_summary': [summary]} 
        self.createTable(data)


    def createTable(self, data):
        # Create DataFrame  
        summary_df = pd.DataFrame(data)  
        try:
        # Create your connection.
            conn = sqlite3.connect("../data/chat_summary.sqlite3")
            
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
                conn = sqlite3.connect('../data/chat_summary.sqlite3',isolation_level=None)
                # The result of a "cursor.execute" can be iterated over by row
                # Load the data into a DataFrame
                cur = conn.cursor()
                sql_select_query = """SELECT chat_summary from chat_summary WHERE channel_name= ?"""
                cur.execute(sql_select_query, (self.channel_name,))
                result = cur.fetchone()
                # Be sure to close the connection
                conn.close()
                return result

            except sqlite3.Error as error:
                print("Failed to read data from chat_summary table", error)

            finally:
                if conn:
                    conn.close()
        

if __name__ == "__main__":
    channel_name = sys.argv[1]
    print("self.channel_name", channel_name)
    chatSummary = ChatSummarization(channel_name)
    chatSummary.readDatabase()
    chatSummary.mergeChat()
    res = chatSummary.getChatSummary()
    print(res[0])





