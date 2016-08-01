#/bin/dash
#auth:����˳
#������2016-2-4
#��;��1.����python�����л���������־�ı���λ�õ� 2.����python�ű������У����������ܲ鿴״̬

#�������Ƿ����
IsFile(){
	file $ScriptPath &>/dev/null
	if [ $? = 1 ];then
		return 0
	fi
	return 1
}

#�������Ƿ��Ѿ�������
IsRun()
{
	Result=`ps -ef|grep $ScriptPath|grep -v ' grep '` 
	if [ ! -z "$Result" ];then
		return 1
	fi
	return 0
}

#�õ��ű����ڵ�·��
#$0��ʾִ��Ŀ¼���ű������·����dirname ���·�������ȣ�cd���ű��ľ���·����Ȼ��pwd�õ�ִ�и�����ľ���·��
SetScriptPath(){
	if [ -z $BasePath ];then
		echo '����û�����û���·����SetScriptPath��'
		exit
	fi

	SoftLink=`ls -l $BasePath|grep ' -> '`
	#�����ǰĿ¼����������õ���ʵ����
	if [ -z "$SoftLink" ];then
		ScriptPath=$BasePath/${ScriptName}
	else
		RealityPath=`echo $SoftLink|awk '{print $NF}'`
		ScriptPath=${RealityPath}/${ScriptName}
	fi
}

#����·��Ϊ�ű����ڵ�·��
SetBasePath(){
	BasePath=$(cd `dirname $0`;pwd)
}

InitModeGS(){
	ExecUser=dy1
	ScriptName='startupgs.py'
	SetGSLogPath
}

InitError(){
	echo '����û��ƥ�䵽ģʽ,��ѡģʽ:als,gs,dts,cls,mnts'
	Tip
	exit
}

#����һ��ģʽ�ļ��
InitMode(){
	Mode=$2
	if [ "$Mode" = 'gs' ];then
		InitModeGS $@
	else
		InitError
	fi
}

#����-lanwood(6349) 2016-2-4
SetGSLogPath(){
	#�ļ������ҿɶ�
	if [ -r /etc/gs.conf ];then
		#�ڵ�ǰshell��ִ�и����ã�ֻ��Ҫ��Ȩ�ޣ�����Ҫִ��Ȩ�ޣ�
		. /etc/gs.conf
		LogPath=/home/dy1/gs${SERVERNUM}/log/srvmgrlog
		#����·����������д��ģ����ǵ�shell�ű�̫�������ˡ���������д��
	else
		echo '����gameserver��Ŀ�������ļ������ڻ��߲����ж�Ȩ��'
		exit
	fi
}

#���ճ����·������ֹ����$1�ǳ���������ű�λ��
killPro(){
	ps -ef|grep $1|grep -v ' grep '|awk '{print $2}'|xargs kill
	if [ $? = 0 ];then
		echo '�ɹ���ֹ'$ScriptName
	else
		echo '��ֹ����ʧ��'$ScriptName
	fi
}

#�����־�����������$LogPath���ǿձ��������д��ϸ
DelLog(){
	if [ -z $LogPath ];then
		echo '����û������LogPath'
		exit
	else
		rm -rf $LogPath/status/*.txt
	fi
}

CheckStart(){
	IsRun
	if [ $? = 0 ];then
		echo '����'$ScriptName'ʧ��'
		return 1
	else
		echo '����'$ScriptName'�ɹ�'
		return 0
	fi
}

WaitStartup(){
	sleep 1
}

Start(){
	#IsFile ����ļ��Ƿ����
	IsRun
	if [ $? != 0 ];then
		exit
	fi
	
	DelLog
	if [ -z "$ExecUser" ] || [ `whoami` = ${ExecUser} ];then
		#��ִ�е�ǰ��shell�ű����û����ִ��
		mkdir -p $LogPath && $(python $ScriptPath --logpath=$LogPath --rootpath=$BasePath &>/dev/null) &
	else
		#����Ŀָ�������ִ��
		su ${ExecUser} -c -l "mkdir -p $LogPath && $(python $ScriptPath --logpath=$LogPath --rootpath=$BasePath &>/dev/null) &"
	fi
	#��˯һ�룬�ȴ���������
	WaitStartup
	CheckStart
}

Stop(){
	IsRun
	if [ $? = 0 ];then
		echo '����'$ScriptName'û��������'
	else
		killPro $ScriptPath
	fi
}

Status(){
	IsRun
	if [ $? = 0 ];then
		echo '����'$ScriptName'û��������'
	else
		echo '#��־·����'$LogPath
		ls $LogPath/status/*|tr '' '\n'|xargs cat
	fi
}

Tip(){
	echo "�﷨��sh opspro.sh ip [gs|als|cls|mnts|dts] [start|stop|restart|status|setup]
	���磺
	Step1.���û��� sh opspro.sh ip gs setup
	Step2.����     sh opspro.sh ip gs start
	������
	�������״̬   sh opspro.sh ip gs status
	ֹͣ����       sh opspro.sh ip gs stop"
}

Init(){
	Opt=$1			#��һ�������ǲ�������
	Pro=$2			#�ڶ�����������Ŀ����
	SetBasePath
	InitMode $@		#���ݴ�������ģʽ
	SetScriptPath	#���python�ű�����·������ýű�·��
}

#������ű���Ϊ����ʽ������ű���ͨ��

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
			echo 'û�����������start|restart|stop|status'
			Tip
			exit
		;;
	esac
}

Init $@
main $@

