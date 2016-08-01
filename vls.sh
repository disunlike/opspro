#/bin/dash
#auth:尤泽顺
#2016-2-4
#用途：1.配置python的运行环境，如日志的保存位置等 2.管理python脚本的运行，启动，并能查看状态

#检查程序是否存在
IsFile(){
	file $ScriptPath &>/dev/null
	if [ $? = 1 ];then
		return 0
	fi
	return 1
}

#检查程序是否已经在运行
IsRun()
{
	Result=`ps -ef|grep $ScriptPath|grep -v ' grep '` 
	if [ ! -z "$Result" ];then
		return 1
	fi
	return 0
}

#得到脚本所在的路径
#$0表示执行目录到脚本的相对路径，dirname 获得路径名。既：cd到脚本的绝对路径，然后pwd得到执行该命令的绝对路径
SetScriptPath(){
	if [ -z $BasePath ];then
		echo '错误：没有设置基础路径（SetScriptPath）'
		exit
	fi

	SoftLink=`ls -l $BasePath|grep ' -> '`
	#如果当前目录是软链接则得到真实链接
	if [ -z "$SoftLink" ];then
		ScriptPath=$BasePath/${ScriptName}
	else
		RealityPath=`echo $SoftLink|awk '{print $NF}'`
		ScriptPath=${RealityPath}/${ScriptName}
	fi
}

#基础路径为脚本所在的路径
SetBasePath(){
	BasePath=$(cd `dirname $0`;pwd)
}

SetLogPath(){
	if [ -z $BasePath ];then
		echo '错误：没有设置基础路径'
		exit
	else
		LogPath=$BasePath/$1
	fi
}

#按照程序的路径来终止程序，$1是程序的启动脚本位置
killPro(){
	ps -ef|grep $1|grep -v ' grep '|awk '{print $2}'|xargs kill
	if [ $? = 0 ];then
		echo '成功终止'$ScriptName
	else
		echo '终止程序失败'$ScriptName
	fi
}

#清空日志，意外清空下$LogPath会是空变量，因此写详细
DelLog(){
	if [ -z $LogPath ];then
		echo '错误：没有设置LogPath'
		exit
	else
		rm -rf $LogPath/status/*.txt
	fi
}

CheckStart(){
	IsRun
	if [ $? = 0 ];then
		echo '启动'$ScriptName'失败'
		return 1
	else
		echo '启动'$ScriptName'成功'
		return 0
	fi
}

WaitStartup(){
	sleep 1
}

Start(){
	#IsFile 检查文件是否存在
	IsRun
	if [ $? != 0 ];then
		#echo '程序'$ScriptName'已经在运行'
		exit
	fi
	
	DelLog
	if [ -z "$ExecUser" ] || [ `whoami` = ${ExecUser} ];then
		#以执行当前的shell脚本的用户身份执行
		mkdir -p $LogPath && python $ScriptPath --logpath=$LogPath --rootpath=$BasePath &
	else
		#以项目指定的身份执行
		su ${ExecUser} -c -l "mkdir -p $LogPath && python $ScriptPath --logpath=$LogPath --rootpath=$BasePath &"
	fi
	#由于python放入后台启动是异步进行的，下面如果不等待启动则CheckStart会得到启动失败的结论
	WaitStartup
	CheckStart
}

Stop(){
	IsRun
	if [ $? = 0 ];then
		echo '程序'$ScriptName'没有在运行'
	else
		killPro $ScriptPath
	fi
}

Status(){
	IsRun
	if [ $? = 0 ];then
		echo '程序'$ScriptName'没有在运行'
	else
		echo '#日志路径：'$LogPath
		ls $LogPath/status/*|tr '' '\n'|xargs cat
	fi
}

Version(){
	echo '输出版本号'
}

Tip(){
	echo "语法：bash vls.sh start|stop|restart Mode
	例如：
	运行一个模式：bash vls.sh start
	结束当前的程序：bash vls.sh stop
	重启当前的程序:bash vls.sh restart
	查看状态：bash vls.sh status"
}

Init(){
	Opt=$1
	ScriptName='startupvls.py' #dasb等号两边不允许空格，否则被视为多个dash命令
	SetBasePath
	SetLogPath Log/
	SetScriptPath	#组合python脚本名和路径名获得脚本路径
}

#将这个脚本改为传入式，这个脚本将通用

main(){
	case $1 in
		start)
			Start
		;;
		stop)
			Stop
		;;
		restart)
			Stop
			Start
		;;
		status)
			Status
		;;
		version)
			Version
		;;
		*)
			echo '没有这个动作，start|restart|stop|status'
			Tip
			exit
		;;
	esac
}

Init $@
main $@
