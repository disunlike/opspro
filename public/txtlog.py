# -*- coding: utf-8 -*-
'''
规则参考游戏日志，不同项目的日志分别自行创建不同的目录管理

使用说明：
'Write('c/d','post')'
'''
from define import *
import path
import os


class CLog():
    def __init__(self, sRootDir='', sPostfix='.txt'):
        self.m_RootDir = sRootDir  # 日记文件的根目录
        self.m_Postfix = sPostfix

    def Write(self, sFilePath, sText, sMode='a+'):
        # 千万不要写if not sText,否则数字0和0.0都不能写！
        if not sFilePath:
            return
        if not isinstance(sText, str):
            sText = str(sText)
        # self.CheckPathFormat(sFilePath)
        sLogName = path.GetFileName(sFilePath)
        sFolder = path.GetFilePath(sFilePath)
        self.CheckNameFormat(sLogName)
        if self.m_RootDir:
            sDirPath = self.m_RootDir + '/' + sFolder
        else:
            sDirPath = sFolder
        self.CreateFolder(sDirPath)
        sText = self.GetText(sText)
        sLogName = self.GetPath(sDirPath, sLogName)
        self.WriteFile(sLogName, sText, sMode)

    def GetPath(self, sDirPath, sLogName):
        sLogName = sDirPath + '/' + sLogName + self.m_Postfix
        return sLogName

    def GetText(self, sText):
        sTime = GetTime()
        if not isinstance(sText, str):
            sText = str(sText)
        sText = sTime + ' ' + sText + '\n'
        return sText

    # 为了让这个函数能够被单独使用，所以增加了类型判断
    def WriteFile(self, sPath, sText, sMode='a+'):
        if not isinstance(sText, str):
            sText = str(sText)
        fLocal = open(sPath, sMode)
        fLocal.write(sText)

    def CheckNameFormat(self, sName):
        if not sName.find(self.m_Postfix):
            raise RuntimeError('不需要使用默认后缀')

    def CheckPathFormat(self, sFilePath):
        ResultList = sFilePath.split('/')
        if len(ResultList) < 2:
            raise RuntimeError('日志的存储至少是两极目录')

    def CreateFolder(self, sDirPath):
        path.CreateDir(sDirPath)


# 做成GlobalManager就是为了避免import这个模块 --程序-基础研发-黄诚恩(2978) 2016-3-15 09:44:45
# def Write(sFilePath,sText):
#	if not sText:
#		return
#	oManager=GetGlobalManager("txtlog")
#	if oManager:
#		oManager.Write(sFilePath, sText)

if __name__ == '__main__':
    g_oLog = CLog('/tmp')
    g_oLog.Write('debug', 0.0)
