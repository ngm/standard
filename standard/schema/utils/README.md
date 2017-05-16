## Standard Utilities

The scripts in this folder support the creation of the versioned release schema, and standard documentation. See the root README file for virtual environment settings. 

### make_validation_schema.py

Whenever the release schema is updated, a versioned release schema has to be created from this, to support validation of versioned OCDS files. 

This can be created by running:

````
./make_validation_schema.py
````

There are tests set-up to ensure this has happened. 

### get_codelists.py

At present, codelist contents is managed through a Google Spreadsheet.

The get_codelists.py script fetches each codelist, and stores it in the /schema/codelists directory as a CSV file. It also fetches the IATI Organisation Identifier codelist.

````
python get_codelists.py
````

should be run whenever codelists are changed.
