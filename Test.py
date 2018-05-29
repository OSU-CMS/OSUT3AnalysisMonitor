#!/usr/bin/env python

import subprocess, time, os, re, threading

class Test:
  _workingDir = None
  _resultsDir = None
  _condorDir = None
  _dateDir = None
  _testDir = None
  _releaseDir = None
  _null = None
  _stdin = None
  _stdout = None
  _condorLogFiles = None
  _condorClusters = None
  _buildPackagesScript = ""
  _launchJobsScript = ""
  _harvestOutputScript = ""
  _expectedOutputFiles = None

  def __init__ (self):
    self._null = open ("/dev/null", "w")
    self._condorLogFiles = []
    self._condorClusters = []
    self._expectedOutputFiles = []

  def setWorkingDir (self, workingDir):
    self._workingDir = workingDir

  def getWorkingDir (self):
    return self._workingDir

  def setResultsDir (self, resultsDir):
    self._resultsDir = resultsDir

  def getResultsDir (self):
    return self._resultsDir

  def setCondorDir (self, condorDir):
    self._condorDir = condorDir

  def getCondorDir (self):
    return self._condorDir

  def setDateDir (self, dateDir):
    self._dateDir = dateDir

  def getDateDir (self):
    return self._dateDir

  def setTestDir (self, testDir):
    self._testDir = testDir

  def getTestDir (self):
    return self._testDir

  def setReleaseDir (self, releaseDir):
    self._releaseDir = releaseDir

  def getReleaseDir (self):
    return self._releaseDir

  def setBuildPackagesScript (self, buildPackagesScript):
    self._buildPackagesScript = buildPackagesScript

  def getBuildPackagesScript (self):
    return self._buildPackagesScript

  def setLaunchJobsScript (self, launchJobsScript):
    self._launchJobsScript = launchJobsScript

  def getLaunchJobsScript (self):
    return self._launchJobsScript

  def setHarvestOutputScript (self, harvestOutputScript):
    self._harvestOutputScript = harvestOutputScript

  def getHarvestOutputScript (self):
    return self._harvestOutputScript

  def addExpectedOutputFile (self, expectedOutputFile):
    self._expectedOutputFiles.append (expectedOutputFile)

  def addExpectedOutputFiles (self, expectedOutputFiles):
    self._expectedOutputFiles.extend (expectedOutputFiles)

  def getExpectedOutputFiles (self):
    return self._expectedOutputFiles

  def addCondorLogFile (self, condorLogFile):
    self._condorLogFiles.append (condorLogFile)

  def addCondorLogFiles (self, condorLogFiles):
    self._condorLogFiles.extend (condorLogFiles)

  def getCondorLogFiles (self):
    return self._condorLogFiles

  def flushOutput (self):
    self._stdout.flush ()
    self._stderr.flush ()

  def writeOutput (self, output):
    self._stdout.write (output)
    self._stdout.flush ()
    self._stderr.write (output)
    self._stderr.flush ()

  def extractCondorClusters (self):
    for condorLogFile in self._condorLogFiles:
      try:
        logFile = open (condorLogFile, "r")
      except:
        self.writeOutput ("Could not open log file \"" + condorLogFile + "\".\n")
        continue
      addedCluster = False
      for line in logFile:
        if "Job submitted from host" not in line:
          continue
        cluster = re.sub (r"[^\(]*\(([^\.]*)\..*", r"\1", line.rstrip ())
        self._condorClusters.append (int (cluster))
        addedCluster = True
        break
      logFile.close ()
      if not addedCluster:
        self.writeOutput ("Could not add cluster from log file \"" + condorLogFile + "\".")

  def buildPackages (self):
    self.writeOutput ("================================================================================\n")
    self.writeOutput ("Building packages with \"" + self._buildPackagesScript + "\"...\n")
    self.writeOutput ("--------------------------------------------------------------------------------\n")
    exitCode = subprocess.call ("eval `scramv1 runtime -sh` && ./" + self._buildPackagesScript, shell = True, stdout = self._stdout, stderr = self._stderr)
    self.flushOutput ()
    self.writeOutput ("--------------------------------------------------------------------------------\n")
    self.writeOutput ("Script " + ("was SUCCESSFUL" if exitCode == 0 else "FAILED") + " (exit code " + str (exitCode) + ").\n")
    self.writeOutput ("================================================================================\n\n")

    return exitCode

  def launchJobs (self):
    self.writeOutput ("================================================================================\n")
    self.writeOutput ("Launching jobs with \"" + self._launchJobsScript + "\"...\n")
    self.writeOutput ("--------------------------------------------------------------------------------\n")
    condorDir = self._condorDir + "/" + self._dateDir + "/" + self._testDir + "/" + self._releaseDir
    os.makedirs (condorDir)
    exitCode = subprocess.call ("eval `scramv1 runtime -sh` && (CONDOR_DIR=" + condorDir + " ./" + self._launchJobsScript + ")", shell = True, stdout = self._stdout, stderr = self._stderr)
    self.flushOutput ()
    self.writeOutput ("--------------------------------------------------------------------------------\n")
    self.writeOutput ("Script " + ("was SUCCESSFUL" if exitCode == 0 else "FAILED") + " (exit code " + str (exitCode) + ").\n")
    self.writeOutput ("================================================================================\n\n")

    self.extractCondorClusters ()

    return exitCode

  def waitOnJobs (self):
    self.writeOutput ("================================================================================\n")
    self.writeOutput ("Waiting for jobs to finish...\n")
    self.writeOutput ("--------------------------------------------------------------------------------\n")
    while True:
      keepWaiting = False
      for cluster in self._condorClusters:
        jobsStillRunning = (subprocess.call ("condor_q " + str (cluster) + " | tail -n 1 | grep \"OWNER\"", shell = True, stdout = self._null, stderr = self._null) != 0)
        keepWaiting = keepWaiting or jobsStillRunning

        if keepWaiting:
          break;

      if not keepWaiting:
        break
      self.writeOutput ("Jobs not done. Sleeping 60 seconds...\n")
      time.sleep (60)
    self.writeOutput ("--------------------------------------------------------------------------------\n")
    self.writeOutput ("Done.\n")
    self.writeOutput ("================================================================================\n\n")

  def harvestOutput (self):
    self.writeOutput ("================================================================================\n")
    self.writeOutput ("Harvesting output with \"" + self._harvestOutputScript + "\"...\n")
    self.writeOutput ("--------------------------------------------------------------------------------\n")
    exitCode = subprocess.call ("eval `scramv1 runtime -sh` && ./" + self._harvestOutputScript, shell = True, stdout = self._stdout, stderr = self._stderr)
    self.flushOutput ()
    self.writeOutput ("--------------------------------------------------------------------------------\n")
    self.writeOutput ("Script " + ("was SUCCESSFUL" if exitCode == 0 else "FAILED") + " (exit code " + str (exitCode) + ").\n")
    self.writeOutput ("================================================================================\n\n")

    return exitCode

  def copyOutput (self):
    self.writeOutput ("================================================================================\n")
    self.writeOutput ("Copying output to \"" + self._resultsDir + "/" + self._dateDir + "/" + self._testDir + "/" + self._releaseDir + "/\"...\n")
    self.writeOutput ("--------------------------------------------------------------------------------\n")
    for outputFile in self._expectedOutputFiles:
      outputFileBaseName = os.path.basename (outputFile)
      self.writeOutput ("Copying \"" + outputFile + "\"... ")
      try:
        shutil.copy (outputFile, self._resultsDir + "/" + self._dateDir + "/" + self._testDir + "/" + self._releaseDir + "/" + outputFileBaseName)
      except:
        self.writeOutput ("FAILED.\n")
      else:
        self.writeOutput ("SUCCEEDED.\n")
    self.writeOutput ("--------------------------------------------------------------------------------\n")
    self.writeOutput ("Script " + ("was SUCCESSFUL" if exitCode == 0 else "FAILED") + " (exit code " + str (exitCode) + ").\n")
    self.writeOutput ("================================================================================\n\n")

    return exitCode

  def runTest (self, lock):
    cwd = os.path.realpath (os.getcwd ())
    os.makedirs (self._resultsDir + "/" + self._dateDir + "/" + self._testDir + "/" + self._releaseDir)
    self._stdout = open (self._resultsDir + "/" + self._dateDir + "/" + self._testDir + "/" + self._releaseDir + "/test.out", "w")
    self._stderr = open (self._resultsDir + "/" + self._dateDir + "/" + self._testDir + "/" + self._releaseDir + "/test.err", "w")

    self.writeOutput ("================================================================================\n")
    self.writeOutput ("Starting test on " + subprocess.check_output (["date"]).rstrip () + ".\n")
    self.writeOutput ("Running on: " + subprocess.check_output (["uname", "-a"]).rstrip () + ".\n")
    self.writeOutput ("System software: " + subprocess.check_output (["cat", "/etc/redhat-release"]).rstrip () + ".\n")
    self.writeOutput ("================================================================================\n\n")

    success = True
    if success:
      lock.acquire ()
      os.chdir (self._workingDir)
      success = (self.buildPackages () == 0)
      os.chdir (cwd)
      lock.release ()
    if success:
      lock.acquire ()
      os.chdir (self._workingDir)
      success = (self.launchJobs () == 0)
      os.chdir (cwd)
      lock.release ()
    if success:
      success = (self.waitOnJobs () == 0)
    if success:
      lock.acquire ()
      os.chdir (self._workingDir)
      success = (self.harvestOutput () == 0)
      os.chdir (cwd)
      success = (self.copyOutput () == 0)
      lock.release ()

    # check output files and do something in the case of failure
