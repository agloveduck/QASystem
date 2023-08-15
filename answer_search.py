
#问题回答模块
from py2neo import Graph
import UserServiceImpl
from personalized_info import PeronalizedInfo

peronalizedinfo = PeronalizedInfo()


class AnswerSearcher:
    def __init__(self):
        self.g = Graph('http://localhost:7474/', auth=("neo4j", "jjrneo4j"))
        self.num_limit = 20
        self.notfoods = []
        self.goodfoods = []


    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls , username):
        user = peronalizedinfo.getUserComplex(username)
        self.goodfoods = user.goodfoods
        print("goodfoods : ",self.goodfoods)
        self.notfoods = user.notfoods
        print("notfoods : " , self.notfoods)
        diseases = user.diseases
        allergies = user.allergy
        textanss = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            print("question_type : ",question_type)
            queries = sql_['sql']
            answers = []
            print("queries : ", queries)
            for query in queries:
                print("query : ",query)
                ress = self.g.run(query).data()
                print("ress:", ress)
                answers += ress
            print("answers : ", answers)
            final_answer = self.answer_prettify(question_type, answers)
            textans = final_answer["final_answer"]
            if textans:
                textanss.append(textans)
        final_answer["final_answer"] = textanss
        return final_answer
    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        nodes = []
        links = []
        setAns = []
        relationshipId = 0
        final_answer = []
        subject =''
        relation = ''
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            setAns = list(set(desc))
            relation = answers[0]['r.name']
            print("relation:",relation)
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['n.name']
            relation = answers[0]['r.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['m.name']
            relation = "病因"
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['m.name']
            relation = "预防"
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            desc = [i['m.cure_lasttime'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['m.name']
            relation = "持续周期"
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            desc = [';'.join(i['m.cure_way']) for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['m.name']
            relation = "治疗方式"
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureprob':
            desc = [i['m.cured_prob'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['m.name']
            relation = "治愈率"
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_easyget':
            desc = [i['m.easy_get'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['m.name']
            relation = "易感"
            final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['m.name']
            relation = "相关信息"
            final_answer = '{0}的相关信息：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            setAns = list(set(desc))
            relation = "并发"
            final_answer = '{0}的并发症包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        #需要改的部分1
        elif question_type == 'disease_not_food':
            notdes = [i['n.name'] for i in self.notfoods]
            goodes = [i['n.name'] for i in self.notfoods]
            desc = [i['n.name'] for i in answers]
            print("desc : ", desc)
            setAns = list(set(desc))

            subject = answers[0]['m.name']
            print("subject : ", subject)
            relation = answers[0]['r.name']
            print("relation :",relation)
            final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        #需要改的部分2,需要筛选掉患者不能食用的食物
        elif question_type == 'disease_do_food':
            notdes = set([i['n.name'] for i in self.notfoods])
            print(notdes)
            goodes = set([i['n.name'] for i in self.notfoods])

            do_desc = set([i['n.name'] for i in answers if i['r.name'] == '宜吃'])
            print("desc :" ,do_desc)
            do_desc.difference_update(notdes)
            print("after_dec:",do_desc)
            setAns = do_desc
            recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
            subject = answers[0]['m.name']
            relation = answers[0]['r.name']
            final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers]
            print("desc :" ,desc)
            setAns = list(set(desc))
            subject = answers[0]['n.name']
            relation = answers[0]['r.name']
            final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'food_do_disease':
            notdes = set([i['n.name'] for i in self.notfoods])
            goodes = set([i['n.name'] for i in self.notfoods])
            desc = set([i['m.name'] for i in answers])
            print("desc :" ,desc)
            desc.difference_update(notdes)
            print("after_dec:", desc)
            setAns = list(set(desc))
            subject = answers[0]['n.name']
            relation = answers[0]['r.name']
            final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['m.name']
            relation = answers[0]['r.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['n.name']
            relation = answers[0]['r.name']
            final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['m.name']
            relation = answers[0]['r.name']
            print(subject)
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_disease':
            desc = [i['m.name'] for i in answers]
            setAns = list(set(desc))
            subject = answers[0]['n.name']
            relation = answers[0]['r.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        node = {
            "id": 0,
            "authorName": subject,
            "linkId": 0
        }
        nodes.append(node)
        j = 0
        for val in setAns:
            j+=1
            node = {
                    "id": j,
                    "authorName": val,
                    "linkId": j
            }
            nodes.append(node)
            link = {
                "source": 0,
                "target": j,
                "relation": {
                    "relationshipId": relationshipId,
                    "relationship": relation,
                    "weight": 0,
                    "created": 0,
                    "lineNumber": None,
                    "isSelf": False
                }
            }
            links.append(link)
        print("nodes:", nodes)
        print("links:", links)

        result ={
            "links": links,
            "nodes": nodes,
            "final_answer":final_answer
        }
        return result


if __name__ == '__main__':
    searcher = AnswerSearcher()
