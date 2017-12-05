# Baseball Stats DB 

The goal of the project is to provide the data provided by the [Baseball Databank files](https://github.com/chadwickbureau/baseballdatabank) in databases to make using the data easier.  Currently there are three officially supported databases PostgreSQL, SQLite and MongoDB.  _If you are wondering why MySQL isn't support [read this](#about_mysql)_.  

## Schemas
The schema file for all the supported databases live in the `schemas` directory.  All schema files follow this naming convention:

 `(postgres|sqlite)_schema_<season>_<github-commit-hash>.sql`

Where `<season>` the most recent season in the databases `<githhub-commit-hash>` is the hash of the latest [Baseball Databank](https://github.com/chadwickbureau/baseballdatabank) repository update. The SQLite schema for the most recent commit, as of 2017-11-22, would be `sqlite_schema_2016_4a64a55.sql`.  

## Backups
If want the schema AND the data you'll find backup files in the `backups/` directory.  The backup file naming convention is:

`(postgres|sqlite|mongodb)_backup_<date of backup>_<season>_<github-commit-hash>.tgz`

If I had a backup file done today would have the name `postgres_backup_20171122_2016_4a64a55.tgz`



## Generating Data Structures
The data structures are generated by reading the [Baseball Databank](https://github.com/chadwickbureau/baseballdatabank) CSV files and creating a language specific structure that maps to each of the CSV files. Currently only Go data structures are supported but in the future I will add others as I need them. If there is a particular language you would like to see you can create an issue or even better, submit a pull request.

### create_data_structures.py
  ```
usage: create_data_structures.py [-h] [--bson] [--csv] [--db] [--input INPUT]
                                 [--input-dir INPUT_DIR] [--json] [--package]
                                 --language {go} [--name NAME]
                                 [--output-dir OUTPUT_DIR] [--verbose]

Generate language specific data structures that model each of the Baseball
Databank CSV files.

optional arguments:
  -h, --help            show this help message and exit
  --bson                If the language supports add bson tags or bson
                        representation to the structure
  --csv                 If the language supports add CSV tags or CSV
                        representation to the structure
  --db                  adds db tags to Go structs.
  --input INPUT         the path to the input CSV file
  --input-dir INPUT_DIR
                        the path to the directory that contains the CSV files
                        to parse
  --json                If the language supports add JSON tags or JSON
                        representation to the structure
  --package             sets the package to the correct name for Go structs
  --language {go}       create language specific data structures
  --name NAME           name of the data structure being created
  --output-dir OUTPUT_DIR
                        the directory where the generated file should be
                        written. If not provided file will be written to
                        stdout
  --verbose             more output during the parsing and creation of the
                        data structures
```

Before running this script you will need to have already downloaded the [Baseball Databank](https://github.com/chadwickbureau/baseballdatabank) repository and installed the Python `inflection` package by running `pip install inflection`.  The next step is to change into the the `scripts/generate-code`.  I used the following command to generate the data structures that are in this repository.

`python create_data_structures.py --language go --csv --db --json --input-dir ~/src/baseballdatabank/core --package --output-dir ../../pkg/bd/models`

Required parameters: 
 - `--language` Since Go is the only supported language at the moment so if `--language` is not given it defaults to Go.
 - `--input` or `--input-dir`.  The first option takes a path to a single csv file and the second option takes a path to a directory of CSV files.

Optional parameters:
- `--name` The value of this parameter will be used to name the data structure that is being created for the file provided in the `--input` parameter
- `--output-dir` Where the newly created files will be stored. If this parameter is not used the output will be written to stdout
- `--verbose`.  

#### Go specific command line options

There following arguments depend on language support `--bson`, `--csv`, `--db`, and `--json`. If any of the `--csv`, `--db`, and `--json` flags are used the generated structs will contain the `csv`, `db` and/or `json` tags.


### dbloader 
After creating the database schema and the data structures you are ready to build the `dbloader`.  You can either build your own  version of `dbloader` using the `Makefile` or you can download the [latest release](https://github.com/rippinrobr/baseball-stats-db/releases) which contains prebuilt an executable for Linux, MacOS, and soon Windows platforms.  After building or downloading the executable and you have cloned the [Baseball Databank](https://github.com/chadwickbureau/baseballdatabank) you are ready to load your database.  Below is the list of available command line arguments.

```
Usage of ./bin/dbloader:
  -dbhost string
    	the name or ip address of the database server. (default "localhost")
  -dbname string
    	the hame of the database to load
  -dbpass string
    	the password to use when loading the database. Required for all dbtypes except SQLite
  -dbpath string
    	the path to your SQLite database
  -dbport int
    	the port to use when connecting to the database the database. Required for all dbtypes except SQLite
  -dbtype string
    	indicates what type of database is the load target. Supported databases are MongoDB, Postgres, and SQLite
  -dbuser string
    	the username to use when loading the database. Required for all dbtypes except SQLite
  -inputdir string
    	the directory where the Baseball Databank CSV files live. Required
  -verbose
    	writes more lines to the logs
```

#### Loading a Postgres DB

`./bin/dbloader -dbtype postgres -dbname baseballdatabank -dbuser myusername -dbpass mypassword -inputdir ~/my-baseball-databank-dir/core`

This will load the data into your `baseballdatabank` database stored on the db server that lives on localhost since a `-dbhost` value wasn't provided.  Since the `-dbport` option was not provided the connection will attempt to use the default Postgres port 5432. 

#### Loading a SQLite DB

`./bin/dbloader -dbtype sqlite -dbpath=./baseball_databank_2016_4a64a55.sqlite3 -inputdir ~/my-baseball-databank-dir/core`

Since this is a SQLite database there are only two required parameters, `-dbtype` and `-dbpath`.  The loader will create the SQLite database using the value of `-dbpath`.

<href name="about_mysql">
## About MySQL

The reason why MySQL isn't officially supported is due to the fact that there are 14 records that aren't in the `pitchingpost` table due to MySQL's decision to not support the `inf` value for infinity.  Having said that there is support in the `dbloader` code for MySQL.  If you choose to use MySQL just remember that you will not have all the data that is present in the CSV files.  Here are the missing records:

```
playerID,yearID,round,teamID,lgID,W,L,G,GS,CG,SHO,SV,IPouts,H,ER,HR,BB,SO,BAOpp,ERA,IBB,WP,HBP,BK,BFP,GF,R,SH,SF,GIDP
poledi01,1975,WS,BOS,AL,0,0,1,0,0,0,0,0,0,1,0,2,0,,inf,0,0,0,0,2,0,1,0,0,0
welchbo01,1981,WS,LAN,NL,0,0,1,1,0,0,0,0,3,2,0,1,0,1.000,inf,0,0,0,0,4,0,2,0,0,0
westda01,1991,WS,MIN,AL,0,0,2,0,0,0,0,0,2,4,1,4,0,1.000,inf,0,0,0,0,6,0,4,0,0,0
holtch01,1999,NLDS1,HOU,NL,0,0,1,0,0,0,0,0,3,3,0,0,0,1.000,inf,0,0,0,0,3,0,3,0,0,0
fultzaa01,2002,NLDS1,SFN,NL,0,0,2,0,0,0,0,0,2,1,0,0,0,1.000,inf,0,0,0,0,2,0,1,0,0,0
myersmi01,2006,ALDS1,NYA,AL,0,0,1,0,0,0,0,0,1,1,1,0,0,1.000,inf,0,0,0,0,1,0,1,0,0,0
saitota01,2008,NLDS1,LAN,NL,0,0,1,0,0,0,0,0,3,2,0,0,0,1.000,inf,0,0,0,0,3,0,2,0,0,0
ramirra02,2009,ALDS2,BOS,AL,0,0,1,0,0,0,0,0,1,2,0,1,0,1.000,inf,0,0,1,0,3,0,2,0,0,0
schleda01,2011,ALCS,DET,AL,0,0,1,0,0,0,0,0,1,1,0,0,0,1.000,inf,0,0,0,0,1,0,1,0,0,0
ueharko01,2011,ALDS2,TEX,AL,0,0,1,0,0,0,0,0,2,3,1,1,0,1.000,inf,0,0,0,0,3,0,3,0,0,0
marshse01,2013,NLWC,CIN,NL,0,0,1,0,0,0,0,0,1,1,0,2,0,1.000,inf,1,0,0,0,3,0,1,0,0,0
choatra01,2014,NLDS2,SLN,NL,0,0,1,0,0,0,0,0,1,1,1,0,0,1.000,inf,0,0,0,0,1,0,1,0,0,0
goedder01,2015,NLDS2,NYN,NL,0,0,1,0,0,0,0,0,4,3,1,0,0,1.000,inf,0,0,0,0,4,0,3,0,0,0
jimenub01,2016,ALWC,BAL,AL,0,1,1,0,0,0,0,0,3,3,1,0,0,1.000,inf,0,0,0,0,3,1,3,0,0,0
```

I do not want to put some placeholder value in place of the `inf` simply because MySQL doesn't support it when PostgreSQL and SQLite do.  If you can come up with a clever way of handling this for MySQL that isn't a complete hack feel free to pass it along or make a pull request.


## Building the databases yourself
_I used the following script to generate the original database schema but have since started updating the schema files to make any changes I needed to make.  You can use this script to build the database if you wish but __I would suggest using either the the schema files or the backups__.  In the future I plan on moving the database generation process out of python and into a language that does not require installation of packages or modules._ 

Before running the database script you will need to install `peewee`. Peewee is what creates the tables and other schema related requirements.  To install `peewee` run the following:

```
pip install peewee
```

### create_database_schema.py
Order of the data structure creation and schema script doesn't really matter but I typically create the schema after creating the structures.  Create the schema is as simple as running `python create_database_schema.py`.  The script lives in the `scripts/create-database` directory and has the options listed below.

```
usage: create_database_schema.py [-h] --dbtype {mysql,postgres,sqlite}
                                 [--dbhost DBHOST] [--dbname DBNAME]
                                 [--dbpath DBPATH] [--dbpass DBPASS]
                                 [--dbport DBPORT] [--dbuser DBUSER]

Generates a DB schema based on the Baseball Databank csv files.

optional arguments:
  -h, --help            show this help message and exit
  --dbtype {mysql,postgres,sqlite}
                        the database type you'd like to generate the schema
                        for
  --dbhost DBHOST       host of the database server
  --dbname DBNAME       Name of the database where the tables are to be added.
                        REQUIRED if not sqlite
  --dbpath DBPATH       SQLITE ONLY - the path for the newly created database
  --dbpass DBPASS       The password for the user given in the --dbuser
                        option, ignored for SQLite
  --dbport DBPORT       The port the database server is listening on, ignored
                        for SQLite, defaults to appropriate value for server
                        type if not provided
  --dbuser DBUSER       username to use when creating the database, ignored
                        for SQLite databases, REQUIRED for others.
  ```

Before you can use this script you will need to have already created the database in Postgres.  In future versions the database will be created for you.

#### Creating the Schema in a SQLite DB
`python create_database_schema.py --dbtype sqlite --dbpath ./baseball_database_db.py`

For SQLite any of the other command line arguments given besides the two used above will be ignored

#### Creating the Schema in a Postgres DB
`python create_database_schema.py --dbtype postgres --dbname baseballdatabank --dbuser myusername --dbpass mypassword`

For PostgreSQL if `--dbport` is not given the default port 5432 is used. 

After creating the schema you will have a db with a matching table for each of the CSV files


## Licensing & Acknowledgments

```
Baseball Databank is a compilation of historical baseball data in a
convenient, tidy format, distributed under Open Data terms.

This work is licensed under a Creative Commons Attribution-ShareAlike
3.0 Unported License.  For details see:
http://creativecommons.org/licenses/by-sa/3.0/

Person identification and demographics data are provided by
Chadwick Baseball Bureau (http://www.chadwick-bureau.com),
from its Register of baseball personnel.

Player performance data for 1871 through 2014 is based on the
Lahman Baseball Database, version 2015-01-24, which is 
Copyright (C) 1996-2015 by Sean Lahman.

The tables Parks.csv and HomeGames.csv are based on the game logs
and park code table published by Retrosheet.
This information is available free of charge from and is copyrighted
by Retrosheet.  Interested parties may contact Retrosheet at 
http://www.retrosheet.org.
```

