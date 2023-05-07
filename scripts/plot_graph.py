import pandas as pd
import numpy as np
import sqlite3
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, render_template

#conn = sqlite3.connect(con_string)
con_string = '../data/db.sqlite3'


def get_graph(channel_name):
    """
    Query sql table and get the change in subscribers for selected stream
    input: channel_name, start_time
    output: subscriber change (int)
    """

    
    conn = sqlite3.connect(con_string)
    
    graph_query =  '''
                    select date, 
                           avg(general_sentiment) as avg_sentiment,
                           avg(follower_count) as avg_follower_count,
                           avg(viewer_count) as avg_viewer_count
                    from chats
                    where channel_name ='summit1g'
                           group by date
                           order by date desc 
                           LIMIT 100 '''
                            
    print(graph_query)
    cursor_obj = conn.cursor()
    cursor_obj.execute(graph_query)
    graph_data = cursor_obj.fetchall()
    #print("Graph data - ",graph_data)
    graph_df = pd.DataFrame(graph_data, columns=['date', 'avg_sentiment', 'avg_follower_count', 'avg_viewer_count'])
    conn.commit()
    conn.close()
    
    print(graph_df.head(5))
    # fig = px.line(graph_df, x='date', y='avg_follower_count', title='Follower Count')
    # fig.write_html('first_figure.html', auto_open=True)
    
    #Create a line chart and bar chart
    fig = go.Figure()
    
    # fig.add_trace(go.Scatter(x=graph_df['date'], y=graph_df['avg_sentiment'],    
    #                 mode='lines',
    #                 name='Avg Sentiment'))
    
    # fig.add_trace(go.Scatter(x=graph_df['date'], y=graph_df['avg_follower_count'],
    #                     mode='lines',
    #                     name='Avg Follower'))
    
    fig.add_trace(go.Scatter(x=graph_df['date'], y=graph_df['avg_viewer_count'],
                        mode='lines',
                        name='Avg Viewer'))
    
    #Display the figures inside card of index.html
    fig.update_layout(template='plotly_dark',
                  title_text='Stock Data')
    
    fig.write_image("../app/static/line_chart.png")
    #fig.show(width=600, height=600)
    #fig.show('svg',width=600, height=600)
    
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return render_template('index.html', graphJSON=graphJSON)

def main():
     print("Hello World!")
     get_graph('summit1g')
    

if __name__ == '__main__':
       main()
         