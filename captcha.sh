#!/bin/bash
# Program:
#	Auto Install Necessary Tools For Project 'qduoj-2.0'
#
# History:
#	2014/06/23	xin	Version 1.0.0
#
#--------------------------------------------------------------
#	Requirements:
#		1. jpeg 
#		2. freetype
#		3. pillow replace PIL
#       4. DjangoVerifyCode
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
#sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev

pip uninstall -y  PIL
rm -rf ../../lib/python2.7/site-packages/PIL*
rm -fr ../../bin/pil*
# 3. Install Python Imaging Library (PIL) 1.7
## 需要先安装jpeg库
#wget http://www.ijg.org/files/jpegsrc.v7.tar.gz 
cp ../tools/jpegsrc.v7.tar.gz ./
tar -zxvf jpegsrc.v7.tar.gz
cd jpeg-7
CC="gcc -arch x86_64"
./configure --enable-shared --enable-static
make
sudo make install
cd ..

##安装freetype开发库
#wget http://download.savannah.gnu.org/releases/freetype/freetype-2.4.0.tar.gz
cp ../tools/freetype-2.4.0.tar.gz ./
tar -zxvf freetype-2.4.0.tar.gz
cd freetype-2.4.0
make
sudo make install
cd ..

##安装pillow
pip install pillow
#安装DjangoVerifyCode
pip install DjangoVerifyCode
cp ../tools/__init__.py ../../lib/python2.7/site-packages/DjangoVerifyCode
# Clear
cd $CurrentDir
sudo rm -rf $BuildDir

exit 0
