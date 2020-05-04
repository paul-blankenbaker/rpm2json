# -*- coding: utf-8 -*-
"""
This is entry point for the console script. To enable/package this script,
add the following lines in the [options.entry_points] section in setup.cfg:

    console_scripts =
         rpm2json = rpm2json.main:run

Then run `python setup.py install` which will install the command `rpm2json`
inside your current environment.
"""

import argparse
import os
import rpm
import sys
import logging

from rpm2json import __version__
from rpm2json import rpmList

__author__ = "Paul Blankenbaker"
__copyright__ = "Paul Blankenbaker"
__license__ = "mit"

_logger = logging.getLogger(__name__)

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Generates JSON file(s) of information from RPMs")
    parser.add_argument(
        "--version",
        action="version",
        version="rpm2json {ver}".format(ver=__version__))
    parser.add_argument(
        "--dir",
        required=True,
        help="Directory where the RPM repository lives")
    parser.add_argument(
        "--outdir",
        help="If you want the JSON files written to a different directory")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    #_logger.debug("Starting crazy calculations...")
    if (args.dir != None):
        #rpm.addMacro('_dpath', args.dir)
        outdir = args.outdir
        if outdir == None:
            outdir = os.path.join(args.dir, "json")
        rpmList(args.dir, outdir)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
