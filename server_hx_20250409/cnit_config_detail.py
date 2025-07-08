# this file is use to detect the configuration hardware from this file VS the real configure from the systems
#
# FW　version Check
expected_bmc_ver_check = True
expected_bios_ver_check = True
# expected_version_check = False
expected_fw_version = {
    'BMC_version':  '1.04.05',
    'BIOS_version': '1.10.07'

}

#   cpu configure check
expected_cpu_check = True
expected_cpu_counts = 2
expected_cpu_check_dict = {

    'expected_cpu_model': 'Intel(R) Xeon(R) Gold 6330 CPU @ 2.00GHz',
    'expected_cpu_core': 28,
    'expected_cpu_thread': 56
}

# 2 memory configure check
expected_memory_check = True
#
expected_memory_locators = ['130','070']
# expected_memory_locators = ['DIMM000', 'DIMM010', 'DIMM020', 'DIMM030', 'DIMM040', 'DIMM050', 'DIMM060', 'DIMM070',
#                             'DIMM100', 'DIMM110', 'DIMM120', 'DIMM130', 'DIMM140', 'DIMM150', 'DIMM160', 'DIMM170']

# expected_memory_locators = ['DIMM000',   'DIMM020',   'DIMM040',   'DIMM060',    'DIMM100' , 'DIMM120',    'DIMM140',   'DIMM160' ]
expected_memory_check_dict = {
    'expected_memory_counts': 2,  # 安装内存的条数
    'expected_memory_brands': ['Hynix'],  # 内存的品牌
    'expected_memory_same_vendor': False,  # 是否检查是同一个品牌，默认不检查 ，即支持混插
    'expected_memory_size': [32,64 ],  # 检查内存的容量,不建议混插容量不同的
    'expected_memory_operation_speed': 2933,  # 检查内存的工作频率
    'expected_memory_ranks': 2
}

# expected PSU
expected_psu_check = True
expected_psu_counts = 2  # 检查安装的PSU的个数
expected_psu_check_dict = {

    'expected_psu_fw': '1.000',
    'expected_psu_model': 'CRPS2000D2',
    'expected_psu_watts': 2000
}

expected_pcie_check = True
expected_pcie_installed_number = 2
expected_pcie_check_dict = {

    'PCIeCard1': True,
    'PCIeCard1_Description': 'MT27800 Family [ConnectX-5]',
    'PCIeCard1_FirmwareVersion': '16.31.2006',
    'PCIeCard1_DeviceLocator': 'MCX512A-ACUT',

    #
    'PCIeCard2': False,
    'PCIeCard2_Description': 'LPe32002-M2 2-Port 32Gb Fibre Channel Adapter',
    'PCIeCard2_FirmwareVersion': '12.8.351.47',
    #
    'PCIeCard3': False,
    'PCIeCard3_Description': '',
    'PCIeCard3_FirmwareVersion': '',

    'PCIeCard4': True,
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
expected_disk_check = False
# expected_disk_check = True
expected_disk_counts = 1
expected_disk_check_dict = {
    'Disk0':('SAMSUNG MZ7L3480HCHQ-00B7C',503424483328,'SATA'),
    # 'Other': ('HWE62P447T6L00LN', 7681500774400, 'PCIe')
}


expected_download_ffdc = False
