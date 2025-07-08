from mytools import *
import logging
logfile = get_testlog_file()
setup_logger(logfile)
logging.info("******Start Hardwar Information Collection******")
#
import pdb
# pdb.set_trace()
mem_info =  get_mem_info()
def log_memory():
    header =  "{}\t{}\t{}\t{}\t{}\t{}".format('Size','Locator','Speed','Manufacturer','Serial Number','Part Number')
    log_line("Check Memory Info")
    logging.info(header)
    for mem in mem_info:
        msg = "{}\t{}\t{}\t{}\t{}\t{}".format(mem['Size'], mem['Locator'], mem['Speed'], mem['Manufacturer'], mem['Serial Number'], mem['Part Number'])
        logging.info(msg)
    log_line(_type=0)

def log_cpu():
    cpu_info = get_cpu_info()
    #pdb.set_trace()
    log_line("Check CPU　Info")
    header = "{}\t{}\t{}\t{}".format('Socket',  'Version', 'Core Count' ,   'Thread Count' )
    logging.info(header)
    for cpu in cpu_info:
        msg = "{}\t{}\t{}\t{}".format(cpu['Socket Designation'],  cpu['Version'], cpu['Core Count'] ,   cpu['Thread Count'] ) 
        logging.info(msg)
    log_line(_type=0)

def log_ocp():
    """
     {'Reference Designation': 'Onboard OCP2 Port 0', 'Type': 'Ethernet', 'Status': 'Enabled', 'Type Instance': '5', 'Bus Address': '0000:81:00.0', 'Physical Slot': '49', 'LnkSta': 'Speed 16GT/s (ok), Width x8 (ok)', 'Product Name': 'Intel(R) Ethernet Controller E810-XXVAM2'}
    """
    ocp_info = get_ocp_info()
    log_line("Check OCP　Adapter info",True)
    header ="{}\t{}\t{}\t{}\t{}\t{}".format('Reference Designation', 'Type','Bus Address', 'Physical Slot','LnkSta','Product Name')
    logging.info(header)
    if not ocp_info:
        msg = "\033[31m**** NO OCP CARD Found in this Server**** \033[0m"
        logging.warning(msg)
    for record in ocp_info:
        link_status = record['LnkSta']
        if is_downgraded(link_status):
            link_status = '\033[31m' + link_status + "\033[0m"
        msg = "{}\t{}\t{}\t{}\t{}\t{}".format(record['Reference Designation'], record['Type'],record['Bus Address'],record[ 'Physical Slot'],link_status,record['Product Name'])
        logging.info(msg)
    
    log_line(_type=0)

