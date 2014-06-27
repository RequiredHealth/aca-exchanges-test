#!/bin/bash
set -ex


# assumes this container has been linked to another container where the api is running
# and the alias 'acaex_api' was used. Also that api container exposes port 5001
export ACAEX_TEST_URL=http://$ACAEX_API_PORT_5001_TCP_ADDR:$ACAEX_API_PORT_5001_TCP_PORT

#echo $@
#if [[ $1 = "dev" ]];then
#    echo "dev mode"
    # set up ssh keys for making git usage easier
    # assume ~/.ssh on the host is mounted at /root/.ssh_host in the container
    # for some reason cant mount stuff directly into /root/.ssh
    mkdir /root/.ssh
    # only need the private key
    cp /root/.ssh_host/id_rsa /root/.ssh/id_rsa
    # give it the right restrictive permissions
    chmod 600 /root/.ssh/id_rsa
    /bin/bash
#else
#    python /acaex/aca/api.py
#fi

