# import libraries
import sqlite3
import pandas as pd
from utils import Utils
import sys
from chatSummarization import ChatSummarization
from pathlib import Path

class topicRecommendation:
    def __init__(self, channel_name, stream_date):
        self.chatsummary_df = pd.DataFrame()
        self.channel_name = channel_name
        self.stream_date = stream_date

    def readDatabase(self):
        # Create a Path object with the path to the file
        path = Path('../data/db.sqlite3')
        chatSummary = ChatSummarization(self.channel_name, self.stream_date)
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
            conn = sqlite3.connect('../data/db.sqlite3',isolation_level=None)
            # Check if the column exists
            column_name = 'topics'
            table_name = 'chat_summary'
            cur = conn.cursor()
            cur.execute(f"PRAGMA table_info({table_name})")
            columns = [column[1] for column in cur.fetchall()]
            if column_name not in columns:
                # Add a new column to the "chat_summary" table
                conn.execute('ALTER TABLE chat_summary ADD COLUMN topics TEXT')
            
            # Insert data into the new "topics" column
            conn.execute("UPDATE chat_summary SET topics = ? WHERE channel_name = ? and stream_date = ?", (topic,self.channel_name, self.stream_date))

            # Commit the changes
            conn.commit()
            print("table updated")
            # Close cursor
            cur.close()
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
                conn = sqlite3.connect('../data/db.sqlite3',isolation_level=None)
                # Load the data into a DataFrame
                result = pd.read_sql_query("SELECT * FROM chat_summary WHERE stream_date = ? AND channel_name = ?", conn, params=(self.stream_date, self.channel_name))
                # Be sure to close the connection
                conn.close()
                return result['topics'][0]

            except sqlite3.Error as error:
                print("Failed to read data from chat_summary table", error)

            finally:
                if conn:
                    conn.close()


if __name__ == "__main__":
    channel_name = sys.argv[1]
    stream_date = sys.argv[2]
    topicRec = topicRecommendation(channel_name, stream_date)
    topicRec.readDatabase()
    topicRec.getChatTopics()





