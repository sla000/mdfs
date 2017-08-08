#!/bin/bash

. config
last=""
for name in $containers;
do
    last=$name
done

num=`echo $last | sed -e "s/$base//g"`
name="node0$((num+1))"
path=/var/lib/lxc
sudo cp -a $path/$last $path/$name

sed -i "s/containers=\"\(.*\)\"/containers=\"\1 $name\"/g" config

mac=`sudo grep -r 'hwaddr' $path/$last/config | sed -e 's/lxc.network.hwaddr = //g'`
newmac=`python -c "
mac='$mac'
last=mac.split(':')[-2:]
s = hex(int(''.join(last),16) +1).replace('0x', '')
s=s[0] + s[1] + ':' + s[2] + s[3]
tmp = ':'.join(last)
print mac.replace(tmp, s)
"`
sudo sed -i "s/$mac/$newmac/g" $path/$name/config

