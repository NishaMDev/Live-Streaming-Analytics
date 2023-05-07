##5 * * * * /home/aspera/my_script.sh


import sqlite3
import pandas as pd



class executeSql:
    def __init__(self):
       
        self.OPENAI_API_KEY = ""
        
    def selectChatTable(self):

        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect('../data/db.sqlite3',isolation_level=None)
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
        
    def selectDateforStreamer(self):

        conn = sqlite3.connect('../data/db.sqlite3',isolation_level=None)
        cur = conn.cursor()
        streamer_name = 'summit1g'
        start_time = '2023-04-16'
        select_query = ''' select distinct stream_date, channel_name from chats where channel_name = '{}' '''.format(streamer_name)
        
        total_messages_query = '''
                        select count(*) as total_messages
                        from chats
                        where channel_name = '{}' and stream_date = '{}'
                        '''.format(streamer_name, start_time)
                        
        print(total_messages_query)
        #cur.execute(select_query)
        #result = cur.fetchall() 
        #print(type(result)) 
        cursor_obj = conn.cursor()
        cursor_obj.execute(total_messages_query)
        message_count = cursor_obj.fetchall()
        print(message_count)
        conn.commit()
        conn.close()  
    
        # chat_df = pd.read_sql(select_query, conn)
        # print("Start to print new chats details :-")
        # print(chat_df.head(10))
        # print("Number of new rows to be processed:- ",chat_df.shape[0])
                      
    def get_message_count(self, channel_name, start_time):
        """
        Query sql table and get the total number of chats for selected stream
        input: channel_name, start_time
        output: message_count (int)
        """
        
        channel_name = '\'' + channel_name + '\''
        start_time = '\'' + start_time + '\''
        
        conn = sqlite3.connect('../data/db.sqlite3',isolation_level=None)
        
        total_messages_query = '''
                            select count(*) as total_messages
                            from chats
                            where channel_name = {} and stream_date = {}
                            '''.format(channel_name, start_time)
        
        print(total_messages_query)
        cursor_obj = conn.cursor()
        cursor_obj.execute(total_messages_query)
        message_count = cursor_obj.fetchall()
        print("message_count", message_count[0][0])
        conn.commit()
        conn.close()      
    
    def get_streamer_dates(self):
       
        
        conn = sqlite3.connect('../data/db.sqlite3',isolation_level=None)
        
        streamer_date_query = '''
                            select DISTINCT channel_name as STREAMER, stream_date as DATE
                            from chats
                            '''
        print(streamer_date_query)
        cursor_obj = conn.cursor()
        cursor_obj.execute(streamer_date_query)
        message_count = cursor_obj.fetchall()
        print("message_count", message_count)
        conn.commit()
        conn.close() 
        
        
    def create_csv(self):
        path = '../data/processed'
        channels = ['zackrawrr','lirik','cryocells','katarinafps','gmhikaru','cdawgva','stewie2k','summit1g','tarik']
        conn = sqlite3.connect('../data/db.sqlite3',isolation_level=None)
        print("Opened database successfully")
        for channel in channels:
            
            sentiment_score_query = """select date, avg(message_sentiment) as value
                                   from chats
                                    where channel_name ='{}'
                                   group by date
                                   order by date asc""".format(channel)
        
            follower_query = """select date, avg(follower_count) as value
                                   from chats
                                    where channel_name ='{}'
                                   group by date
                                   order by date asc""".format(channel)
        
        
            viewer_query = """select date, avg(viewer_count) as value
                                   from chats
                                    where channel_name ='{}'
                                   group by date
                                   order by date asc""".format(channel)
            
            sentiment_df = pd.read_sql_query(sentiment_score_query, conn)
            follower_df = pd.read_sql_query(follower_query, conn)
            viewer_df = pd.read_sql_query(viewer_query, conn)
            
            sentiment_df.to_csv(path + '/sentiment_values_{}.csv'.format(channel))
            follower_df.to_csv(path + '/follower_values_{}.csv'.format(channel))
            viewer_df.to_csv(path + '/viewer_values_{}.csv'.format(channel))
            print("CSV files created successfully")
                              
        conn.close()   
    
    def main(self):
        #self.selectChatTable()     
        #self.getMaxDate()
        #self.selectNewChats()
        #self.copytables()
        #self.selectDateforStreamer()
        #self.get_message_count('summit1g', '2023-04-16')
        #self.get_streamer_dates()
        self.create_csv()

        
if __name__ == "__main__":
    executeSql = executeSql()
    executeSql.main()
    