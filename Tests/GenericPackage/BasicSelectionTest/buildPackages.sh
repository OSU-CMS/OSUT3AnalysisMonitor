#!/usr/bin/env bash

echo "*** Checking out OSUT3Analysis and DisappTrks... ***"
git clone https://github.com/OSU-CMS/OSUT3Analysis.git
git clone https://github.com/aehart/DisappTrks.git

echo ""

echo "*** Switching to DisappTrks/generic_test branch... ***"
cd DisappTrks/
git checkout generic_test
cd ../

echo ""

echo "*** Changing data format to \"MINI_AOD\"... ***"
./OSUT3Analysis/AnaTools/scripts/changeDataFormat.py -f MINI_AOD -c DisappTrks/StandardAnalysis/interface/CustomDataFormat.h

echo ""

echo "*** Building release... ***"
scram b -j 9 -k
