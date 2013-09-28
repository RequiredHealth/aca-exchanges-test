aca-exchanges-test
==================

Assumptions
===========
A working Python 2.7 environment with pip installed along with git.

Install virtualenv
====================

    $ pip install virtualenv
    
Install the tests
=================
```Shell
# setup the virtualenv 
mkdir aca
cd aca
virtualenv aca-ex-test
source aca-ex-test/bin/activate
#
git clone ...
cd aca-exchanges-test

```

Run the tests
=============
```Shell
# install dependencies
pip install -r requirements.txt
pylint --rcfile=.pylintrc --errors-only TestAPI.py
nosetests
```
