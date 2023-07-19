from main import *
import json
from flask import request
import config
from core.nlp import NLP
from core.extractor import Extractor
import os.path
import Logging


@app.route('/ExtractRelationEntity',methods=['POST','GET'])
def ExtractRelationEntity():
    search2_condition = request.json
    print(search2_condition)
    final_result = {}
    final_result = {'text': "", 'relation': []}
    # 取得前端返回的查询条件
    content = search2_condition['content']
    print("content")
    print(content)

    ent1 = "控制血糖"
    ent2 = "糖尿病"
    rel = "预防"
    final_result = {
            'text': content,
             'relation': [
                {'entity1': {'text': "控制血糖"},
                 'entity2': {'text': "糖尿病"},
                 'relation': {'text': "预防" }
                }
            ]}

    # 情况1 输入为空
    # if len(content) == 0:
    #     final_result = {'text': "", 'relation': []}
    #     print(final_result)
    # else:
    #     #记录日志
    #     # Logger = Logging.Log(Logging.ExtractRelationLoggerName)
    #     # Logger.ExcuteLoging("IP:{}, QUERY:{}".format(request.remote_addr, content))
    #     # 先去User_Ner_dict找
    #     # UserDictNer = open("user_Ner_dict", 'r', encoding="utf-8")
    #     # for triple in UserDictNer:
    #     #     # print(triple)
    #     #     triple = triple.split('\n')
    #     #     # 中文逗号
    #     #     str_valid = triple[0].split('，')
    #     #     # print(str_valid)
    #     #     # 如果元组词同时存在句子中，返回用户自定义结果
    #     #     if str_valid[0] in content and str_valid[1] in content and str_valid[2] in content:
    #     #         final_result = {
    #     #             'text': content,
    #     #             'relation': [
    #     #                 {'entity1': {'text': str_valid[0], 'loc': content.find(str_valid[0]), 'len': len(str_valid[0])},
    #     #                  'entity2': {'text': str_valid[1], 'loc': content.find(str_valid[1]), 'len': len(str_valid[1])},
    #     #                 'relation': {'text': str_valid[2], 'loc': content.find(str_valid[2]), 'len': len(str_valid[2])}
    #     #                  }
    #     #             ]}
    #     #         print('用户词典中存在')
    #     #         exist = True
    #     #         print(final_result)
    #     #         return json.dumps(final_result)
    #     #         exit(0)
    #     # User_Ner_dict找不到，再去模型中抽取
    #     # 输出处理结果的Json文件
    #     output_path = 'data/extract_triple.json'  # 输出的处理结果Json文件
    #     if os.path.isfile(output_path):
    #         os.remove(output_path)
    #
    #     # 实例化 NLP
    #     nlp = NLP()
    #     # 知识三元组数量
    #     num = 1
    #     # ------------- 开始----------
    #     print('start processing')
    #     # 分词处理
    #     lemmas = nlp.segment(content.strip())
    #     # 词性标注
    #     words_postag = nlp.postag(lemmas)
    #     # 命名实体识别
    #     words_netag = nlp.netag(words_postag)
    #     # 依存句法分析
    #     sentence = nlp.parse(words_netag)
    #     print("依存句法分析")
    #     print(sentence.to_string())
    #     extractor = Extractor()
    #     num = extractor.extract(content.strip(), sentence, output_path, num)
    #     # 判断是否生成有效三元组
    #     if os.path.isfile('data/extract_triple.json'):
    #         # 情况2 输入是有效文本，能输出三元组
    #         with open('data/extract_triple.json', 'rb') as rf:
    #             result = {}
    #             relation_lst = []
    #             for line in rf:
    #                 line_re = json.loads(line)
    #                 # print(line_re)
    #                 result['text'] = line_re['句子']
    #                 dict_relation = {}
    #                 dict_relation_entity1 = {}
    #                 dict_relation_entity1['text'] = line_re['知识'][0]
    #                 dict_relation_entity1['loc'] = line_re['句子'].find(line_re['知识'][0])
    #                 dict_relation_entity1['len'] = len(line_re['知识'][0])
    #                 dict_relation_entity2 = {}
    #                 dict_relation_entity2['text'] = line_re['知识'][-1]
    #                 dict_relation_entity2['loc'] = line_re['句子'].find(line_re['知识'][-1])
    #                 dict_relation_entity2['len'] = len(line_re['知识'][-1])
    #                 dict_relation_relation = {}
    #                 dict_relation_relation['text'] = line_re['知识'][1]
    #                 dict_relation_relation['loc'] = line_re['句子'].find(line_re['知识'][1])
    #                 dict_relation_relation['len'] = len(line_re['知识'][1])
    #                 dict_relation['entity1'] = dict_relation_entity1
    #                 dict_relation['entity2'] = dict_relation_entity2
    #                 dict_relation['relation'] = dict_relation_relation
    #                 relation_lst.append(dict_relation)
    #             result['relation'] = relation_lst
    #         final_result = result
    #     else:
    #         # 情况3 输入为无效文本，输不出三元组
    #         final_result = {'text': content, 'relation': []}

    print(final_result)
    return json.dumps(final_result)
