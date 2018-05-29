#!/usr/bin/env bash

echo "*** Merging output with \"mergeOut.py\"... ***"
cd DisappTrks/StandardAnalysis/test/
mergeOut.py -l localConfig_2016DEFGH.py -w basicSelectionTest
