#!/bin/bash

. config
for name in $containers;
do
    sudo lxc-start -n $name -d
done

