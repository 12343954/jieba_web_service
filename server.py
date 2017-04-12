#coding:utf-8

import sys
import os

import jieba
import jieba.analyse
import jieba.posseg
from flask import Flask, jsonify, request

from python_mysql_helper import PTConnectionPool, getPTConnection

reload(sys)
sys.setdefaultencoding('utf-8')

# setting up template directory
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')
app = Flask(__name__, template_folder = ASSETS_DIR, static_folder = ASSETS_DIR)
app.config.DEBUG=True

# app.json_encoder = 'NonASCIIJsonEncoder'
HOST,PORT='0.0.0.0',8888

#default port : http://localhost:8888
@app.route('/')
def root():
    return app.send_static_file("Doc.html")

#精准模式分词
@app.route('/api/cut/<string:str_words>')
def cut(str_words):
    result = jieba.cut(str_words,HMM=False)
    return ' / '.join(result)

#搜索模式分词
@app.route('/api/cut_for_search/<string:str_words>')
def cut_for_search(str_words):
    result = jieba.cut_for_search(str_words)
    return ' / '.join(result)

#添加生词
@app.route('/api/suggest_freq/<string:str_words>')
def suggest_freq(str_words):
    if(len(str_words) == 0):
        return jsonify(return_code=-1,
                        msg='str_words is empty',
                        data=None)
    
    new_Words = tuple(set(filter(None, str_words.split(','))))
    return jsonify(return_code=1,
                    msg='success',
                    data=jieba.suggest_freq(new_Words, True))

@app.route('/api/pos/<string:str_words>')
@app.route('/api/part_of_speech/<string:str_words>')
def part_of_speech(str_words):
    words = jieba.posseg.cut(str_words)
    f=[]
    w=[]
    out=[]
    for word, flag in words:
        f.append('%s' % flag)
        w.append('%s' % word)
        out.append('%s%s ' % (word, flag))

    # print('\n '.join(out))
    result = insertToDB("POS",str_words,f,w,1)
    # print(result[0][0])
    return '\n'.join(out)

    #return jsonify({"result":result})
    return '\n'.join(w)

#test db
@app.route('/api/testdb/<string:str_words>')
def testdb(str_words):
    return insertToDB('testdb',str_words,None,None,1)
     
