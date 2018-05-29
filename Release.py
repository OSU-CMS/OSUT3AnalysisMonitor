#!/usr/bin/env python

class Release:
  _arch = None
  _releaseVersion = None

  def __init__ (self, arch = None, releaseVersion = None):
    self._arch = arch
    self._releaseVersion = releaseVersion

  def setArch (self, arch):
    self._arch = arch

  def setReleaseVersion (self, releaseVersion):
    self._releaseVersion = releaseVersion

  def getArch (self):
    return self._arch

  def getReleaseVersion (self):
    return self._releaseVersion
