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
        conn = sqlite3.connect('../data/chat_table.sqlite3',isolation_level=None)
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
        print(chat_df.head())
        print(chat_df.shape)
            
        
        #for row in result:
        #    print(row)         
             
        
    def main(self):
        self.selectChatTable()     
        #self.getMaxDate()
        #self.selectNewChats()

        
if __name__ == "__main__":
    executeSql = executeSql()
    executeSql.main()
    