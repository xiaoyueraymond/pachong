import argparse
import time

from redfish import redfish_client

from mytools import *
from xfusion_config_detail_v5 import *

##
##
# cmdline parameters
parser = argparse.ArgumentParser(description='Query  information from the xFusion iBMC ).')
parser.add_argument('-U', '--USER', dest='username', default='Administrator',
                    help='specify the username to use to access the iBMC')
parser.add_argument('-P', '--PASS', dest='password', default='Admin@9000',
                    help='specify the password to use to access the iBMC')
parser.add_argument('-H', '--host', dest='host', default='192.168.2.100',
                    help='specify the IP Address or hostname of the target iBMC,default ip is 192.168.89.109')
parser.add_argument('-p', '--port', dest='port', default='443',
                    help='specify the port to the target iBMC, default is 443')

args = parser.parse_args()
##

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
logfile = logdir + 'xfusion_redfish.log'
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


##
class xFusion_redfish:
    """
    read bmc info via redfish
    """

    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.username = args.username
        self.password = args.password
        self.error_log = error_logfile
        self.url = 'https://' + self.host + ':' + self.port
        self.client = redfish_client(base_url=self.url, username=self.username, password=self.password)
        self.client.login()
        self.get_system_overview()
        self.get_all_extension_boards()
        self.get_mainboard_info()
        self.get_raidcard_info()
        self.get_riser_info()
        self.get_diskbp_info()
        self.get_ocp_info()
        # self.download_full_ffdc()
        # self.get_raid_controller()
        # self.parse_alarm()
        self.get_cpu_info()
        self.get_memory_summary()
        self.get_hdd_info()
        self.get_pci_devices()
        # self.get_nic_info()
        self.parse_psu()
        self.parse_alarm()
        self.show_msg()
        # self.get_fru_info()
        self.client.logout()

    def append_to_errorlogs(self, type, msg):
        new_msg = "\t".join((self.sn, type, msg))
        append_to_error_log(self.error_log, new_msg)

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
                  'MemoryDeviceType', 'PN', 'RankCount']
        #  {'@odata.id': '/redfish/v1/Systems/1/Memory/mainboardDIMM001'}
        for v in values:
            # logging.info(v['@odata.id'])
            self.mem_list.append(self.get_detail_memory(v['@odata.id']))

        table = mf.create_table(header, self.mem_list)
        self.mem_msg = f"{self.mem_counts} Memory installed"
        mf.display(table)
        #
        if expected_memory_check_dict['expected_memory_counts'] != self.mem_counts:
            msg = f"installed memory is mismatch ,expected is {expected_memory_check_dict['expected_memory_counts']},but actual result is {self.mem_counts}"
            # new_msg = "Memory\t{self.sn\t" + msg
            self.append_to_errorlogs("MEMORY", msg)
            mf.display(msg)
            raise Exception(msg)

        if expected_memory_check_dict['expected_memory_same_vendor']:
            vendor_result = [x[2] == self.mem_list[0][2] for x in self.mem_list]
            if not all(vendor_result):
                pdb.set_trace()
                msg = "not all memory with same vendor,please check "
                new_msg = "Memory\t{self.sn\t" + msg
                self.append_to_errorlogs("MEMORY", msg)
                mf.display(msg)
                raise Exception(msg)

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
                contents['PartNumber'],
                contents['RankCount']
                ]

        #  contents['CapacityMiB'], -> int
        # expected_rsp = f"Expected MEM: {expected_memory_locators}"
        # actuall_resp = f""
        locator_rsp = contents['DeviceLocator'] in expected_memory_locators
        capacity_rsp = contents['CapacityMiB'] in expected_memory_check_dict['expected_memory_size']
        speed_rsp = contents['OperatingSpeedMhz'] == expected_memory_check_dict['expected_memory_operation_speed']
        rank_rsp = contents['RankCount'] == expected_memory_check_dict['expected_memory_ranks']

        if not all((locator_rsp, capacity_rsp, speed_rsp, rank_rsp)):
            msg_header = "SLot\tSize\tSpeed\tRanks"
            mf.display(msg_header)
            mem_result = [str(item) if isinstance(item, bool) else item for item in
                          (locator_rsp, capacity_rsp, speed_rsp, rank_rsp)]
            msg = ('\t').join(mem_result)
            mf.display(msg)
            raise Exception(msg)
        # if expected_memory_same_vendor:
        #
        #
        # if (contents['DeviceLocator'] not in expected_memory_locators) or
        #     ( contents['CapacityMiB'] not in expected_memory_check_dict['expected_memory_size'] ）or
        #     (contents['OperatingSpeedMhz'] == expected_memory_check_dict['expected_memory_operation_speed']) :
        #     msg1 = " Memory Install or Detect Error ,please double check"
        #     mf.display(msg1)
        #     pdb.set_trace()
        #     msg = " ".join([str(x) for x in data])
        #     mf.display(msg)
        #
        #     raise Exception(msg1)
        # new_dat = [x.strip() for x in data if isinstance(x,str) else x ]
        return data

    def get_system_overview(self):
        msg = 'get system overview'
        mf.display(mf.create_section(msg))
        url = '/redfish/v1/SystemOverview'
        rsp = self.client.get(url).dict
        bios_ver = rsp['Systems'][0]['BiosVersion']
        if expected_bios_ver_check:
            expected_bios_version = expected_fw_version['BIOS_version']
            msg = f"BIOS Version check enable ,expected BIOS main version is {expected_bios_version}"
            mf.display(msg)
            if not bios_ver.startswith(expected_bios_version):
                msg = f"expected BIOS Version: {expected_bios_version}"
                mf.display(msg)
                msg1 = f"Actually BIOS Version:\t {bios_ver} "
                mf.display(msg1)
                msg2 = f"BIOS Version mismatch:\t Expect:{expected_bios_version}\tActual:\t{bios_ver}"
                mf.display(msg2)
                raise Exception(msg2)
            else:
                msg2 = f"BIOS Version MATCH:\t Expect:{expected_bios_version}\tActual:\t{bios_ver},\tresult is PASS"
                mf.display(msg2)
        bmc_ver = rsp['Managers'][0]['FirmwareVersion']
        if expected_bmc_ver_check:
            expected_bmc_version = expected_fw_version['BMC_version']
            msg = f"BMC Version check enable ,expected BMC main version is {expected_bmc_version}"
            mf.display(msg)
            if not bmc_ver.startswith(expected_bmc_version):
                msg = f"expected BMC Version: {expected_bmc_version}"
                mf.display(msg)
                msg1 = f"Actually BMC Version:\t {bmc_ver} "
                mf.display(msg1)
                msg2 = f"BMC Version mismatch:\t Expect:{expected_bmc_version}\tActual:\t{bmc_ver}"
                mf.display(msg2)
                raise Exception(msg2)
            else:
                msg2 = f"BMC Version MATCH:\t Expect:{expected_bmc_version}\tActual:\t{bmc_ver},\tresult is PASS"
                mf.display(msg2)
        # pdb.set_trace()
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
        self.debug_file = logdir + 'debug_' + self.sn + '.log'

        append_to_file(self.debug_file, show_dict(rsp), seperator=True)
        #
        self.sn_logfile = sn_logfile
        if validate_sn_only(self.sn_logfile, self.sn):
            msg = get_datetime_str() + f'      {self.sn}\n'
            append_to_file(self.sn_logfile, msg)
        else:
            timestamp = get_datetime_str()
            msg = f"SN exist in {self.sn_logfile},need to check again:\t\t{timestamp}\t {self.sn}  \n"
            mf.display(msg)
            append_to_file(self.sn_logfile, msg)

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
            # mf.display('\t'.join([str(x) for x in result]))
            if expected_cpu_check:
                #
                model = result[3]
                fequency = result[4]
                cores = result[5]
                total_threads = result[6]
                cpu_tables.append(result)
                #
                cpu_model_bool = (expected_cpu_check_dict['expected_cpu_model'] in model)
                cpu_core_bool = (expected_cpu_check_dict['expected_cpu_core'] == cores)
                cpu_thread_bool = (expected_cpu_check_dict['expected_cpu_thread'] == total_threads)
                if all((cpu_thread_bool, cpu_core_bool, cpu_model_bool)):
                    msg = "CPU check and passed,so this cpu is ok ,tag cpu_ok"
                    logging.info(msg)

                else:
                    msg = "CPU　check and mismatch found ...."
                    mf.display(msg)
                    mf.display('\t'.join([str(x) for x in result]))
                    # mf.display(msg)
                    # new_msg = f"CPU\t{self.sn}\t Wrong CPU found /Installed\n"
                    self.append_to_errorlogs("CPU", msg)
                    msg1 = f"Model:{cpu_model_bool} \t Cores:{cpu_core_bool}\tThreads:{cpu_thread_bool}"
                    mf.display(msg1)
                    raise Exception(msg1)

        tables = mf.create_table(headers, cpu_tables)
        self.cpu_counts = len(cpu_tables)
        if self.cpu_counts != expected_cpu_counts:
            msg = "CPU counts mismatch,please double check or report to Peter！！！"
            new_msg = f"CtWrong number of CPU installed \n"
            self.append_to_errorlogs("CPU", new_msg)
            raise Exception(msg)
        self.cpu_msg = f"{self.cpu_counts}  CPU installed"
        mf.display(tables)
        append_to_file(self.debug_file, show_dict(rsp), seperator=True)

    def get_detail_cpu(self, url):
        rsp = self.client.get(url).dict
        name = rsp['Name']
        InstructionSet = rsp['InstructionSet']
        Manufacturer = rsp['Manufacturer']
        Model = rsp['Model']
        FrequencyMHz = rsp['Oem']['Huawei']['FrequencyMHz']
        TotalCores = rsp['TotalCores']
        TotalThreads = rsp['TotalThreads']
        SerialNumber = rsp['Oem']['Huawei']['SerialNumber']
        return [name, InstructionSet, Manufacturer, Model, FrequencyMHz, TotalCores, TotalThreads, SerialNumber]

    def get_hdd_info(self):
        msg = "Check HDD/SSD info "
        mf.display(mf.create_section(msg))
        #
        url = '/redfish/v1/Chassis/1/Drives'
        rsp = self.client.get(url).dict
        # pdb.set_trace()
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
            # pdb.set_trace()
            hdd_tables.append(result)

        tables = mf.create_table(headers, hdd_tables)
        self.hdd_counts = len(hdd_tables)
        self.hdd_msg = f"{self.hdd_counts} HDD Installed"
        mf.display(tables)
        if hdd_count != expected_disk_counts:
            msg = f"expetced install disk number is {expected_disk_counts},but we only find {hdd_count} disk installed"
            mf.display(msg)
            # new_msg = f"HDD\t{self.sn}\t{msg}"
            self.append_to_errorlogs("HDD", msg)
            raise Exception(msg)
        if expected_disk_check:
            for disk in hdd_tables:
                # pdb.set_trace()
                expected_hdd_tuple = expected_disk_check_dict.get(disk[0], expected_disk_check_dict.get('Other', None))
                if not expected_hdd_tuple:
                    msg = "Can not detected the hdd check info,please contact Developer for check!!!!"
                    mf.display(msg)
                    raise Exception(msg)
                model_result = expected_hdd_tuple[0] == disk[1]
                size_result = expected_hdd_tuple[1] == disk[3]
                proto_result = expected_hdd_tuple[2] == disk[4]
                if not all((model_result, size_result, proto_result)):
                    model_msg = f"Expected is {expected_hdd_tuple[0]},but we found {disk[1]}"
                    size_msg = f"Expected is {expected_hdd_tuple[1]},but we found {disk[3]}"
                    protocol_msg = f"Expected is {expected_hdd_tuple[2]},but we found {disk[4]}"
                    mf.display(model_msg)
                    mf.display(size_msg)
                    mf.display(protocol_msg)
                    msg = f"mismatch found on disk {disk[0]}"
                    # new_msg = f"HDD\t{self.sn}\t{msg}"
                    self.append_to_errorlogs("HDD", new_msg)
                    mf.display(msg)
                    raise Exception(msg)
                else:
                    msg = f"check on disk {disk[0]}, and result is PASSED"
                    mf.display(msg)

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
        pci_check_result = True
        if num:
            pci_tables = []
            headers = ['Name', 'Description', 'Manufacturer', 'FirmwareVersion', 'DeviceLocator', 'Position', "RESULT"]

            pci_urls = rsp['Members']
            for item in pci_urls:
                pci_url = item['@odata.id']
                result = self.get_pci_detail(pci_url)
                if result[-1] == "FAILED":
                    pci_check_result = False
                pci_tables.append(result)

            tables = mf.create_table(headers, pci_tables)
            self.pci_counts = len(pci_tables)
            self.pci_msg = f"{self.pci_counts} PCI device installed"
            mf.display(tables)
        if num != expected_pcie_installed_number:
            msg = f"expected pcie card installed is {expected_pcie_installed_number}, but we only found {num} cards install in this system"
            mf.display(msg)
            self.append_to_errorlogs("PCIE", msg)
            raise Exception(msg)
        if not pci_check_result:
            msg = "PCI check failed ,please check the tables for detail in about result output"
            mf.display(msg)
            raise Exception(msg)

    # expected_cpu_counts
    def get_pci_detail(self, url):
        rsp = self.client.get(url).dict
        # pdb.set_trace()
        """
         'PCIeCard1', 'Description': 'MT2892 Family [ConnectX-6 Dx]', 'Manufacturer': 'Mellanox Technologies', 'Model': None, 
        """
        Name = rsp['Name']
        Description = rsp['Description']
        Manufacturer = rsp['Manufacturer']
        DeviceLocator = rsp['Oem']['Huawei']['DeviceLocator']
        Position = rsp['Oem']['Huawei']['Position']
        FirmwareVersion = rsp['FirmwareVersion']
        check_Description = Name + '_Description'
        check_FirmwareVersion = Name + '_FirmwareVersion'
        check_DeviceLocator = Name + '_DeviceLocator'
        check_pci_result = "PASSED"

        if expected_pcie_check:
            msg = f'start to check the pci info on {Name}'
            mf.display(msg)
            if expected_pcie_check_dict[Name]:
                msg = f'Checking the info about {Name} now'
                mf.display(msg)
                expect_msg = f"Expect info: Name: {Name}\tDescription: {expected_pcie_check_dict[check_Description]},FW:{expected_pcie_check_dict[check_FirmwareVersion]}"
                actual_msg = f"Actual info: Name: {Name}\tDescription: {Description},FW:{FirmwareVersion}"
                check_result = [
                    Description == expected_pcie_check_dict[check_Description],
                    FirmwareVersion == expected_pcie_check_dict[check_FirmwareVersion]

                ]
                if expected_pcie_check_dict.get('check_DeviceLocator', None):
                    check_result.append(expected_pcie_check_dict[check_DeviceLocator] in DeviceLocator)
                if not all(check_result):
                    mf.display(expect_msg)
                    mf.display(actual_msg)
                    if not FirmwareVersion:
                        msg = "\t".join((expect_msg, actual_msg))
                        self.append_to_errorlogs("PCIE", msg)
                        check_pci_result = "FAILED"
                    # pdb.set_trace()
                else:
                    msg = f"check {Name} and the result is PASSED"
                    mf.display(msg)

                return [Name, Description, Manufacturer, FirmwareVersion, DeviceLocator, Position, check_pci_result]

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
        name = rsp['Oem']['Huawei']['Name']
        # pdb.set_trace()
        oem_info = rsp['Oem']['Huawei']
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
        port_info = rsp['Oem']['Huawei']
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

    def post_content(self, url):
        rsp = self.client.post(url).dict
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
            # Status ->>> {'State': 'Absent',
            if psu['Status']['State'] == 'Absent':
                msg = 'a Empty PSU slot or PSU not install correctlly'
                mf.display(msg)
                continue
            Name = psu['Name']
            Type = psu['PowerSupplyType']
            PowerCapacityWatts = psu['PowerCapacityWatts']
            Model = psu['Model']
            FirmwareVersion = psu['FirmwareVersion']
            SerialNumber = psu['SerialNumber']
            pn = psu['PartNumber']
            record = [Name, Type, PowerCapacityWatts, Model, FirmwareVersion, SerialNumber, pn]

            if expected_psu_check:
                model_result = (Model == expected_psu_check_dict['expected_psu_model'])
                powerCapacity_result = (PowerCapacityWatts == expected_psu_check_dict['expected_psu_watts'])
                firmware_result = (FirmwareVersion == expected_psu_check_dict['expected_psu_fw'])
                if not all([model_result, powerCapacity_result, firmware_result]):
                    msg = f" model_result : {model_result},  powerCapacity_result:{powerCapacity_result}  ,   firmware_result{firmware_result}"
                    mf.display(msg)
                    expected_item = f"expect PSU: PSU Model:{expected_psu_check_dict['expected_psu_model']}, PSU_Watts:{expected_psu_check_dict['expected_psu_watts']},PSU_FW:{expected_psu_check_dict['expected_psu_fw']}"
                    mf.display(expected_item)
                    actual_item = f" Actual PSU: PSU Model: {Model}, PSU_Watts: {PowerCapacityWatts}, PSU_FW: {FirmwareVersion} "
                    mf.display(actual_item)
                    # pdb.set_trace()
                    raise Exception(msg)
            psu_tables.append(record)
        if len(psu_tables) != expected_psu_counts:
            msg = f"PSU counts mismatch ,{expected_psu_counts}  PSU should be installed but we found {len(psu_tables)} installed "
            raise Exception(msg)

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
            if rsp['Oem'].get('Huawei', None):
                if 'HealthEvent' in rsp['Oem']['Huawei'].keys():
                    alert_num = len(rsp['Oem']['Huawei']['HealthEvent'])
                    if alert_num:
                        table = []
                        headers = ['Severity', 'Level', 'EventId', 'Message']
                        logging.warning("WARNING".center(70, '*'))
                        msg = "we found {} alert message ,please double check before continue".format(alert_num)
                        logging.warning(msg)
                        for msg_dict in rsp['Oem']['Huawei']['HealthEvent']:
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

    def get_raid_controller(self):
        url = '/redfish/v1/Chassis/1/Boards'
        rsp = self.get_content(url)
        pdb.set_trace()

    def query_task_state(self, task_id):
        """
        /redfish/v1/TaskService/Tasks/taskid

        """
        url = '/redfish/v1/TaskService/Tasks/' + task_id
        rsp = self.get_content(url)
        if 'Completed' in rsp['TaskState']:
            msg = f"Task ID {task_id} completed"
            mf.display(msg)
            return True
        else:
            msg = f"Task ID {task_id} now in {rsp['TaskState']} state ,please wait"
            mf.display(msg)
            return False

    def download_via_https(self, file):
        url = "/redfish/v1/Managers/1/Actions/Oem/Huawei/Manager.GeneralDownload"
        body = {"TransferProtocol": "HTTPS",
                "Path": file}
        target_diag_file = file.split('/')[-1]
        rsp = self.client.post(url, body=body)
        # pdb.set_trace()
        with open(target_diag_file, 'wb') as fh:
            fh.write(rsp.read)

    def download_full_ffdc(self):
        """
        https://support.xfusion.com/support/#/zh/docOnline/DOC2020000341?path=zh-cn_topic_0000001139168127&relationId=DOC2020000343&mark=281
        expected_download_ffdc = True
        https://device_ip/redfish/v1/Managers/managers_id/Actions/Oem/xFusion/Manager.Dump
        /redfish/v1/Managers/1/Actions/Oem/xFusion/Manager.Dump
        """
        if not expected_download_ffdc:
            msg = "no full log download requirement ,skip ..."
            logging.info(msg)
        else:
            msg = "expect to download the FFDC for future usage purpose .now try to download the info "
            url = '/redfish/v1/Managers/1/Actions/Oem/Huawei/Manager.Dump'
            file = '2288h6_' + self.sn + '.tar.gz'
            self.content = '/tmp/web/' + file
            mf.display(self.content)
            body = {'Type': 'URI',
                    'Content': self.content}
            # body_json = json.dumps(body)
            headers = {'Content-Type': 'application/json'}
            # print(type(body_json))
            # header = {
            #     X-Auth-Token: self.client.get_authorization_key(),
            #     Content-Type: 'application/json'
            # }
            rsp = self.client.post(url, body=body).dict
            task_id = rsp['Id']

            time.sleep(10)
            # time_1 = 10
            # for i in range(20):
            for i in range(1, 20):
                msg = f"now sleep {i * 10} seconds ,check the FFDC is ready to download or not"
                mf.display(msg)
                if self.query_task_state(task_id):
                    self.download_via_https(self.content)
                    break
                time.sleep(10)
            else:
                msg = "not ready to download the logs "
                mf.display(msg)
                return
            msg = f"file downloaded ,please check in current directory {file}"
            mf.display(msg)
            return None

            #     msg = "sleep {} seconds,now checking the FFDC status if complete or not ".format(10 + i * 10)
            #     mf.display(msg)
            #     rsp = self.client.post(url,body=body,headers=headers)
            #     pdb.set_trace()
            #     if "Completed" in rsp["TaskState"]:
            #         msg = "log collection is complete ,ready to download the FFDC now"
            #         mf.display(msg)
            #         pdb.set_trace()
            #         break
            #     else:
            #         msg = "log collection is not in complete state ,wait ..."
            #         mf.display(msg)
            # ready to try to do the download

    def get_all_extension_boards(self):

        self.chassisMainboard = []
        self.mainboardRAIDCard = []
        self.mainboardRiserCard = []
        self.chassisDiskBP = []
        self.MainboardOCPCard = []

        url = '/redfish/v1/Chassis/1/Boards'
        result = self.get_content(url)
        """
        [{'@odata.id': '/redfish/v1/Chassis/1/Boards/chassisMainboard'}, 
        {'@odata.id': '/redfish/v1/Chassis/1/Boards/mainboardRAIDCard1'},
         {'@odata.id': '/redfish/v1/Chassis/1/Boards/mainboardRiserCard1'},
          {'@odata.id': '/redfish/v1/Chassis/1/Boards/mainboardRiserCard3'},
           {'@odata.id': '/redfish/v1/Chassis/1/Boards/chassisDiskBP1'}, 
           {'@odata.id': '/redfish/v1/Chassis/1/Boards/MainboardOCPCard1(GE350-T2)'}]
(Pdb)
        """
        if result['Members']:
            for item in result['Members']:
                v = item['@odata.id']
                if 'chassisMainboard' in v:
                    self.chassisMainboard.append(v)
                elif 'mainboardRAIDCard' in v:
                    self.mainboardRAIDCard.append(v)
                elif 'MainboardOCPCard' in v:
                    self.MainboardOCPCard.append(v)
                elif 'chassisDiskBP' in v:
                    self.chassisDiskBP.append(v)
                elif 'mainboardPCIeRiser1' in v:
                    self.mainboardRiserCard.append(v)
                elif  'mainboardPCIeRiser2' in v:
                    self.mainboardRiserCard.append(v)
                elif 'mainboardPCIeRiser3' in v:
                    self.mainboardRiserCard.append(v)

    def get_raidcard_info(self):
        """
        DeviceLocator ->>> RAIDCard1
        DeviceType ->>> RAIDCard
        Location ->>> mainboard
        Manufacturer ->>> XFUSION
        ProductName ->>> XR450C-MX 2G
        SerialNumber ->>> 027XWQXENC002432
        PartNumber ->>> 03027XWQ
        AssetTag ->>> None
        CPLDVersion ->>> 0.18
        PCBVersion ->>> .B
        BoardName ->>> BC11RLCH
        BoardId ->>> 0x0020
        ManufactureDate ->>> 2022/12/15 Thu 13:36:00
        AssociatedResource ->>> CPU1
        PositionId ->>> None
        PowerWatts ->>> None
        SupportedRAIDLevels ->>> RAID(0/1/10/5/50/6/60)

        """
        mf.display(mf.create_section("check RAID adapters"))
        if self.mainboardRAIDCard:
            raidcard_table = []
            header = ['DeviceLocator', 'ProductName', 'SerialNumber', 'PartNumber', 'CPLDVersion', 'BoardName',
                      'AssociatedResource']
            for url in self.mainboardRAIDCard:
                rsp = self.get_content(url)
                DeviceLocator = rsp['DeviceLocator']
                ProductName = rsp['ProductName']
                SerialNumber = rsp['SerialNumber']
                PartNumber = rsp['PartNumber']
                CPLDVersion = rsp['CPLDVersion']
                BoardName = rsp['BoardName']
                AssociatedResource = rsp['AssociatedResource']
                raidcard_table.append(
                    (DeviceLocator, ProductName, SerialNumber, PartNumber, CPLDVersion, BoardName, AssociatedResource))

            tables = mf.create_table(header, raidcard_table)
            mf.display(tables)
        else:
            msg = "No RAID Controller Fund in BMC"
            mf.display(msg)

    def get_riser_info(self):
        """
        Id ->>> mainboardRiserCard3
        Description ->>> Riser(X8*2)
        Name ->>> mainboardRiserCard3
        CardNo ->>> 3
        Status ->>> {'State': 'Enabled', 'Severity': 'Informational', 'Health': 'OK'}
        DeviceLocator ->>> RiserCard3
        DeviceType ->>> PCIeRiserCard
        Location ->>> mainboard
        Manufacturer ->>> XFUSION
        ProductName ->>> None
        SerialNumber ->>> None
        PartNumber ->>> 03026BUX
        AssetTag ->>> None
        CPLDVersion ->>> None
        PCBVersion ->>> .B
        BoardName ->>> BC13PRUS
        BoardId ->>> 0x0040
        ManufactureDate ->>> None

        """
        if self.mainboardRiserCard:
            tables = []
            header = ['Id', 'Description', 'DeviceLocator', 'PartNumber', 'BoardName']
            for url in self.mainboardRiserCard:
                rsp = self.get_content(url)
                Description = rsp['Description']
                DeviceLocator = rsp['DeviceLocator']
                PartNumber = rsp['PartNumber']
                BoardName = rsp['BoardName']
                Id = rsp['Id']
                tables.append((Id, Description, DeviceLocator, PartNumber, BoardName))
            #
            riser_tables = mf.create_table(header, tables)
            mf.display(riser_tables)
            # breakpoint()




        else:
            msg = "   ************    no riser card found ...   ************    "
            mf.display(msg)

    def get_mainboard_info(self):
        """
        Id ====> chassisMainboard
        Description ====> MainBoard
        Name ====> chassisMainboard
        CardNo ====> 0
        Status ====> {'State': 'Enabled', 'Severity': 'Informational', 'Health': 'OK'}
        DeviceLocator ====> Mainboard
        DeviceType ====> MainBoard
        Location ====> chassis
        Manufacturer ====> XFUSION
        ProductName ====> 2288H V6
        SerialNumber ====> 029UKSXDNA012556
        PartNumber ====> 03029UKS
        AssetTag ====> None
        CPLDVersion ====> 2.08(U34)
        PCBVersion ====> .A
        BoardName ====> BC13MBSBC
        BoardId ====> 0x00b1
        ManufactureDate ====> 2023/01/12 Thu 22:13:00
        AssociatedResource ====> None
        PositionId ====> None
        PowerWatts ====> None
        SupportedRAIDLevels ====> None
        PchModel ====> LBG PCH S2 - LBG QS/PRQ - C621A

        """
        mf.display(mf.create_section("check Planar Info"))
        if self.chassisMainboard:
            tables = []
            header = ['Description', 'ProductName', 'SerialNumber', 'BoardName', 'PartNumber']
            for url in self.chassisMainboard:
                rsp = self.get_content(url)
                Description = rsp['Description']
                ProductName = rsp['ProductName']
                SerialNumber = rsp['SerialNumber']
                BoardName = rsp['BoardName']
                PartNumber = rsp['PartNumber']
                tables.append((Description, ProductName, SerialNumber, BoardName, PartNumber))
            mb_tables = mf.create_table(header, tables)
            mf.display(mb_tables)
        else:
            msg = "   ************    no  motherboard found ...   ************    "
            mf.display(msg)
            raise Exception(msg)

    def get_diskbp_info(self):
        """
        Id ->>> chassisDiskBP1
        Description ->>> 12*3.5 SAS/SATA, Expander
        Name ->>> chassisDiskBP1
        CardNo ->>> 1
        Status ->>> {'State': 'Enabled', 'Severity': 'Informational', 'Health': 'OK'}
        DeviceLocator ->>> DiskBP1
        DeviceType ->>> DiskBackplane
        Location ->>> chassisFront
        Manufacturer ->>> XFUSION
        ProductName ->>> None
        SerialNumber ->>> None
        PartNumber ->>> 0302Y255
        AssetTag ->>> None
        CPLDVersion ->>> 1.03
        PCBVersion ->>> .A
        BoardName ->>> BC11THBQC
        BoardId ->>> 0x0073
        ManufactureDate ->>> None
        AssociatedResource ->>> None
        PositionId ->>> U3
        PowerWatts ->>> None
        SupportedRAIDLevels ->>> None
        PchModel ->>> None
        LinkWidthAbility ->>> None
        LinkSpeedAbility ->>> None
        LinkWidth ->>> None
        LinkSpeed ->>> None
        WorkMode ->>> None
        M2Device1Presence ->>> None
        M2Device2Presence ->>> None
        RetimerVersion ->>> None

        """
        mf.display(mf.create_section("check Disk BackPlane"))
        tables = []
        header = ['Name', 'Description', 'DeviceLocator', 'PartNumber', 'BoardName']
        if self.chassisDiskBP:
            for url in self.chassisDiskBP:
                rsp = self.get_content(url)
                Name = rsp['Name']
                Description = rsp['Description']
                DeviceLocator = rsp['DeviceLocator']
                PartNumber = rsp['PartNumber']
                BoardName = rsp['BoardName']
                tables.append((Name, Description, DeviceLocator, PartNumber, BoardName))
            bp_tables = mf.create_table(header, tables)
            mf.display(bp_tables)
        else:
            msg = "   ************    no  BackPlane found ...   ************    "
            mf.display(msg)
            raise Exception(msg)

    # def get_fru_info(self):
    #     cmd = r'c:\ipmitool\ipmitool.exe -I lanplus -H 192.168.2.100 -U Administrator -P Admin@9000 fru list'.split()
    #     rsp = run(cmd)
    #     mf.display(rsp)

    def get_ocp_info(self):
        """
        Id ->>> MainboardOCPCard1(GE350-T2)
        Description ->>> I350 Gigabit Network Connection
        Name ->>> MainboardOCPCard1(GE350-T2)
        CardNo ->>> 1
        Status ->>> {'State': 'Enabled', 'Severity': 'Informational', 'Health': 'OK'}
        DeviceLocator ->>> OCPCard1(GE350-T2)
        DeviceType ->>> OCPCard
        Location ->>> Mainboard
        Manufacturer ->>> ATC
        ProductName ->>> GE350-T2
        SerialNumber ->>> 026HUAX6NB000951
        PartNumber ->>> 03026HUA
        AssetTag ->>> None
        CPLDVersion ->>> None
        PCBVersion ->>> .B
        BoardName ->>> BC51ETHJ
        BoardId ->>> None
        ManufactureDate ->>> 2022/11/08 Tue 00:00:00
        AssociatedResource ->>> CPU1
        PositionId ->>> None
        PowerWatts ->>> None
        SupportedRAIDLevels ->>> None
        PchModel ->>> None
        LinkWidthAbility ->>> None
        LinkSpeedAbility ->>> None
        LinkWidth ->>> None
        LinkSpeed ->>> None
        WorkMode ->>> None
        M2Device1Presence ->>> None
        M2Device2Presence ->>> None
        RetimerVersion ->>> None
        """
        mf.display(mf.create_section("check OCP adapters"))
        tables = []
        header = ['Name', 'Description', 'DeviceLocator', 'SerialNumber', 'PartNumber', 'BoardName',
                  'AssociatedResource']
        if self.MainboardOCPCard:
            for url in self.MainboardOCPCard:
                rsp = self.get_content(url)
                Name = rsp['Name']
                Description = rsp['Description']
                DeviceLocator = rsp['DeviceLocator']
                PartNumber = rsp['PartNumber']
                BoardName = rsp['BoardName']
                SerialNumber = rsp['SerialNumber']
                AssociatedResource = rsp['AssociatedResource']
                tables.append(
                    (Name, Description, DeviceLocator, SerialNumber, PartNumber, BoardName, AssociatedResource))
            ocp_tables = mf.create_table(header, tables)
            mf.display(ocp_tables)
        else:
            msg = "   ************    no  OCP cards found ...   ************    "
            mf.display(msg)
            # raise Exception(msg)

    # def get_riser_info(self):
    #     url = '/redfish/v1/Chassis/1/Boards'
    #     rsp  = self.get_content(url)
    #     breakpoint()


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
