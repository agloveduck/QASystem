# coding=utf-8
#To张思凡学长：
#py2neo库建议使用5.0b1版本(执行下面这行)
#pip install py2neo==5.0b1
#从第30行开始我做了修改，可以读到数据库的数据，但flask架构我不知道怎么改回去。。。
#请学长帮改一改：-）
from main import *
import re
import QASystem.Logging
from flask import Flask, jsonify, render_template,request
from py2neo import Graph

from collections import Counter
print("connecting")
#graph = Graph('http://localhost:7474',username='neo4j',password='NEO$J') #认证连接数据库
graph = Graph('http://localhost:7474/', auth=("neo4j", "123456"))

NeedNodes = ['华为', '中国', '美国', '中国联通', '中国移动', '爱立信', '中兴', '高通', '诺基亚', '三星', '工信部','AT&T','特朗普','任正非', '上海', '北京', '中国电信']
def buildeliteNodes(nodeRecord):
    tmp = {}
    data = {}
    data.update(dict(nodeRecord['n']))
    tmp['id'] = data['name']
    tmp['name'] = data['name']
    tmp['label']= 'Person'
    if tmp['id'].strip() == "" or tmp['id'] not in NeedNodes:
        return
    return {"data": tmp}

def buildEdges(relationRecord):
    line = str(relationRecord['r'])
    x = re.findall(r'[(](.*?)[)]', line) #取括号内的内容,得到起始节点以及目标节点
    # print (x)
    data = {"source": x[0], "target": x[1]}
    if x[0].strip() == "" or x[1].strip() == "":
        return
    return {"data": data}

@app.route('/query_graph', methods=['POST','GET'])#两个路由指向同一个网页，返回图的节点和边的结构体
def query_graph():
    print("query_graph------")
    #接受数据
    Querydata = request.json
    entity1 = Querydata["entity1"]
    entity2 = Querydata["entity2"]
    print(entity1, entity2)
    print("跳转步数")
    steps = Querydata["steps"]

    #处理数据
    #查询结点是否存在
    Data = {}
    Data["info"] = None
    Data["elements"] = None
    if entity1.strip() == "" or str(graph.run('MATCH (n:elite{name:"%s"}) RETURN n' % entity1)).strip() == "":
        Data["info"] = "实体1不存在，请重试"
    elif entity2.strip() == "" or str(graph.run('MATCH (n:elite{name:"%s"}) RETURN n' % entity2)).strip() == "":
        Data["info"] = "实体2不存在，请重试"
    else:
        Logger = Logging.Log(Logging.GraphLoggerName)
        Logger.ExcuteLoging("IP:{}, QUERY:{},{},{}".format(request.remote_addr, entity1, entity2, steps))
        Data["info"] = "查询成功"
        #找到结点对应的路径，去重
        querySentence = 'MATCH p= (n:elite{name:"%s"})-[*%s]->(m:elite{name:"%s"}) RETURN p' % (entity1, steps, entity2)
        QueryData = graph.run(querySentence).data()
        #对所有结点、关系去重
        AllNodes = set()
        AllRelations = set()
        for OriRelation in QueryData:
            line = str(OriRelation['p'])
            nodes = re.findall(r'[(](.*?)[)]', line)  # 取括号内的内容,得到起始节点以及目标节点
            temp_relations = []
            for i in range(len(nodes)-1):
                if nodes[i] != "" and nodes[i+1] != "":
                    temp_relations.append((nodes[i], nodes[i+1]))
                    AllNodes.add(nodes[i])
                    AllNodes.add(nodes[i+1])
            AllRelations.update(temp_relations)
        #构建所有的关系、结点的数据
        # nodes:[{'data':{'id':XX, 'name':XX}}]
        nodes = []
        edges = []
        for node in AllNodes:
            nodes.append({'data':{'id':node, 'name':node}})
        for edge in AllRelations:
            edges.append({'data':{'source':edge[0], 'target':edge[1]}})
        elements = {
            "nodes":nodes,
            "edges":edges
        }
        Data["elements"] = elements

    # #返回数据
    #     # Data = {
    #     #     "nodes":[
    #     #         {"data":{"id":"j", "name":"Jerry"}},
    #     #         {"data":{"id":"e", "name":"Elaine"}},
    #     #     ],
    #     #     "edges":[
    #     #         {"data": {"source": "j", "target": "e"}},
    #     #     ]
    #     # }

    return jsonify(Data)

