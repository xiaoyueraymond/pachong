import argparse
import os
import pdb
import time
import json
import requests

import myformat as mf
import sys
import logging
from mytools import *
from xfusion_config_detail import *

import urllib3

urllib3.disable_warnings()

#
if os.name == 'nt':
    logdir = 'd:\\'
elif os.name == 'posix':
    logdir = '/tmp/'
else:
    msg = '无法判断系统，请联系开发者检查'
    print(msg)
#
log_diag_dir = logdir + 'dump_info'
logfile = logdir + 'xfusion_redfish_download.log'
cmd = "echo 123456 >d:\\xfusion_redfish_download.log"
os.system(cmd)
loglevel = logging.INFO
logging.getLogger("redfish").setLevel(logging.CRITICAL)
mylogger(logfile)
##
##
# cmdline parameters
parser = argparse.ArgumentParser(description='Query  information from the xFusion iBMC ).')
parser.add_argument('-U', '--USER', dest='username', default='Administrator',
                    help='specify the username to use to access the iBMC')
parser.add_argument('-P', '--PASS', dest='password', default='Admin@9000',
                    help='specify the password to use to access the iBMC')
parser.add_argument('-H', '--host', dest='host', default='192.168.89.119',
                    help='specify the IP Address or hostname of the target iBMC,default ip is 192.168.2.100')

args = parser.parse_args()
##


# pdb.set_trace()

#
url = 'https://' + args.host
login_url = url + '/UI/Rest/Login'
body = {
    "UserName": args.username,
    "Password": args.password,
    "Type": "Local",
    "Domain": "LocaliBMC"
}
#
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    'Content-Type': 'application/json;charset=utf-8',
    'Connection': 'keep-alive'

}
# session.headers.update({'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"})
# session.headers.update({'content-type':'application/json'})
login_info = session.post(login_url, json=body, headers=headers, verify=False)
# session.cookies.update(login_info.cookies)
#
# headers.update({'Token': login_info.headers['Token']})
# cookies = login_info.headers['Set-Cookie'].split(';')
# for i in cookies:
#     if i.startswith('SessionId'):
#         cookie = i
#         break
# else:
#     raise Exception("no cookie found!!!")
# headers.update({'Cookie': cookie})
# session.headers.update(login_info.headers)
# GenericInfo = '/UI/Rest/GenericInfo'
# GenericInfo_URL = url + GenericInfo
#
# info = session.get(GenericInfo_URL, verify=False)
# #
# print(info.text)
# print('*' * 50)
# print(info.headers)
#
# #
ProductInfo = '/UI/Rest/System/ProductInfo'
ProductInfo_URL = url + ProductInfo
# pdb.set_trace()
"""
(Pdb) rsp.json()['DigitalWarranty']
{'Lifespan': None, 'ProductName': '2288H V6', 'ManufactureDate': '2023-01-12 Thu 22:13:00', 
'UUID': '79A37381-3473-B5E5-EE11-23094C94AF2B', 'UnitType': 'Device', 'StartPoint': '2023-09-19', 
'SerialNumber': '2106195VSFXEP1000001'}
"""
rsp = session.get(ProductInfo_URL, verify=False)
#
server_info_dict = rsp.json()['DigitalWarranty']
MT = server_info_dict['ProductName'].replace(' ', '')
SN = server_info_dict['SerialNumber']
mytimestamp = get_datetime_str()
down_file = '_'.join([MT, SN, mytimestamp]) + '.tar.gz'
#
print(rsp.text)
print('#' * 70)
print(rsp.__dict__)
print('#' * 70)
#
dl_url = url + '/UI/Rest/Dump'
body1 = {
    "Type": "URI",
    "Content": "/tmp/web/2288HV6_2106195VSFXEP1000001_20240525-1234.tar.gz"
}
headers.update({'Cookie': login_info.headers['Set-Cookie']})
headers.update({'X-Csrf-Token': login_info.headers['Token']})
rsp = session.post(dl_url, json=body1, headers=headers, verify=False)
# print('*' * 70)
# print("rsp_status:", rsp)
# print(rsp.__dict__)
# print('*' * 70)
#
# # print(rsp)
msg = "start the post action to collect the logs now"
mf.display(msg)
if 'url' in rsp.json():
    status_url = url + rsp.json()['url']
    for i in range(1, 40):
        rsp = session.get(status_url, headers=headers, verify=False)
        if 'prepare_progress' in rsp.json():
            msg = f"current progress  is {rsp.json()['prepare_progress']}"
            mf.display(msg)
        if "downloadurl" in rsp.json():
            down_url = url + rsp.json()['downloadurl']
            rsp = session.get(down_url, headers=headers, verify=False)
            with open(down_file, 'wb') as fh:
                fh.write(rsp.content)
                msg = f"the BMC log file will save with name f{down_file}"
                mf.display(msg)
                break
        time.sleep(5)
