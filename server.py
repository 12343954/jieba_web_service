#coding:utf-8

import sys

import jieba
import jieba.analyse
import jieba.posseg
from flask import Flask, jsonify

from python_mysql_helper import PTConnectionPool, getPTConnection

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.DEBUG=True
# app.json_encoder = 'NonASCIIJsonEncoder'
HOST,PORT='0.0.0.0',8888

#default port : http://localhost:5000
@app.route('/')
def index():
    return 'hello jieba services!'

#
@app.route('/api/cut/<string:str_words>')
def cut(str_words):
    result = jieba.cut(str_words,HMM=False)
    return ' / '.join(result)

#
@app.route('/api/cut_for_search/<string:str_words>')
def cut_for_search(str_words):
    result = jieba.cut_for_search(str_words)
    return ' / '.join(result)

@app.route('/api/part_of_speech/<string:str_words>')
def part_of_speech(str_words):
    words = jieba.posseg.cut(str_words)
    result={}
    res=[]
    for word, flag in words:
        result[word]=flag
        res.append('%s %s' % (word, flag))
        #print('%s %s' % (word, flag))

    #return jsonify({"result":result})
    return '\n'.join(res)

#test db
@app.route('/api/testdb/<string:str_words>')
def testdb(str_words):
    return insertToDB('testdb',str_words,1)
     

def insertToDB(method,strInput,userID):

    #apply db
    with getPTConnection() as db:
        # SQL
        sql = "SELECT * FROM test";
        sql2 = "INSERT INTO test(title,userID) VALUES('%s',%d)" %(strInput,userID)
        print(sql2)
        try:
            # select
            db.cursor.execute('SET NAMES utf8mb4')
            db.cursor.execute("SET CHARACTER SET utf8mb4")
            db.cursor.execute("SET character_set_connection=utf8mb4")
            db.cursor.execute(sql2)
            # db.commit()
            db.cursor.execute(sql)
            results = db.cursor.fetchall();

            for row in results:
                ID = row[0]
                title= row[1]         
                userID= row[2]
                inputTime = row[3]
                # print输出
                print ("ID=%d,title=%s,userID=%s,inputTime=%s" %\
                     (ID,  title, userID, inputTime ))
                     
            # print(list(results))
        except Exception as e:
            print ("Error: unable to database %s" % e)
        finally:
            return jsonify({"result":results})



if __name__ == "__main__":
    app.run(debug=True,host=HOST,port=PORT)