@app.route('/get_graph', methods=['POST','GET'])#两个路由指向同一个网页，返回图的节点和边的结构体
def get_graph():
    print("GETTING NODES")
    #todo：分开步骤
    nodes = []
    # 获取节点
    nodes = [x for x in list(map(buildeliteNodes, graph.run('MATCH (n:elite) RETURN n').data())) if x]
    print("GETTING EDGES")
    AllNodesId = [x['data']['id'] for x in nodes]
    # 获取边
    edges = [e for e in list(map(buildEdges, graph.run('MATCH ()-[r]->() RETURN r').data()))
             if e and (e['data']['source'] in AllNodesId and e['data']['target'] in AllNodesId)]
    print(nodes)
    Data = {}
    elements = {"nodes": nodes, "edges": edges}
    Data["elements"] = elements
    Data["info"] = "查询成功"
    #返回结果
    return jsonify(Data)

if __name__ == "__main__":
    # todo :1.查询结点是否存在的语句实例
    # print(graph.run('MATCH (n:elite{name:"SunJinDa"}) RETURN n'))
    # nodes = list(map(buildeliteNodes, graph.run('MATCH (n:elite{name:"SunJinDa"}) RETURN n').data()))
    # print("SunJinDa查询结果：")
    # print(nodes == [])
    # #没有这个点，结果为空
    # nodes = list(map(buildeliteNodes, graph.run('MATCH (n:elite{name:"中国"}) RETURN n').data()))
    # print("中国查询结果：")
    # print(nodes==[])
    # todo:2. 查询结点A和结点B，N步跳转之内的所有关系
    #从“中国电信”到“北京”，长度为3的路径
    #不要查询长度为4及以上的路径，否则计算量过大
    print(len(str(graph.run('MATCH (n:elite{name:"%s"}) RETURN n' % "AAAI"))))
    #
    # querySentence = 'MATCH p= (n:elite{name:"%s"})-[*3]->(m:elite{name:"%s"}) RETURN p'%("中国电信", "北京")
    # print(querySentence)
    # QueryData = graph.run(querySentence).data()
    # print(len(QueryData))
    # x=list(map(GetRoad, graph.run('MATCH p= (n:elite{name:"中国电信"})-[*3]->(m:elite{name:"北京"}) RETURN p').data()))
    # print(x)
    # for i in x:
    #     print(i['data'])

    #


    # pass
    # nodes = list(map(buildeliteNodes, graph.run('MATCH (n:elite) RETURN n').data()))
    # print(nodes)
    # print("GETTING nodes")
    # nodes = [x for x in list(map(buildeliteNodes, graph.run('MATCH (n:elite) RETURN n').data())) if x]
    # print("GETTING edges")
    # edges = [e for e in list(map(buildEdges, graph.run('MATCH ()-[r]->() RETURN r').data())) if e]
    # EdgesNode = []
    # for e in edges:
    #     EdgesNode.extend([e['data']['source'], e['data']['target']])
    # EdgesNodeCounter = dict(Counter(EdgesNode))
    # NeedEdges = []
    # #利用NeedNodes选择需要的边放入NeedEdges
    # for x in edges:
    #     if (x['data']['target'] in NeedNodes) and (x['data']['source'] in NeedNodes):
    #         NeedEdges.append(x['data'])
    # print(NeedEdges)
    # EdgesNode = []
    # for edgename, count in EdgesNodeCounter.items():
    #     EdgesNode.append((edgename, count))
    # EdgesNode = sorted(EdgesNode, key = lambda x:x[1], reverse = True)
    # print([x[0] for x in EdgesNode[:50]])
    #