def log_qlogic_fc_info():
    """
2a:00.0 Fibre Channel: QLogic Corp. ISP2684 (rev 01)
        Subsystem: QLogic Corp. Device 029d
        Physical Slot: 1
        Control: I/O- Mem- BusMaster- SpecCycle- MemWINV- VGASnoop- ParErr+ Stepping- SERR+ FastB2B- DisINTx-
        Status: Cap+ 66MHz- UDF- FastB2B- ParErr- DEVSEL=fast >TAbort- <TAbort- <MAbort- >SERR- <PERR- INTx-
        Interrupt: pin A routed to IRQ 255
        NUMA node: 0
        Region 0: Memory at 202fffe0b000 (64-bit, prefetchable) [disabled] [size=4K]
        Region 2: Memory at 202fffe06000 (64-bit, prefetchable) [disabled] [size=8K]
        Region 4: Memory at 202fffd00000 (64-bit, prefetchable) [disabled] [size=1M]
        Expansion ROM at a9ec0000 [disabled] [size=256K]
        Capabilities: [44] Power Management version 3
                Flags: PMEClk- DSI- D1- D2- AuxCurrent=0mA PME(D0-,D1-,D2-,D3hot-,D3cold-)
                Status: D0 NoSoftRst+ PME-Enable- DSel=0 DScale=0 PME-
        Capabilities: [4c] Express (v2) Endpoint, MSI 00
                DevCap: MaxPayload 2048 bytes, PhantFunc 0, Latency L0s <4us, L1 <1us
                        ExtTag- AttnBtn- AttnInd- PwrInd- RBE+ FLReset+ SlotPowerLimit 0.000W
                DevCtl: CorrErr+ NonFatalErr+ FatalErr+ UnsupReq-
                        RlxdOrd+ ExtTag- PhantFunc- AuxPwr- NoSnoop+ FLReset-
                        MaxPayload 512 bytes, MaxReadReq 4096 bytes
                DevSta: CorrErr+ NonFatalErr- FatalErr- UnsupReq+ AuxPwr- TransPend-
                LnkCap: Port #0, Speed 8GT/s, Width x8, ASPM L0s L1, Exit Latency L0s <512ns, L1 <2us
                        ClockPM- Surprise- LLActRep- BwNot- ASPMOptComp+
                LnkCtl: ASPM Disabled; RCB 64 bytes, Disabled- CommClk+
                        ExtSynch- ClockPM- AutWidDis- BWInt- AutBWInt-
                LnkSta: Speed 8GT/s (ok), Width x8 (ok)
                        TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
                DevCap2: Completion Timeout: Range B, TimeoutDis+ NROPrPrP- LTR-
                         10BitTagComp- 10BitTagReq- OBFF Not Supported, ExtFmt- EETLPPrefix-
                         EmergencyPowerReduction Not Supported, EmergencyPowerReductionInit-
                         FRS- TPHComp- ExtTPHComp-
                         AtomicOpsCap: 32bit- 64bit- 128bitCAS-
                DevCtl2: Completion Timeout: 50us to 50ms, TimeoutDis- LTR- OBFF Disabled,
                         AtomicOpsCtl: ReqEn+
                LnkCap2: Supported Link Speeds: 2.5-8GT/s, Crosslink- Retimer- 2Retimers- DRS-
                LnkCtl2: Target Link Speed: 8GT/s, EnterCompliance- SpeedDis-
                         Transmit Margin: Normal Operating Range, EnterModifiedCompliance- ComplianceSOS-
                         Compliance De-emphasis: -6dB
                LnkSta2: Current De-emphasis Level: -6dB, EqualizationComplete+ EqualizationPhase1+
                         EqualizationPhase2+ EqualizationPhase3+ LinkEqualizationRequest-
                         Retimer- 2Retimers- CrosslinkRes: unsupported
        Capabilities: [88] Vital Product Data
                Product Name: QLogic 16Gb 4-port FC to PCIe Gen3 x8 Adapter
                Read-only fields:
                        [PN] Part number: QTE2684
                        [SN] Serial number: RFD1537H34537
                        [EC] Engineering changes: BK3210405-01  A
                        [V9] Vendor specific: 011009
                        [RV] Reserved: checksum good, 0 byte(s) reserved
                End
        Capabilities: [90] MSI-X: Enable- Count=16 Masked-
                Vector table: BAR=2 offset=00000000
                PBA: BAR=2 offset=00001000
        Capabilities: [9c] Vendor Specific Information: Len=0c <?>
        Capabilities: [100 v1] Advanced Error Reporting
                UESta:  DLP- SDES- TLP- FCP- CmpltTO- CmpltAbrt- UnxCmplt- RxOF- MalfTLP- ECRC- UnsupReq- ACSViol-
                UEMsk:  DLP- SDES- TLP- FCP- CmpltTO- CmpltAbrt- UnxCmplt- RxOF- MalfTLP- ECRC+ UnsupReq+ ACSViol-
                UESvrt: DLP+ SDES+ TLP+ FCP+ CmpltTO- CmpltAbrt- UnxCmplt- RxOF+ MalfTLP+ ECRC- UnsupReq- ACSViol-
                CESta:  RxErr- BadTLP- BadDLLP- Rollover- Timeout- AdvNonFatalErr+
                CEMsk:  RxErr+ BadTLP+ BadDLLP+ Rollover+ Timeout+ AdvNonFatalErr+
                AERCap: First Error Pointer: 00, ECRCGenCap+ ECRCGenEn- ECRCChkCap+ ECRCChkEn-
                        MultHdrRecCap- MultHdrRecEn- TLPPfxPres- HdrLogCap-
                HeaderLog: 00000000 00000000 00000000 00000000
        Capabilities: [154 v1] Alternative Routing-ID Interpretation (ARI)
                ARICap: MFVC- ACS-, Next Function: 1
                ARICtl: MFVC- ACS-, Function Group: 0
        Capabilities: [1c0 v1] Secondary PCI Express
                LnkCtl3: LnkEquIntrruptEn- PerformEqu-
                LaneErrStat: 0
        Capabilities: [1f4 v1] Vendor Specific Information: ID=0001 Rev=1 Len=014 <?>

    """
    log_line("Check QLogic FC　Card")
    content = get_qlogic_fc_info()
    header = "{}\t{}\t{}\t{}\t{}".format('Fibre Channel','Physical Slot','LnkSta','Part number','Serial number')
    logging.info(header)
    for info in content:
        link_status = info['LnkSta']
        if is_downgraded(link_status):
            link_status = '\033[31m' + link_status + "\033[0m"
        msg = "{}\t{}\t{}\t{}\t{}".format(info['Fibre Channel'],info['Physical Slot'],link_status,info['[PN] Part number'],info['[SN] Serial number'])
        logging.info(msg)

    if not content:
        msg = "\033[31m**** NO QLogic FC　Card Found in this Server**** \033[0m"
        logging.warning(msg)

    log_line(_type=0)


