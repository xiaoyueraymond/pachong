import argparse
import os
import pdb
from redfish import redfish_client
import myformat as mf
import sys
import logging
from mytools import *


##
##
# cmdline parameters
parser = argparse.ArgumentParser(description='Query  information from the xFusion iBMC ).')
parser.add_argument('-U', '--USER', dest='username', default='Administrator',
                    help='specify the usernane to use to access the iBMC')
parser.add_argument('-P', '--PASS', dest='password', default='Admin@9000',
                    help='specify the password to use to access the iBMC')
parser.add_argument('-H', '--host', dest='host', default='192.168.2.100',
                    help='specify the IP Address or hostname of the target iBMC,default ip is 192.168.2.100')
args = parser.parse_args()
##
if os.name == 'nt':
    logdir = 'd:\\'
elif os.name == 'posix':
    logdir = '/tmp/'
else:
    msg = '无法判断系统，请联系开发者检查'
    print(msg)
#
log_diag_dir = logdir + 'dump_info'
logfile = logdir + 'xfusion_redfish.log'
cmd = "echo 123456 >d:\\xfusion_redfish_download.log"
os.system(cmd)
loglevel = logging.INFO
logging.getLogger("redfish").setLevel(logging.CRITICAL)
setup_logger(logfile)


##
class xFusion_redfish:
    """
    read bmc info via redfish
    """

    def __init__(self, args):
        self.host = args.host
        self.username = args.username
        self.password = args.password
        self.url = 'https://' + self.host
        self.client = redfish_client(base_url=self.url, username=self.username, password=self.password)
        self.client.login()
        self.get_system_overview()
        self.parse_alarm()
        self.get_cpu_info()
        self.get_memory_summary()
        self.get_summary_extend_cards()
        self.get_hdd_info()
        self.get_pci_devices()
        # self.get_nic_info()
        self.parse_psu()
        self.parse_alarm()
        self.show_msg()
        self.client.logout()

    def get_memory_summary(self):
        msg = 'Check memory info'
        mf.display(mf.create_section(msg))
        self.mem_list = []
        mem_url = '/redfish/v1/Systems/1/Memory'
        contents = self.client.get(mem_url).dict
        # pdb.set_trace()
        self.mem_counts = contents['Members@odata.count']  # ->  'Members@odata.count': 8
        values = contents['Members']
        header = ['Locator', 'Size', 'Manufacturer', 'OperatingSpeedMhz', 'AllowedSpeedsMHz', 'SerialNumber',
                  'MemoryDeviceType', 'PN']
        #  {'@odata.id': '/redfish/v1/Systems/1/Memory/mainboardDIMM001'}
        for v in values:
            # logging.info(v['@odata.id'])
            self.mem_list.append(self.get_detail_memory(v['@odata.id']))

        table = mf.create_table(header, self.mem_list)
        self.mem_msg = f"{self.mem_counts} Memory installed"
        mf.display(table)

    def get_detail_memory(self, endpoint):
        """
         'Name': 'mainboardDIMM000',
        'Id': 'mainboardDIMM000',
        'CapacityMiB': 32768,
         'Manufacturer': 'Hynix',
        'OperatingSpeedMhz': 2666,
        'AllowedSpeedsMHz': [2933],
        'SerialNumber': '20012922',
        'MemoryDeviceType': 'DDR4',
         'DataWidthBits': 72,
         'RankCount': 2,
         'PartNumber': 'HMA84GR7JJR4N-WM',
        'DeviceLocator': 'DIMM000',
        """
        rsp = self.client.get(endpoint)
        contents = rsp.dict
        data = [contents['DeviceLocator'],
                contents['CapacityMiB'],
                contents['Manufacturer'],
                contents['OperatingSpeedMhz'],
                contents['AllowedSpeedsMHz'],
                contents['SerialNumber'],
                contents['MemoryDeviceType'],
                contents['PartNumber']
                ]
        expected_locators = ['DIMM000', 'DIMM010', 'DIMM020', 'DIMM030', 'DIMM040', 'DIMM050', 'DIMM060', 'DIMM070',
                             'DIMM100', 'DIMM110', 'DIMM120', 'DIMM130', 'DIMM140', 'DIMM150', 'DIMM160', 'DIMM170']
        #  contents['CapacityMiB'], -> int
        if (contents['DeviceLocator'] not in expected_locators) or (contents['CapacityMiB'] not in [65536]):
            msg1 = "Memory install Error or bad memory ,please check "
            mf.display(msg1)
            pdb.set_trace()
            msg = " ".join([str(x) for x in data])
            mf.display(msg)

            raise Exception(msg1)
        # new_dat = [x.strip() for x in data if isinstance(x,str) else x ]
        return data

    def get_system_overview(self):
        msg = 'get system overview'
        mf.display(mf.create_section(msg))
        url = '/redfish/v1/SystemOverview'
        rsp = self.client.get(url).dict
        bios_ver = rsp['Systems'][0]['BiosVersion']
        bmc_ver = rsp['Managers'][0]['FirmwareVersion']
        sn = rsp['Systems'][0]['SystemSerialNumber']
        pname = rsp['Systems'][0]['ProductName']
        bmc_mac = rsp['Managers'][0]['PermanentMACAddress']
        bmc_ip = rsp['Managers'][0]['DeviceIPv4']
        uuid = rsp['Managers'][0]['UUID']
        msg = []
        msg.append(f"Machine Type:\t{pname}")
        msg.append(f"Serial Number:\t{sn}")
        msg.append(f"UUID:\t{uuid}")
        msg.append(f"BIOS Version:\t {bios_ver}")
        msg.append(f"BMC Version:\t{bmc_ver}")
        msg.append(f"BMC MAC:\t{bmc_mac}")
        msg.append(f"BMC IP:\t{bmc_ip}")
        self.sn = sn
        for item in msg:
            mf.display(item)

    def get_cpu_info(self):
        msg = "check CPU Info"
        mf.display(mf.create_section(msg))
        cpu_url = '/redfish/v1/Systems/1/Processors'
        rsp = self.client.get(cpu_url).dict
        cpu_counts = rsp['Members@odata.count']
        cpu_dict = rsp['Members']
        headers = ['name', 'InstructionSet', 'Manufacturer', 'Model', 'Frequency(MHz)', 'TotalCores', 'TotalThreads',
                   'SerialNumber']
        cpu_tables = []
        for cpu in cpu_dict:
            cpu_detail = cpu['@odata.id']
            result = self.get_detail_cpu(cpu_detail)
            cpu_tables.append(result)

        tables = mf.create_table(headers, cpu_tables)
        self.cpu_counts = len(cpu_tables)
        self.cpu_msg = f"{self.cpu_counts}  CPU installed"
        mf.display(tables)

    def get_detail_cpu(self, url):
        rsp = self.client.get(url).dict
        name = rsp['Name']
        InstructionSet = rsp['InstructionSet']
        Manufacturer = rsp['Manufacturer']
        Model = rsp['Model']
        FrequencyMHz = rsp['Oem']['xFusion']['FrequencyMHz']
        TotalCores = rsp['TotalCores']
        TotalThreads = rsp['TotalThreads']
        SerialNumber = rsp['Oem']['xFusion']['SerialNumber']
        return [name, InstructionSet, Manufacturer, Model, FrequencyMHz, TotalCores, TotalThreads, SerialNumber]

    def get_hdd_info(self):
        msg = "Check HDD/SSD info "
        mf.display(mf.create_section(msg))
        #
        url = '/redfish/v1/Chassis/1/Drives'
        rsp = self.client.get(url).dict
        # 'Members@odata.count': 2,
        # 'Members': [{'@odata.id': '/redfish/v1/Chassis/1/Drives/HDDPlaneDisk3'}, {'@odata.id': '/redfish/v1/Chassis/1/Drives/HDDPlaneDisk5'}]}
        hdd_count = rsp['Members@odata.count']
        msg = f"we found {hdd_count} HDD/SSD in this Server"
        mf.display(msg)
        headers = ['Name', 'Model', 'Revision', 'Size', 'Protocol', 'SN', 'Speed']
        hdd_tables = []
        hdd_dict = rsp['Members']
        for item in hdd_dict:
            hdd_url = item['@odata.id']
            result = self.get_detail_hdd(hdd_url)
            hdd_tables.append(result)

        tables = mf.create_table(headers, hdd_tables)
        self.hdd_counts = len(hdd_tables)
        self.hdd_msg = f"{self.hdd_counts} HDD Installed"
        mf.display(tables)

    def get_detail_hdd(self, url):
        rsp = self.client.get(url).dict
        # pdb.set_trace()
        Name = rsp['Name']
        Model = rsp['Model']
        Revision = rsp['Revision']
        Size = rsp['CapacityBytes']
        Protocol = rsp['Protocol']
        SN = rsp['SerialNumber']
        Speed = ['NegotiatedSpeedGbs']
        return [Name, Model, Revision, Size, Protocol, SN, Speed]

    def get_pci_devices(self):
        msg = "Check PCI Devices"
        mf.display(mf.create_section(msg))
        url = '/redfish/v1/Chassis/1/PCIeDevices'
        rsp = self.client.get(url).dict
        # pdb.set_trace()
        num = rsp["Members@odata.count"]
        msg = f"we have found {num} PCI DEVICES Install in this system "
        mf.display(msg)
        if num:
            pci_tables = []
            headers = ['Name', 'Description', 'Manufacturer', 'DeviceLocator', 'Position']

            pci_urls = rsp['Members']
            for item in pci_urls:
                pci_url = item['@odata.id']
                result = self.get_pci_detail(pci_url)
                pci_tables.append(result)

            tables = mf.create_table(headers, pci_tables)
            self.pci_counts = len(pci_tables)
            self.pci_msg = f"{self.pci_counts} PCI device installed"
            mf.display(tables)

    def get_pci_detail(self, url):
        rsp = self.client.get(url).dict
        """
         'PCIeCard1', 'Description': 'MT2892 Family [ConnectX-6 Dx]', 'Manufacturer': 'Mellanox Technologies', 'Model': None, 
        """
        Name = rsp['Name']
        Description = rsp['Description']
        Manufacturer = rsp['Manufacturer']
        DeviceLocator = rsp['Oem']['xFusion']['DeviceLocator']
        Position = rsp['Oem']['xFusion']['Position']
        return [Name, Description, Manufacturer, DeviceLocator, Position]

    def get_nic_info(self):
        logging.info('')  # blank line
        msg = "Check Network Adapters Info"
        mf.display(mf.create_section(msg))
        #
        url = '/redfish/v1/Chassis/1/NetworkAdapters'
        rsp = self.client.get(url).dict
        # pdb.set_trace()
        num = rsp["Members@odata.count"]
        msg = f"we have found {num} Network Adapters Install in this system "
        mf.display(msg)
        if num:
            nic_tables = []
            nic_headers = ['Manufacturer', 'CardModel', 'Locator', 'Bus info']
            for item in rsp['Members']:
                nic_url = item['@odata.id']
                result = self.get_detail_nic(nic_url)
                nic_tables.append(result)

        tables = mf.create_table(nic_headers, nic_tables)
        mf.display(tables)

    def get_detail_nic(self, url):
        rsp = self.client.get(url).dict
        name = rsp['Oem']['xFusion']['Name']
        # pdb.set_trace()
        oem_info = rsp['Oem']['xFusion']
        if oem_info:
            Manufacturer = oem_info.get('CardManufacturer', rsp.get('Manufacturer', 'NA'))
            CardModel = oem_info.get('CardModel', rsp.get('Model', 'NA'))
            Locator = oem_info.get('DeviceLocator', 'NA')
            BDF = oem_info.get('RootBDF', 'NA')
        else:
            Manufacturer = rsp['Manufacturer']
            CardModel = rsp['Model']
            Locator = rsp.get('DeviceLocator', 'NA')
            BDF = rsp.get('RootBDF', 'NA')

        if rsp.get('Controllers', None):
            if rsp['Controllers'][0].get('Links', None):
                if rsp['Controllers'][0]['Links'].get('NetworkPorts@odata.count', 0):
                    urls = rsp['Controllers'][0]['Links'].get('NetworkPorts', [])
                    port_details = []
                    if urls:
                        for item in urls:
                            # msg = "url is {item['@odata.id']}"
                            # logging.info(msg)
                            result = self.get_detail_ports(item['@odata.id'])
                            port_details.append(result)

                headers = ['LinkStatus', 'MAC', 'Type', 'PortType', 'PortMaxSpeed', 'BUS']
                tables = mf.create_table(headers, port_details)
                mf.display(tables)

        return [Manufacturer, CardModel, Locator, BDF]

    #
    # Controllers ======= [{'FirmwarePackageVersion': None, 'ControllerCapabilities': {'NetworkPortCount': 4},
    # 'Links': {'NetworkPorts@odata.count': 4, 'NetworkPorts':
    # [{'@odata.id': '/redfish/v1/Chassis/1/NetworkAdapters/mainboardLOM/NetworkPorts/1'},
    # {'@odata.id': '/redfish/v1/Chassis/1/NetworkAdapters/mainboardLOM/NetworkPorts/2'},
    # {'@odata.id': '/redfish/v1/Chassis/1/NetworkAdapters/mainboardLOM/NetworkPorts/3'},
    # {'@odata.id': '/redfish/v1/Chassis/1/NetworkAdapters/mainboardLOM/NetworkPorts/4'}]}}
    def get_detail_ports(self, url):
        rsp = self.client.get(url).dict
        """
       
        """
        LinkStatus = rsp['LinkStatus']
        mac = rsp['AssociatedNetworkAddresses']
        type = rsp['ActiveLinkTechnology']
        port_info = rsp['Oem']['xFusion']
        PortType = port_info['PortType']
        PortMaxSpeed = port_info['PortMaxSpeed']
        BDF = port_info['BDF']

        # if 'UP' in LinkStatus:
        #     pdb.set_trace()
        return [LinkStatus, mac, type, PortType, PortMaxSpeed, BDF]

    def get_content(self, url):
        url = url
        rsp = self.client.get(url).dict
        return rsp

    def parse_psu(self):
        msg = "check PSU Info"
        mf.display(mf.create_section(msg))
        #
        url = '/redfish/v1/Chassis/1/Power'
        rsp = self.get_content(url)
        psu_tables = []
        headers = ['Name', 'Type', 'PowerCapacityWatts', 'Model', 'FirmwareVersion', 'SerialNumber', 'pn']
        psu_dict = rsp['PowerSupplies']
        for psu in psu_dict:
            Name = psu['Name']
            Type = psu['PowerSupplyType']
            PowerCapacityWatts = psu['PowerCapacityWatts']
            Model = psu['Model']
            FirmwareVersion = psu['FirmwareVersion']
            SerialNumber = psu['SerialNumber']
            pn = psu['PartNumber']
            record = [Name, Type, PowerCapacityWatts, Model, FirmwareVersion, SerialNumber, pn]
            psu_tables.append(record)

        #
        table = mf.create_table(headers, psu_tables)
        mf.display(table)
        self.psu_counts = len(psu_tables)
        self.psu_msg = f"{self.psu_counts} PSU  installed"

    def show_msg(self):
        msg = "summary".center(70, '*')
        mf.display(msg)
        mf.display(self.cpu_msg)
        mf.display(self.mem_msg)
        mf.display(self.pci_msg)
        mf.display(self.hdd_msg)
        mf.display(self.psu_msg)

    def parse_alarm(self):
        url = '/redfish/v1/Systems/1/LogServices/Log1'
        rsp = self.get_content(url)
        if rsp.get('Oem', None):
            if rsp['Oem'].get('xFusion', None):
                if 'HealthEvent' in rsp['Oem']['xFusion'].keys():
                    alert_num = len(rsp['Oem']['xFusion']['HealthEvent'])
                    if alert_num:
                        table = []
                        headers = ['Severity', 'Level', 'EventId', 'Message']
                        logging.warning("WARNING".center(70, '*'))
                        msg = "we found {} alert message ,please double check before continue".format(alert_num)
                        logging.warning(msg)
                        for msg_dict in rsp['Oem']['xFusion']['HealthEvent']:
                            msg_Severity = msg_dict['Severity']
                            msg_Level = msg_dict['Level']
                            msg_Message = msg_dict['Message']
                            EventId = msg_dict['EventId']
                            info = [msg_Severity, msg_Level, EventId, msg_Message]
                            table.append(info)
                        #
                        tables = mf.create_table(headers, table)
                        mf.display(tables)
                        #
                        pdb.set_trace()
                    else:
                        msg = "no Warning Message found"
                        mf.display(msg)
                else:
                    msg = "no Keyword :HealthEvent found "
                    mf.display(msg)
            else:
                mf.display("no keyword: xFusion found")
                pdb.set_trace()
        else:
            mf.display("no keyword :OEM Found")
            pdb.set_trace()

    def get_summary_extend_cards(self):
        url = '/redfish/v1/Chassis/1/Boards'
        rsp = self.client.get(url).dict
        pdb.set_trace()


app = xFusion_redfish(args)
sn = app.sn

target_file = logdir + 'xFusion_' + sn + '.log'
if os.name == 'nt':
    cmd = ['copy', '/Y', logfile, target_file]
else:
    cmd = ['mv', '-f ', logfile, target_file]

msg = ' '.join(cmd)
logging.info(msg)
os.system(msg)
sys.exit(0)
