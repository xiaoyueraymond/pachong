#
#
import myformat as mf
import paramiko
import argparse
import os
import sys
import logging
from mytools import *
from pathlib import Path
import pdb
import shutil

#
# cmdline parameters
parser = argparse.ArgumentParser(description='Query  information from the xFusion iBMC ).')
parser.add_argument('-U', '--USER', dest='username', default='Administrator',
                    help='specify the usernane to use to access the iBMC')
parser.add_argument('-P', '--PASS', dest='password', default='Admin@9000',
                    help='specify the password to use to access the iBMC')
parser.add_argument('-H', '--host', dest='host', default='192.168.2.100',
                    help='specify the IP Address or hostname of the target iBMC')
args = parser.parse_args()

#
if os.environ.get('enable_debug'):
    print(args)
#
if os.name == 'nt':
    logdir = 'c:\\'
elif os.name == 'posix':
    logdir = '/tmp/'
else:
    msg = '无法判断系统，请联系开发者检查'
    print(msg)
#
log_diag_dir = logdir + 'dump_info'
logfile = logdir + 'xfusion.log'
time_str = get_datetime_str()
fp = Path(logfile)
new_logfile = False
# print(time_str)
if Path.exists(fp):
    new_log_filename = 'xFusion_' + time_str
    fp.rename(fp.with_name(new_log_filename))
    new_logfile = True
    # print(new_log_file)


def backup_file(sn):
    dest_file = logdir + 'xFusion_' + sn + '.log'
    dest = 'xFusion_' + sn + '.log'
    dest_fp = Path(dest_file)
    if Path.exists(dest_fp):
        dest_new_name = 'xFusion_' + sn + '_' + time_str + '.log'
        dest_fp.rename(dest_fp.with_name(dest_new_name))
        msg = f"目标文件存在，用时间戳作为标记备份为{dest_new_name}"
        mf.display(msg)
    # pdb.set_trace()
    if os.name == 'nt':
        shutil.copy(fp, dest_fp)
    elif os.name == 'posix':
        fp.rename(fp.with_name(dest))
    mf.display(f"backup 此次测试的日志文件为{dest} ")


