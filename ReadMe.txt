游戏服规范:
	1.对于gs项目，当测试通过的时，使用enca命令打包改编码为gbk
	2.使用游戏服

测试环境到上线的调整：
	1.测试通过
	2.注释掉测试版本配置，去除和该项目无关的代码文件
	3.【重要】清理掉所有的内容输出，改为写入文本
	4.用测试函数进行功能测试
	5.【重要】转换编码为gbk
	
2.编写上线测试指令，针对上次报警不成功的情况给出测试指令

3.备份数据，并打包标识版本号，去除测试数据，上线。


4.最后：使用打包程序，删除多余的内容。（svn信息还没使用打包程序检查过）

说明：
	gs：游戏服性能监控
	als：报警信息分析
	cls：数据采集服务
	dts：数据存储服务
	mnt：监控节点服务

操作：
	dash opspro/promanager.sh start|stop|status gs|als|cls|dts|mnt

游戏服性能监控
	环境初始化：
		useradd dy1 -m -d /home/dy1
		mv opspro/ /home/dy1
		cd /home/dy1/
		touch /etc/gs.conf
		dash opspro/confkernlog.sh
			 * Stopping enhanced syslogd rsyslogd[ OK ]
			 * Starting enhanced syslogd rsyslogd[ OK ]
			提示:rsyslog配置完成
		dash opspro/promanager.sh start gs
			启动startupgs.py成功

	root权限执行：
	dash opspro/gameserver/confkernlog.sh start
	
	dy1权限执行：
	dash opspro/promanager.sh start gs
	
	查看运行状态:
	dash opspro/promanager.sh status gs


数据存储服务
	dash opspro/promanager.sh start dts
	dash opspro/promanager.sh stop dts

数据采集服务
	配置collectserver下的clsconf，更改目标ip和端口
	dash opspro/promanager.sh start cls
	dash opspro/promanager.sh stop cls



ecplise 设置：
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
		
