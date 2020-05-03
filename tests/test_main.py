# -*- coding: utf-8 -*-

import pytest
import json
import os
from rpm2json import _makeDir
from rpm2json import rpmList

__author__ = "Paul Blankenbaker"
__copyright__ = "Paul Blankenbaker"
__license__ = "mit"

def needDir(subDir):
    buildRoot = _makeDir(os.path.join(os.getcwd(), "build"))
    testRoot = _makeDir(os.path.join(buildRoot, "tests"))
    return _makeDir(os.path.join(testRoot, subDir))

def readJson(dir, file):
    jsonObj = None
    f = None
    err = None
    try:
        f = open(os.path.join(dir, file), 'r')
        jsonObj = json.load(f)
        print(jsonObj)
    except Exception as msg:
        err = msg
    finally:
        if f != None:
            f.close()
    assert err == None
    assert jsonObj != None
    return jsonObj

def assertJsonObjectsEqual(expJson, gotJson, jsonFile):
    for key in expJson.keys():
        exp = { "f": jsonFile, "key": key, "val": expJson[key] }
        got = { "f": jsonFile, "key": key, "val": gotJson[key] }
        assert exp == got

    for key in gotJson.keys():
        exp = { "f": jsonFile, "key": key, "val": expJson[key] }
        got = { "f": jsonFile, "key": key, "val": gotJson[key] }
        assert exp == got

def assertJsonEqual(expDir, gotDir, jsonFile):
    expJson = readJson(expDir, jsonFile)
    gotJson = readJson(gotDir, jsonFile)
    assertJsonObjectsEqual(expJson, gotJson, jsonFile)

def assertJsonArraysEqual(expDir, gotDir, jsonFile):
    expJson = readJson(expDir, jsonFile)
    gotJson = readJson(gotDir, jsonFile)
    expLen = len(expJson)
    assert expLen == len(gotJson)

    for i in range(expLen):
        assertJsonObjectsEqual(expJson[i], gotJson[i], jsonFile)

def test_rpmList():
    inDir = os.path.join(os.getcwd(), "tests", "repo")
    assert os.path.isdir(inDir)
    outDir = needDir("jsonout")
    assert os.path.isdir(outDir)
    rpmList(inDir, outDir)

    expDir = os.path.join(os.getcwd(), "tests", "expect")
    expDirInfo = os.path.join(expDir, "info")
    outDirInfo = os.path.join(outDir, "info")
    print(expDirInfo)
    assertJsonArraysEqual(expDir, outDir, "rpmlist.json")
    assertJsonEqual(expDirInfo, outDirInfo, "100000.json")
    assertJsonEqual(expDirInfo, outDirInfo, "100001.json")
    assertJsonEqual(expDirInfo, outDirInfo, "100002.json")

    
