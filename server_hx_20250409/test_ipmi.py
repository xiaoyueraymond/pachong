import argparse
import sys

from mytools import *

##
##
# cmdline parameters
parser = argparse.ArgumentParser(description='Query  information from the xFusion iBMC ).')
parser.add_argument('-U', '--USER', dest='username', default='Administrator',
                    help='specify the username to use to access the iBMC')
parser.add_argument('-P', '--PASS', dest='password', default='Admin@9000',
                    help='specify the password to use to access the iBMC')
parser.add_argument('-H', '--host', dest='host', default='192.168.0.94',
                    help='specify the IP Address or hostname of the target iBMC,default ip is 192.168.89.109')
parser.add_argument('-p', '--port', dest='port', default='443',
                    help='specify the port to the target iBMC, default is 443')
parser.add_argument('--raw_start', type=str,
                    help='raw start strings')
parser.add_argument('--raw_end', nargs='?', default=None,
                    help='raw end strings')
# parser.add_argument("-e", '--enable', dest='enable', action='store_true',
#                     help="enable the value change accordingly ,like for 0 ,to 5")

parser.add_argument('--var', nargs="+", default=None,
                    help='1 or 4 valid int for test with ipmi run')

# parser.add_argument('--var1',nargs="+", default=None,
#                     help="3 valid int for test with ipmi run")

def check_args(args):
    if args.var1 and args.var:
        raise argparse.ArgumentError("参数var1和var不能同时使用。")
    return args
##
parser.set_defaults(func=check_args)
args = parser.parse_args()

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
logfile = logdir + 'impi_test.log'
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
mylogger(logfile)
wrong_value = 0
if args.var:
    if 1 <= len(args.var) <= 4:
        mf.display(f"we are expect to have 1 to 4 variables ,and we get {len(args.var)}")
    else:
        mf.display(f"we are expect to have 1 to 4 variables ,and we get {len(args.var)}")
        sys.exit(1)

    for i in args.var:
        if not i.isdigit():
            msg = f"expect the int value ,but we get {type(i)}"
            mf.display(msg)
            wrong_value = 1
# pdb.set_trace()

# if args.var1:
#     if len(args.var1) != 3:
#         mf.display(f"var1 expect to 3 values ,but we get {len(args.var1)} ")
#         sys.exit(2)
#     for i in args.var1:
#         if not i.isdigit():
#             msg = f"expect the int value ,but we get {type(i)}"
#             mf.display(msg)
#             wrong_value = 1

if wrong_value:
    sys.exit(2)

# 电源 0x30 0x93 0x14 0xe3 0x00 0x36 0x27 0x00 0x01 0xff 0x00 0x00 0x0c 0x00 0x79 0x01 0x01 0x14 0x00
cmd_start = f"ipmitool  -I lanplus -H {args.host} -U {args.username} -P {args.password}   -C17  raw " + args.raw_start + " "
if args.var:
    if len(args.var) == 1:
        cmds = [f" {i}  " for i in range(int(args.var[0]))]
    elif  len(args.var) == 2:
            cmds = [f" {i} {j}  " for i in range(int(args.var[0])) for j in
                    range(int(args.var[1]))]
    elif  len(args.var) == 3:
        cmds = [f" {i} {j} {k}  " for i in range(int(args.var[0])) for j in
                range(int(args.var[1])) for k in range(int(args.var[2]))]
    elif  len(args.var) == 4:
        cmds = [f" {i} {j} {k}  " for i in range(int(args.var[0])) for j in
                range(int(args.var[1])) for k in range(int(args.var[2])) ]
    else:
        cmds = [f" {i} {j}  {k}  {l} " for i in range(int(args.var[0])) for j in
                range(int(args.var[1])) for k in range(int(args.var[2]))  for l in range(int(args.var[3]))]

else:
    cmds = [" ", ]

for cmd in cmds:
    try:
        # print(cmd)
        if args.raw_end:
            cmd = cmd_start + cmd + args.raw_end
        else:
            cmd = cmd_start + cmd
        #
        rsp = run_only(cmd.split())
        msg = f"当前运行的命令是{cmd}"
        mf.display(msg)
        msg1 = f"当前的运行结果是{rsp}"
        if "0x30 0x93 0x14 0xe3 0x00 0x5e 0x00 0x00" in cmd:
            msg = "parse the NIC port with BDF info"
            mf.display(msg)
            data = rsp.split()[6:]
            x1_len = int(data[0], 16)
            x1_data = data[1:x1_len + 1]
            x2_len = int(data[x1_len + 1], 16)
            x2_data = data[x1_len + 2:x1_len + 2 + x2_len]
            x3_len = int(data[x1_len + 2 + x2_len], 16)
            x3_data = data[x1_len + 2 + x2_len + 3:x1_len + 3 + x2_len + x3_len]
            x4_len = int(data[x1_len + 3 + x2_len + x3_len], 16)
            x4_data = data[x1_len + x2_len + x3_len + 4:x1_len + x2_len + x3_len + x4_len + 4]
            x5_len = int(data[x1_len + x2_len + x3_len + x4_len + 4], 16)
            x5_data = data[x1_len + x2_len + x3_len + x4_len + 5:x1_len + x2_len + x3_len + x4_len + x5_len + 5]
            x6_len = int(data[x1_len + x2_len + x3_len + x4_len + x5_len + 5], 16)
            x6_data = data[
                      x1_len + x2_len + x3_len + x4_len + x5_len + 6:x1_len + x2_len + x3_len + x4_len + x5_len + x6_len + 5]

            data1 = ''.join([chr(int(i, 16)) for i in x1_data])
            data2 = ''.join([chr(int(i, 16)) for i in x2_data])
            data3 = ''.join([chr(int(i, 16)) for i in x3_data])
            data4 = ''.join([chr(int(i, 16)) for i in x4_data])
            data5 = ''.join([chr(int(i, 16)) for i in x5_data])
            data6 = ':'.join(x6_data)
            msg1 = "网卡名称：" + data1
            msg2 = "网卡丝印名：" + data2
            msg3 = "网卡父BDF信息" + data3
            msg4 = "网卡自己的BDF信息" + data4
            msg5 = "网卡端品名称：" + data5
            msg6 = "网卡MAC地址：" + data6
            mf.display(msg1)
            mf.display(msg2)
            mf.display(msg3)
            mf.display(msg4)
            mf.display(msg5)
            mf.display(msg6)
        else:
            mf.display(msg1)
            msg2 = "当前的解析结果是：" + ''.join([chr(int(i, 16)) for i in rsp.split()[1:]])
            mf.display(msg2)
            mf.display('\n\n ')
    except:
        pass
