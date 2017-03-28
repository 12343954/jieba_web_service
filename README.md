

安装jieba分词

1，代码对 Python 2/3 均兼容

全自动安装：easy_install jieba 或者 pip install jieba / pip3 install jieba

2，testing：


安装flask，制作python的RESTful风格 webservice

1，$ sodu pip install flask

2，useage in python:
	from Flask import request


安装Mysql
下载dmg安装

安装	MySQL-python

出现：EnvironmentError: mysql_config not found
解决：
PATH="/usr/local/mysql/bin:${PATH}"
export PATH
export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
export VERSIONER_PYTHON_PREFER_64_BIT=yes
export VERSIONER_PYTHON_PREFER_32_BIT=no

最后
sudo pip install MySQL-python


推荐安装：PyMySQL + DBUtils
#http://blog.csdn.net/cyh1111/article/details/53337895

	$ sudo pip install PyMySQL
	$ sudo pip install DBUtils

vscode push to github

1,在vscode终端窗口，输入

	$ git remote add origin https://github.com/12343954/jieba_web_service
	$ git pull origin master

2,vscode git 窗口 右上角 “推送到”，弹出窗口，填入账号密码，确认，即可添加到github