def firmware_version():
    """
{'Firmware Component Name': 'BMC Firmware', 'Firmware Version': '3.02', 'Firmware ID': 'Not Specified', 'Release Date': 'Not Specified', 'Manufacturer': '157', 'Lowest Supported Firmware Version': 'Not Specified', 'Image Size': 'Unknown', 'Characteristics': '', 'Updatable': 'Yes', 'Write-Protect': 'No', 'State': 'Enabled', 'Associated Components': '1'}
(Pdb) interact
*interactive*
>>> get_bios_info()
[{'Vendor': 'American Megatrends International, LLC.', 'Version': '1.02.02', 'Release Date': '03/27/2024', 'Address': '0xF0000', 'Runtime Size': '64 kB', 'ROM Size': '64 MB', 'Characteristics': '', 'BIOS Revision': '5.32'}]
    """
    log_line("Check Firmware Version")
    bmc_ver  = get_bmc_info()
    bios_ver = get_bios_info()
    header = "Firmware \tVersion\tRelease Date"
    logging.info(header)
    bios_msg = "BIOS\t{}\t{}".format(bios_ver["Version"],bios_ver['Release Date'])
    bmc_msg  = "BMC\t{}\t{}".format(bmc_ver['Firmware Version'], bmc_ver['Release Date'])
    logging.info(bios_msg)
    logging.info(bmc_msg)
    log_line(_type=0)


def log_nvidia_gpu_info():
    """
     Tesla T4 supported

    """
    log_line("Check Nvidia GPU Info")
    gpu_info = get_nvidia_gpu_info()
    header = "{}\t{}\t{}\t{}\t{}".format('GPU Card', 'Physical Slot', 'LnkSta', 'Part number', 'Serial number')
    logging.info(header)
    content = get_nvidia_gpu_info()
    for info in content:
        link_status = info['LnkSta']
        if is_downgraded(link_status):
            link_status = '\033[31m' + link_status + "\033[0m"
        gpu_card =  info.get('3D controller','GPU Card')
        msg = "{}\t{}\t{}\t{}\t{}".format(gpu_card, info['Physical Slot'], link_status,
                                          "To be defind after nvidia driver install", "To be defined")

        logging.info(msg)

    if not content:
        msg = "\033[31m**** NO NVIDIA　Card Found in this Server**** \033[0m"
        logging.warning(msg)

    log_line(_type=0)
    # pdb.set_trace()



def main():
    log_nvidia_gpu_info()
    firmware_version()
    log_cpu()
    log_memory()
    log_ocp()
    log_qlogic_fc_info()



if __name__ == "__main__":
    main()
