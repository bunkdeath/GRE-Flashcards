#!/usr/bin/python

import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('GRE.db')
cursor = conn.cursor()

def create_table():
    # Create table
    cursor.execute('''CREATE TABLE questions
             (date text, level text, word text, meaning text, failed_count int, success_count int)''')
    conn.commit()

def exists(word, meaning):
    query = 'SELECT * FROM questions WHERE word="%s" and meaning="%s";' % (word, meaning);
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return True
    except Exception, e:
        print query
        print e

    return False

def insert_data():
    data = json.loads(open("gre_questions.json").read())
    for item in data:
        time = datetime.now().strftime("%Y-%m-%d")

        level = item.get("level", "")
        word = item.get("word", "")
        meaning = item.get("meaning", "").replace('"', '\\"')
        failed_count = 0
        success_count = 0
        if not exists(word, meaning):
            cursor.execute('INSERT INTO questions VALUES (? , ?, ?, ?, ?, ?)', (time, level, word, meaning, failed_count, success_count))
    
    conn.commit()
    
    conn.close()
if __name__ == "__main__":
    create_table()
    insert_data()
