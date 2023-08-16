import jieba
from lxml import etree
import re
from main import *
# import Constant
import json
import Logging
from flask import request
import config
from py2neo import Graph
from question_classifier import QuestionClassifier
from question_parser import  QuestionPaser
from answer_search import AnswerSearcher
import requests
from user_info.User_bean import User

classifer = QuestionClassifier()
parser = QuestionPaser()
searcher = AnswerSearcher()




#这个文件拿数据处理问题
@app.route('/VQA',methods=['POST','GET'])
def method(arg):
    content = arg
    print(content) #问句
    question = content["question"]
    username = content["username"]
    res_classify = classifer.classify(question)  # 问题分类匹配
    print("分类匹配：", res_classify)  # 分类匹配
    if not res_classify:
        return {"answer" : ["您好，我是智能医学问答助理，很抱歉没有查询到您的问题"]}
    else:
        res_sql = parser.parser_main(res_classify)
        print("res_sql:", res_sql)
        final_answers = searcher.search_main(res_sql,username)
        if not final_answers:
            answer = "您好，我是智能医学问答助理，很抱歉没有查询到您的问题"
        else:
            answer = final_answers["final_answer"]
            print("question:", question)

            print("answer:", answer)
        FinalResult = {
            "answer" : answer
        }
        return FinalResult
    """
    #开始对用户问题进行处理
    contents = []
    strcontent = "我是一名"+user.gender+"性，"+content
    contents.append(strcontent)
    if user.smoke:
        strcontent = "我有吸烟史"+content
        contents.append(str)
    else:
        strcontent = "我没有吸烟史，"+content
        contents.append(strcontent)
    for disease in diseases:
        strcontent = "我目前患有"+disease+","+content
        contents.append(strcontent)

    for allergy in allergys:
        strcontent = "我对"+allergy+"过敏，"+content
        contents.append(strcontent)

    answers =[]
    for question in contents:
        res_classify = classifer.classify(question)  # 问题分类匹配
        print("分类匹配：", res_classify)  # 分类匹配
        if not res_classify:
            answer = "您好，我是智能医学问答助理，很抱歉没有查询到您的问题"
        else:
            res_sql = parser.parser_main(res_classify)
            print("res_sql:", res_sql)
            final_answers = searcher.search_main(res_sql)
            if not final_answers:
                answer = "您好，我是智能医学问答助理，很抱歉没有查询到您的问题"
            else:
                answer = final_answers["final_answer"]
                print("question:", question)
                #print(type(answer))
                answers.append(''.join(answer))
                print("answer:",answer)
    if not answers:
        answers.append("您好，我是智能医学问答助理，很抱歉没有查询到您的问题")

    final_answer = ''
    for answer in answers:
        print("f_answer:",answer)
        final_answer = final_answer+answer
    print("final_answer:",final_answer)
    FinalResult = {
        "content": final_answer
    }

    FinalResult["content"] = final_answer
    final_answers ={
        "final_answer":final_answer
    }
    print("FinalResult:",FinalResult)
    return json.dumps(final_answers)
    """

