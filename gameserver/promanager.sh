#/bin/dash
#auth:尤泽顺
#创建：2016-2-4
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

InitModeGS(){
	ExecUser=dy1
	ScriptName='startupgs.py'
	SetGSLogPath
}

InitError(){
	echo '错误：没有匹配到模式,可选模式:als,gs,dts,cls,mnts'
	Tip
	exit
}

#增加一个模式的检查
InitMode(){
	Mode=$2
	if [ "$Mode" = 'gs' ];then
		InitModeGS $@
	else
		InitError
	fi
}

#程序-lanwood(6349) 2016-2-4
SetGSLogPath(){
	#文件存在且可读
	if [ -r /etc/gs.conf ];then
		#在当前shell下执行该配置（只需要读权限，不需要执行权限）
		. /etc/gs.conf
		LogPath=/home/dy1/gs${SERVERNUM}/log/srvmgrlog
		#创建路径本来不该写这的，考虑到shell脚本太容易乱了。还是贴着写吧
	else
		echo '错误：gameserver项目的配置文件不存在或者不具有读权限'
		exit
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
		exit
	fi
	
	DelLog
	if [ -z "$ExecUser" ] || [ `whoami` = ${ExecUser} ];then
		#以执行当前的shell脚本的用户身份执行
		mkdir -p $LogPath && $(python $ScriptPath --logpath=$LogPath --rootpath=$BasePath &>/dev/null) &
	else
		#以项目指定的身份执行
		su ${ExecUser} -c -l "mkdir -p $LogPath && $(python $ScriptPath --logpath=$LogPath --rootpath=$BasePath &>/dev/null) &"
	fi
	#沉睡一秒，等待程序启动
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

Tip(){
	echo "语法：sh opspro.sh ip [gs|als|cls|mnts|dts] [start|stop|restart|status|setup]
	例如：
	Step1.配置环境 sh opspro.sh ip gs setup
	Step2.运行     sh opspro.sh ip gs start
	其它：
	检查运行状态   sh opspro.sh ip gs status
	停止运行       sh opspro.sh ip gs stop"
}

Init(){
	Opt=$1			#第一个参数是操作类型
	Pro=$2			#第二个参数是项目名称
	SetBasePath
	InitMode $@		#根据传参设置模式
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
		*)
			echo '没有这个动作，start|restart|stop|status'
			Tip
			exit
		;;
	esac
}

Init $@
main $@

