import os
import stat
import subprocess
import logging
import sys
import pdb
import datetime
import tarfile
import myformat as mf

loglevel = logging.INFO
mtsn_dir = '/dfcxact/mtsn'


#
class DMIDevice(dict):
    """ Base class for a DMI device

    This object is basically a dictionary
    """

    def __init__(self, handle, type_, size, description=''):
        super().__init__()
        assert isinstance(handle, int), \
            'Argument for handle must be an int'
        assert isinstance(type_, int), \
            'Argument for type_ must be an int'
        assert isinstance(size, int), \
            'Argument for size must be an int'
        self.handle = handle
        self.type = type_
        self.size = size
        self.description = description


def run_only(cmd):
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
                              universal_newlines=True).stdout
    except subprocess.CalledProcessError as e:
        msg = "命令执行失败，请忽略:" + ' '.join(cmd) 
        logging.debug(msg)
        #logging.exception(e.stderr)
        sys.exit(1)

def run(cmd):
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
                              universal_newlines=True).stdout
    except subprocess.CalledProcessError as e:
        logging.exception(e.stderr)
        sys.exit(1)


#

def get_datetime_str():
    """
    """
    now = datetime.datetime.now()
    timefrm = now.strftime('%Y_%m_%d_%H%M%S')
    return timefrm


def get_date_str():
    """
    """
    now = datetime.datetime.now()
    timefrm = now.strftime('%Y_%m_%d')
    return timefrm


#


def set_permissions(directory):
    # 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        # 修改目录权限
        os.chmod(root, 0o777)  # 设置读写权限（以八进制表示）

        # 修改子目录权限
        for d in dirs:
            dir_path = os.path.join(root, d)
            os.chmod(dir_path, 0o777)  # 设置读写权限（以八进制表示）


def remove_readonly(func, path, _):  # 定义回调函数

    os.chmod(path, stat.S_IWRITE)  # 删除文件的只读属性

    func(path)  # 再次执行删除操作


def extract_tar_gz(filename, extract_directory):
    with tarfile.open(filename, 'r:gz') as tar:
        tar.extractall(extract_directory)


def get_mtsn():
    """
    read the mtsn from environment variables or setup the mtsn var 
    """
    if not os.environ.get('MTSN', None):
        MTSN = mtsn_dir + '/' + run(['dmidecode', '-s', 'system-serial-number']).strip()
    else:
        MTSN = os.environ.get('MTSN')
    #
    cmd = ['mkdir', '-p', MTSN]
    run(cmd)
    #
    return MTSN


def get_testlog_file():
    mtsn = get_mtsn()
    logfile = mtsn + '/tester.log'
    return logfile


#
def setup_logger(log_file):
    # 配置日志处理程序
    time_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=loglevel,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt=time_format,
                        handlers=[
                            logging.StreamHandler(),  # 终端处理程序
                            logging.FileHandler(log_file)  # 文件处理程序
                        ])


def mylogger(logfile):
    # logfile = get_testlog_file()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s  \t %(levelname)s \t  %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # only record info level log
    file_handler1 = logging.FileHandler('/root/default_info.log')
    file_handler1.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s  \t %(levelname)s \t  %(message)s')
    file_handler1.setFormatter(formatter)
    logger.addHandler(file_handler1)
    #
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def get_dmi_info(_type=None):
    """
    get all  dmi device list by defautl 
    if _type is specify with int or type ,then get the type info
    """
    mtsn = get_mtsn()
    if not _type:

        command = ['dmidecode']
        content = run(command)
        dmilog = get_mtsn() + '/dmi.log'
        with open(dmilog, 'w') as dmilog:
            dmilog.write(content)
    else:
        command = ['dmidecode', '-t', '{}'.format(_type)]
        content = run(command)

    #
    # start to parse the dmilog content 
    dmidecode_level = None
    smbios_level = None
    table_location = None
    number_of_structures = None
    records = []
    record = None
    #
    #
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('# dmidecode'):
            dmidecode_level = line[len('# dmidecode'):].strip()
        elif line.startswith('SMBIOS'):
            smbios_level = line[len('SMBIOS'):].strip().split(None, 1)[0]
        elif line.startswith('Table at'):
            table_location = int(line[len('Table at'):-1].strip(), 16)
        elif line.startswith('Getting SMBIOS data') or line.startswith(
                '# SMBIOS implementations newer') or line.startswith('# fully supported by'):
            continue
        elif line.startswith('Handle'):
            items = line.split(',')
            handle = int(items[0].strip().split(None, 1)[1], 16)
            type_ = int(items[1].strip().split(None, 2)[2], 10)
            size = int(items[2].strip().split(None, 1)[0], 10)

            record = DMIDevice(handle=handle, type_=type_, size=size)
        elif ':' in line:
            key, value = line.split(':', 1)
            record[key.strip()] = value.strip()
        # 一个记录的结束就是窄行
        elif not line:
            """
            if record:
                if record.type == 17:
                    record['nLocator'] = normalize_mem_locator(record, flavor=flavor)
                elif record.type == 9:
                    record['nDesignation'] = normalize_pci_locator(record)
                elif record.type == 41 and record.get('Type', None) == 'Ethernet':
                    record['nDesignation'] = 'PHY:{}'.format(record['Reference Designation'])
                    record['Current Usage'] = 'In Use' if record['Status'] == 'Enabled' else record['Status']

                    if hasattr(ProductDMI, 'normalize_ethernet_record'):
                        # normalize_ethennet_record returns True to keep the record
                        if not ProductDMI.normalize_ethernet_record(record):
                            continue
            """
            if record:
                ## 排除dmidecode 头部信息 与 handle 之间的空行
                records.append(record)
            record = None
        elif record is not None:
            ## keep appending lines that don't match anything else
            record.description += line

    return records


