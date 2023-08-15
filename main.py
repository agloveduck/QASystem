from flask import Flask, render_template, url_for, redirect,session
from flask_cors import CORS
import jieba
jieba.load_userdict('user_dict')
import jieba.posseg as jp
import json
from flask import request
import os
from datetime import timedelta
import config
import copy
import Constant
import VQA
import UserServiceImpl

app = Flask(__name__)
CORS(app,origins=['http://localhost'], supports_credentials=True)  # 关键是这一句设置跨域
app.config.from_object(config)
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 配置7天有效


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/',methods=['POST','GET'])
def index():
    return render_template('MainPage.html')

@app.route('/build',methods=['POST','GET'])
def build():
    return render_template('build.html')

@app.route('/ner',methods=['POST','GET'])
def ner():
    return render_template('ner.html')

@app.route('/segmentation',methods=['POST','GET'])
def segmentation():
    return render_template('segmentation.html')


@app.route('/fqa_question',methods=['POST','GET'])
def fqa_question():
    return render_template('fqa_question.html')

@app.route('/test',methods=['POST','GET'])
def test():
    return render_template('index.html')

@app.route('/QuestionSubmit',methods=['POST','GET'])
def QuestionSubmit():
    requestData = request.form.to_dict()
    print(requestData)
    ques = requestData.get('question')
    user = requestData.get('user')
    print("user : ", user)
    print("ques:",ques)
    FinalResult = VQA.method(requestData)
    print("FinalResult : ",FinalResult)
    return FinalResult

@app.route('/AddUserInfo',methods=['POST','GET'])
def AddUserInfo():
    requestData = request.form.to_dict()
    FinalResult = UserServiceImpl.addHealthInfo(requestData)
    return FinalResult


@app.route('/SessionUser',methods=['GET','POST'])
def SessionUser():
    #requestData = request.form.to_dict()
    username = session.get('username')
    print("len : " , session.__len__())
    print("getUser : " , session.get('username'))
    if username == None:
        FinalResult = {
            'username' : None,
        }
        return FinalResult
    FinalResult = UserServiceImpl.getUserInfo(username)
    print("GetUser FinaleResult : " ,FinalResult)
    return FinalResult

@app.route('/GetUser',methods=['GET','POST'])
def GetUser():
    requestData = request.form.to_dict()
    print("GetUserRequestData : ",requestData)
    username = requestData["username"]
    print("len : " , session.__len__())
    print("getUser username : " , username)
    if username == None:
        FinalResult = {
            'username' : None,
        }
        return FinalResult
    FinalResult = UserServiceImpl.getUserInfo(username)
    print("GetUser FinaleResult : " ,FinalResult)
    return FinalResult

@app.route('/Register',methods=['POST'])
def Register():
    requestData = request.form.to_dict()
    FinalResult1 = UserServiceImpl.register(requestData)
    FinalResult2 = UserServiceImpl.addHealthInfo(requestData)

    print(FinalResult2)
    return FinalResult2

@app.route('/Login',methods=['POST'])
def Login():
    requestData = request.form.to_dict()
    # requestData = request.get_json()  # Get JSON data from the request
    print("requestData : ",requestData)
    FinalResult = UserServiceImpl.login(requestData)
    print(FinalResult)
    if FinalResult['state'] == 200:#设置session
        session['username'] = requestData['username']
        session['password'] = requestData['password']
        session.permanent = True
        print("sessionlen : ",session.__len__())
    print("session['username'] : ",session['username'])
    return FinalResult


if __name__ == '__main__':
    from FQA import *
    CORS(app, supports_credentials=True)
    app.run(host='localhost', port='5000', debug=True)
