#!/bin/bash

. config
for name in $containers;
do 
    sudo lxc-info -n $name -iH
done
