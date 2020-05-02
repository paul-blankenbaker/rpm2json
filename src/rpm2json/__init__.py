# -*- coding: utf-8 -*-
import rpm
import json
import os
import time
import logging

_logger = logging.getLogger(__name__)

from functools import cmp_to_key
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound


def encodeList(l):
    # for i in range(len(l)):
    #     if type(l[i]) is bytes:
    #         l[i] = l[i].decode()
    return l

def safeDecode(val):
    if val == None:
        return None
    # elif isinstance(val, bytes):
    #     return val.decode()
    else:
        return val

def createRpmInfo(h):
    """ Creates dictionary from handle to RPM object. """

    # From http://yum.baseurl.org/download/misc/checksig.py
    string = '%|DSAHEADER?{%{DSAHEADER:pgpsig}}:{%|RSAHEADER?{%{RSAHEADER:pgpsig}}:{%|SIGGPG?{%{SIGGPG:pgpsig}}:{%|SIGPGP?{%{SIGPGP:pgpsig}}:{(none)}|}|}|}|'
    siginfo = h.sprintf(string)
    
    info = {
        "arch" : safeDecode(h[rpm.RPMTAG_ARCH]),
        "archiveSize" : h[rpm.RPMTAG_ARCHIVESIZE],
        "buildHost" : safeDecode(h[rpm.RPMTAG_BUILDHOST]),
        "buildTime" : h[rpm.RPMTAG_BUILDTIME],
        "changeLogName" : encodeList(h[rpm.RPMTAG_CHANGELOGNAME]),
        "changeLogText" : encodeList(h[rpm.RPMTAG_CHANGELOGTEXT]),
        "changeLogTime" : h[rpm.RPMTAG_CHANGELOGTIME],
        "conflicts" : encodeList(h[rpm.RPMTAG_CONFLICTS]),
        "description" : safeDecode(h[rpm.RPMTAG_DESCRIPTION]),
        "epochNum" : h[rpm.RPMTAG_EPOCHNUM],
        "fileModes" : encodeList(h[rpm.RPMTAG_FILEMODES]),
        "fileNames" : encodeList(h[rpm.RPMTAG_FILENAMES]),
        "fileSizes" : encodeList(h[rpm.RPMTAG_FILESIZES]),
        "group" : safeDecode(h[rpm.RPMTAG_GROUP]),
        "installTime" : h[rpm.RPMTAG_INSTALLTIME],
        "installPrefixes" : encodeList(h[rpm.RPMTAG_INSTPREFIXES]),
        "license" : safeDecode(h[rpm.RPMTAG_LICENSE]),
        "longSize" : h[rpm.RPMTAG_LONGSIZE],
        "name" : safeDecode(h[rpm.RPMTAG_NAME]),
        "obsoletes" : encodeList(h[rpm.RPMTAG_OBSOLETES]),
        "os" : safeDecode(h[rpm.RPMTAG_OS]),
        "packager" : safeDecode(h[rpm.RPMTAG_PACKAGER]),
        "platform" : safeDecode(h[rpm.RPMTAG_PLATFORM]),
        "postIn" : safeDecode(h[rpm.RPMTAG_POSTIN]),
        "postInProg" : encodeList(h[rpm.RPMTAG_POSTINPROG]),
        "postTrans" : safeDecode(h[rpm.RPMTAG_POSTTRANS]),
        "postTransProg" : encodeList(h[rpm.RPMTAG_POSTTRANSPROG]),
        "postUn" : safeDecode(h[rpm.RPMTAG_POSTUN]),
        "postUnProg" : encodeList(h[rpm.RPMTAG_POSTUNPROG]),
        "preIn" : safeDecode(h[rpm.RPMTAG_PREIN]),
        "preInProg" : encodeList(h[rpm.RPMTAG_PREINPROG]),
        "preTrans" : safeDecode(h[rpm.RPMTAG_PRETRANS]),
        "preTransProg" : encodeList(h[rpm.RPMTAG_PRETRANSPROG]),
        "preUn" : safeDecode(h[rpm.RPMTAG_PREUN]),
        "preUnProg" : encodeList(h[rpm.RPMTAG_PREUNPROG]),
        "provides" : encodeList(h[rpm.RPMTAG_PROVIDES]),
        "release" : safeDecode(h[rpm.RPMTAG_RELEASE]),
        "requires" : encodeList(h[rpm.RPMTAG_REQUIRES]),
        "sigInfo" : siginfo,
        "size" : h[rpm.RPMTAG_SIZE],
        "sourceRpm" : safeDecode(h[rpm.RPMTAG_SOURCERPM]),
        "summary" : safeDecode(h[rpm.RPMTAG_SUMMARY]),
        "url" : safeDecode(h[rpm.RPMTAG_URL]),
        "triggerScripts" : encodeList(h[rpm.RPMTAG_TRIGGERSCRIPTS]),
        "triggerScriptsConds" : encodeList(h[rpm.RPMTAG_TRIGGERCONDS]),
        "triggerScriptsFlags" : encodeList(h[rpm.RPMTAG_TRIGGERFLAGS]),
        "triggerScriptsIndex" : encodeList(h[rpm.RPMTAG_TRIGGERINDEX]),
        "triggerScriptsName" : encodeList(h[rpm.RPMTAG_TRIGGERNAME]),
        "triggerScriptsProg" : encodeList(h[rpm.RPMTAG_TRIGGERSCRIPTPROG]),
        "triggerScriptsScriptFlags" : encodeList(h[rpm.RPMTAG_TRIGGERSCRIPTFLAGS]),
        "triggerScriptsType" : encodeList(h[rpm.RPMTAG_TRIGGERTYPE]),
        "triggerScriptsVersion" : encodeList(h[rpm.RPMTAG_TRIGGERVERSION]),
        "vendor" : safeDecode(h[rpm.RPMTAG_VENDOR]),
        "verifyScript" : safeDecode(h[rpm.RPMTAG_VERIFYSCRIPT]), # NoneType
        "verifyScriptProg" : encodeList(h[rpm.RPMTAG_VERIFYSCRIPTPROG]),
        "version" : safeDecode(h[rpm.RPMTAG_VERSION]),
        #          rpm.RPMTAG_ : safeDecode(h[rpm.RPMTAG_]),
    }
    return info

