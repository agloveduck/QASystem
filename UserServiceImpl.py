import jieba
from lxml import etree
import re
from main import *
import pymysql
import Logging
from flask import request,session
import config
from py2neo import Graph

app = Flask(__name__)
app.config.from_object(config)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def addHealthInfo(arg):  # 向数据库中添加用户的健康信息 返回一个字典对象作为结果
    content = arg
    print(content)
    username = content['username']
    password = "123456"
    smoke = int(content['smoke'])
    alcohol = int(content['alcohol'])
    allergy = content['allergy']
    diseases = content['diseases']
    print("diseases :" + diseases)
    DBHOST = "localhost"
    DBUSER = "root"
    DBPASS = "jjrmysql"
    DBNAME = "medcine"
    conn = pymysql.connect(host = DBHOST,user = DBUSER,password=DBPASS,database= DBNAME)
    print("数据库连接成功")
    cursor = conn.cursor()
    sql_insert = "insert into meduser(username,smoke,alcohol,allergy,diseases) values(%s,%s,%s,%s,%s)"
    update_sql = "UPDATE  meduser SET  smoke = %s,alcohol=%s,allergy=%s,diseases=%s WHERE  username=%s"
    value = (smoke,alcohol,allergy,diseases,username)
    print(value)
    cursor.execute(update_sql,value)
    conn.commit()
    print("数据库修改成功")
    FinalResule = {
        "content" : 200
    }
    return FinalResule

def login(arg):
    content = arg
    print(content)
    loginname = content['username']
    loginpwd = content['password']
    DBHOST = "localhost"
    DBUSER = "root"
    DBPASS = "jjrmysql"
    DBNAME = "medcine"
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
    print("数据库连接成功")
    cursor = conn.cursor()
    sql_get = "select * from meduser where username='" + loginname + "'"
    cursor = conn.cursor()
    cursor.execute(sql_get)
    results = cursor.fetchall()
    print("数据库result:")
    print(results)
    if results.__len__() == 0:

        FinalResult = {
            "state": 202,
            "content": "用户名输入错误"
        }
        return FinalResult
    results = results.__getitem__(0)
    username = results[1]
    print(username)
    password = results[2]
    FinalResult = {}
    if username == loginname:
        if loginpwd == password:
            FinalResult = {
                "state" : 200,
                "content" : "登陆成功",
                "info" : results
            }
        else:
            print("密码错误的：" + loginpwd)
            FinalResult = {
                "state" : 201,
                "content" : "密码错误"
            }
    else:

        FinalResult = {
            "state" : 202,
            "content" : "用户名输入错误"
        }
    return FinalResult

def register(arg):
    content = arg
    print(content)
    username = content['username']
    password = content['password']
    DBHOST = "localhost"
    DBUSER = "root"
    DBPASS = "jjrmysql"
    DBNAME = "medcine"
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
    print("数据库连接成功")
    cursor = conn.cursor()
    sql_insert = "insert into meduser(username,password) values(%s,%s)"
    value = (username,password)
    print(value)
    cursor.execute(sql_insert, value)
    conn.commit()
    print("数据库添加成功")

    FinalResult = {
        "state" : 200
    }
    return FinalResult



#获得患者健康信息
def getUserInfo(arg):
    content = arg
    print(content)
    username = content
    DBHOST = "localhost"
    DBUSER = "root"
    DBPASS = "jjrmysql"
    DBNAME = "medcine"
    conn = pymysql.connect(host = DBHOST,user = DBUSER,password=DBPASS,database= DBNAME)
    table = "meduser"
    print("数据库连接成功")
    sql_get = "select * from meduser where username='"+ username + "'"
    cursor = conn.cursor()
    cursor.execute(sql_get)
    results = cursor.fetchall().__getitem__(0)
    smoke = results[3]
    alcohol = results[4]
    disease = results[6]
    if disease is None or '、' not in disease:
        diseases = []
        diseases.append(disease)
    else:
        diseases = disease.split('、')
    allergy =  results[5]
    if allergy is None or '、' not in allergy:
        allergies = []
        allergies.append(allergy)
    else:
        allergies = allergy.split('、')
    print(results)
    FinalResult = {
        "username" : username,
        "smoke" : smoke,
        "alcohol" : alcohol,
        "disease" : diseases,
        "allergy" : allergies

    }#只包含了患者的个人信息
    return FinalResult

