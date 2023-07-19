import logging
import time
import os
#建立其他文件所需要的logging函数,目前有3个功能
'''
1.分词功能
记录哪个IP什么时间查询了分词。
记录哪个IP什么时间插入了什么词语。
2.实体关系功能
记录哪个IP什么时间查询了什么样的语句
3.知识图谱功能
记录哪个IP访问了知识图谱
'''
SegmentLoggerName = "SegmentationLog"
ExtractRelationLoggerName = "ExtractRelationLog"
GraphLoggerName = "GraphLog"

class Log():
    def __init__(self, Name):
        self.name = Name
        self.logger = logging.getLogger(Name)

    #进行日志输出，输出信息由各调用者自行定义
    def ExcuteLoging(self, message):
        self.logger.setLevel(logging.DEBUG)
        #确定输出的日志名称，为三种功能后面贴上当前日期
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        log_path = 'logging'
        logfile = "{}/{}_{}.log".format(log_path, self.name, rq)
        #创建输出位置
        fh = logging.FileHandler(logfile, mode='a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
        #确定输出格式
        formatter = logging.Formatter("%(asctime)s, %(message)s")
        fh.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(fh)
        self.logger.info(message)
        self.logger.removeHandler(fh)

if __name__ == "__main__":
    TestLog = Log(SegmentLoggerName)
    TestLog.ExcuteLoging("testing")