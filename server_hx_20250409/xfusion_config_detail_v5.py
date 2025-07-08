# this file is use to detect the configuration hardware from this file VS the real configure from the systems
# for V5 version only
# FW　version Check
expected_bmc_ver_check = True
expected_bios_ver_check = True
# expected_version_check = False
expected_fw_version = {
    'BMC_version':  '6.84',
    'BIOS_version': '8.56'

}

#   cpu configure check
expected_cpu_check = True
expected_cpu_counts = 2
expected_cpu_check_dict = {

    'expected_cpu_model': 'Intel(R) Xeon(R) Gold 6248R CPU @ 3.00GHz',
    'expected_cpu_core': 24,
    'expected_cpu_thread': 48
}

# 2 memory configure check
expected_memory_check = True
# 
# expected_memory_locators = ['DIMM000', 'DIMM010', 'DIMM020', 'DIMM030', 'DIMM040', 'DIMM050',
#                             'DIMM100', 'DIMM110', 'DIMM120', 'DIMM130', 'DIMM140', 'DIMM150' ]
expected_memory_locators = ['DIMM000', 'DIMM100']
                            
# expected_memory_locators = ['DIMM000',   'DIMM020',   'DIMM040',   'DIMM060',    'DIMM100' , 'DIMM120',    'DIMM140',   'DIMM160' ]
expected_memory_check_dict = {
    'expected_memory_counts': 2,  # 安装内存的条数
    'expected_memory_brands': ['Samsung'],  # 内存的品牌
    'expected_memory_same_vendor': True,  # 是否检查是同一个品牌，默认不检查 ，即支持混插
    'expected_memory_size': [65536, ],  # 检查内存的容量
    'expected_memory_operation_speed': 2933,  # 检查内存的工作频率
    'expected_memory_ranks': 2
}

# expected PSU
expected_psu_check = True
expected_psu_counts = 2  # 检查安装的PSU的个数
expected_psu_check_dict = {

    'expected_psu_fw': 'DC:131 PFC:131',
    'expected_psu_model': 'PAC900S12-BW',
    'expected_psu_watts': 900
}

expected_pcie_check = True
expected_pcie_installed_number = 2
expected_pcie_check_dict = {

    'PCIeCard1': True,
    'PCIeCard1_Description': 'MT27800 Family [ConnectX-5]',
    'PCIeCard1_FirmwareVersion': '16.28.1002',
    'PCIeCard1_DeviceLocator': 'PCIe Card 1 (SP382)',

    #
    'PCIeCard2': True,
    'PCIeCard2_Description': 'MT27800 Family [ConnectX-5]',
    'PCIeCard2_FirmwareVersion': '16.28.1002',
    'PCIeCard2_DeviceLocator': 'PCIe Card 2 (SP382)',
    #
    'PCIeCard3': False,
    'PCIeCard3_Description': '',
    'PCIeCard3_FirmwareVersion': '',

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
expected_disk_check = True
# expected_disk_check = True
expected_disk_counts = 1
expected_disk_check_dict = {
    'Disk0':(None,None,'SATA/SAS'),
    # 'Other': ('HWE62P447T6L00LN', 7681500774400, 'PCIe')
}


expected_download_ffdc = False
