#!/usr/bin/env bash

cwd=`pwd`
tmpdir=`mktemp -d`
cd ${tmpdir}
SCRAM_ARCH=slc6_amd64_gcc630 scramv1 project CMSSW CMSSW_10_1_5
cd CMSSW_10_1_5/src/
eval `scramv1 runtime -sh`
cd ${cwd}/

./run.py

rm -rf ${tmpdir}
