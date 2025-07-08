import requests
#
#
session = requests.Session()
import pdb

# 使用 session 发送请求
data = '{"UserName":"Administrator","Password":"Admin@9000"}'
header = {"Content-Type":"application/json"}
host = "https://192.168.3.136"
endpoint = "/redfish/v1/SessionService/Sessions"
"""
curl -k -u Administrator:Admin@9000 -X POST https://192.168.3.136/redfish/v1/SessionService/Sessions
-H  'Content-Type:application/json' -d '{"UserName":"Administrator","Password":"Admin@9000"}'

{"@odata.context":"/redfish/v1/$metadata#Session.Session",
 "@odata.id":"/redfish/v1/SessionService/Sessions/875dea3cc7b58f90",
 "@odata.type":"#Session.v1_0_2.Session","Id":"875dea3cc7b58f90","Name":"User Session","Oem":{"Huawei":{"UserAccount":"Administrator",
                 "LoginTime":"2024-04-24T05:50:16+00:00","UserId":2,"UserValidDays":null,
        "AccountInsecurePromptEnabled":false,"UserIP":"192.168.3.110","UserTag":"Redfish","MySession":true,"UserRole":["Administrator"]}}}
"""
url = host +endpoint
response = session.post(url,data=data, headers=header,verify=False)
# response.status_code = 201 创建会话成功
print(response.status_code)
# pdb.set_trace()
header['X-Auth-Token'] = response.headers['X-Auth-Token']
print(header['X-Auth-Token'])
# system_request = host + '/redfish/v1/Systems/1/Memory'
mem_url = host + '/redfish/v1/Systems/1/Memory/mainboardDIMM000'
rsp = session.get(mem_url,headers=header)
pdb.set_trace()
