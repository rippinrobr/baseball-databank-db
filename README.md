# Baseball Databank DB 

The goal of the project is to provide the data provided by the [Baseball Databank files](https://github.com/chadwickbureau/baseballdatabank) in databases to make using the data easier.  The data will be available in SQLite, PostgreSQL, MySQL and MongoDB.  Currently the only supported database is SQLite.  Support will be added for the other databases in the order they are listed above.  As support for the other databases is added a Docker container will be added that contains all the data preloaded.  If Docker isn't your thing you will also be able to load backups, create the schema via sql file or run the tools yourself to create your version of the database.

## Schemas and Backups
The schema file for all the supported databases live in the `schemas` directory.  The naming convention for the files is `<type-of-database>_schema_<season>_<github-commit-hash>.sql`
Currently `<type of database>` is sqlite, `<season>` what is the latest season in the data, and `<githhub-commit-hash>` is the hash for the commit in [Baseball Databank](https://github.com/chadwickbureau/baseballdatabank) repository.  At the time of writing the current schema file has the name `sqlite_schema_2016_4a64a55.sql`.  

If want the schema AND the data you'll find backup files in the `backups/` directory.  The files have a similar naming convention `<type-of-database>_backup_<date of backup>_<season>_<github-commit-hash>.(sql|appropriate extension for db type backups)`. If I had a backup file done today for my SQLite database the name of the file would be `sqlite_backup_20171119_2016_4a64a55.sql`

## Building the databases yourself
If you want to build the database yourself you'll need to run the `create_database_schema.py` script.  In order to that you'll need to have the `peewee` package installed, assuming you already have Python installed.  You can install `peewee` by running `pip install peewee`. Once you've installed the package you are ready to create the database.


### create_database_schema.py
Create the schema is as simple as running `python create_database_schema.py`.  The script lives in the `scripts/create-database` directory and has the options listed below.

```
usage: create_database_schema.py [-h] [--dbtype {sqlite}] [--dbpath DBPATH]

Generates a DB schema based on the Baseball Databank csv files.

optional arguments:
  -h, --help         show this help message and exit
  --dbtype {sqlite}  the database type you'd like to generate the schema for
  --dbpath DBPATH    SQLITE ONLY - the path for the newly created database
  ```

  Since SQLite is currently the only supported database running the `create_database_schema.py` script really only requires one command line argument since `--dbtype` defaults to `SQLite`.  Here's how to create the database:

  `python create_database_schema.py --dbpath ./baseball_database_db.py`

  If you were to run the script this way when the script finished you would have a new SQLite database in the directory that you ran the script in.  If you pass a path to the script of a pre-existing database you will receive an error.  In future version of the script this will be handled more gracefully.

  ## Generating Data Structures
  This script creates the data structures code that describes the data in each of the [Baseball Databank](https://github.com/chadwickbureau/baseballdatabank) CSV files.  The script reads each of the CSV files, determines the data types of the columns and will write source code files for each of the CSV files. In order to run this script you will need to have the package `inflection` installed. The script has been tested using `inflection` 0.3.1.  As of now Go is the only supported language, C#, Python, JavaScript and other languages are planned.  If there is a particular language you would like to see you can create an issue or even better, submit a pull request.

  ### create_data_structures.py
  ```
usage: create_data_structures.py [-h] [--csv] [--db] [--input INPUT]
                                 [--input-dir INPUT_DIR] [--json] --language
                                 {go} [--name NAME] [--output-dir OUTPUT_DIR]
                                 [--verbose]

Generate language specific data structures that model each of the Baseball
Databank CSV files.

optional arguments:
  -h, --help            show this help message and exit
  --csv                 If the language supports add CSV tags or CSV
                        representation to the structure
  --db                  adds db tags to Go structs.
  --input INPUT         the path to the input CSV file
  --input-dir INPUT_DIR
                        the path to the directory that contains the CSV files
                        to parse
  --json                If the language supports add JSON tags or JSON
                        representation to the structure
  --language {go}       create language specific data structures
  --name NAME           name of the datas tructure being created
  --output-dir OUTPUT_DIR
                        the directory where the generated file should be
                        written. If not provided file will be written to
                        stdout
  --verbose             more output during the parsing and creation of the
                        data structures
```

The required options are `--language` and either the `--input` or `--input-dir` flags.  Since Go is the only supported language now if `--language` is not provided it defaults to go.  This behavior will change as soon as another language is added. The `--input` flag expects a path to a single CSV file.  THe `--input-dir` expects a path to a directory that contains *.CSV files.  

Optional parameters are `--name`, `--output-dir` and `--verbose`.  The `--name` parameter is what will be used to name the generated data structure.  If `--name` is not provided the name of the file will be used to create the name following the language's naming conventions.  The `--ouptut-dir` takes a path to the directory that the files should be written to.

#### Go specific command line options

There following arguments depend on language support `--csv`, `--db`, and `--json`. If any of the `--csv`, `--db`, and `--json` flags are used the generated structs will contain the `csv`, `db` and/or `json` tags.