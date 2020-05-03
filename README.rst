========
rpm2json
========


Builds static JSON files containing information from a collection of
RPM files (a repository) to support AJAX based HTML based repository
viewers (like *repoview``).


Description
===========

The Network Security Toolkit (NST) project that I have been involved
with over the years used a tool call *repoview* to generate information
about the RPMs in a repository as a static HTML report.

Unfortunately, repoview no longer appears to be maintained.

This NST (https://networksecuritytoolkit.org) project has an AJAX
based repository viewer built into its web interface. This project
borrows code and ideas from NST to:

- Read information from a collection of RPM files.
- Writes a JSON file for each RPM containing details from the RPM.
- Write one "index" JSON file containing a list of RPMs.

The static JSON files produced can be leveraged to produce an AJAX
based repository viewer similar in function to *repoview*.


Using
=====

The ``rpm2json`` command is fairly straight forward. First identify
your top level directory that contains a collection of RPM files. The
example below indicates that there are 3 RPM files available under the
tests directory::
  
  [nst@nst32-repo rpm2json]$ find tests -name "*.rpm"
  tests/repo/SRPMS/virtualbox-repo-32-10.nst32.src.rpm
  tests/repo/noarch/virtualbox-repo-32-10.nst32.noarch.rpm
  tests/repo/noarch/RandomUUID-1.0.0-5.nst32.noarch.rpm
  [nst@nst32-repo rpm2json]$ 

Next, invoke the ``rpm2json`` command specifying the directory where
the RPM files can be found and it will create the JSON files.::

  [nst@nst32-repo rpm2json]$ rpm2json --dir tests
  [nst@nst32-repo rpm2json]$ find tests -name "*.json"
  tests/json/rpmlist.json
  tests/json/info/100001.json
  tests/json/info/100000.json
  tests/json/info/100002.json
  [nst@nst32-repo rpm2json]$ cat tests/json/rpmlist.json | jq .
  [
    {
      "id": 100000,
      "name": "RandomUUID",
      "e": 0,
      "v": "1.0.0",
      "r": "5.nst32",
      "arch": "noarch",
      "src": false,
      "buildTime": 1586633458,
      "f": "repo/noarch/RandomUUID-1.0.0-5.nst32.noarch.rpm"
    },
    {
      "id": 100001,
      "name": "virtualbox-repo",
      "e": 0,
      "v": "32",
      "r": "10.nst32",
      "arch": "noarch",
      "src": true,
      "buildTime": 1586633869,
      "f": "repo/SRPMS/virtualbox-repo-32-10.nst32.src.rpm"
    },
    {
      "id": 100002,
      "name": "virtualbox-repo",
      "e": 0,
      "v": "32",
      "r": "10.nst32",
      "arch": "noarch",
      "src": false,
      "buildTime": 1586633869,
      "f": "repo/noarch/virtualbox-repo-32-10.nst32.noarch.rpm"
    }
  ]
  [nst@nst32-repo rpm2json]$ 

The output from the commands shown above indicates that:

- There were four JSON files created (rpmlist.json, 100000.json,
  100001.json and 100002.json).
- The ``rpmlist.json`` file contains 3 entries related to the
  individual JSON files containing details extracted from each RPM.

The JSON files produced only provide the core "static database" of
information about the RPMs. In order to view the information, you will
need to:

- Provide HTML, CSS, and JavaScript to read and render the files.
- Copy the HTML, CSS, JavaScript and JSON files to a web server. AJAX
  calls are required to fetch the JSON files when building the
  presentation in the browser and this can not be done (or at least I
  don't know how to do it without having the files installed on a web
  server).
  

Building
========

This project has been set up using PyScaffold 3.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

After cloning the project (or extracting the source file), you should
be able to make use of the ``setup.py`` file. For usage::

  python3 setup.py --help
  python3 setup.py --help-commands

To build::

  python3 setup.py build

Surely there is a better way, but here is what I've been doing to run
the rpm2json command directly out of the ``build`` directory (after a
build).::

  export PYTHONPATH="${PWD}/build/lib/rpm2json"
  python3 "${PYTHONPATH}/main.py" -h
  python3 "${PYTHONPATH}/main.py" --outdir build/t1 --dir tests -vv  

To check build::

  python3 setup.py check

To test::

  python3 setup.py test

To build RPM that can be installed and provide the rpm2json command::

  python3 setup.py bdist_rpm
