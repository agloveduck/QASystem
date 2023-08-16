from main import *
import re
from flask import Flask, jsonify, render_template
from py2neo import Graph

graph = Graph('http://localhost:7474',username='neo4j',password='jjrneo4j') #认证连接数据库
app = Flask(__name__) #flask框架必备

def buildPersonNodes(nodeRecord):
    tmp = {}
    data = {}
    data.update(dict(nodeRecord['n']))
    tmp['id'] = data['name']
    tmp['name'] = data['person:ID']
    tmp['label']= 'Person'
    return {"data": tmp}

def buildMoivesNodes(nodeRecord):
    tmp = {}
    data = {}
    data.update(dict(nodeRecord['n']))
    tmp['id'] = data['name']
    tmp['name'] = data['name']
    tmp['label']= 'Movies'
    return {"data": tmp}

def buildEdges(relationRecord):
    line = str(relationRecord['r'])
    x = re.findall(r'[(](.*?)[)]', line) #取括号内的内容,得到起始节点以及目标节点
    print (x)
    data = {"source": x[0], "target": x[1]}
    return {"data": data}


@app.route('/get_graph')#两个路由指向同一个网页，返回图的节点和边的结构体
def get_graph():
    print("GETTING NODES")
    #todo：分开步骤
    nodes = []

    #获取Person的节点
    temp_nodes = []
    temp_nodes = list(map(buildPersonNodes, graph.run('MATCH (n:Person) RETURN n').data()))
    nodes.extend(temp_nodes)

    # 获取Moives的节点
    temp_nodes = []
    temp_nodes = list(map(buildMoivesNodes, graph.run('MATCH (n:Movies) RETURN n').data()))
    nodes.extend(temp_nodes)

    print("GETTING EDGES")
    edges = list(map(buildEdges, graph.run('MATCH ()-[r]->() RETURN r').data()))
    elements = {"nodes": nodes, "edges": edges}
    print (elements)
    return jsonify(elements = {"nodes": nodes, "edges": edges})
