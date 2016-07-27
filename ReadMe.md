# 用途
运维开发包工程，以server结尾的包是特定项目使用的包。其他包是通用的包，对一些常用的功能进行分装

# 包说明
gs：游戏服性能监控
als：报警信息分析
cls：数据采集服务 -- 未使用
dts：数据存储服务 -- 未使用
analysis 提供数据分析。目前分析数据的变化特征是否符合dos的特性
dev:提供设备的管理，比如获得ＩＯ使用，系统负载。目前用于获得网卡流量
public:通用代码。比如写日志，火星报警，路径解析
shellcmd:封装shell命令

# 操作：
	dash opspro/promanager.sh start|stop|status gs|als|cls|dts|mnt

# 游戏服规范要点:
1.编码为gbk
2.统一使用tab换行
3.权限必须最小化，需要root权限的那部分代码必须分离开运行
4.不允许带着异常运行，程序某个功能异常，整个进程必须都停止。
5.不能有多余的文件，注意工具的配置文件，他们一般是隐藏的。如.svn,.git


# 演示gameserver的部署
## 环境初始化：
	useradd dy1 -m -d /home/dy1
	mv opspro/ /home/dy1
	cd /home/dy1/
	touch /etc/gs.conf
	sudo dash opspro/confkernlog.sh #这步需要root权限
		 * Stopping enhanced syslogd rsyslogd[ OK ]
		 * Starting enhanced syslogd rsyslogd[ OK ]
		提示:rsyslog配置完成
	dash opspro/promanager.sh start gs
		启动startupgs.py成功

## dy1权限执行：
dash opspro/promanager.sh start gs

## 查看运行状态:
dash opspro/promanager.sh status gs

## 数据存储服务
	dash opspro/promanager.sh start dts
	dash opspro/promanager.sh stop dts

# ecplise 设置：
	1.显示换行符和缩进
		Window->Preferences->General->Editors->Text Editors->Show whitespace characters
	2.配置python ide
	3.字体
		Window->Preferences->general->appearance->colors and fonts->
	4.编码设置为UTF-8
		window->preferences->general->editors->text editors->spelling->encoding->UTF-8，编辑器的编码格式
		window->preferences->workspace->text file encoding->UTF-8
	5.设置换行符为Linux换行符
		同设置编码
	6.使用tab作为换行符
		pydev->editor->replace tabs with spaces when typing
	7.代码联想
		和编译器的ide有关，python的设置方式是在windows中安装python的编译器有	