def get_pci_info(_bus):
    """
    _bus : '0000:81:00.1'
    """
    if _bus.startswith('0000:'):
        bus = _bus[5:]
    else:
        bus = _bus
    result = run(['lspci', '-vvv', '-s', bus])

    bus_dict = {}
    for line in result.splitlines():
        if bus in line:
            bus_dict[line.split(':')[1][4:].strip()] = line.split(':')[2].strip()
        else:
            if ":" not in line:
                continue
            k, v = line.split(':', 1)
            if 'Capabilities' in k and bus_dict.get(k, None):
                bus_dict[k.strip()] = bus_dict[k] + '\n' + v.strip()
            else:
                bus_dict[k.strip()] = v.strip()
    # pdb.set_trace()
    return bus_dict


def filter_contents(cmd, filter_content):
    """
    run cmd and get the resutl,then filter the content by keyword
    lspci ,QLogic
    """
    result = []
    content = run(cmd)
    for line in content.splitlines():
        if filter_content in line:
            result.append(line)

    return result


def get_mem_info():
    """
    BYD　example:
    # dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 3.6.0 present.
# SMBIOS implementations newer than version 3.5.0 are not
# fully supported by this version of dmidecode.

Handle 0x0042, DMI type 17, 92 bytes
Memory Device
        Array Handle: 0x0041

    """
    mem_installed = []
    result = get_dmi_info(17)
    for item in result:
        if 'Installed' not in item['Size']:
            mem_installed.append(item)
    return mem_installed


def get_cpu_info():
    cpu_info = []
    result = get_dmi_info(4)
    return result


def log_line(message=None, _type=True):
    if _type:
        logging.info("")
        msg = "Start " + message
        msg = msg.center(60, '-')
        logging.info(msg)
    else:

        msg = 'End'.center(60, '-')
        logging.info(msg)
        logging.info("")


def get_ocp_info():
    """
    Handle 0x0198, DMI type 41, 11 bytes
Onboard Device
        Reference Designation: Onboard OCP2 Port 1
        Type: Ethernet
        Status: Enabled
        Type Instance: 6
        Bus Address: 0000:81:00.1

    """
    ocp_info = []
    result = get_dmi_info(41)
    ocp_info = [item for item in result if item['Type'] == "Ethernet"]
    for item in ocp_info:
        pci_info = get_pci_info(item['Bus Address'])
        # pdb.set_trace()
        item['Physical Slot'] = pci_info['Physical Slot'] if pci_info.get('Physical Slot', None) else "LOM card"
        item['LnkSta'] = pci_info['LnkSta']
        item['Product Name'] = pci_info['Product Name']
    return ocp_info


def get_bios_info():
    """
    Handle 0x0000, DMI type 0, 26 bytes
BIOS Information
        Vendor: BYD
        Version: JXEGS2 0.04.005
        Release Date: 03/26/2024
        Address: 0xF0000
        Runtime Size: 64 kB
        ROM Size: 64 MB


    return dict

    """
    # cmd = ['dmidecode','-t','0']
    content = get_dmi_info('0')
    return content[0]


