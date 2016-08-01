# -*- coding:utf-8 -*-

#����ʱ��: Mar 15, 2016
#����: youzeshun  (IM: 8766)
#��;:
#	1.Ϊ���ܹ�Ȩ�޷��룬�ó���ͨ��ʹ��dy1�˻�ִ�У���Ҫ��root�û��Ĳ����������
#	2.���������ļ����ݵĶ�ȡȨ�޸���dy1

#���ݣ�����ϵͳ��־
#��;���������ռ���ֱ𵥶�����

. /etc/gs.conf

CheckPath(){

	#���������ں���־��shell�ű����ýű���ҪrootȨ�ޣ����Է�������
	if [ -f '/var/log/kern.emerg.log' ] && [ -f '/var/log/kern.crit.log' ] && [ -f '/var/log/kern.alert.log' ];then
		echo '��ά���rsyslog����:rsyslog�Ѿ����ù���'
		BoolConf=0
		return 0
	fi
	
	User=`whoami`
	if [ ${User} != 'root' ];then
		echo '��ά���rsyslog����:rsyslog��û�б�����,����root,��û�㹻��Ȩ������rsyslog'
		BoolConf=0
		return 0
	fi
		
	#ֻ�а汾����׼ȷ���еģ��汾���Ͱ汾������Ҳ���С�
	Version=`rsyslogd -v|head -n1|awk '{print $2}'|awk -F. '{print $1}'`
	if [ "$Version" -gt 7 ] || [ "$Version" -lt 4 ];then
		echo '��ά���rsyslog����:rsyslog��û�б�����,��֧��rsyslog�汾4-7�İ汾'
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
	
	#����������������Ч
	service rsyslog restart
	
	#�����ļ���������Ϊdy1���Ի�ö�ȡȨ��
	if [ -f '/var/log/kern.emerg.log' ] && [ -f '/var/log/kern.crit.log' ] && [ -f '/var/log/kern.alert.log' ] && [ -f '/var/log/kern.err.log' ];then
		chown dy1 /var/log/kern.err.log
		chown dy1 /var/log/kern.crit.log
		chown dy1 /var/log/kern.alert.log
		chown dy1 /var/log/kern.emerg.log
		echo '��ʾ:rsyslog�������'
	else
		echo '��ά���rsyslog����:����ʧ�ܣ���־û������'
	fi
}

InitTip(){
	if [ -z "$@" ];then
		BoolTip=1
	fi
}

Init(){
	#��黷��
	CheckPath
}

Start(){
	if [ "${BoolConf}" = 0 ];then
		return 0
	fi
	#��ʼ����
	ConfRsyslog
}

Temp(){
	BasePath=$(cd `dirname $0`;pwd)
	#���Ǹ�Σ����,��������һ�����.���$BasePath�ǿյģ���ô��ɾ����Ŀ¼�µ�data
	if [ -d "$BasePath" ] && [ -d "$BasePath/data" ];then
		rm -r $BasePath/data
	fi
	
	#����ɰ汾�Ĵ���
	if [ -f '/var/log/kern.emerg.log' ] || [ -f '/var/log/kern.crit.log' ] || [ -f '/var/log/kern.alert.log' ];then
		chown dy1 /var/log/kern.*.log
	fi
	
	#�ɰ���root���ɵ�Ŀ¼������֮
	if [ -d '/home/dy1/shellpublic/ddos/srvmgr/log' ];then
		rm -rf /home/dy1/shellpublic/ddos/srvmgr/log
	fi
	
	
	#������Ŀ¼������Ϊ�����ڶ���root���ɹ�.������־�ļ����ܱ�dy1�޸ģ������߸�Ϊdy1
	if [ -d "/home/dy1/gs${SERVERNUM}/log/srvmgrlog" ];then
		chown -R dy1 /home/dy1/gs${SERVERNUM}/log/srvmgrlog
	fi
}

Temp
#��ʼ������
Init
Start

