#
import argparse
import pdb
import time

from redfish import redfish_client

from cnit_config_detail import *
from mytools import *

##
##
# cmdline parameters
parser = argparse.ArgumentParser(description='Query  information from the CNIT BMC ).')
parser.add_argument('-U', '--USER', dest='username', default='Administrator',
                    help='specify the username to use to access the iBMC')
parser.add_argument('-P', '--PASS', dest='password', default='Admin@9000',
                    help='specify the password to use to access the iBMC')
parser.add_argument('-H', '--host', dest='host', default='192.168.1.254',
                    help='specify the IP Address or hostname of the target iBMC,default ip is 192.168.89.109')
parser.add_argument('-p', '--port', dest='port', default='443',
                    help='specify the port to the target iBMC, default is 443')

args = parser.parse_args()
##
## 帐号信息： sshpass -p 0penBmc ssh root@192.168.0.48 云尖BMC的SSH信息
datestr = get_date_str()
if os.name == 'nt':
    if os.path.exists("d:"):
        logdir = f'd:\\logs\\{datestr}\\'
        logrootdir = f'd:\\logs\\'
    else:
        logdir = f'c:\\logs\\{datestr}\\'
        logrootdir = f'c:\\logs\\'
elif os.name == 'posix':
    logdir = f'/tmp/{datestr}/'
    logrootdir = f'/tmp/'
else:
    msg = 'Can not determine the system arch, please contact the Developer for help'
    print(msg)
    raise Exception(msg)
#
if not os.path.exists(logdir):
    os.makedirs(logdir)
    msg = f" {logdir} not exist ,now create it "
    mf.display(msg)
log_diag_dir = logdir + 'dump_info'
logfile = logdir + 'cnit_redfish.log'
sn_logfile = logrootdir + 'sn_list.txt'
error_logfile = logrootdir + 'validate_errors.log'
if not os.path.exists(sn_logfile):
    with open(sn_logfile, 'w') as file:
        pass

if not os.path.exists(error_logfile):
    with open(error_logfile, 'w') as file:
        pass
#
cmd = f"echo 123456 >{logfile}"
os.system(cmd)
loglevel = logging.INFO
logging.getLogger("redfish").setLevel(logging.CRITICAL)
setup_logger(logfile)

elabelGetCmd = {
    "ProductAssetTag":       " raw 0x30 0x90 0x5 0x0 0x3 0x5 0x0 ",
    "ProductName":           " raw 0x30 0x90 0x5 0x0 0x3 0x1 0x0 ",
    "ProductSerialNumber":   " raw 0x30 0x90 0x5 0x0 0x3 0x4 0x00 ",
    "DeviceSerialNumber":    " raw 0x30 0x90 0x5 0x0 0x6 0x3 0x00 ",
    "DeviceName":            " raw 0x30 0x90 0x5 0x0 0x6 0x1 0x00 ",
    "ChassisPartnumber":     " raw 0x30 0x90 0x5 0x0 0x1 0x1 0x0 ",
    "ChassisType":           " raw 0x30 0x90 0x5 0x0 0x1 0x0 0x0 ",
    "IOChassisSerialNumber": " raw 0x30 0x90 0x5 0x1 0x3 0x4 0x00 ",
    "IOChassisAssetTag":     " raw 0x30 0x90 0x5 0x1 0x3 0x5 0x0 ",

}
#  0x30 0x90 0x05 0x00 0x03 0x04 0x00 0x20
for command in elabelGetCmd.keys():
    cmd = f"ipmitool  -I lanplus  -H {args.host} -U {args.username} -P {args.password}  " +elabelGetCmd[command] + " 0x30"
    mycmd = cmd.split()
    rsp = run(mycmd)
    mf.display(rsp)
    mf.display(command)
    msg = ''.join([chr(int(a,16) ) for a in rsp.split()[1:]])
    mf.display(msg)
    mf.display('*******************')



