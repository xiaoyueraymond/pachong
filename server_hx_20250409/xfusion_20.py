# this file is use to detect the configuration hardware from this file VS the real configure from the systems
#
# FW　version Check
expected_version_check = False
expected_fw_version = {
    'BMC_version': '',
    'UEFI_Version': ''

}

#   cpu configure check
expected_cpu_check = True
expected_cpu_counts = 2
expected_cpu_check_dict = {

    'expected_cpu_model': 'Intel(R) Xeon(R) Gold 5320 CPU @ 2.20GHz',
    'expected_cpu_core': 26,
    'expected_cpu_thread': 52
}

# 2 memory configure check
expected_memory_check = True
# 
# expected_memory_locators = ['DIMM000', 'DIMM010', 'DIMM020', 'DIMM030', 'DIMM040', 'DIMM050', 'DIMM060', 'DIMM070',
#                             'DIMM100', 'DIMM110', 'DIMM120', 'DIMM130', 'DIMM140', 'DIMM150', 'DIMM160', 'DIMM170']
expected_memory_locators = ['DIMM000',  'DIMM020',  'DIMM040',  'DIMM060',
                            'DIMM100',  'DIMM120',  'DIMM140',  'DIMM160', ]
expected_memory_check_dict = {
    'expected_memory_counts': 8,  # 安装内存的条数
    'expected_memory_brands': ['Samsung'],  # 内存的品牌
    'expected_memory_same_vendor': True,  # 是否检查是同一个品牌，默认不检查 ，即支持混插
    'expected_memory_size': [32768, ],  # 检查内存的容量
    'expected_memory_operation_speed': 2933,  # 检查内存的工作频率
    'expected_memory_ranks': 2
}

# expected PSU
expected_psu_check = True
expected_psu_counts = 2  # 检查安装的PSU的个数
expected_psu_check_dict = {

    'expected_psu_fw': 'DC:102 PFC:102',
    'expected_psu_model': 'PAC2000S12-B1',
    'expected_psu_watts': 2000
}

expected_pcie_check = True
expected_pcie_check_dict = {

    'PCIeCard1': False,
    'PCIeCard1_Description': 'MT27800 Family [ConnectX-5]',
    'PCIeCard1_FirmwareVersion': '16.31.2006',
    'PCIeCard1_DeviceLocator': 'MCX512A-ACUT',

    #
    'PCIeCard2': False,
    'PCIeCard2_Description': 'LPe32002-M2 2-Port 32Gb Fibre Channel Adapter',
    'PCIeCard2_FirmwareVersion': '12.8.351.47',
    #
    'PCIeCard3': True,
    'PCIeCard3_Description': 'MT27800 Family [ConnectX-5]',
    'PCIeCard3_FirmwareVersion': '16.31.2006',
    'PCIeCard3_DeviceLocator': 'MCX512A-ACUT',

    'PCIeCard4': False,
    'PCIeCard4_Description': 'MT27800 Family [ConnectX-5]',
    'PCIeCard4_FirmwareVersion': '16.31.2006',
    'PCIeCard4_DeviceLocator': 'MCX512A-ACUT',

    'PCIeCard5': False,
    'PCIeCard5_Description': '',
    'PCIeCard6_FirmwareVersion': '',

    'PCIeCard7': False,
    'PCIeCard7_Description': '',
    'PCIeCard7_FirmwareVersion': '',

    'PCIeCard8': False,
    'PCIeCard8_Description': '',
    'PCIeCard8_FirmwareVersion': '',

    'OCPCard1': True,
    'OCPCard1_Description': 'I350 Gigabit Network Connection',
    'OCPCard1_FirmwareVersion': None,

    'OCPCard2': False,
    'OCPCard2_Description': '',
    'OCPCard2_FirmwareVersion': ''
}

#
#  #  'Name'  |           'Model'            | 'Revision' |    'Size'     | 'Protocol' |        'SN'        |        'Speed'         #
# 2024-06-03 15:26:52 - INFO - #=================================================================================================================================#
# 2024-06-03 15:26:52 - INFO - # 'Disk0'  | 'SAMSUNG MZ7L3480HCHQ-00B7C' | 'JXTC404Q' | 503424483328  | 'SATA'     | 'S6KLNN0X237725'   | ['NegotiatedSpeedGbs'] #
# 2024-06-03 15:26:52 - INFO - # 'Disk4'  | 'HWE62P447T6L00LN'           | '1015'     | 7681500774400 | 'PCIe'     | '035HBAD9Q4000845' | ['NegotiatedSpeedGbs'] #
expected_disk_check = True
expected_disk_counts = 13
expected_disk_check_dict = {
    'Disk0':('SAMSUNG MZ7L3480HCHQ-00B7C',503424483328,'SATA'),
    'Other': ('HWE62P447T6L00LN', 7681500774400, 'PCIe')
}

expected_download_ffdc = False
