#!/bin/bash
set -ex

# assumes this container has been linked to another container where the api is running
# and the alias 'acaex_api' was used. Also that api container exposes port 5001
export ACAEX_TEST_URL=http://$ACAEX_API_PORT_5001_TCP_ADDR:$ACAEX_API_PORT_5001_TCP_PORT

echo $@
# set up ssh keys for making git usage easier
# assume ~/.ssh on the host is mounted at /root/.ssh_host in the container
# for some reason cant mount stuff directly into /root/.ssh
if [[ ! -f /root/.ssh/id_rsa ]];then
    mkdir /root/.ssh
    # only need the private key
    cp /root/.ssh_host/id_rsa /root/.ssh/id_rsa
    # give it the right restrictive permissions
    chmod 600 /root/.ssh/id_rsa
fi

# two command line args, assume they are git related
if [[ -n "$1" && -n "$2" ]];then
    # only try to clear out settings if they exist
    # --unset will return non-zero and so fail the script
    # setting is not present
    if [[ -n `git config --local user.name` ]];then
        git config --local --unset user.name
    fi
    if [[ -n `git config --local user.email` ]];then
        git config --local --unset user.email
    fi
    git config --local --add user.name "$1"
    git config --local --add user.email "$2"
fi

# finally startup the bash console which will be the process
# for this container
/bin/bash
