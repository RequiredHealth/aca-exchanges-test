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
virtualenv aca-ex-test-venv
source aca-ex-test-venv/bin/activate
# get the test source
git clone https://github.com/RequiredHealth/aca-exchanges-test.git
cd aca-exchanges-test
# tell git to ignore the file which tells the tests what URL to test
# you are free to point this anywhere you like: local or remote
git update-index --assume-unchanged test_url.cfg
# install dependencies
pip install -r requirements.txt
# run the tests
pylint --rcfile=.pylintrc --errors-only TestAPI.py
nosetests

```

