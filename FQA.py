import jieba
from lxml import etree
import re
from main import *
# import Constant
import json
import Logging
from flask import request
import config
from question_classifier import QuestionClassifier
from question_parser import  QuestionPaser
from answer_search import AnswerSearcher
import requests

classifer = QuestionClassifier()
parser = QuestionPaser()
searcher = AnswerSearcher()




@app.route('/FQA',methods=['POST','GET'])
def FQA():

    FqaData = request.json
    content = FqaData['content'].strip()
    print(content) #问句


    encoding = FqaData['encoding']
    res_classify = classifer.classify(content)#问题分类匹配
    print("分类匹配：",res_classify)#分类匹配
    if not res_classify:
        answer = "您好，我是智能医学问答助理，很抱歉没有查询到您的问题"
    else :
        res_sql = parser.parser_main(res_classify)
        print("res_sql:",res_sql)
        final_answers = searcher.search_main(res_sql)
        if not final_answers:
            answer = "您好，我是智能医学问答助理，很抱歉没有查询到您的问题"
        else :
            answer = final_answers

    FinalResult = {
        "content": answer
    }

    FinalResult["content"] = answer
    print("FinalResult:",FinalResult)
    return json.dumps(FinalResult)

