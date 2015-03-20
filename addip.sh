#!/bin/bash
# A small program for add ip
# Author: jing.ma@chinacache.com

. /etc/rc.d/init.d/functions

function usage() {
    cat << eof
A small program for add new ip automatic.

Usage: addip [-s|--start the_first_ip] [-m|--mask netmask] [-n{" "|number}]

Description
    -s, --start     first of the new ips.
    -m, --mask      the netmask of the new ips.
    -n, --number    the number you want to add begin the_first_ip to count, default 1 if no number given.

Report bugs to <jing.ma@chinacache.com>.
eof
    exit 1
}

function check() {
    local newip=$1
    if ip -o a s eth0:* | grep -Pqo "(?<=inet )$newip";then
        action "$newip being used by localhost" /bin/false
        return 1
    elif ping $newip -i 0.1 -c 2 >/dev/null 2>&1;then
        action "$newip being used by other host" /bin/false
        return 1
    else
        return 0
    fi
}

function addip() {
    local newip=$1
    local netmask=$2
    local nic=$3
    cd /etc/sysconfig/network-scripts
    \cp -f ifcfg-eth0 ifcfg-$nic
    sed -i "s/^DEVICE=\(.*\)$/DEVICE=$nic/" ifcfg-$nic
    sed -i "s/^IPADDR=\(.*\)$/IPADDR=$newip/" ifcfg-$nic
    sed -i "s/^NETMASK=\(.*\)$/NETMASK=$netmask/" ifcfg-$nic
    sed -i '/GATEWAY\|NETWORK\|BROADCAST/d' ifcfg-$nic
    ifup $nic
    ping -I $newip 8.8.8.8 -i 0.1 -c 2 >/dev/null 2>&1 && \
        action "$newip at $nic configure" /bin/true || action "$newip at $nic configure" /bin/false
}

[ $# -lt 4 ] && usage
TEMP=`getopt -a -o s:m:n::h -l start:,mask:,number::,help -- "$@"`
[ $? -ne 0 ] && usage

eval set -- "$TEMP"

declare -i count=1

while true
do
    case $1 in
        -s|--start)
            first_ip="$2"
            shift
            ;;
        -m|--mask)
            netmask="$2"
            shift 
            ;;
        -n|--number)
            case $2 in
                "") count=1;shift;;
                *) count="$2";shift;;
            esac
            ;;
        -h|--help)
            usage
            ;;
        --)
            shift
            break
            ;;
    esac
    shift
done

eth0_num=`ip a s dev eth0 scope global | awk 'END {if($NF!~/eth0$/) {split($NF,a,":");print a[2]} else print 0}'`
start_eth0_num=$((eth0_num+1))
end_eth0_num=`expr $eth0_num + $count`

for((i=start_eth0_num,j=0;i<=end_eth0_num,j<count;i++,j++))
do
    next_ip=`echo $first_ip | awk -v inter=$j 'BEGIN {FS=OFS="."} {print $1,$2,$3,$4+inter}'`
    check $next_ip && addip $next_ip $netmask eth0:$i || i=$((i-1));continue
done