def compareVersion(ha, hb):
    """
Compares RPM header information epoch, version and release.

Returns: 0 - If equal, -1 if ha < hb, +1 if ha > hb.
"""
    return rpm.versionCompare(ha, hb)

def isSourceRpm(h):
    srcRpm = safeDecode(h[rpm.RPMTAG_SOURCERPM])
    if srcRpm == None:
        return 0
    return 1

def compareName(ha, hb):
    """
Compares two RPM node entries to see if they are for the same package (not necessarily same release).

To be considered the same:

 - Package name must be identical
 - Package type must be identical (binary or source)
 - Package architecture must be identical

Returns:

   0  - If two packages are same
   +1 - If package "b" comes after package "a" (or is newer release)
   -1 - If package "a" comes after package "b" (or is newer release)
"""
    # If different package names, the exit now (compare package names)
    aname = ha[rpm.RPMTAG_NAME];
    bname = hb[rpm.RPMTAG_NAME];

    if (aname < bname):
      return -1
    if (aname > bname):
      return 1

    # If different types (one binary and one source), then exit now
    asrc = isSourceRpm(ha)
    bsrc = isSourceRpm(hb)

    if asrc < bsrc:
      return -1
    if asrc > bsrc:
      return 1

    return 0

def compareNameVersion(a, b):
    """
Compares two RPM node by name/arch and version.

To be considered a duplicate:

 - Package name must be identical
 - Package type must be identical (binary or source)
 - Package architecture must be identical
 - Package epoch must be identical
 - Package version must be identical
 - Package release must be identical

Returns:

   0  - If two packages are duplicates (same version and release)
   +1 - If package "b" comes after package "a" (or is newer release)
   -1 - If package "a" comes after package "b" (or is newer release)
"""
    rc = compareName(a, b)
    if rc != 0:
      return rc

    # Otherwise, use epoch, version, release
    return compareVersion(a, b)