def get_bmc_info():
    """
    return dict
    """
    content = get_dmi_info(45)
    bmc_info = [info for info in content if 'BMC' in info['Firmware Component Name']]
    # pdb.set_trace()
    return bmc_info[0]


def get_qlogic_fc_cards_bus():
    """
    2a:00.0 Fibre Channel: QLogic Corp. ISP2684 (rev 01)
    ab:00.0 Fibre Channel: QLogic Corp. ISP2714-based 16/32Gb Fibre Channel to PCIe Adapter (rev 01)
    e1:00.1 Fibre Channel: QLogic Corp. ISP2812-based 64/32G Fibre Channel to PCIe Controller (rev 02)
    """
    support_FC = {'ISP2684', "ISP2714", "ISP2812"}
    #
    bus_info = []
    cmd = ['lspci']
    content = filter_contents(cmd, 'QLogic')
    for line in content:
        if 'Fibre Channel' in line:
            bus = line.split()[0]
            # logging.info(bus)
            bus_info.append(bus)
    return bus_info


def get_qlogic_fc_info():
    """
    get the bus info
    get pci info
    """
    FC_info = []
    bus_info = get_qlogic_fc_cards_bus()
    for bus in bus_info:
        content = get_pci_info(bus)
        if content:
            FC_info.append(content)
    return FC_info

    # pdb.set_trace()


def get_nvidia_gpu_info():
    """
    get the nvidia bus first
    from the bus to get the detail bus info with lspci -vvv -s bus
    """
    gpu_info = []
    bus_info = get_nvidia_cards_bus()
    for bus in bus_info:
        content = get_pci_info(bus)
        if content:
            gpu_info.append(content)
    return gpu_info


def is_downgraded(line):
    """
    (Pdb) content['LnkSta']
'Speed 8GT/s (ok), Width x8 (ok)'
 LnkSta: Speed 8GT/s (ok), Width x8 (downgraded)

    """
    if 'downgraded' in line:
        return True
    else:
        return False


def get_nvidia_cards_bus():
    """
   3d:00.0 3D controller: NVIDIA Corporation TU104GL [Tesla T4] (rev a1)
   bd:00.0 3D controller: NVIDIA Corporation TU104GL [Tesla T4] (rev a1)

    """

    #
    bus_info = []
    cmd = ['lspci']
    content = filter_contents(cmd, 'NVIDIA')
    for line in content:
        if 'NVIDIA Corporation' in line:
            bus = line.split()[0]
            # logging.info(bus)
            bus_info.append(bus)
    return bus_info


def show_dict(mydict):
    msg = []
    for k, v in mydict.items():
        # print(k, '->>>', v)
        _to_print = ' '.join([str(x) for x in (k, '->>>', v)])
        msg.append(_to_print)
    return '\n'.join(msg)


def show_list(mylist):
    for item in mylist:
        print(item)


def check_list_field(mylist, index, name, field):
    """
    check the mylist[index] are same or not
    """
    result = all([x[index] == mylist[0][index] for x in mylist])
    if result:
        msg = f'Check {name}  with {field} ,the result is PASS with {mylist[0][index]} '
        mf.display(msg)
    if not result:
        msg = f'Check {name}  with {field} ,the result is FAILED ....................'
        mf.display(msg)
        pdb.set_trace()


def show_format_tables(headers, tables):
    table = mf.create_table(headers, tables)
    mf.display(table)

def hex2str(hex_string):
    return ''.join([chr(int(hex_num, 16)) for hex_num in hex_string.split()])

def str2hex(strings):
    return ' '.join( [hex(ord(i)) for i in strings])

def append_to_file(filename, content, seperator=None):
    with open(filename, 'a') as fh:
        if seperator:
            fh.write("\n\n" + '*' * 70)
        fh.write(content)

def append_to_error_log(filename,msg):
    now = datetime.datetime.now()
    timefrm = now.strftime('%Y-%m-%d %H:%M:%S')
    message = f"{timefrm} \t {msg} \n"
    with open(filename,'a') as fh:
        fh.write(message)



def validate_sn_only(filename, sn):
    with open(filename, 'r') as fh:
        contents = fh.readlines()
    for line in contents:
        if sn in line:
            return False
    else:
        return True
