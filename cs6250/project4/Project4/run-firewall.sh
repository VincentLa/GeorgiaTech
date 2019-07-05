#!/bin/bash

if [ -z $1 ]; then
    echo "Usage: run-firewall.sh <firewall configfile>.pol"
    exit
fi

cp $1 ~/pyretic/pyretic/modules/firewall-policies.cfg
cp pyretic_switch.py ~/pyretic/pyretic/modules
cp firewall.py ~/pyretic/pyretic/modules
cp firewall_policy.py ~/pyretic/pyretic/modules
pushd ~/pyretic
python pyretic.py -m p0 pyretic.modules.firewall
popd
