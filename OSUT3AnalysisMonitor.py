#!/usr/bin/env python

import os, subprocess, shutil, threading, sys
import Release, Test

class OSUT3AnalysisMonitor:
  _tests = None
  _releases = None

  def __init__ (self, releases = None, tests = None):
    self._tests = []
    self._releases = []
    if releases is not None:
      self._releases.extend (releases)
    if tests is not None:
      self._tests.extend (tests)

  def addRelease (self, release):
    self._releases.append (release)

  def addReleases (self, releases):
    self._releases.extend (releases)

  def getReleases (self):
    return self._releases

  def addTest (self, test):
    self._tests.append (test)

  def addTests (self, tests):
    self._tests.extend (tests)

  def getTests (self):
    return self._tests

  def runTests (self):
    try:
      os.mkdir ("tmp")
    except OSError:
      print "Working directory \"tmp/\" already exists."
      print "OSUT3AnalysisMonitor appears to still be running."
      print "Either wait for completion or remove \"tmp/\"."
      sys.exit (1)

    cwd = os.path.realpath (os.getcwd ())
    lock = threading.Lock ()
    threads = []

    for release in self._releases:
      for test in self._tests:
        releaseDir = release.getArch ()
        os.makedirs ("tmp/" + test.getTestDir () + "/" + releaseDir)

        os.chdir ("tmp/" + test.getTestDir () + "/" + releaseDir)
        subprocess.call ("SCRAM_ARCH=" + release.getArch () + " scramv1 project CMSSW " + release.getReleaseVersion (), shell = True)
        releaseDir += "/" + release.getReleaseVersion ()
        test.setReleaseDir (releaseDir)

        os.chdir (release.getReleaseVersion () + "/src/")
        shutil.copy (cwd + "/Tests/" + test.getTestDir () + "/" + test.getBuildPackagesScript (), "./" + test.getBuildPackagesScript ())
        shutil.copy (cwd + "/Tests/" + test.getTestDir () + "/" + test.getLaunchJobsScript (), "./" + test.getLaunchJobsScript ())
        shutil.copy (cwd + "/Tests/" + test.getTestDir () + "/" + test.getHarvestOutputScript (), "./" + test.getHarvestOutputScript ())
        test.setWorkingDir (os.path.realpath (os.getcwd ()))
        os.chdir (cwd)

        threads.append (threading.Thread (target = test.runTest, args = (lock,)))

    for thread in threads:
      thread.start ()
    for thread in threads:
      thread.join ()
    shutil.rmtree ("tmp")
