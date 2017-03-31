This builder generates `dlkit` from the `xosid` `xml` packages. It assumes
the `xosid` packages defined in `config.py` are located in a sibling
directory to this, like:

```
dlkit_builders
 |- build_controller.py
xosid
 |- assessment.xml
```

To run the builder, you can build all or a subset of `dlkit`:

```
    Usage: python build_controller.py [commands]
    where:
      [commands] is any set of supported commands
    
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
      --buildto <directory>: the target build-to directory (relative to the current one)
```

This will build the files to the directory specified, default of `../dlkit/`.

Examples:
  - `python build_controller.py map patterns abc mdata json`
  - `python build_controller.py --all`

NOTE: there are no builder tests, so the Travis CI build just does a PEP8 check.
