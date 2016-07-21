#/bin/dash
#auth:尤泽顺
#2016-5-30
#用途逻辑：
#		如果当前存在opspro进程，则退出
#		如果当前环境未初始化，则配置环境
#		用dy1身份启动opspro相关进程

#基础路径为脚本所在的路径
SetBasePath(){
	sBasePath=$(cd `dirname $0`;pwd)
}

#检查环境
CheckPath(){
	sScriptStart=$sBasePath/promanager.sh
	test -r $sScriptManager || exit 0
	
	sScriptInit=$sBasePath/confkernlog.sh
	test -r $sScriptInit || exit 0
}

#检查程序是否已经在运行
IsRun()
{
	sScripGS=$sBasePath/startupgs.py
	Result=`ps -ef|grep $sScripGS|grep -v ' grep '` 
	if [ ! -z "$Result" ];then
		return 1
	fi
	return 0
}

IsExit(){
	IsRun
	if [ $? = 1 ];then
		#echo '程序opspro已经在执行，退出程序'
		exit 0
	fi
}

SetBasePath
IsExit
CheckPath
dash $sScriptInit
dash $sScriptStart start gs
