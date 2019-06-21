#!/bin/bash
mysql -uroot -proot123 < ../testSQL/test.sql
num=$1

if [ -e work_dir ]; then
	echo "work_dir is exists"
else
	mkdir work_dir && chmod 777 work_dir
fi
if [ -e data_dir ]; then
	echo "data_dir is exists"
else
	mkdir data_dir && chmod 777 data_dir
fi

if [ $num -eq 1 ]; then
	sudo python3 ../acmjudger-master/protect.py
fi
