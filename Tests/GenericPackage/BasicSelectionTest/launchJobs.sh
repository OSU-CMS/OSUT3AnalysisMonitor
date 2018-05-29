#!/usr/bin/env bash

echo "*** Launching jobs with \"osusub.py\"... ***"
cd DisappTrks/StandardAnalysis/test/
ln -s ${CONDOR_DIR} condor
ln -s /data/users/hart/condor/2016_final_prompt condor/2016_final_prompt
osusub.py -t OSUT3Ntuple -l localConfig_2016DEFGH.py -w basicSelectionTest -s 2016_final_prompt/metMinimalSkim_new -a metMinimalSkim
