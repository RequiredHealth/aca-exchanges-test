# basic dockerfile for containerizing acaex-test repo
FROM eggtree/ub12:base

#Expects the acadata repo to have already been cloned on the host
ADD .  /acaex-test
WORKDIR /acaex-test

RUN pip install -r requirements.txt

ENTRYPOINT ["./start.sh"]

