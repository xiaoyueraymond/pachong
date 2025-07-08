import requests
import argparse
import json


parser = argparse.ArgumentParser(description='chat with AI).')
parser.add_argument('-m', '--message', dest='message', default='helllo world',
                    help='specify the usernane to use to access the iBMC')
# parser.add_argument('-P', '--PASS', dest='password', default='admin#254',
#                     help='specify the password to use to access the iBMC')
# parser.add_argument('-H', '--host', dest='host', default='192.168.3.116',
#                     help='specify the IP Address or hostname of the target iBMC,default ip is 192.168.2.100')
args = parser.parse_args()

mykey = 'eNIJmUsdUvsrwV0XFhAvewVLhDJbCAHp'
url = 'https://apikey.net/api/ai/index'
headers = {
    "Content-Type":"application/x-www-form-urlencoded;charset:utf-8;",
}
data = {
    "key": mykey,
    "message": args.message
}
responce = requests.post(url,headers=headers,data=data)

result =responce.json()
print (result)
