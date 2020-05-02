# -*- coding: utf-8 -*-

import pytest
import os
from rpm2json import makeDir
from rpm2json import rpmList

__author__ = "Paul Blankenbaker"
__copyright__ = "Paul Blankenbaker"
__license__ = "mit"

def needDir(subDir):
    buildRoot = makeDir(os.path.join(os.getcwd(), "build"))
    testRoot = makeDir(os.path.join(buildRoot, "tests"))
    return makeDir(os.path.join(testRoot, subDir))

def test_rpmList():
    inDir = os.path.join(os.getcwd(), "tests", "repo")
    assert os.path.isdir(inDir)
    outDir = needDir("jsonout")
    assert os.path.isdir(outDir)
    rpmList(inDir, outDir)
