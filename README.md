

### install jieba split words ###

1. compatible with Python 2/3

auto-install：easy_install jieba 或者 pip install jieba / pip3 install jieba

2. testing：


### install flask，make python RESTful api webservice ###

1. $ sodu pip install flask

2. useage in python:
	from Flask import request


### install Mysql ###
1. download dmg and install
	export PATH=${PATH}:/usr/local/mysql/bin

2. install	MySQL-python

error：EnvironmentError: mysql_config not found  
fix：  
PATH="/usr/local/mysql/bin:${PATH}"  
export PATH  
export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/  
export VERSIONER_PYTHON_PREFER_64_BIT=yes  
export VERSIONER_PYTHON_PREFER_32_BIT=no  

3. finally
sudo pip install MySQL-python  


### recommend：PyMySQL + DBUtils ###

#http://blog.csdn.net/cyh1111/article/details/53337895

	$ sudo pip install PyMySQL
	$ sudo pip install DBUtils

### vscode push to github ###

1. vscode console

	$ git remote add origin https://github.com/12343954/jieba_web_service  
	$ git pull origin master

2. vscode git window “push”，pop-up window，input usename/pwd，confirm，then push to github


### git drop local code，force remote code

	git fetch --all
	git reset --hard origin/master
	







