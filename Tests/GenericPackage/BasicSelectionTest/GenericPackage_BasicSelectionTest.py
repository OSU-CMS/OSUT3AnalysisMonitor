#!/usr/bin/env python

from Test import Test

# If the test is in PackageName/TestName, then this file must be called
# PackageName_TestName.py and the object must be called PackageName_TestName.
GenericPackage_BasicSelectionTest = Test ()

# Each of these must be an executable (Bash script, Python script, etc.) in the
# same directory.
GenericPackage_BasicSelectionTest.setBuildPackagesScript ("buildPackages.sh")
GenericPackage_BasicSelectionTest.setLaunchJobsScript ("launchJobs.sh")
GenericPackage_BasicSelectionTest.setHarvestOutputScript ("harvestOutput.sh")

# Add a single log file for each dataset that is submitted to HTCondor. This is
# used to get the cluster number of the jobs so they can be monitored.
GenericPackage_BasicSelectionTest.addCondorLogFile ("DisappTrks/StandardAnalysis/test/condor/basicSelectionTest/MET_2016F/condor_0.log")

# Add each of the expected ROOT output files. These will be copied to the
# results directory and compared to a reference version.
GenericPackage_BasicSelectionTest.addExpectedOutputFile ("DisappTrks/StandardAnalysis/test/condor/basicSelectionTest/MET_2016F.root")
