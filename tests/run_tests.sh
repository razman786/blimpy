#!/usr/bin/env bash
echo "------ Running Coverage Tests! ------"

# Find current working dir
DIR=$(pwd -P)
if [ -d $DIR"/tests" ]
then
    TESTDIR=$DIR"/tests"
else
    TESTDIR=$DIR
    DIR="$(dirname "$TESTDIR")"
fi

# Check if running as sudo user and install Python packages
if [ `id -u` -eq 0 ]
then
        echo "------ Installing coverage, codecov and pyyaml packages system wide ------"
        pip3 install coverage codecov pyyaml pytest pySLALIB
else
        echo "------ Installing coverage, codecov and pyyaml packages as a user ------"
        pip3 install coverage codecov pyyaml pytest pySLALIB --user
fi

# Check if Git is already installed
if ! command -v 'git' &> /dev/null
then
    # Check if script is running on a Debian-based distro
    if [ "$(grep -Ei 'debian|buntu|mint' /etc/*release)" ]
    then
        # Check if running as sudo user
        if [ `id -u` -eq 0 ]
        then
            echo "------ Installing Git ------"
            apt-get install git
        else
            echo "------ Installing Git. Please enter 'sudo' password ------"
            sudo apt-get install git
        fi
    else
        # Git is not found and the script is on a Non-Debian system
        echo "------ Non-Debian system detected and 'git' command not found. Please install the Git package on your system ------"
        exit
    fi
else
    echo "------ Git is already installed ------"
fi

# Run blimpy setup.py
# Check if script us running with sudo
cd $DIR
if [ `id -u` -eq 0 ]
then
        echo "------ Installing blimpy (system wide) ------"
        python3 setup.py install
else
    echo "------ Installing blimpy (as a user) ------"
        python3 setup.py install --user
fi

# run coverage
cd $TESTDIR
coverage run --source=blimpy -m pytest
EXITCODE=$?
if [ $EXITCODE -ne 0 ]; then
    echo
    echo '*** Oops, coverage pytest failed, exit code = '$EXITCODE' ***'
    echo
    exit $EXITCODE
fi

# Run coverage report
coverage report
EXITCODE=$?
if [ $EXITCODE -ne 0 ]; then
    echo
    echo '*** Oops, coverage report failed, exit code = '$EXITCODE' ***'
    echo
    exit $EXITCODE
fi

# Run codecov
codecov
