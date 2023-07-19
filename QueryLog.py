from main import *
import json
from flask import request
import Constant
import os

@app.route('/GetLog',methods=['POST','GET'])
def GetLog():
    '''
        将前端传来的需要取的日志数量及类型，按照对应的格式传回去
    :return: 格式化的Json
    '''
    LogParams = request.json
    print(LogParams)
    LogNum = int(LogParams['num'].strip())
    LogType = LogParams['type']

    #从FileName对应的文件中取得最新的LogNum条日志，返回前端
    #对于打印出的Log，只需要返回按照,分开后的结果即可
    FinalResult = {}
    FinalResult["TableId"] = LogType
    FinalResult["Data"] = []
    #todo: 改为倒着读,
    #此处应为倒着读文件,先要找到对应的文件倒序
    AllFileNames = [filename for filename in os.listdir("logging/") if LogType in filename]
    AllFileNames.sort()
    AllFileNames.reverse()
    Count = 0
    for filename in AllFileNames:
        if Count > LogNum:
            break
        LogFile = open("logging/" + filename, 'r', encoding = 'utf-8')
        Temp = []
        for EveryLine in LogFile:
            if EveryLine.strip() == "":
                continue
            Count += 1
            if Count > LogNum:
                break
            line = [part.strip() for part in EveryLine.split(',')]
            del(line[1])
            #将最后一部分的Message内容,如果超过3个字，则只截取实际信息的前三个字
            MaxLen = 20
            if len(line[-1].split(':')[-1].strip()) > MaxLen:
                line[-1] = line[-1][:line[-1].find(':')+MaxLen] + "..."
            Temp.append(line)
        Temp.reverse()
        FinalResult["Data"].extend(Temp)
    print(FinalResult)
    return json.dumps(FinalResult)