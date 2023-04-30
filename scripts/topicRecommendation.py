# import libraries
import sqlite3
import pandas as pd
from utils import Utils
import sys
from chatSummarization import ChatSummarization
from pathlib import Path

class topicRecommendation:
    def __init__(self, channel_name):
        self.chatsummary_df = pd.DataFrame()
        self.channel_name = channel_name

    def readDatabase(self):
        # Create a Path object with the path to the file
        path = Path('../data/chat_summary.sqlite3')
        chatSummary = ChatSummarization(self.channel_name)
        if path.is_file() == False:
            chatSummary.readDatabase()
            chatSummary.mergeChat()
        result = chatSummary.getChatSummary()
        self.chatsummary_df = pd.DataFrame([result], columns=['chat_summary'])
        summary = self.chatsummary_df['chat_summary']
        self.getTopicRecommendations(summary[0])

    def getTopicRecommendations(self, summary):
        util = Utils()
        openai = util.getAPIKeys()
        prompt = "Provide topic recommendations from the text: \n"+ summary
        model = "text-davinci-002"
        completions = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=120,
            n=20,
            stop=None,
            temperature=0,
        )

        message = completions.choices[0].text.strip()
        topic = str(message)
        try:
            conn = sqlite3.connect('../data/chat_summary.sqlite3',isolation_level=None)
            # Add a new column to the "chat_summary" table
            conn.execute('ALTER TABLE chat_summary ADD COLUMN topics TEXT')

            # Insert data into the new "topics" column
            conn.execute("UPDATE chat_summary SET topics = ? WHERE channel_name = ?", (topic,self.channel_name))

            # Commit the changes
            conn.commit()
            print("table updated")
            # Close the connection
            conn.close()

        except sqlite3.Error as error:
                print("Failed to update data to chat_summary table", error)

        finally:
            if conn:
                conn.close()

    def getChatTopics(self):
            # Create a SQL connection to our SQLite database
            try:
                conn = sqlite3.connect('../data/chat_summary.sqlite3',isolation_level=None)
                # The result of a "cursor.execute" can be iterated over by row
                # Load the data into a DataFrame
                cur = conn.cursor()
                sql_select_query = """SELECT * from chat_summary WHERE channel_name= ?"""
                cur.execute(sql_select_query, (self.channel_name,))
                result = cur.fetchone()
                # Be sure to close the connection
                conn.close()
                print(result[2])

            except sqlite3.Error as error:
                print("Failed to read data from chat_summary table", error)

            finally:
                if conn:
                    conn.close()


if __name__ == "__main__":
    channel_name = sys.argv[1]
    topicRec = topicRecommendation(channel_name)
    topicRec.readDatabase()
    topicRec.getChatTopics()