#insert POS_CN
@app.route('/api/insert_pos_cn')
def insert_POS_CN():
    sql="""INSERT INTO POS_CN(FPOS,FNAME,FDESCRIPTION)
SELECT 'Ag','形语素','形容词性语素。形容词代码为a，语素代码ｇ前面置以A。' 
 UNION SELECT 'a','形容词','取英语形容词adjective的第1个字母。'  
 UNION SELECT 'ad','副形词','直接作状语的形容词。形容词代码a和副词代码d并在一起。'  
 UNION SELECT 'an','名形词','具有名词功能的形容词。形容词代码a和名词代码n并在一起。'  
 UNION SELECT 'b','区别词','取汉字“别”的声母。'  
 UNION SELECT 'c','连词','取英语连词conjunction的第1个字母。'  
 UNION SELECT 'dg','副语素','副词性语素。副词代码为d，语素代码ｇ前面置以D。' 
 UNION SELECT 'd','副词','取adverb的第2个字母，因其第1个字母已用于形容词。' 
 UNION SELECT 'e','叹词','取英语叹词exclamation的第1个字母。'  
 UNION SELECT 'f','方位词','取汉字“方”'  
 UNION SELECT 'g','语素','绝大多数语素都能作为合成词的“词根”，取汉字“根”的声母。'  
 UNION SELECT 'h','前接成分','取英语head的第1个字母。'  
 UNION SELECT 'i','成语','取英语成语idiom的第1个字母。'  
 UNION SELECT 'j','简称略语','取汉字“简”的声母。'  
 UNION SELECT 'k','后接成分',''  
 UNION SELECT 'l','习用语','习用语尚未成为成语，有点“临时性”，取“临”的声母。'  
 UNION SELECT 'm','数词','取英语numeral的第3个字母，n，u已有他用。'  
 UNION SELECT 'Ng','名语素','名词性语素。名词代码为n，语素代码ｇ前面置以N。'  
 UNION SELECT 'n','名词','取英语名词noun的第1个字母。'  
 UNION SELECT 'nr','人名','名词代码n和“人(ren)”的声母并在一起。'  
 UNION SELECT 'ns','地名','名词代码n和处所词代码s并在一起。'  
 UNION SELECT 'nt','机构团体','“团”的声母为t，名词代码n和t并在一起。'  
 UNION SELECT 'nz','其他专名','“专”的声母的第1个字母为z，名词代码n和z并在一起。'  
 UNION SELECT 'o','拟声词','取英语拟声词onomatopoeia的第1个字母。'  
 UNION SELECT 'p','介词','取英语介词prepositional的第1个字母。'  
 UNION SELECT 'q','量词','取英语quantity的第1个字母。'  
 UNION SELECT 'r','代词','取英语代词pronoun的第2个字母,因p已用于介词。'  
 UNION SELECT 's','处所词','取英语space的第1个字母。'  
 UNION SELECT 'tg','时语素','时间词性语素。时间词代码为t,在语素的代码g前面置以T。'  
 UNION SELECT 't','时间词','取英语time的第1个字母。'  
 UNION SELECT 'u','助词','取英语助词auxiliary'  
 UNION SELECT 'vg','动语素','动词性语素。动词代码为v。在语素的代码g前面置以V。'  
 UNION SELECT 'v','动词','取英语动词verb的第一个字母。'  
 UNION SELECT 'vd','副动词','直接作状语的动词。动词和副词的代码并在一起。'  
 UNION SELECT 'vn','名动词','指具有名词功能的动词。动词和名词的代码并在一起。'  
 UNION SELECT 'w','标点符号',''  
 UNION SELECT 'x','非语素字','非语素字只是一个符号，字母x通常用于代表未知数、符号。'  
 UNION SELECT 'y','语气词','取汉字“语”的声母。'  
 UNION SELECT 'z','状态词','取汉字“状”的声母的前一个字母。'  
 UNION SELECT 'un','未知词','不可识别词及用户自定义词组。取英文Unkonwn首两个字母。(非北大标准，CSW分词中定义)' """
    print(sql)
    # return "True"
    with getPTConnection() as db:
        try:
            db.cursor.execute(sql)
        except Exception as ex:
            print("error : %s" % ex)
            return "False"
        finally:
            return "True"


def insertToDB(method,sentence,tags=[],words=[],userID=1):

    #apply db
    with getPTConnection() as db:
        # SQL
        sql = []
        sql2 = ["INSERT INTO TSentence(FSentence,FPOSmethod,FPOStag,FPOSwords,FGrammar,userID) \
                VALUES('%s','%s','%s','%s','%s',%d);" %(sentence,method,' '.join(tags),' '.join(words),'',userID)]
        sql2.append("SET @last_id_in_table1 = LAST_INSERT_ID();")
        sql2.append("INSERT INTO TPOS(QID,FTag,FWord) ")
        
        for index in range(len(tags)):
            sql.append("SELECT @last_id_in_table1,'%s','%s'" % (tags[index],words[index]))

        # print('UNION'.join(sql))
        sql2.append(' UNION ALL '.join(sql))
        sql2.append(';SELECT @last_id_in_table1')
        print(''.join(sql2))

        # return ""
        try:
            # select
            # db.cursor.execute('SET NAMES utf8mb4')
            # db.cursor.execute("SET CHARACTER SET utf8mb4")
            # db.cursor.execute("SET character_set_connection=utf8mb4")
            db.cursor.execute(''.join(sql2))
            # db.commit()
            # db.cursor.execute(sql)
            results = db.cursor.fetchall()

            for row in results:
                ID = row[0]
            #     title= row[1]         
            #     userID= row[2]
            #     inputTime = row[3]
            #     # print输出
            #     print ("ID=%d,title=%s,userID=%s,inputTime=%s" %\
            #          (ID,  title, userID, inputTime ))
                print("%s" % ID)
                     
            # print(results)
        except Exception as e:
            print ("Error: unable to database %s" % e)
        finally:
            return results



if __name__ == "__main__":
    app.run(debug=True,host=HOST,port=PORT)
