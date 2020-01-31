# -*- coding: utf-8 -*-
from collections import Counter
import operator


class Reduct(object):
    rowsNum = 0  # 行数
    listsNum = 0  # 列数
    attrTable = []  # 信息系统，包含条件属性集和决策属性集
    attrD = []  # 决策属性集
    attrB = []  # 约简属性集
    rule = []  # 条件属性集与约简集的差集
    yuejian = []  # 约简集的下标

    def __init__(self, filePath, separator=';', decisionNum=1, precision=[0, 1e-7, 0]):
        """
        基于知识粒度的经典启发式属性约简算法
        :param filePath: 文件路径
        :param separator: 文件中的分割符，默认为;
        :param decisionNum: 决策属性个数，默认为1
        :param precision: 算法一中三个可能的参数(精度)
        """
        self.filePath = filePath
        self.separator = separator
        self.decisionNum = decisionNum
        self.precision = precision
        Reduct.rowsNum = 0
        Reduct.listsNum = 0
        Reduct.attrTable = []
        Reduct.attrD = []
        Reduct.attrB = []
        Reduct.rule = []
        Reduct.yuejian = []
        file = open(filePath, 'r')
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            line = line.split(separator)
            Reduct.attrTable.append(line)
        Reduct.rowsNum = len(Reduct.attrTable)
        Reduct.listsNum = len(Reduct.attrTable[0])
        for i in range(1, Reduct.listsNum - self.decisionNum + 1):
            Reduct.rule.append(i)

    def __del__(self):
        class_name = self.__class__.__name__

    def listToString(self, attr):
        """
        将二维列表中的每维个列表转化为字符串
        :param attr: 属性，为二维列表
        :return: 
        返回一个一维的字符串列表
        @attrTemp
        """
        attrTemp = []
        for i in range(len(attr)):
            string = ''
            string = string.join(attr[i])
            attrTemp.append(string)
        return attrTemp

    def gainKonwledge(self, attr):
        """
        求知识粒度
        :param attr: 传入的参数是二维列表
        :return: 
        返回知识粒度
        @divide / float(self.rowsNum * self.rowsNum)
        """
        divide = 0
        attrString = self.listToString(attr)  # 调用list_to_string,将二维列表转化维一维列表
        count = Counter(attrString)  # 类型： <class 'collections.Counter'>
        countDict = dict(count)  # 类型： <type 'dict'>
        for key in countDict:
            divide += countDict.get(key) * countDict.get(key)
        return divide / float(self.rowsNum * self.rowsNum)

    def gainCondiction(self):
        """
        得到条件属性
        :return: 
        返回的是含条件属性的二维列表
        @attrC
        """
        attrC = []
        for i in range(self.rowsNum):
            attrC.append(self.attrTable[i][0:self.listsNum - self.decisionNum])
            self.attrD.append(self.attrTable[i][self.listsNum - self.decisionNum:self.listsNum])  # 得到决策属性
        return attrC

    def gainReduct(self):
        """
        属性约简过程
        :return: NULL
        """
        '''选择核属性'''
        attrC = self.gainCondiction()
        sub = self.gainKonwledge(attrC) - self.gainKonwledge(self.attrTable)
        for j in range(1, self.listsNum - self.decisionNum + 1):
            result = (self.gainInner(attrC, j) - self.gainInner(self.attrTable, j)) - sub
            if result > self.precision[0]:
                self.yuejian.append(j)
        '''根据下标求得约简集'''
        for i in range(self.rowsNum):
            attrBTemp = [self.attrTable[i][j - 1] for j in self.yuejian]
            self.attrB.append(attrBTemp)
        attrBD = self.gainBandD()
        '''求c-b的差集下标'''
        for i in self.yuejian:
            self.rule.remove(i)
        '''在c-b中选择外部重要度大的元素往约简集中添加'''
        while abs((self.gainKonwledge(self.attrB) - self.gainKonwledge(attrBD)) - sub) >= self.precision[1]:
            maxSigOuter = {}
            for i in self.rule:  # C-B的差集下标
                preOuter = self.gainKonwledge(self.attrB) - self.gainKonwledge(attrBD)
                nextOuter = self.gainOuter(self.attrB, i) - self.gainOuter(attrBD, i)
                aResult = preOuter - nextOuter
                maxSigOuter[i] = aResult
            maxSigOuter = sorted(maxSigOuter.items(), key=operator.itemgetter(1), reverse=True)
            a0 = maxSigOuter[0][0]
            self.yuejian.append(a0)
            self.rule.remove(a0)
            self.gainBanda0(a0)
            attrBD = self.gainBandD()
        '''去冗余'''
        for i in self.yuejian:
            if abs(self.gainInner(self.attrB, i) - self.gainInner(attrBD, i) - sub) <= self.precision[2]:
                self.gainBsubai(i)
                attrBD = self.gainBandD()
                self.yuejian.remove(i)

    def gainInner(self, attr, j):
        """
        计算((C条件属性-j)或者(C条件属性和D决策属性-j)),取决于attr
        :param attr: 属性集
        :param j: 第j个特征(属性)
        :return: 
        返回知识粒度
        @self.gainKonwledge(attrTemp)
        """
        attrTemp = []
        length = len(attr[0])
        for i in range(self.rowsNum):
            '''下标为j-1的元素被去除,即第j个元素'''
            attrTemp.append(attr[i][0:j - 1] + attr[i][j:length])
        return self.gainKonwledge(attrTemp)

    def gainBandD(self):
        """
        求约简集和决策属性的并集
        :return:
        返回并集
        @attrBD
        """
        attrBD = []
        for i in range(self.rowsNum):
            if len(Reduct.attrB) == 0:
                attrBD.append((self.attrD[i]))
            else:
                attrBD.append(self.attrB[i] + (self.attrD[i]))
        return attrBD

    def gainOuter(self, attr, j):
        """
        :param attr: 属性集
        :param j: 第j个特征(属性)
        :return: 
        返回知识粒度
        @self.gainKonwledge(attrInclude)
        """
        attrInclude = []
        for i in range(self.rowsNum):
            if len(attr[0]) == 0:
                attrInclude.append(list(self.attrTable[i][j - 1]))
            else:
                attrInclude.append(attr[i] + list(self.attrTable[i][j - 1]))
        return self.gainKonwledge(attrInclude)

    def gainBanda0(self, a0):
        """
        求约简集和第a0个属性的并集
        :param a0: 第a0个特征(属性)
        :return: NULL
        """
        for i in range(self.rowsNum):
            self.attrB[i].append(self.attrTable[i][a0 - 1])

    def gainBsubai(self, j):
        """
        求约简集和第a0个属性的并集
        :param j: 第j个属性
        :return: NULL
        """
        for i in range(self.rowsNum):
            self.attrB[i].remove(self.attrTable[i][j - 1])
