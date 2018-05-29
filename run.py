#!/usr/bin/env python

def main ():

  import os, sys, glob, re, datetime, getpass
  from OSUT3AnalysisMonitor import OSUT3AnalysisMonitor
  from Release import Release
  from Test import Test

  cwd = os.path.realpath (os.getcwd ())

  if os.path.basename (cwd) != "OSUT3AnalysisMonitor":
    print sys.argv[0] + " is running in \"" + cwd + "\"."
    print "Should be run in OSUT3AnalysisMonitor instead. Exiting..."
    sys.exit (1)

  sys.path.append (cwd)
  os.environ["PATH"] += ":."

  monitor = OSUT3AnalysisMonitor ()
  monitor.addRelease (Release ("slc6_amd64_gcc530", "CMSSW_8_0_30"))

  resultsDir = os.path.realpath (os.path.expanduser ("~") + "/public_html/test") # hart
  condorDir = "/data/users/" + getpass.getuser ()
  now = datetime.datetime.now ()
  dateDir = now.strftime ("%Y_%m_%d/%H_%M_%S")

  for dir in glob.glob ("Tests/*"):
    if "__init__.py" in dir:
      continue
    testPackage = os.path.basename (dir)
    for test in glob.glob (dir + "/*"):
      if "__init__.py" in test:
        continue
      testName = os.path.basename (test)
      testDir = testPackage + "/" + testName

      exec ("from Tests." + testPackage + "." + testName + "." + testPackage + "_" + testName + " import " + testPackage + "_" + testName)
      test = locals ()[testPackage + "_" + testName]
      test.setResultsDir (resultsDir)
      test.setCondorDir (condorDir)
      test.setDateDir (dateDir)
      test.setTestDir (testDir)

      monitor.addTest (test)

  monitor.runTests ()

if __name__ == "__main__":
  main()
