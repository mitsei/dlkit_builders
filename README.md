[![Build Status](https://travis-ci.org/mitsei/dlkit_builders.svg?branch=master)](https://travis-ci.org/mitsei/dlkit_builders)

# Introduction

This builder generates `dlkit` from the `xosid` `xml` packages. It assumes
the `xosid` packages defined in `config.py` are located in a sibling
directory to this, like:

```
dlkit_builders
 |- build_dlkit.py
 |- config.py
xosid
 |- assessment.xml
```

Note that you need to create your own `config.py` file. A skeleton file
is included in this repository as an example.

# XOSID files

The `xosid` definitions are located [here](https://app.assembla.com/spaces/osid/git/source/master/definitions/xosid).

# First time build steps

1. Copy `config.py.skel` to `config.py`.
2. Download the `xosid` files into the `xosid` directory, that you want to build.
3. Update `config.py` to include the packages, managers,
    sessions, and objects you want to build.
4. Run `python build_dlkit.py`.

For future builds, you only need to update `config.py` and the files in the
`xosid` directory if you bring in new packages.

# Running the builder

To run the builder, you can build all or a subset of `dlkit`. The first time
you run the builder, you will need to build `map`, `patterns`, `abc`, `manager`,
and `mdata`. After that, depending on what you change, you could build just
`json`, `authz`, or `services`. 

```
    Usage: python build_dlkit.py [commands]
    where:
      - [commands] is any set of supported commands
      - By default, python build_dlkit.py will build all packages
    
    Supported commands:
      map: map the xosid files into pattern_maps/ and package_maps/
      abc: build the abstract_osids
      patterns: build the patterns
      mdata: build the metadata files for the json implementation
      authz: build the authz_adapter impl
      json: build the JSON OSID impl (use MongoDB or Filesystem based on config)
      stub: build developer stub impl
      services: build the dlkit convenience service impls
      manager: build the manager_impls base classes
      tests: build the tests. You should always use this with the --buildto flag.
      --all: build all of the above. Tests will be placed into a ../tests/ directory.
      --buildto <directory>: the target build-to directory (this will be sibling to this script, ../<directory)
```

This will build the files to the directory specified, default of `../dlkit/`.

Examples:
  - `python build_dlkit.py --buildto dlkit-dev/dlkit`
  - `python build_dlkit.py map patterns abc mdata json`
  - `python build_dlkit.py --all`
  - `python build_dlkit.py json --buildto dlkit_testing`


NOTE: there are no builder tests, so the Travis CI build just does a PEP8 check.
