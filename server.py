import sys

import jieba
import jieba.analyse
import jieba.posseg
from flask import Flask, jsonify

from python_mysql_helper import PTConnectionPool, getPTConnection

app = Flask(__name__)
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



if __name__ == "__main__":
    app.run(debug=True,host=HOST,port=PORT)
