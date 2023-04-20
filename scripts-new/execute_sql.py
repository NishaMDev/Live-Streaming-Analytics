##5 * * * * /home/aspera/my_script.sh


import sqlite3
import pandas as pd



class executeSql:
    def __init__(self):
       
        self.OPENAI_API_KEY = ""
        
    def selectChatTable(self):

        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect('../data/chat_table.sqlite3',isolation_level=None)
        cur = conn.cursor()
        query = '''SELECT date,
                            stream_datetime, 
                            stream_length, 
                            username, 
                            message_text, 
                            channel_name,
                            stream_topic,
                            stream_title, 
                            chatter_count, 
                            viewer_count, 
                            follower_count, 
                            subscriber_count, 
                            stream_date, 
                            stream_id, 
                            new_message_text,
                            general_sentiment,
                            specific_sentiment
                        FROM chats 
                        WHERE general_sentiment = '' 
                    '''
                      
        cur.execute(query) 
        result = cur.fetchall() 
        print(len(result))

    def getMaxDate(self):
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect('../data/db.sqlite3',isolation_level=None)
        cur = conn.cursor()
        query = '''SELECT DISTINCT MAX(stream_datetime) FROM chats'''
                    
        cur.execute(query) 
        result = cur.fetchall() 
        maxDate = result[0][0]
        print(maxDate)
        return maxDate
    
    
    def selectNewChats(self):
        maxDate = self.getMaxDate()
        conn = sqlite3.connect('../data/db.sqlite3',isolation_level=None)
        cur = conn.cursor()
        
        select_query = '''SELECT * FROM chats_table_demo WHERE stream_datetime > '%s' ''' % (maxDate)
        
        print(select_query)
        #cur.execute(select_query)
        #result = cur.fetchall() 
        #print(type(result)) 
        
        chat_df = pd.read_sql(select_query, conn)
        print("Start to print new chats details :-")
        print(chat_df.head())
        print("Number of new rows to be processed:- ",chat_df.shape[0])
            
        
        #for row in result:
        #    print(row)       
    
    def copytables(self):
        # connecting to the source sqlite3 database
        conn1 = sqlite3.connect('../data/chat_table.sqlite3')
        
        # connecting to the target sqlite3 database
        conn2 = sqlite3.connect('../data/db.sqlite3')
        
        # creating a cursor for the source database
        c1 = conn1.cursor()
        
        # executing a SELECT query to fetch all rows from the chats table in the source database
        c1.execute('SELECT * FROM chats')
        
        # creating a cursor for the target database
        c2 = conn2.cursor()
        
        create_query = '''CREATE TABLE IF NOT EXISTS 
                            chats(date datetime,
                               stream_datetime datetime,
                               stream_length INTEGER,
                               username text,
                               message_text text,
                               channel_name text,
                               stream_topic text,
                               stream_title text,
                               chatter_count INTEGER,
                               viewer_count INTEGER,
                               follower_count INTEGER,
                               subscriber_count INTEGER,
                               stream_date datetime,
                               stream_id text,
                               message_sentiment INTEGER,
                               new_message_text text,
                               general_sentiment text,
                               specific_sentiment text)'''
        conn2.execute(create_query)
        conn2.commit()
        
        # executing an INSERT query to copy the rows fetched from the source database to the target database
        c2.executemany('INSERT INTO chats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', c1.fetchall())
        
        # committing the changes to the target database
        conn2.commit()
        
        # closing the connections
        conn1.close()
        conn2.close()
             
        
    def main(self):
        #self.selectChatTable()     
        #self.getMaxDate()
        self.selectNewChats()
        #self.copytables()

        
if __name__ == "__main__":
    executeSql = executeSql()
    executeSql.main()
    