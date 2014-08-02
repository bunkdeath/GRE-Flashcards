#!/usr/bin/python

__author__ = "Bunkdeath <contact@bunkdeath.com>"
__version__ = "0.0.1"

import os
import sqlite3

path = "/Volumes/BAKUP/Projects/GRE-FlashCards"
db = os.path.join(path, 'GRE.db')

conn = sqlite3.connect(db)
cursor = conn.cursor()

CD_BASE = "/Library/Application\ Support"
CD_PATH = os.path.join(CD_BASE, "CocoaDialog.app/Contents/MacOS/CocoaDialog")

class Answer:
    global CD_BASE
    global CD_PATH
    def __init__(self, word, answer):
        template = '%s yesno-msgbox --no-cancel --title "GRE Flashcards" --informative-text "%s\n\n%s" --text "Did you know?"'
        import subprocess
        command =  template % (CD_PATH, word, answer)
        self.pipe = os.popen(command)

    def get_result(self):
        while True:
            try:
                result = self.pipe.readline()
                if result:
                    return result
            except Exception, e:
                print e

    def close(self):
        self.pipe.close()

class Question:
    global CD_BASE
    global CD_PATH
    def __init__ (self, question, result_summary):
        # template = "%s ok-msgbox --no-cancel --no-newline --text '%s' --informative-text '%s'"
        template = '%s ok-msgbox --no-cancel --no-newline --title "GRE Flashcards" --text "%s" --informative-text "%s"'
        import subprocess
        # command =  template % (CD_PATH, category, question)
        command =  template % (CD_PATH, question, result_summary)
        self.pipe = os.popen(command)

    def get_result(self):
        while True:
            try:
                result = self.pipe.readline()
                if result:
                    return result
            except Exception, e:
                print e

    def close(self):
        self.pipe.close()

def get_question():
    query = "SELECT * FROM questions ORDER BY RANDOM();"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return result

def update_result(word, meaning, success):
    query = 'SELECT * FROM questions WHERE word="%s" and meaning="%s";' % (word, meaning);
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        if success:
            success_count = result[5]
            success_count += 1
            query = "UPDATE questions SET success_count=%s WHERE word='%s' and meaning='%s';" % (success_count, word, meaning)
        else:
            failed_count = result[4]
            failed_count += 1
            query = "UPDATE questions SET failed_count=%s WHERE word='%s' and meaning='%s';" % (failed_count, word, meaning)

        cursor.execute(query)
        conn.commit()
    else:
        print "row not found"

def start():
    data = get_question()
    level = data[1]
    word = data[2]
    meaning = data[3]
    success = data[4]
    failure = data[5]
    print "%s|%s|%s|%s|%s" % (level, word, meaning, success, failure)
    result_summary = "No summary yet"
    if success or failure:
        success_rate = (success*1.0)/(success+failure)*100
        result_summary = """success count : %s
    failure count : %s
    success rate  : %s""" % (success, failure, success_rate)

    question = Question(word, result_summary)
    question.get_result()
    question.close()

    answer = Answer(word, meaning)
    result = int(answer.get_result())
    if result == 1:
        update_result(word, meaning, True)
    else:
        update_result(word, meaning, False)

    answer.close()


if __name__ == "__main__":
    start()