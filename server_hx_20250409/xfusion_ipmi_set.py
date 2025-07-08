import argparse
import time

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
# parser.add_argument('-p', '--port', dest='port', default='443',
#                     help='specify the port to the target iBMC, default is 443')
# parser.add_argument('--raw_start', type=str,
#                     help='raw start strings')
# parser.add_argument('--raw_end', nargs='?', default=None,
#                     help='raw end strings')
# # parser.add_argument("-e", '--enable', dest='enable', action='store_true',
# #                     help="enable the value change accordingly ,like for 0 ,to 5")
#
# parser.add_argument('--var', nargs="+", default=None,
#                     help='1 or 4 valid int for test with ipmi run')
#
# # parser.add_argument('--var1',nargs="+", default=None,
# #                     help="3 valid int for test with ipmi run")

parser.add_argument("--set_fan_mode", dest='set_fan_mode', nargs='?', choices=['auto', 'manual'], default=None,
                    help="set the fan speed to manual mode")
parser.add_argument("--get_fan_mode", dest='get_fan_mode', action='store_true', default=None,
                    help="get the fan speed to manual mode")
parser.add_argument("--set_fan_ratio", nargs='?', default=None, help="set the Fan speed x percentage ")
parser.add_argument("--recovery_point", action="store_true", default=None,
                    help="set the recovery point so load default can back to this state ")

# def check_args(args):
#     if args.var1 and args.var:
#         raise argparse.ArgumentError("参数var1和var不能同时使用。")
#     return args
# ##
# parser.set_defaults(func=check_args)
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
logfile = logdir + 'fan.log'
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

class Fan:
    def __init__(self, args):
        self.host = args.host
        # self.port = args.port
        self.username = args.username
        self.password = args.password
        self.error_log = error_logfile
        # self.url = 'https://' + self.host + ':' + self.port
        self.cmd_start = f"ipmitool  -I lanplus -H {args.host} -U {args.username} -P {args.password}   -C17  raw "

    def get_fan_mode(self):
        fan_mode = {'00': '自动模式', '01': '手动模式'}
        cmd = self.cmd_start + " 0x30 0x91 0x14 0xe3 0x00 0x02"
        rsp = run(cmd.split())
        mode = rsp.split()[3].strip()
        msg = f" 当前的风扇模式是{fan_mode[mode]}"
        mf.display(msg)
        if mode == '01':
            delta_time = rsp.split()[4:8]
            a_time = ''.join([i for i in delta_time[::-1]]).strip()
            int_time = int(a_time, 16)
            mf.display(f"这个模式还有{int_time}秒就会失效")
        else:
            msg = "当前模式为自动模式，默认不会失效"
            mf.display(msg)

    def set_fan_mode(self, mode=None):
        fan_mode = {"auto": '0x00', "manual": '0x01'}
        if args.set_fan_mode:
            mode = args.set_fan_mode
        elif mode:
            mode = mode

        msg = f"设置风扇模式为{mode}模式"
        mf.display(msg)

        cmd = self.cmd_start + f" 0x30 0x91 0x14 0xe3 0x00 0x01 {fan_mode[mode]} 0xff 0xff 0xff 0xff"
        rsp = run(cmd.split())
        time.sleep(1)
        self.get_fan_mode()

    def set_fan_ratio(self):
        msg = f"设置风扇模式为手动模式"
        mf.display(msg)
        self.set_fan_mode('manual')
        time.sleep(0.5)
        msg = f"设置风扇转速百分比为: {args.set_fan_ratio}%"
        mf.display(msg)
        cmd = self.cmd_start + f"   0x2c 0x15 0x01 0x00  {args.set_fan_ratio} "
        rsp = run(cmd.split())
        time.sleep(1)
        self.get_fan_mode()

    def get_fan_speed(self):
        msg = "读取风扇速度中..."
        cmd = self.cmd_start + f"0x30 0x93 0x14 0xe3 0x00 0x38 0x26 0x00 0x01 0xff 0x00 0x00 0x06 0x00"
        rsp = run(cmd.split())
        fan_rsp = rsp.split()[4:]
        fan_count = len(fan_rsp) // 6
        mf.display(f"我们读到了{fan_count}个风扇的数据")
        fans_data = [fan_rsp[(i + 0) * 6:(i + 1) * 6] for i in range(fan_count)]
        # 取每组数据的最后2位构成转速
        #
        for i in range(fan_count):
            msg1 = f"这是第{i + 1}个风扇的数据：\t"
            data = fans_data[i]
            fanSpeed = int((data[-1] + data[-2]), 16)
            msg2 = ""
            msg = msg1 + f" {fanSpeed} RPM"
            if fanSpeed == 0:
                msg2 = "\33[31m       ***风扇可能安装错或者没有安装，请检查*****\033[0m "
                msg = msg + msg2

            mf.display(msg)

    def recovery_point(self):
        """ set the bmc as a snapshot point ,so when load default ,it will be back to this state"""
        cmd = self.cmd_start + "  0x30 0x93 0x14 0xe3 0x00 0x07 0x00 0xaa"
        rsp = run(cmd.split())
        if "14 e3 00 01" in rsp:
            msg = "成功设置还原点了"
            mf.display(msg)
        else:
            msg = "设置还原点异常了:  " + str(rsp)
            mf.display(msg)

    def main(self):
        if args.get_fan_mode:
            self.get_fan_mode()
        elif args.set_fan_mode:
            self.set_fan_mode(mode=args.set_fan_mode)
        elif args.set_fan_ratio:
            self.set_fan_ratio()
        elif args.recovery_point:
            self.recovery_point()
        self.get_fan_speed()


if __name__ == "__main__":
    myfan = Fan(args)
    myfan.main()
