#问题回答模块
from py2neo import Graph
import UserServiceImpl
from user_info.User_bean import User

# 进行个性化检索，需要按照不同的查询类型进行不同的个性化

class PeronalizedInfo:

    def __init__(self):
        self.g = Graph('http://localhost:7474/', auth=("neo4j", "jjrneo4j"))
        self.num_limit = 20

    def getUserComplex(self,username):
        FinalResult = UserServiceImpl.getUserInfo(username)
        print("FinalResult : ",FinalResult)
        smoke = FinalResult["smoke"]
        alcohol = FinalResult["alcohol"]
        diseases = []
        #print(FinalResult["disease"].type)
        diseases = FinalResult["disease"]
        """
        print(FinalResult["disease"])
        print('、' not in FinalResult["disease"])
        if FinalResult["disease"] is None or '、' not in FinalResult["disease"]:
            print("a")
            diseases.append(FinalResult["disease"])

        else:
            diseases = FinalResult["disease"].split('、')
            print("b")
        """
        print("diseases : ",diseases)
        allergies = []
        allergies = FinalResult["allergy"]
        """
        if FinalResult["allergy"] is None or '、' not in FinalResult["allergy"]:
            allergies.append(FinalResult["allergy"])
        else:
            allergies = FinalResult["allergy"].split('、')
        """
        user = User(username=username, diseases=diseases, allergy=allergies,smoke = smoke,alcohol = alcohol)
        #获取用户的忌食信息
        sqls = []
        if diseases is not None:
            for i in diseases:
                sql = "MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i)
                sqls.append(sql)

        if allergies is not None:
            for i in allergies:
                sql = "MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i)
                sqls.append(sql)
        print(sqls.__len__())
        notfoods = []
        for sql in sqls:
            print(sql)
            print(self.g.run(sql).data())
            ress = self.g.run(sql).data()
            notfoods += ress
        user.notfoods = notfoods
        #获取用户的宜食信息
        sqls = []
        if diseases is not None:
            for i in diseases:
                sql = "MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i)
                sqls.append(sql)
            for i in diseases:
                "MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i)
                sqls.append(sql)
        if allergies is not None:
            for i in allergies:
                sql = "MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i)
                sqls.append(sql)
            for i in allergies:
                sql = "MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i)
                sqls.append(sql)
        goodfoods = []

        for sql in sqls:
            ress = self.g.run(sql).data()
            goodfoods += ress
        print(goodfoods)
        user.goodfoods = goodfoods
        return user



"""
def personalized_search(self,question_type,username):
    FinalResult = UserServiceImpl.getUserInfo(username)
    diseases = FinalResult["disease"]
    allergies = FinalResult["allergy"]
    if question_type == "disease_not_food":#忌食问题
        for disease in diseases:
            sql =


    elif question_type == "disease_do_food":#宜食问题
"""