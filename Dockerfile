# basic dockerfile for containerizing acaex-test repo
FROM eggtree/ub12:base

#Expects the acadata repo to have already been cloned on the host
ADD .  /acaex-test

RUN pip install -r /acaex-test/requirements.txt

ENTRYPOINT ["/acaex-test/start.sh"]

