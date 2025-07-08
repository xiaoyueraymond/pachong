#!/bin/bash
#
#
echo -e "检查日志信息"
#
#
cwd=$(pwd)
cd ${cwd}
for i in *.tar.gz
do
        echo $i
        name=$(echo ${i}|cut -d_ -f2)
        echo ${name}
        echo -e "准备检查节点${name}"
        mkdir -p ${name}
        rm -fr ${name}/*
        cd ${name}
                tar xf ../${i}
                echo -e  "\n1:\t检查CPU"
                grep -i 6254  dump_info/RTOSDump/versioninfo/server_config.txt
                echo -e  "\n2:\t检查内存"
                grep -i 65536  dump_info/RTOSDump/versioninfo/server_config.txt
                grep Kingston dump_info/RTOSDump/versioninfo/server_config.txt  >/dev/null
                if [ $? -eq 0 ];then
                        echo -e "${name}  have wrong memory installed "
                fi
                echo -e  "\n3:\t检查硬盘\n\n"
                grep -A11 MZ7LH960HAJR-00005  dump_info/RTOSDump/versioninfo/server_config.txt

                echo -e  "\n4:\t检查RAID卡"
                grep -i 450C  dump_info/RTOSDump/versioninfo/server_config.txt
                echo -e  "\n5:\t检查电源"
                grep -i PAC900S12-B2  dump_info/RTOSDump/versioninfo/server_config.txt
                echo -e  "\n6:\t检查RISER 卡"
                grep -i Riser  dump_info/RTOSDump/versioninfo/server_config.txt
                echo -e  "\n7:\t检查电容BBU"
                grep -A2 'BBU Status'  dump_info/RTOSDump/versioninfo/server_config.txt
                echo -e  "\n8:\t检查风扇"
                grep -i Fan  dump_info/RTOSDump/versioninfo/server_config.txt
                echo -e  "\n9:\t检查PCIE网卡"
                grep -i MCX4121A-XCAT  dump_info/RTOSDump/versioninfo/server_config.txt
                echo -e "\n10:\t检查硬盘背板"
                grep -i BC11THBHB1  dump_info/RTOSDump/versioninfo/server_config.txt
                echo -e "\n11:\t检查LOM卡信息"
                cat dump_info/LogDump/netcard/netcard_info.txt |grep -A14 -B2 'ProductName     :LOM'|tail -n 17
                echo -e "\n12:\t检查BIOS版本"
                cat dump_info/RTOSDump/versioninfo/app_revision.txt |grep BIOS
                echo -e "\n13:\t检查iBMC版本"
                cat dump_info/RTOSDump/versioninfo/app_revision.txt |grep 'Active iBMC     Version:'
                echo -e "\n\n\n\n\n\n"
       cd ..


done
