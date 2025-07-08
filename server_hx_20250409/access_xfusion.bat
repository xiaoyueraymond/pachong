@echo off
cd D:\serverhx\servers_hx
set IP_PREFIX=192.168.0

REM 组合IP地址
set FULL_IP=%IP_PREFIX%.%1
python open_xfusion.py -H %FULL_IP%
