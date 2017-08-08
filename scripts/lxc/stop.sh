#!/bin/bash

. config
for name in $containers;
do
    sudo lxc-stop -n $name
done

