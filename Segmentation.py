import copy

import jieba

import Constant
from main import *
# import Constant
import json
import Logging
from flask import request
import config

#todo: ysh @time:2019.11.14 17:53
@app.route('/segmente',methods=['POST','GET'])
def segmente():
    '''
        将前端传来的内容进行标注
    :return: 格式化的Json
    '''
    '''
        SegmentaionData:{
            "text":"abc",
            "encoding":"utf-8"·0
            
        }
    '''
    SegmentaionData = request.json
    print(SegmentaionData)
    content = SegmentaionData['text'].strip()
    encoding = SegmentaionData['encoding']
    #此处记录日志信息
    Logger = Logging.Log(Logging.SegmentLoggerName)
    Logger.ExcuteLoging("IP:{}, QUERY:{}".format(request.remote_addr, content))

    #todo：如果内容是GBK,将其转为utf-8,注意返回时也需要进行转换   2019.11.14 zsf
    FinalResult = {
        "text"  : content,
        "items" : []
    }
    #加入到FinalResult中的 items中的内容
    item = {
        "byte_length"   : 0,
        "byte_offset"   : 0,
        "formal"        : "",
        "item"          : "",
        "ne"            : "",
        "pos"           : [],
        "uri"           : "",
        "loc_details"   : [],
        "basic_words"   : []
    }
    #分词
    if content != '':
        #1. 加载用户自定义的词典
        # jieba.load_userdict(open("user_dict", 'r', encoding='utf-8'))
        #2. 读入词典，一个个add_word
        UserDict = open("user_dict", 'r', encoding="utf-8")
        Words = [word.strip() for word in UserDict]
        for word in Words:
            jieba.add_word(word)

        SegmentResult = jp.lcut(content)
        temp_item = copy.deepcopy(item)
        for word, flag in SegmentResult:
            temp_item['basic_words'].append(word)
            temp_item['pos'].append(Constant.Tag2Chinese.get(flag, "其他"))
        FinalResult["items"].append(temp_item)
    print(FinalResult)
    return json.dumps(FinalResult)

#todo: ysh @time:2019.11.14 17:53
#todo 需要加上可持久化的分词结果，用加载用户词典的方法实现
#todo 若之后用数据库，可以考虑利用add_word的方法将分词结果进行扩充
@app.route('/addword',methods=['POST','GET'])
def addword():
    '''
        添加手动分词结果
    :return: 无返回
    '''
    AddContent = request.json
    ContentToAdd = AddContent['ContentToAdd']
    SegmentContent = AddContent['SegmentContent']
    Logger = Logging.Log(Logging.SegmentLoggerName)

    #将每个词的词频设置高一些
    AddWords = [word.strip() for word in ContentToAdd.split("\n")]
    for word in AddWords:
        Logger.ExcuteLoging("IP:{}, AddWord:{}".format(request.remote_addr, word))

    #打开词典文件
    UserDict = open('user_dict', 'a', encoding='utf-8')

    for word in AddWords:
        #暂时提高词频使其显示出来
        jieba.suggest_freq(word, True)
        #todo 需要修改为写入数据库中
        UserDict.write(word + "\n")

    UserDict.close()
    return json.dumps({})
