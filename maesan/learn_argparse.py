import argparse

parser = argparse.ArgumentParser(description='Query  information from the CNIT BMC ).')
parser.add_argument('-U', '--USER', dest='username', default='admin',
                    help='specify the username to use to access the iBMC')
parser.add_argument('-P', '--PASS', dest='password', default='admin#254',
                    help='specify the password to use to access the iBMC')
parser.add_argument('-H', '--host', dest='host', default='192.168.1.254',
                    help='specify the IP Address or hostname of the target iBMC,default ip is 192.168.89.109')
parser.add_argument('-p', '--port', dest='port', default='443',
                    help='specify the port to the target iBMC, default is 443')

args = parser.parse_args()
print(args)

# PS D:\python> & C:/Users/musk8/AppData/Local/Programs/Python/Python311/python.exe d:/python/maesan/learn_argparse.py -U 132465
# Namespace(username='132465', password='admin#254', host='192.168.1.254', port='443')