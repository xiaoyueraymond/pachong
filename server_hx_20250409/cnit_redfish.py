import argparse
import os
import pdb
import time

import requests
from redfish import redfish_client
from myBMC import *
import myformat as mf
import sys
import logging
from mytools import *

parser = argparse.ArgumentParser(description='Query  information from the xFusion iBMC ).')
parser.add_argument('-U', '--USER', dest='username', default='admin',
                    help='specify the usernane to use to access the iBMC')
parser.add_argument('-P', '--PASS', dest='password', default='admin#254',
                    help='specify the password to use to access the iBMC')
parser.add_argument('-H', '--host', dest='host', default='192.168.3.116',
                    help='specify the IP Address or hostname of the target iBMC,default ip is 192.168.2.100')
myargs = parser.parse_args()

#
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
logfile = logdir + 'cnit_redfish.log'
cmd = "echo 123456 >d:\\cnit_redfish.log"
os.system(cmd)
loglevel = logging.INFO
logging.getLogger("redfish").setLevel(logging.CRITICAL)
setup_logger(logfile)


class CNIT(BMC):
    """
    BMC base class for the different BMC　Vendor
    """

    def __init__(self, args):
        super().__init__(args)
        # self.get_session_id()
        self.parse_sysinfo()
        # self.download_server_logs() ## 已完成
        self.check_system_health()
        self.get_cpu_info()
        self.get_mem_info()
        self.get_pcie_info()
        self.get_psu_info()
        self.get_tpm_info()
        self.get_fru()
        # pdb.set_trace()
        # self.client.logout()  # 退出功能有异常，等云尖反馈

    #

    def parse_sysinfo(self):
        """
        BIOS : "/redfish/v1/UpdateService/FirmwareInventory/bios_active"



        """
        bios_url = "/redfish/v1/UpdateService/FirmwareInventory/bios_active"
        BIOS_VER = self.get_redfish_contents(bios_url)['Version']
        #
        #
        bmc_url = "/redfish/v1/UpdateService/FirmwareInventory/bmc_active"
        BMC_VER = self.get_redfish_contents(bmc_url)['Version']
        #
        #
        bmc_backup_url = "/redfish/v1/UpdateService/FirmwareInventory/bmc_backup"
        BMC_BACKUP_VER = self.get_redfish_contents(bmc_backup_url)['Version']
        #
        #
        me_url = "/redfish/v1/UpdateService/FirmwareInventory/me"
        ME_VER = self.get_redfish_contents(me_url)['Version']
        #
        #
        cpld_url = "/redfish/v1/UpdateService/FirmwareInventory/cpld_active"
        CPLD_VER = self.get_redfish_contents(cpld_url)['Version']
        #
        """
        Mfg ->>> CNIT
        Name ->>> G7466 X6
        PartNumber ->>> 0235K000
        Serial ->>> 210235K0000606000001
        """
        baseboard_url = "/redfish/v1/Chassis/1/Fru/BaseBoard"
        baseboard_dict = self.get_redfish_contents(baseboard_url)['Product']
        self.MT = baseboard_dict['Name']
        # self.PN = baseboard_dict['PartNumber']
        self.SN = baseboard_dict['Serial']
        self.Vendor = baseboard_dict['Mfg']
        ##
        ##
        bmc_url = "/redfish/v1/Managers/1"
        rsp = self.get_redfish_contents(bmc_url)
        # show_dict(rsp)
        uuid_url = "/redfish/v1/Managers/1/"
        uuid_dict = self.get_redfish_contents(uuid_url)
        # show_dict(uuid_dict)
        bmc_model = uuid_dict['Model']
        uuid = uuid_dict['UUID']
        #
        #
        myMSG = []
        myMSG.append(f"Server Machine Type: \t{self.MT}")
        myMSG.append(f"Server Serial Number:\t {self.SN}")
        myMSG.append(f"Server Venor: \t{self.Vendor}")
        myMSG.append(f"Server UUIDr:\t {uuid}")
        myMSG.append(f"Server BIOS VERSION: \t{BIOS_VER}")
        myMSG.append(f"Server BMC VERSION: \t{BMC_VER}")
        myMSG.append(f"Server BMC BACKUP VERSION: \t{BMC_BACKUP_VER}")
        myMSG.append(f"Server BMC Model: \t{bmc_model}")
        myMSG.append(f"Server ME VERSION: \t{ME_VER}")
        myMSG.append(f"Server CPLD VERSION: \t{CPLD_VER}")
        for item in myMSG:
            logging.info(item)

    def get_session_id(self):
        url = '/redfish/v1/SessionService/Sessions'
        rsp = self.client.get(url).dict
        pdb.set_trace()

    def get_cpu_info(self):
        msg = 'Check CPU　Info'
        mf.display(mf.create_section(msg))
        #
        url = '/redfish/v1/Systems/1/Processors'
        rsp = self.get_redfish_contents(url)
        # pdb.set_trace()
        cpu_list = rsp['Members']
        self.cpu_counts = len(cpu_list)
        headers = ['Name', 'Cores', 'Threads', 'Frequency', 'PPIN']
        cpu_tables = []
        for item in cpu_list:
            content = self.get_redfish_contents(item['@odata.id'])
            # pdb.set_trace()
            Name = content['Name']
            Cores = content['Cores']
            Threads = content['Threads']
            Frequency = content['Frequency']
            PPIN = content['PPIN']
            info = [Name, Cores, Threads, Frequency, PPIN]
            cpu_tables.append(info)

        table = mf.create_table(headers, cpu_tables)
        mf.display(table)

    def get_mem_info(self):
        msg = 'check Memory Info'
        mf.display(mf.create_section(msg))
        #
        url = '/redfish/v1/Systems/1/Memory'
        rsp = self.get_redfish_contents(url)
        mem_list = rsp['Members']
        self.mem_counts = len(mem_list)
        headers = ['PN', 'SN', 'Size', 'Type', 'Vendor', 'Frequency', 'CPULocation', 'ChannelLocation', 'DIMMLocation']
        mem_tables = []
        for item in mem_list:
            content = self.get_redfish_contents(item['@odata.id'])
            # pdb.set_trace()
            CPULocation = content['CPULocation']
            ChannelLocation = content['ChannelLocation']
            DIMMLocation = content['DIMMLocation']
            Frequency = content['Frequency']
            PN = content['PN'].strip()
            SN = content['SN']
            Size = content['Size']
            Type = content['Type']
            Vendor = content['Vendor']

            info = [PN, SN, Size, Type, Vendor, Frequency, CPULocation, ChannelLocation, DIMMLocation]
            mem_tables.append(info)
        table = mf.create_table(headers, mem_tables)
        mf.display(table)

    def get_pcie_info(self):
        msg = 'Check PCIE　Info'
        mf.display(mf.create_section(msg))
        #
        url = "/redfish/v1/Chassis/1/PCIeDevices"
        rsp = self.get_redfish_contents(url)
        pci_list = rsp['Members']
        self.pci_counts = len(pci_list)
        headers = ['Location', 'ProductName', 'ChipVendor', 'ModouleVendor', 'NegotiatedLinkWidth',
                   'NegotiatedProtocol', 'NegotiatedSpeed']
        pci_tables = []
        for item in pci_list:
            content = self.get_redfish_contents(item['@odata.id'])
            # pdb.set_trace()
            Location = content['Location']
            ProductName = content['ProductName']
            ChipVendor = content['ChipVendor']
            ModouleVendor = content['ModouleVendor']
            NegotiatedLinkWidth = content['NegotiatedLinkWidth']
            NegotiatedProtocol = content['NegotiatedProtocol']
            NegotiatedSpeed = content['NegotiatedSpeed']

            info = [Location, ProductName, ChipVendor, ModouleVendor, NegotiatedLinkWidth, NegotiatedProtocol,
                    NegotiatedSpeed]
            pci_tables.append(info)
        table = mf.create_table(headers, pci_tables)
        mf.display(table)

    def get_fru(self):
        msg = "check FRU info"
        mf.display(mf.create_section(msg))
        """
        
        Board ->>> {'Extra1': '02K0DY0310000001', 'Mfg': 'CNIT', 'MfgData': '2023-06-30 - 08:34:00', 'PartNumber': '0302K0WJ', 'Product': 'BP-12LUG5', 'Serial': '02K0DY0310000001'}
        DeviceID ->>> 4
        DeviceName ->>> BP_12LUG5
        
        Board ->>> {'Extra1': 'PCBA Ver:A', 'Mfg': 'CNIT', 'MfgData': '2024-03-07 - 03:14:00', 'PartNumber': '0302K0TU', 'Product': 'BP-12S9x12G5S2', 'Serial': '02K0TU03100000000001'}
        DeviceID ->>> 2
        DeviceName ->>> BP_12S9x12G5S2
        
        Board ->>> {'Extra1': 'PCBA Ver:A', 'Mfg': 'CNIT', 'MfgData': '2024-03-11 - 06:46:00', 'PartNumber': '0302K0UD', 'Product': 'BM-X13DEP', 'Serial': '02K0LE06060000000001'}
        Chassis ->>> {'Extra1': '210200K0000606000001', 'PartNumber': '0235K000', 'Serial': '210235K0000606000001', 'Type': 'Rack Mount Chassis'}
        DeviceID ->>> 0
        DeviceName ->>> BaseBoard
        Product ->>> {'Mfg': 'CNIT', 'Name': 'G7466 X6', 'PartNumber': '0235K000', 'Serial': '210235K0000606000001'}
        
        DeviceID ->>> 3
        DeviceName ->>> G1302_2600WNA_
        Product ->>> {'Mfg': 'GOSPOWER', 'Name': 'G1302-2600WNA ', 'PartNumber': 'CRPS2600-AH         ', 'Serial': 'G1302262NA240300444'}
        
        """
        url = '/redfish/v1/Chassis/1/Fru'
        rsp = self.get_redfish_contents(url)
        # pdb.?set_trace()
        BP_table = []
        BP_header = ['DeviceName', 'Mfg', 'MfgData', 'PartNumber', 'Product', 'Serial']
        baseboard = []
        baseboard_header = ['DeviceName', 'Mfg', 'Name', 'PartNumber', 'Serial']
        PSU = []
        PSU_header = ['DeviceName', 'Mfg', 'Name', 'PartNumber', 'Serial']
        #
        for item in rsp['Fru']:
            # pdb.set_trace()
            content = self.get_redfish_contents(item[1])
            DeviceName = content['DeviceName']
            if content['DeviceName'].startswith("BP"):
                Mfg = content['Board']['Mfg']
                MfgData = content['Board']['MfgData']
                PartNumber = content['Board']['PartNumber']
                Product = content['Board']['Product']
                Serial = content['Board']['Serial']
                info = [DeviceName, Mfg, MfgData, PartNumber, Product, Serial]
                BP_table.append(info)
            if content['DeviceName'].strip() == 'BaseBoard':
                Mfg = content['Product']['Mfg']
                Name = content['Product']['Name']
                PartNumber = content['Product']['PartNumber']
                Serial = content['Product']['Serial']
                info = [DeviceName, Mfg, Name, PartNumber, Serial]
                baseboard.append(info)
            if content['DeviceName'].startswith('G1302_2600WNA'):
                Mfg = content['Product']['Mfg']
                Name = content['Product']['Name']
                PartNumber = content['Product']['PartNumber'].strip()
                Serial = content['Product']['Serial']
                info = [DeviceName, Mfg, Name, PartNumber, Serial]
                PSU.append(info)

        if len(BP_table):
            show_format_tables(BP_header, BP_table)
        #
        if len(baseboard):
            show_format_tables(baseboard_header, baseboard)
        #
        if len(PSU):
            show_format_tables(PSU_header, PSU)

    def get_psu_info(self):
        msg = 'Check PSU　Info'
        mf.display(mf.create_section(msg))
        url = '/redfish/v1/Chassis/1/PowerSupply'
        rsp = self.get_redfish_contents(url)
        psu_list = rsp['Members']
        self.psu_counts = len(psu_list)
        headers = ['Id', 'Manufacturer', 'Model', 'SerialNumber', 'ActiveStandby', 'FWVersion', 'CapacityWatts']
        psu_tables = []
        for item in psu_list:
            content = self.get_redfish_contents(item['@odata.id'])
            #
            Id = content['Id']
            Manufacturer = content['Manufacturer']
            Model = content['Model']
            SerialNumber = content['SerialNumber']
            ActiveStandby = content['ActiveStandby']
            FWVersion = content['FWVersion']
            CapacityWatts = content['CapacityWatts']
            info = [Id, Manufacturer, Model, SerialNumber, ActiveStandby, FWVersion, CapacityWatts]
            psu_tables.append(info)
        table = mf.create_table(headers, psu_tables)
        mf.display(table)
        expected_psu_check = False
        if expected_psu_check:
            check_list_field(psu_tables, 1, 'PSU', 'Manufacturer', )
            check_list_field(psu_tables, 2, 'PSU', 'Model')
            check_list_field(psu_tables, 5, 'PSU', 'FWVersion')

    def get_tpm_info(self):
        msg = 'Check TPM Info'
        section = mf.create_section(msg)
        mf.display(section)
        #
        url = '/redfish/v1/Chassis/1/TPM'
        rsp = self.get_redfish_contents(url)
        # {'TPMEnable': 'Enabled', 'TPMPresent': 'not present'}
        if rsp['TPMPresent'] == 'not present':
            msg = ":\tTPM　NOT installed in this Server\t".center(50, '*')
            mf.display(msg)
        elif rsp['TPMPresent'] == 'present':
            msg = "\tTPM　installed in this Server,and state is :\t{rsp['TPMEnable']} \t".center(50, '*')
            mf.display(msg)
        else:
            msg = "exception found ,please check with RD"
            mf.display(msg)
            pdb.set_trace()

    def check_system_health(self):
        url = '/redfish/v1/Systems/1'
        rsp = self.get_redfish_contents(url)
        system_health = rsp['Oem']['SystemHealth']
        #
        """
        (Pdb) show_dict(rsp['Oem']['SystemHealth'])
        Board ->>> {'Critical': 1, 'Fatal': 0, 'Health': 'Critical', 'Warning': 0}
        Fans ->>> {'Critical': 0, 'Fatal': 0, 'Health': 'OK', 'Warning': 0}
        Memory ->>> {'Critical': 0, 'Fatal': 0, 'Health': 'OK', 'Warning': 0}
        Other ->>> {'Critical': 0, 'Fatal': 0, 'Health': 'OK', 'Warning': 0}
        OverallHealth ->>> {'Critical': 1, 'Fatal': 0, 'Health': 'Critical', 'Warning': 1}
        PCIe ->>> {'Critical': 0, 'Fatal': 0, 'Health': 'OK', 'Warning': 0}
        Power ->>> {'Critical': 0, 'Fatal': 0, 'Health': 'OK', 'Warning': 0}
        Processor ->>> {'Critical': 0, 'Fatal': 0, 'Health': 'Warning', 'Warning': 1}
        Storage ->>> {'Critical': 0, 'Fatal': 0, 'Health': 'OK', 'Warning': 0}
        Temperature ->>> {'Critical': 0, 'Fatal': 0, 'Health': 'OK', 'Warning': 0}
        """
        health_state = True
        health_tables = []
        headers = ['Name', 'Health Status', 'Critical', 'Fatal', 'Warning']
        items = ['Board', 'Processor', 'Memory', 'PCIe', 'Storage', 'Power', 'Fans', 'Other', 'Temperature',
                 'OverallHealth']
        for item in items:
            info = [item, system_health[item]['Health'], system_health[item]['Critical'], system_health[item]['Fatal'],
                    system_health[item]['Warning']]
            health_tables.append(info)
        table = mf.create_table(headers, health_tables)
        mf.display(table)

        overall_health = system_health['OverallHealth']
        if (overall_health['Critical'] != 0) or (overall_health['Fatal'] != 0) or (overall_health['Warning'] != 0) or (
                overall_health['Health'] != 'OK'):
            health_state = False

        if not health_state:
            msg = "Server is not in Health status ,please check for make sure......"
            logging.critical(msg)
            pdb.set_trace()

    def download_file(self, src, sn):
        """

        """
        save_path = logdir + sn + '.tar'
        url = f"https://{self.host}/{src}"
        mf.display(url)
        response = requests.get(url,verify=False)
        if response.status_code == 200:
            # 以二进制模式写入文件
            with open(save_path, 'wb') as f:
                f.write(response.content)
            mf.display(f"Log file down to {save_path}")
        else:
            print('文件下载失败:', response.status_code)

    def download_server_logs(self):
        url1 = '/redfish/v1/Systems/1/LogServices/all/download'
        url2 = '/redfish/v1/Systems/1/LogServices/download/progress'
        # Log210235K0000606000001_20240430
        # Log+SN+timestamp.tar
        # 1. 请求download接口，获取文件路径及产品序列号（没有也正常）
        # 2. 循环请求progress接口，当进度 progress 为2时即可下载
        # 3. 下载
        msg = "Start to trigger the LOG collections"
        section = mf.create_section(msg)
        mf.display(section)
        msg = "send Command to start the Log Collections"
        mf.display(msg)
        rsp = self.get_redfish_contents(url1)
        for i in range(100):
            time.sleep(10)
            msg = "Start to query the Log Collections progress after {} seconds".format((i+1) * 10)
            mf.display(msg)
            progress = self.get_redfish_contents(url2)
            #
            if progress['progress'] == 1:
                continue
            elif progress['progress'] == 2:
                #
                # pdb.set_trace()
                msg = "Log Collections finished,start to download now..."
                productSN = progress['productSN']
                mf.display(msg)
                break
        #
        #
        rsp = self.get_redfish_contents(url1)
        if rsp.get('filename', None):
            filename = rsp['filename']
            # productSN = rsp['productSN']
            msg = f"target filename is:\t {filename}\t,Product SN is {productSN}"
            mf.display(msg)
            self.download_file(filename, productSN)

        # pdb.set_trace()


app = CNIT(myargs)
