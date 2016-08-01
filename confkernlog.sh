# -*- coding:utf-8 -*-

#创建时间: Mar 15, 2016
#作者: youzeshun  (IM: 8766)
#用途:
#	1.为了能够权限分离，让程序通常使用dy1账户执行，需要将root用户的操作分离出来
#	2.将部分如文件内容的读取权限给予dy1

#内容：配置系统日志
#用途：将错误按照级别分别单独保存

. /etc/gs.conf

CheckPath(){

	#启动配置内核日志的shell脚本，该脚本需要root权限，所以放在这里
	if [ -f '/var/log/kern.emerg.log' ] && [ -f '/var/log/kern.crit.log' ] && [ -f '/var/log/kern.alert.log' ];then
		echo '运维监控rsyslog配置:rsyslog已经配置过了'
		BoolConf=0
		return 0
	fi
	
	User=`whoami`
	if [ ${User} != 'root' ];then
		echo '运维监控rsyslog配置:rsyslog并没有被配置,不是root,有没足够的权限配置rsyslog'
		BoolConf=0
		return 0
	fi
		
	#只有版本５是准确不行的，版本６和版本７可能也不行。
	Version=`rsyslogd -v|head -n1|awk '{print $2}'|awk -F. '{print $1}'`
	if [ "$Version" -gt 7 ] || [ "$Version" -lt 4 ];then
		echo '运维监控rsyslog配置:rsyslog并没有被配置,仅支持rsyslog版本4-7的版本'
		BoolConf=0
		return 0
	fi
	
	BoolConf=1
	return 1
}

ConfRsyslog(){
	ConfContent='
	#Create By youzeshun
	\nkern.=err   /var/log/kern.err.log
	\nkern.=crit   /var/log/kern.crit.log
	\nkern.=alert   /var/log/kern.alert.log
	\nkern.=emerg   /var/log/kern.emerg.log'
	
	ConfPath='/etc/rsyslog.d/kern0-3.conf'
	
	echo ${ConfContent} > ${ConfPath}
	
	#重启服务，让配置生效
	service rsyslog restart
	
	#更改文件的所有者为dy1，以获得读取权限
	if [ -f '/var/log/kern.emerg.log' ] && [ -f '/var/log/kern.crit.log' ] && [ -f '/var/log/kern.alert.log' ] && [ -f '/var/log/kern.err.log' ];then
		chown dy1 /var/log/kern.err.log
		chown dy1 /var/log/kern.crit.log
		chown dy1 /var/log/kern.alert.log
		chown dy1 /var/log/kern.emerg.log
		echo '提示:rsyslog配置完成'
	else
		echo '运维监控rsyslog配置:配置失败，日志没有生成'
	fi
}

InitTip(){
	if [ -z "$@" ];then
		BoolTip=1
	fi
}

Init(){
	#检查环境
	CheckPath
}

Start(){
	if [ "${BoolConf}" = 0 ];then
		return 0
	fi
	#开始配置
	ConfRsyslog
}

Temp(){
	BasePath=$(cd `dirname $0`;pwd)
	#这是高危操作,额外增加一个检查.如果$BasePath是空的，那么会删除根目录下的data
	if [ -d "$BasePath" ] && [ -d "$BasePath/data" ];then
		rm -r $BasePath/data
	fi
	
	#解决旧版本的代码
	if [ -f '/var/log/kern.emerg.log' ] || [ -f '/var/log/kern.crit.log' ] || [ -f '/var/log/kern.alert.log' ];then
		chown dy1 /var/log/kern.*.log
	fi
	
	#旧版用root生成的目录，清理之
	if [ -d '/home/dy1/shellpublic/ddos/srvmgr/log' ];then
		rm -rf /home/dy1/shellpublic/ddos/srvmgr/log
	fi
	
	
	#后续的目录可能因为不存在而被root生成过.导致日志文件不能被dy1修改，所有者改为dy1
	if [ -d "/home/dy1/gs${SERVERNUM}/log/srvmgrlog" ];then
		chown -R dy1 /home/dy1/gs${SERVERNUM}/log/srvmgrlog
	fi
}

Temp
#初始化参数
Init
Start

