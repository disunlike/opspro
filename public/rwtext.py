# -*- coding: utf-8 -*-
'''
规则参考游戏日志，不同项目的日志分别自行创建不同的目录管理

使用说明：
'Write('c/d','post')'
'''
from define import *
import path
import os


class CRWText():
    def __init__(self, sRootDir='', sPostfix='.txt'):
        self.m_RootDir = sRootDir  # 日记文件的根目录
        self.m_Postfix = sPostfix

    # 缓存数据默认是清空重写的，并且不需要记录缓存的时间
    # 在一个方法上加太多参数不好，所以这个方法从write中分离出来了。主要用于记录缓存
    def Cache(self, sFilePath, sText, sMode='w+'):
        # 千万不要写if not sText,否则数字0和0.0都不能写！
        if not sFilePath:
            return
        if not isinstance(sText, str):
            sText = str(sText)
        sLogName = path.GetFileName(sFilePath)
        sFolder = path.GetFilePath(sFilePath)
        self.CheckNameFormat(sLogName)
        if self.m_RootDir:
            sDirPath = self.m_RootDir + '/' + sFolder
        else:
            sDirPath = sFolder
        self.CreateFolder(sDirPath)
        sCacheName = sDirPath + '/' + sLogName
        self.WriteFile(sCacheName, sText, 'w+')

    # 写日志默认是追加文本内容
    def WriteLog(self, sFilePath, sText, sMode='a+'):
        # 千万不要写if not sText,否则数字0和0.0都不能写！
        if not sFilePath:
            return
        if not isinstance(sText, str):
            sText = str(sText)
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
        self.WriteFile(sLogName, sText, 'a+')

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

    def CreateFolder(self, sDirPath):
        path.CreateDir(sDirPath)
