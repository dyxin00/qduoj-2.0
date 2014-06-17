#!/bin/bash
# Program:
#	Auto Install Necessary Tools For Project 'OLP'
#
# History:
#	2014/05/02	Potter	Version 1.0.0
#
#--------------------------------------------------------------
#	Requirements:
#		1. django==1.5.5
#		2. django-debug-toolbar==1.2.
#		3. Python Imaging Library (PIL) 1.7
#       4. south
#	
#	Platform:
#		Ubuntu

ScriptName="This Script"
CurrentDir=$(pwd)
BuildDir=${CurrentDir}"/BuildANO"

rm -rf $BuildDir	
mkdir $BuildDir	
cd $BuildDir

# Before Installation, we need some download tools
sudo apt-get install python-pip python-dev python-setuptools
sudo apt-get install git-flow

# 1. Install django==1.5.5
pip install django==1.5.5
if [ "$?" != "0" ]; then
	git clone https://github.com/django/django.git django1.5.x
	cd django.1.5.x
	python setup.py install
	cd ..
fi

# 2. Install django-debug-toolbar=1.2 ( Here will Instll latest Version, now is 1.2)
git clone https://github.com/django-debug-toolbar/django-debug-toolbar.git django-debug-toolbar
cd django-debug-toolbar
python setup.py install
cd ..

# 3. Install Python Imaging Library (PIL) 1.7
easy_install -f http://www.pythonware.com/products/pil/ Imaging
if [ "$?" != "0" ]; then
	wget https://gitcafe.com/Potter/Softwares/raw/master/Imaging-1.1.7.tar.gz
	tar -zxvf Imaging-1.1.7.tar.gz
	cd Imaging*
	python setup.py install
	cd ..
fi

# 4 south
pip install south

# 5 linaro-django-pagination 第三方分页插件
pip install linaro-django-pagination

# Clear
cd $CurrentDir
rm -rf $BuildDir

exit 0
