#!/bin/bash
#
#!/bin/bash

# 检查是否提供了关键字参数
if [ $# -eq 0 ]; then
    echo "Usage: $0 <keyword>"
    exit 1
fi

# 提取关键字参数
keyword="$1"

# 使用 ipmitool 删除包含关键字的 SEL 日志条目
ipmitool sel elist | grep "$keyword" | while read -r line; do
    entry_id=$(echo "$line" | awk '{print $1}')
    ipmitool sel delete "0x$entry_id"
    echo "Deleted SEL log entry with keyword '$keyword'"
done