def _compareListEntries(a, b):
    (fa, ha) = a
    (fb, hb) = b
    return compareNameVersion(ha, hb)

def rpmBuildList(list, topdir):
    _logger.debug("Looking for RPMs under {topdir}".format(topdir=topdir))
    for root, subdirs, files in os.walk(topdir):
        for f in files:
            _logger.debug("Adding file {file}".format(file=f))
            list.append(os.path.join(root, f))

def makeDir(dir):
    if not os.path.isdir(dir):
        _logger.debug("Creating directory {dir} were valid RPM files".format(dir=dir))
        os.mkdir(dir)
    return dir

def getEpoch(h):
    epoch = h[rpm.RPMTAG_EPOCH]
    if epoch == None:
        epoch = 0
    return epoch

def rpmList(topdir, jsonDir):
    """ Generates JSON string containing list of all RPMs. """
    now = time.time()
    ts = rpm.TransactionSet()
    #mi = ts.dbMatch()

    # Make sure that output directories exist
    jsonDir = makeDir(jsonDir)
    jsonRpmDir = makeDir(os.path.join(jsonDir, 'info'))

    _logger.debug("Recursively searching for files under {dir}".format(dir=topdir))
    fileList = [ ]
    rpmBuildList(fileList, topdir)
    rootLen = len(topdir) + 1
    rpmHeaders = [ ]
    
    _logger.debug("Checking to see how many of the {fileCnt} files are readable RPMs".format(fileCnt=len(fileList)))
    
    for f in fileList:
        fd = None
        try:
          fd = os.open(f, os.O_RDONLY)
          h = ts.hdrFromFdno(fd)
          relPath = f[rootLen:]
          rpmHeaders.append((relPath, h))
          _logger.debug("Processed RPM file {file}".format(file=relPath))
        except Exception:
          pass
        finally:
            if fd != None:
                os.close(fd)

    _logger.info("{rpmCnt} of the {fileCnt} files under {dir} were valid RPM files".format(
        rpmCnt=len(rpmHeaders), fileCnt = len(fileList), dir=topdir))

    sortedList = sorted(rpmHeaders, key=cmp_to_key(_compareListEntries), reverse=False)

    jsonObj = []
    id = 100000
    
    for f, h in sortedList:
        name = str(h[rpm.RPMTAG_NAME])
        epoch = getEpoch(h)
        version = str(h[rpm.RPMTAG_VERSION])
        release = str(h[rpm.RPMTAG_RELEASE])
        arch = str(h[rpm.RPMTAG_ARCH])
        # Hmmm, seems like there should be a better way
        isSrc = (safeDecode(h[rpm.RPMTAG_SOURCERPM]) == None)
        
        jsonObj.append({
            "id": id,
            "name": name,
            "e": epoch,
            "v": version,
            "r": release,
            "arch": arch,
            "src": isSrc,
            "buildTime": h[rpm.RPMTAG_BUILDTIME],
            "f": f            
        })
        ofile = os.path.join(jsonRpmDir, str(id) + ".json")
        _logger.debug("Writing JSON info file {file} for {name}-{epoch}:{version}-{release}.{arch}".format(
            file=ofile, name=name, epoch=epoch, version=version, release=release, arch=arch))
        f = open(ofile, "w")
        info = createRpmInfo(h)
        info["src"] = isSrc
        info["id"] = id
        f.write(json.dumps(info))
        f.close()
        id = id + 1

    # Write out main index file
    ofile = os.path.join(jsonDir, "rpmlist.json")
    _logger.debug("Writing JSON file with list of all {rpmCnt} RPMs to {outFile}".format(
        rpmCnt=len(jsonObj), outFile=ofile))
    f = open(ofile, "w");
    f.write(json.dumps(jsonObj))
    f.close()