def download_diag(sn):
    """
    get the diag file from BMC　/tmp
    sshpass -f /tmp/password  scp Administrator@192.168.3.129:/tmp/dump_info.tar.gz .
    """
    dfile = logdir + 'xFusion_DIAG_' + sn + '.tgz'
    fp = Path(dfile)
    if Path.exists(fp):
        new_file = 'xFusion_DIAG_' + sn + '_' + time_str + '_' + '.tgz'
        fp.rename(fp.with_name(new_file))
        msg = f"当前目录有DIAG文件 {dfile}存在，重命名为{new_file}"
        mf.display(msg)
    transport = paramiko.Transport((args.host, 22))
    transport.connect(username=args.username, password=args.password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get('/tmp/dump_info.tar.gz', dfile)
    sftp.close()
    transport.close()


#
loglevel = logging.INFO
setup_logger(logfile)

#
#
if new_logfile:
    msg = "日志文件 {} 已存在，将重命名为   ***\t\033[31m{}\t***\033[0m".format(logfile, new_log_filename)
    mf.display(msg)

#
msg = "开始从服务器中读取数据"
mf.display(msg)


class xFusion_BMC():
    """
    """

    def __init__(self, args):
        self.username = args.username
        self.password = args.password
        self.host = args.host
        msg = f"使用下面参数进行连接xFusion BMC 服务器：\t  主机名:  {self.host} \t用户名:\t{self.username}\t密码:\t{self.password}"
        mf.display(msg)
        self.client = self.get_client()
        self.data = {}
        # will log the SN　via fruinfo
        #
        self.SN = self.run_cmd('ipmcget -d serialnumber', 'SN').split(':')[1].strip()
        # self.version = self.run_cmd('ipmcget -d version', 'version')
        # self.pdinfo = self.get_pdinfo()
        # self.fru = self.run_cmd('ipmcget -d fruinfo', 'fru')
        # self.controller = self.run_cmd('ipmcget -t storage -d ctrlinfo -v all', 'controller')
        # self.macaddr = self.run_cmd('ipmcget -d macaddr', 'macaddr')
        # self.ethport = self.run_cmd('ipmcget -d ethport', 'ethport')
        # self.health = self.run_cmd('ipmcget -d health', 'health')
        self.get_diaginfo()

        # pdb.set_trace()

    #
    # 
    def get_client(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.username, password=self.password, allow_agent=False,
                            look_for_keys=False)
        return self.client

    ##
    ##
    def run_cmd(self, cmd, key=False):
        """
        """

        stdin, stdout, stderr = self.client.exec_command(cmd)
        err = stderr.read().decode('utf-8')
        if err:
            msg = "发现错误执行命令{cmd},请排查"
            logging.warning(msg)
        else:
            msg = stdout.read().decode()
            #
            if msg and key:
                for line in msg.splitlines():
                    mf.display(line)

            #
            if key:
                self.data[key] = msg
        stdin.close()
        return msg

    def get_version(self):
        """
        get version form

        """

    # def get_sn(self):
    #     """
    #     """
    #     if self.data.get('fru', None):
    #         info = self.data.get('fru')
    #         for line in info.splitlines():
    #             if '' in line:
    #                 sn = line.split(':')[1]
    #                 logging.info(sn)
    #     else:
    #         info = self.run_cmd('ipmcget -d fruinfo', 'fru')
    #         for line in info.splitlines():
    #             if 'Product Serial Number' in line:
    #                 sn = line.split(':')[1]
    #                 msg = f"SN:{sn}"
    #                 logging.info(msg)
    #     return sn.strip()
    #
    def get_pdinfo(self):
        """
        ipmcget -t storage  -d pdinfo -v all
        """
        cmd = 'ipmcget -t storage  -d pdinfo -v all'
        pdinfo = self.run_cmd(cmd, 'pdinfo')
        return pdinfo

    def get_diaginfo(self):
        msg = "get the diag info"
        mf.display(mf.create_section(msg))
        mf.display("Diag info download may take a few minutes ,please wait...")
        self.run_cmd('ipmcget -d diaginfo')


class Parse_Diag:
    """
    1 :解压文件
    2： 分析CPU 信息： logdir + dump_info/AppDump/CpuMem/cpu_info
    3： 分析内存信息：  logdir + dump_info/AppDump/CpuMem/mem_info
    4： 分析PSU信息：  logdir + dump_info/AppDump/BMC/psu_info.txt

    dfile = logdir + 'xFusion_DIAG_' + sn + '.tgz'
    """

    def __init__(self, file):

        # 先清空目录
        diag_path = Path(log_diag_dir)
        if Path.exists(diag_path):
            msg = "解压目录已存在，准备清空..."
            mf.display(msg)
            # pdb.set_trace()
            # set_permissions(log_diag_dir)
            # linux rhels9.3 不支持onexc
            # shutil.rmtree(dir, onexc=handler) but the onexc kwarg was only introduced in Python 3.12!
            #shutil.rmtree(log_diag_dir, onexc=remove_readonly)
            shutil.rmtree(log_diag_dir, onerror=remove_readonly)
            # pdb.set_trace()
            msg = "目录已清空"
            mf.display(msg)
            #

        diag_file = Path(file)
        if Path.exists(diag_file):
            extract_tar_gz(file, logdir)
            # extract_tar_gz(filename, extract_directory)

        else:
            msg = f"找不到Diag 文件：{file} ,强制退出 ... "
            mf.display(msg)
            sys.exit(1)

        #
        self.parse_cpu()
        self.parse_mem()
        self.parse_psu()

    # def extract_file(self):
    #     pass

    def parse_cpu(self):
        cpu_file = logdir + 'dump_info/AppDump/CpuMem/cpu_info'
        with open(cpu_file, 'r') as fh:
            mf.display(mf.create_section(" Check CPU　Info "))
            # mf.display(mf.create_section(msg))
            lines = fh.readlines()
        #
        header = ['Slot', 'version', 'core count', 'thread count', 'processor ID']
        cpus = []
        for line in lines:
            if line.startswith('Cpu') and 'present' in line:
                info = line.split(',')
                cpus.append([info[0], info[2], info[4], info[5], info[3]])
        tables = mf.create_table(header, cpus)
        mf.display(tables)

    def parse_mem(self):
        """
        'slot(col 1), dimm location(col 2), dimm name(col 3),manufacturer(col 4),
          size(col 5), speed(col 6), current speed(col 7), memory type(col 8), SN(col 9),
           minimum voltage(col 10), rank(col 11), bit width(col 12), memory technology(col 13),
             bom number(col 14), part number(col 15),remaining service life(col 16),
                firmware version(col 17), medium temp(col 18), controller temp(col 19),
                   volatile capacity(col 20), persistent capacity(col 21)), health(col 22)  \n',
                   'Memory000 , mainboard, DIMM000, Hynix,  32768 MB,  2933 MHz,  2666 MHz, DDR4, 20012922,
                    1200 mV, 2 rank, 72 bit, Synchronous| Registered (Buffered), N/A,
                    HMA84GR7JJR4N-WM, Unknown, N/A, Unknown, Unknown, Unknown, Unknown, OK\n',
        """

        mem_file = logdir + 'dump_info/AppDump/CpuMem/mem_info'
        with open(mem_file, 'r') as fh:
            mf.display(mf.create_section(" Check Memory Info "))
            # mf.display(mf.create_section(msg))
            lines = fh.readlines()
        #
        header = ['Slot', 'manufacturer', 'Size', 'Speed', 'current speed','Type','SN', 'PN']
        mems = []
        # pdb.set_trace()
        for line in lines:
            if line.startswith('Memory') and ('NO DIMM' not in line):
                info = line.split(',')
                mems.append([info[2], info[3], info[4], info[5], info[6],info[7], info[8], info[14]])
        tables = mf.create_table(header, mems)
        mf.display(tables)
        # pdb.set_trace()

    def parse_psu(self):
        """
        $ cat /c/dump_info/AppDump/BMC/psu_info.txt
Slot   |  presence  |  Manufacturer     |  Type                              |  SN                                |  Version                    |  Rated Power   |  InputMode  |  PartNum           |  DeviceName        |  Vin
1      |  present   |  Huntke           |  PAC900S12-BW                      |  2102131725AAMA011891              |  DC:131 PFC:131             |  900           |  N/A       |  02131725          |  PSU1              |  0.00
2      |  present   |  Huntke           |  PAC900S12-BW                      |  2102131725AAMA011905              |  DC:131 PFC:131             |  900           |  AC        |  02131725          |  PSU2              |  240.00

        """
        psu_file = logdir + 'dump_info/AppDump/BMC/psu_info.txt'
        with open(psu_file, 'r') as fh:
            mf.display(mf.create_section(" Check PSU Info "))
            # mf.display(mf.create_section(msg))
            lines = fh.readlines()
        #
        header = ['Slot', 'manufacturer', 'type', 'SN', 'Version', 'Rated Power', 'PN']
        psus = []
        # pdb.set_trace()
        for line in lines:
            if  'PSU'  in line:
                info = line.split('|')
                psus.append([x.strip() for x in [info[9], info[2], info[3], info[4], info[5], info[6], info[8]]])
        tables = mf.create_table(header,  psus)
        mf.display(tables)



my_xfusion = xFusion_BMC(args)
msg = "开始处理数据"
mf.display(msg)
msg = "最后一步，将日志文件以服务器的流水号保存"
mf.display(msg)
# pdb.set_trace()
sn = my_xfusion.SN
# backup_file(sn)
download_diag(sn)
# xFusion_DIAG_2106196LTVXDP4000127.tgz
# sn = '2106196LTVXDP4000127'
log_diag_file = logdir + 'xFusion_DIAG_' + sn + '.tgz'
Parse_Diag(log_diag_file)
backup_file(sn)


sys.exit(0)
"""
# 创建 SSH 客户端
client = paramiko.SSHClient()
# 自动添加主机密钥 (不写这个可能会报错找不到主机)
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接到远程服务器
client.connect('192.168.3.129', username=args.username, password=args.password, allow_agent=False, look_for_keys=False)
# 参数说明：
# - hostname: 远程主机的IP地址或域名
# - username: 用于SSH连接的用户名
# - password: 用于SSH连接的密码
# - allow_agent: 是否允许使用代理验证，默认为False
# - look_for_keys: 是否在本地寻找私钥文件，默认为False
# 执行命令
print('#' * 50)
stdin, stdout, stderr = client.exec_command('ipmcget -d version')

print(stdout.read().decode())
#stdin,stdout,stderr = client.exec_command('ipmcget -t storage -d pdinfo -v all')
stdin,stdout,stderr = client.exec_command('ipmcget  -d fruinfo')
print('#' * 50)
msg = stdout.read().decode()
mf.display(msg)
mf.display(mf.create_section(msg))
stdin.close()
# 关闭连接
try:
    client.close()
except:
    pass
"""
