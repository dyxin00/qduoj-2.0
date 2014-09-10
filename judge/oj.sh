

sudo apt-get install make flex g++ libmysql++-dev  mysql-server 

APACHEUSER=qduoj

sudo  /usr/sbin/useradd -m -u 1536 judge


#create work dir set default conf
sudo    mkdir /home/judge
sudo    mkdir /home/judge/etc
sudo    mkdir /home/judge/data
sudo    mkdir /home/judge/log
sudo    mkdir /home/judge/run0
sudo    mkdir /home/judge/run1
sudo    mkdir /home/judge/run2
sudo    mkdir /home/judge/run3
sudo cp java0.policy  judge.conf /home/judge/etc
sudo chown -R judge /home/judge
sudo chgrp -R $APACHEUSER /home/judge/data
sudo chgrp -R root /home/judge/etc /home/judge/run?
sudo chmod 775 /home/judge /home/judge/data /home/judge/etc /home/judge/run? 


#pid file
sudo touch /var/run/judged.pid

sudo ./make.sh
