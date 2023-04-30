import sqlite3
import json
import scripts.sentimentAnalysis as sentimentAnalysis

con_string = 'data/db.sqlite3'

def read_sentiments():
	# Create a SQL connection to our SQLite database
	conn = sqlite3.connect(con_string,isolation_level=None)
	cursor_obj = conn.cursor()
	cursor_obj.execute("select new_message_text, username, message_text from chats order by RANDOM() limit 1")
	output = cursor_obj.fetchall()
	msg = output[0][0]
	uname = output[0][1]
	original_msg = output[0][2]
	conn.commit()
	conn.close()  

	sentimentAnalyzer = sentimentAnalysis.sentimentAnalyzer()
	proba_dict = sentimentAnalyzer.get_sentiment_probability(msg)
	top_prob = max(proba_dict.values())
	for key, value in proba_dict.items():
		if value == top_prob:
			pred_class = key
  
	pred_class = '<h1 style="font-family:verdana;color:green;">'+pred_class+'</h1>' if pred_class=='Positive' \
						else '<h1 style="font-family:verdana;color:red;">'+pred_class+'</h1>' \
						if pred_class=='Negative' else '<h1 style="font-family:verdana;color:gray;">'+pred_class+'</h1>'
	pred_proba = format(top_prob[0], '.6f') if pred_class=='Positive' else format(top_prob[0] * -1, '.6f') if pred_class=='Negative' else 0

	return json.dumps([{
		# 'sentiment_display': '<p>Sentiment for: <B>'+ msg + '</B> sent by user: <B>'+ uname + '</B> is: <B>' + pred_class + '</B></p>', 
		# 'prob_score' : pred_proba
		'sentiment_display': '<p> "'+ original_msg + ' " <i> -'+uname+'</i></p>',
		'user': '<p> -'+uname+'</p>',
		'pred_class':pred_class, 
		'prob_score' : pred_proba		
	}])
